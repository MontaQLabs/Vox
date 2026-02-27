"""Local storage management for Vox."""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
import toml
from pydantic import BaseModel


class Contact(BaseModel):
    """Contact model."""
    name: str
    vox_id: str


class Message(BaseModel):
    """Message model."""
    from_vox_id: str
    to_vox_id: str
    timestamp: str
    conversation_id: str
    body: str


class Conversation(BaseModel):
    """Conversation model."""
    conversation_id: str
    with_contact: str
    messages: List[Message]


class Storage:
    """Local storage manager for Vox."""
    
    def __init__(self, vox_home: Optional[Path] = None):
        if vox_home is None:
            vox_home = Path(os.environ.get("VOX_HOME", Path.home() / ".vox"))
        
        self.vox_home = vox_home
        self.vox_home.mkdir(parents=True, exist_ok=True)
        
        self.contacts_file = self.vox_home / "contacts.toml"
        self.rooms_file = self.vox_home / "rooms.toml"
        self.history_file = self.vox_home / "history.toml"
        self.sync_token_file = self.vox_home / "sync_token"
        
        self._ensure_contacts_file()
    
    def _ensure_contacts_file(self) -> None:
        """Ensure contacts file exists."""
        if not self.contacts_file.exists():
            with open(self.contacts_file, "w") as f:
                toml.dump({}, f)
        if not self.rooms_file.exists():
            with open(self.rooms_file, "w") as f:
                toml.dump({}, f)
        if not self.history_file.exists():
            with open(self.history_file, "w") as f:
                toml.dump({"conversations": {}}, f)
    
    def add_contact(self, name: str, vox_id: str) -> None:
        """Add a contact."""
        contacts = self.get_contacts()
        contacts[name] = vox_id
        
        with open(self.contacts_file, "w") as f:
            toml.dump(contacts, f)
    
    def get_contacts(self) -> Dict[str, str]:
        """Get all contacts."""
        with open(self.contacts_file, "r") as f:
            return toml.load(f)
    
    def get_contact(self, name: str) -> Optional[str]:
        """Get a specific contact."""
        contacts = self.get_contacts()
        return contacts.get(name)
    
    def remove_contact(self, name: str) -> bool:
        """Remove a contact."""
        contacts = self.get_contacts()
        if name in contacts:
            del contacts[name]
            with open(self.contacts_file, "w") as f:
                toml.dump(contacts, f)
            return True
        return False
    
    def get_sync_token(self) -> Optional[str]:
        """Get the last sync token."""
        if not self.sync_token_file.exists():
            return None
        
        with open(self.sync_token_file, "r") as f:
            return f.read().strip()
    
    def set_sync_token(self, token: str) -> None:
        """Set the sync token."""
        with open(self.sync_token_file, "w") as f:
            f.write(token)
    
    def get_room(self, vox_id: str) -> Optional[str]:
        """Get the room ID for a specific Vox ID."""
        with open(self.rooms_file, "r") as f:
            rooms = toml.load(f)
            return rooms.get(vox_id)
            
    def set_room(self, vox_id: str, room_id: str) -> None:
        """Set the room ID for a specific Vox ID."""
        with open(self.rooms_file, "r") as f:
            rooms = toml.load(f)
        rooms[vox_id] = room_id
        with open(self.rooms_file, "w") as f:
            toml.dump(rooms, f)

    def save_messages(self, conversation_id: str, with_contact: str, messages: List[Message]) -> None:
        """Save messages to local history."""
        with open(self.history_file, "r") as f:
            data = toml.load(f)
            
        if conversation_id not in data["conversations"]:
            data["conversations"][conversation_id] = {
                "with_contact": with_contact,
                "messages": []
            }
            
        existing_messages = data["conversations"][conversation_id]["messages"]
        added = False
        for msg in messages:
            msg_dict = msg.model_dump()
            # Simple deduplication by timestamp and body
            if not any(m["timestamp"] == msg_dict["timestamp"] and m["body"] == msg_dict["body"] for m in existing_messages):
                existing_messages.append(msg_dict)
                added = True
        
        if added:
            # Sort messages by timestamp
            existing_messages.sort(key=lambda x: str(x["timestamp"]))
            with open(self.history_file, "w") as f:
                toml.dump(data, f)
                
    def get_history(self, conversation_id: str) -> Optional[Conversation]:
        """Get local conversation history."""
        with open(self.history_file, "r") as f:
            data = toml.load(f)
            
        conv_data = data["conversations"].get(conversation_id)
        if not conv_data:
            return None
            
        return Conversation(
            conversation_id=conversation_id,
            with_contact=conv_data["with_contact"],
            messages=[Message(**m) for m in conv_data["messages"]]
        )

    def get_all_conversations(self) -> List[Conversation]:
        """Get all stored conversations."""
        with open(self.history_file, "r") as f:
            data = toml.load(f)
            
        results = []
        for conv_id, conv_data in data["conversations"].items():
            results.append(Conversation(
                conversation_id=conv_id,
                with_contact=conv_data["with_contact"],
                messages=[Message(**m) for m in conv_data["messages"]]
            ))
        return results

    def clear_sync_token(self) -> None:
        """Clear the sync token."""
        if self.sync_token_file.exists():
            self.sync_token_file.unlink()
