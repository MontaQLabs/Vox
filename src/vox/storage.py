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
        self.sync_token_file = self.vox_home / "sync_token"
        
        self._ensure_contacts_file()
    
    def _ensure_contacts_file(self) -> None:
        """Ensure contacts file exists."""
        if not self.contacts_file.exists():
            with open(self.contacts_file, "w") as f:
                toml.dump({}, f)
    
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
    
    def clear_sync_token(self) -> None:
        """Clear the sync token."""
        if self.sync_token_file.exists():
            self.sync_token_file.unlink()
