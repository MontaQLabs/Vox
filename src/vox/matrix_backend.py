"""Matrix backend integration for Vox."""

import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from nio import AsyncClient, RoomMessageText, RoomPreset
from .config import Config
from .storage import Storage, Message, Conversation


class MatrixBackend:
    """Matrix backend for Vox communication."""
    
    def __init__(self, config: Config, storage: Storage):
        self.config = config
        self.storage = storage
        self.client = AsyncClient(
            homeserver=config.homeserver,
        )
        self.client.access_token = config.access_token
        self._initialized = False
    
    async def initialize(self) -> None:
        """Initialize the Matrix client (no-op after first call)."""
        if self._initialized:
            return
        try:
            await self.client.sync()
            self._initialized = True
        except Exception as e:
            # Conduit/nio sometimes have validation issues on first sync, ignore for now
            print(f"Initial sync warning: {e}")
            self._initialized = True
    
    async def send_message(
        self, 
        to_vox_id: str, 
        body: str, 
        conversation_id: Optional[str] = None
    ) -> str:
        """Send a message to another Vox agent."""
        if conversation_id is None:
            conversation_id = f"conv_{uuid.uuid4().hex[:8]}"
        
        # Get (or lazily create) the persistent per-contact room
        room_id = await self._get_or_create_room(to_vox_id)
        
        # Send the message
        content = {
            "msgtype": "m.text",
            "body": body,
            "vox": {
                "from": self.config.vox_id,
                "to": to_vox_id,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "conversation_id": conversation_id,
            }
        }
        
        await self.client.room_send(
            room_id=room_id,
            message_type="m.room.message",
            content=content
        )

        # Save sent message to local history
        msg = Message(
            from_vox_id=self.config.vox_id,
            to_vox_id=to_vox_id,
            timestamp=datetime.utcnow().isoformat() + "Z",
            conversation_id=conversation_id,
            body=body
        )
        with_contact = "unknown"
        contacts = self.storage.get_contacts()
        for name, v_id in contacts.items():
            if v_id == to_vox_id:
                with_contact = name
                break

        self.storage.save_messages(conversation_id, with_contact, [msg])
        return conversation_id
    
    async def get_inbox(self, from_contact: Optional[str] = None) -> List[Conversation]:
        """Get conversations with new messages."""
        try:
            sync_token = self.storage.get_sync_token() or ""
            
            response = await self.client.sync(
                timeout=30000,
                since=sync_token if sync_token else None
            )
            
            conversations = []
            
            # Auto-join invited rooms and persist the room mapping so replies
            # don't need an extra alias-resolution round-trip.
            if hasattr(response, 'rooms') and response.rooms.invite:
                for inv_room_id, inv_info in response.rooms.invite.items():
                    await self.client.join(inv_room_id)
                    print(f"Auto-joined room: {inv_room_id}")
                    # Extract the inviter's user ID from the invite state events
                    inviter = None
                    try:
                        for event in inv_info.invite_state.events:
                            sender = getattr(event, "sender", None)
                            if sender and sender != (self.config.user_id or self._to_matrix_id(self.config.vox_id)):
                                inviter = sender
                                break
                    except Exception:
                        pass
                    if inviter and not self.storage.get_room(inviter):
                        self.storage.set_room(inviter, inv_room_id)

            # Process joined rooms
            if hasattr(response, 'rooms') and response.rooms:
                rooms = response.rooms.join
            else:
                rooms = {}
            
            for room_id, room_info in rooms.items():
                # First pass: find if any message in the timeline has a conversation_id
                # or if we have a way to derive it from the room
                room_conv_id = None
                if hasattr(room_info, 'timeline') and room_info.timeline:
                    for event in room_info.timeline.events:
                        if isinstance(event, RoomMessageText):
                            v_data = event.source.get("content", {}).get("vox", {})
                            if v_data.get("conversation_id"):
                                room_conv_id = v_data.get("conversation_id")
                                break
                
                if not room_conv_id:
                    room_conv_id = f"conv_{room_id.replace('!', '').replace(':', '_')[:12]}"

                # Second pass: process messages
                messages = []
                if hasattr(room_info, 'timeline') and room_info.timeline:
                    for event in room_info.timeline.events:
                        if isinstance(event, RoomMessageText):
                            content = event.source.get("content", {})
                            vox_data = content.get("vox", {})
                            
                            from_id = vox_data.get("from", event.sender)
                            to_id = vox_data.get("to", self.config.vox_id)
                            ts = vox_data.get("timestamp", event.server_timestamp)
                            
                            # Use the unified room_conv_id
                            conv_id = vox_data.get("conversation_id", room_conv_id)

                            message = Message(
                                from_vox_id=from_id,
                                to_vox_id=to_id,
                                timestamp=str(ts),
                                conversation_id=conv_id,
                                body=event.body
                            )
                            messages.append(message)
                
                if messages:
                    # Get the contact name from room members or latest message
                    with_contact = self._extract_contact_from_room(room_id, messages)
                    
                    # Save to local history
                    self.storage.save_messages(messages[0].conversation_id, with_contact, messages)
                    
                    if from_contact is None or with_contact == from_contact:
                        conversation = Conversation(
                            conversation_id=messages[0].conversation_id,
                            with_contact=with_contact,
                            messages=messages
                        )
                        conversations.append(conversation)
            
            # Update sync token if available
            if hasattr(response, 'next_batch'):
                self.storage.set_sync_token(response.next_batch)
            
            return conversations
        except Exception as e:
            # For now, return empty list on sync errors
            print(f"Sync error (this is normal for Conduit servers): {e}")
            return []
    
    async def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """Get full conversation history."""
        # Check local history first
        history = self.storage.get_history(conversation_id)
        if history:
            return history
            
        # Fallback: check inbox (which will sync and save)
        conversations = await self.get_inbox()
        for conv in conversations:
            if conv.conversation_id == conversation_id:
                return conv
        return None
    
    async def discover_agents(self, query: str) -> List[Dict[str, str]]:
        """Search for agents in directory."""
        # This would integrate with a Matrix room-based directory
        # For now, return empty list
        return []
    
    async def advertise_agent(self, description: str) -> None:
        """List agent in public directory."""
        # This would post to a Matrix room-based directory
        pass
    
    def _server_domain(self) -> str:
        """Extract the bare domain from the configured homeserver URL."""
        return (
            self.config.homeserver
            .replace("https://", "")
            .replace("http://", "")
            .split(":")[0]
            .split("/")[0]
        )

    def _to_matrix_id(self, vox_id: str) -> str:
        """Ensure vox_id is a fully-qualified Matrix user ID."""
        if vox_id.startswith("@") and ":" in vox_id:
            return vox_id
        return f"@{vox_id}:{self._server_domain()}"

    def _make_room_alias(self, other_matrix_id: str) -> str:
        """Return a stable, human-readable alias for the DM room between us and other_matrix_id.

        Uses bare localparts sorted alphabetically so either party derives the
        same alias, preventing duplicate rooms.
        """
        own_matrix_id = self.config.user_id or self._to_matrix_id(self.config.vox_id)
        own_local = own_matrix_id.lstrip("@").split(":")[0]
        other_local = other_matrix_id.lstrip("@").split(":")[0]
        a, b = sorted([own_local, other_local])
        return f"vox-dm-{a}-{b}"

    async def _get_or_create_room(self, to_vox_id: str) -> str:
        """Return the persistent Matrix room ID for a contact.

        Rooms are per-contact and identified by a deterministic alias so they
        survive local-storage resets.  Room creation and invite are separated
        so federated invites (e.g. matrix.org users) don't break room creation
        on Conduit.  The room is marked is_direct so Matrix clients show it in
        the DMs section.
        """
        # Fast path: local storage already has the room
        existing_room_id = self.storage.get_room(to_vox_id)
        if existing_room_id:
            return existing_room_id

        invite_user_id = self._to_matrix_id(to_vox_id)
        room_alias = self._make_room_alias(invite_user_id)
        full_alias = f"#{room_alias}:{self._server_domain()}"

        # Room may already exist on the server (e.g. after a storage reset)
        try:
            resolve = await self.client.room_resolve_alias(full_alias)
            if hasattr(resolve, "room_id") and resolve.room_id:
                room_id = resolve.room_id
                await self.client.join(room_id)
                self.storage.set_room(to_vox_id, room_id)
                print(f"Rejoined existing room {room_id} via alias {full_alias}")
                return room_id
        except Exception:
            pass

        # Create the room first (no inline invite — avoids Conduit federation errors)
        try:
            response = await self.client.room_create(
                alias=room_alias,
                name="Vox Chat",
                preset=RoomPreset.private_chat,
                is_direct=True,
            )

            if hasattr(response, "room_id") and response.room_id:
                room_id = response.room_id
            elif isinstance(response, str):
                room_id = response
            else:
                raise Exception(f"Unexpected room_create response: {response}")

            self.storage.set_room(to_vox_id, room_id)
            print(f"Created room {room_id} with alias {full_alias}")

            # Invite separately so federated users work correctly
            try:
                await self.client.room_invite(room_id=room_id, user_id=invite_user_id)
            except Exception as e:
                print(f"Invite warning (room still created): {e}")

            return room_id
        except Exception as e:
            print(f"Room creation error: {e}")
            return f"!demo_{uuid.uuid4().hex[:8]}:localhost"
    
    def _extract_contact_from_room(self, room_id: str, messages: List[Message]) -> str:
        """Extract contact name from room information."""
        # For now, use the vox_id from first message that's not from self
        for message in messages:
            if message.from_vox_id != self.config.vox_id:
                # Try to find contact name
                contacts = self.storage.get_contacts()
                for name, vox_id in contacts.items():
                    if vox_id == message.from_vox_id:
                        return name
                return message.from_vox_id
        
        return "unknown"
    
    async def close(self) -> None:
        """Close the Matrix client."""
        await self.client.close()
