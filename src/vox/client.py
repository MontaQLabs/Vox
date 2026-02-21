"""Main Vox client."""

import asyncio
import uuid
import secrets
from typing import Optional, List, Dict, Any
from .config import Config
from .storage import Storage, Conversation
from .matrix_backend import MatrixBackend


class VoxClient:
    """Main Vox client for agent-to-agent communication."""
    
    def __init__(self, vox_home: Optional[str] = None):
        self.storage = Storage(vox_home)
        self.config = None
        self.backend = None
    
    def _ensure_initialized(self) -> None:
        """Ensure Vox is initialized."""
        if self.config is None:
            self.config = Config.load()
        if self.backend is None:
            self.backend = MatrixBackend(self.config, self.storage)
    
    async def initialize(self, username: Optional[str] = None) -> str:
        """Initialize Vox identity."""
        vox_id = username or f"vox_{secrets.token_hex(4)}"
        
        # In a real implementation, this would register with Matrix homeserver
        # For now, create a mock configuration
        self.config = Config(
            vox_id=vox_id,
            homeserver="http://vox.pm:3338",
            access_token=f"mock_token_{uuid.uuid4().hex}",
            device_id=f"device_{uuid.uuid4().hex[:8]}",
            user_id=f"@{vox_id}:vox.pm"
        )
        
        self.config.save()
        
        return vox_id
    
    def whoami(self) -> str:
        """Get current Vox ID."""
        self._ensure_initialized()
        return self.config.vox_id
    
    def status(self) -> Dict[str, Any]:
        """Get Vox status."""
        self._ensure_initialized()
        contacts = self.storage.get_contacts()
        return {
            "vox_id": self.config.vox_id,
            "homeserver": self.config.homeserver,
            "contacts": len(contacts)
        }
    
    def add_contact(self, name: str, vox_id: str) -> None:
        """Add a contact."""
        self.storage.add_contact(name, vox_id)
    
    def list_contacts(self) -> Dict[str, str]:
        """List all contacts."""
        return self.storage.get_contacts()
    
    def remove_contact(self, name: str) -> bool:
        """Remove a contact."""
        return self.storage.remove_contact(name)
    
    async def send_message(
        self, 
        contact: str, 
        message: str, 
        conversation_id: Optional[str] = None
    ) -> str:
        """Send a message to a contact."""
        self._ensure_initialized()
        
        # Get vox_id from contact name
        vox_id = self.storage.get_contact(contact)
        if vox_id is None:
            raise ValueError(f"Contact '{contact}' not found")
        
        await self.backend.initialize()
        
        conv_id = await self.backend.send_message(vox_id, message, conversation_id)
        return conv_id
    
    async def get_inbox(self, from_contact: Optional[str] = None) -> List[Conversation]:
        """Get conversations with new messages."""
        self._ensure_initialized()
        
        await self.backend.initialize()
        
        conversations = await self.backend.get_inbox(from_contact)
        return conversations
    
    async def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """Get full conversation history."""
        self._ensure_initialized()
        
        await self.backend.initialize()
        
        return await self.backend.get_conversation(conversation_id)
    
    async def discover_agents(self, query: str) -> List[Dict[str, str]]:
        """Search for agents."""
        self._ensure_initialized()
        
        await self.backend.initialize()
        
        return await self.backend.discover_agents(query)
    
    async def advertise(self, description: str) -> None:
        """Advertise agent in directory."""
        self._ensure_initialized()
        
        await self.backend.initialize()
        
        await self.backend.advertise_agent(description)
    
    async def close(self) -> None:
        """Close the client."""
        if self.backend:
            await self.backend.close()
