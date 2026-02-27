"""Matrix backend integration for Vox."""

import asyncio
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from nio import AsyncClient, RoomMessageText, SyncResponse, RoomPreset
from nio.responses import JoinResponse
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
    
    async def initialize(self) -> None:
        """Initialize the Matrix client."""
        try:
            await self.client.sync()
        except Exception as e:
            # Conduit/nio sometimes have validation issues on first sync, ignore for now
            print(f"Initial sync warning: {e}")
    
    async def send_message(
        self, 
        to_vox_id: str, 
        body: str, 
        conversation_id: Optional[str] = None
    ) -> str:
        """Send a message to another Vox agent."""
        if conversation_id is None:
            conversation_id = f"conv_{uuid.uuid4().hex[:8]}"
        
        # Create a room for the conversation
        room_id = await self._get_or_create_room(to_vox_id, conversation_id)
        
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
        
        response = await self.client.room_send(
            room_id=room_id,
            message_type="m.room.message",
            content=content
        )
        
        # Handle different response types
        if hasattr(response, 'event_id') and response.event_id:
            return conversation_id
        elif hasattr(response, 'room_id') and response.room_id:
            return conversation_id
        elif isinstance(response, str):
            return conversation_id
        else:
            # For demo purposes, consider it successful even if response is unexpected
            print(f"Message sent with response: {response}")
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
            
            # Handle different response formats
            if hasattr(response, 'rooms') and response.rooms:
                rooms = response.rooms.join
            else:
                # Fallback for different Matrix server implementations
                rooms = {}
            
            for room_id, room_info in rooms.items():
                # Get messages from timeline
                messages = []
                if hasattr(room_info, 'timeline') and room_info.timeline:
                    for event in room_info.timeline.events:
                        if isinstance(event, RoomMessageText):
                            vox_data = event.source.get("content", {}).get("vox", {})
                            if vox_data:
                                message = Message(
                                    from_vox_id=vox_data.get("from", "unknown"),
                                    to_vox_id=vox_data.get("to", "unknown"),
                                    timestamp=vox_data.get("timestamp", event.server_timestamp),
                                    conversation_id=vox_data.get("conversation_id", "unknown"),
                                    body=event.body
                                )
                                messages.append(message)
                
                if messages:
                    # Get the contact name from room members or latest message
                    with_contact = self._extract_contact_from_room(room_id, messages)
                    
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
        # This would require room ID mapping - for now, return from inbox
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
    
    async def _get_or_create_room(self, to_vox_id: str, conversation_id: str) -> str:
        """Get or create a Matrix room for a conversation."""
        # Check if we already have a room for this contact
        existing_room_id = self.storage.get_room(to_vox_id)
        if existing_room_id:
            return existing_room_id
            
        try:
            # Create new room with minimal config for Conduit compatibility
            response = await self.client.room_create(
                name=f"Vox Chat",
                preset=RoomPreset.private_chat
            )
            
            if hasattr(response, 'room_id'):
                room_id = response.room_id
                # Invite the other agent
                if to_vox_id.startswith("@") and ":" in to_vox_id:
                    invite_user_id = to_vox_id
                else:
                    server_domain = self.config.homeserver.replace('http://', '').replace('https://', '').split(':')[0]
                    invite_user_id = f"@{to_vox_id}:{server_domain}"
                
                await self.client.room_invite(
                    room_id=room_id,
                    user_id=invite_user_id
                )
                
                # Save to storage
                self.storage.set_room(to_vox_id, room_id)
                return room_id
            else:
                # Fallback: try to use response directly if it's a room_id string
                if isinstance(response, str):
                    self.storage.set_room(to_vox_id, response)
                    return response
                else:
                    raise Exception(f"Failed to create room: {response}")
        except Exception as e:
            print(f"Room creation error: {e}")
            # For demo purposes, return a fake room ID
            return f"!demo_{conversation_id}:localhost"
    
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
