"""Main Vox client."""

import asyncio
import uuid
import secrets
from typing import Optional, List, Dict, Any
from .config import Config, VOX_HOMESERVER, VOX_DOMAIN
from .storage import Storage, Conversation
from .matrix_backend import MatrixBackend


class VoxClient:
    """Main Vox client for agent-to-agent communication."""
    
    def __init__(self, vox_home: Optional[str] = None):
        self.storage = Storage(vox_home)
        self.config: Optional[Config] = None
        self.backend: Optional[MatrixBackend] = None
    
    def _ensure_config(self) -> Config:
        """Ensure config is loaded. Does NOT create the Matrix backend."""
        if self.config is None:
            self.config = Config.load()
        return self.config
    
    def _ensure_backend(self) -> MatrixBackend:
        """Ensure the Matrix backend is initialized (lazy)."""
        config = self._ensure_config()
        if self.backend is None:
            self.backend = MatrixBackend(config, self.storage)
        return self.backend
    
    async def initialize(self, username: Optional[str] = None) -> str:
        """Initialize Vox identity.
        
        Args:
            username: Optional human-readable username. If provided, the Vox ID
                     will be vox_<username>. If not, a random hex ID is generated.
        
        Returns:
            The created Vox ID string.
        """
        vox_id = f"vox_{username}" if username else f"vox_{secrets.token_hex(4)}"
        
        self.config = Config(
            vox_id=vox_id,
            homeserver=VOX_HOMESERVER,
            access_token=f"token_{uuid.uuid4().hex}",
            device_id=f"device_{uuid.uuid4().hex[:8]}",
            user_id=f"@{vox_id}:{VOX_DOMAIN}"
        )
        
        self.config.save()
        
        return vox_id
    
    def whoami(self) -> str:
        """Get current Vox ID."""
        config = self._ensure_config()
        return config.vox_id
    
    def status(self) -> Dict[str, Any]:
        """Get Vox status."""
        config = self._ensure_config()
        contacts = self.storage.get_contacts()
        return {
            "vox_id": config.vox_id,
            "homeserver": config.homeserver,
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
        """Send a message to a contact.
        
        Args:
            contact: Contact name (must exist in contacts).
            message: Message body text.
            conversation_id: Optional conversation ID for threaded replies.
        
        Returns:
            The conversation ID.
        
        Raises:
            ValueError: If contact not found in contacts list.
        """
        backend = self._ensure_backend()
        
        # Get vox_id from contact name
        vox_id = self.storage.get_contact(contact)
        if vox_id is None:
            raise ValueError(f"Contact '{contact}' not found")
        
        await backend.initialize()
        
        conv_id = await backend.send_message(vox_id, message, conversation_id)
        return conv_id
    
    async def get_inbox(self, from_contact: Optional[str] = None) -> List[Conversation]:
        """Get conversations with new messages."""
        backend = self._ensure_backend()
        await backend.initialize()
        return await backend.get_inbox(from_contact)
    
    async def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """Get full conversation history."""
        backend = self._ensure_backend()
        await backend.initialize()
        return await backend.get_conversation(conversation_id)
    
    async def discover_agents(self, query: str) -> List[Dict[str, str]]:
        """Search for agents."""
        backend = self._ensure_backend()
        await backend.initialize()
        return await backend.discover_agents(query)
    
    async def advertise(self, description: str) -> None:
        """Advertise agent in directory."""
        backend = self._ensure_backend()
        await backend.initialize()
        await backend.advertise_agent(description)
    
    async def close(self) -> None:
        """Close the client."""
        if self.backend:
            await self.backend.close()
