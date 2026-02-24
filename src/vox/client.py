"""Main Vox client."""

import asyncio
import uuid
import secrets
import aiohttp
from typing import Optional, List, Dict, Any
from .config import Config, VOX_HOMESERVER, VOX_DOMAIN
from .storage import Storage, Conversation
from .matrix_backend import MatrixBackend


class VoxClient:
    """Main Vox client for agent-to-agent communication.
    
    Uses real Matrix registration — each `vox init` creates a real account
    on the homeserver and returns a real access token.
    """
    
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
    
    async def initialize(
        self,
        username: Optional[str] = None,
        homeserver: Optional[str] = None,
    ) -> str:
        """Initialize Vox identity by registering on the Matrix homeserver.
        
        This performs REAL Matrix registration:
        1. Generates a vox_<username> or vox_<random> ID
        2. Registers on the homeserver via /_matrix/client/v3/register
        3. Stores the real access token locally
        
        Args:
            username: Optional human-readable username. If provided, the Vox ID
                     will be vox_<username>. If not, a random hex ID is generated.
            homeserver: Optional custom homeserver URL. Defaults to the official
                       Vox homeserver. Users can point to their own Matrix server
                       for self-hosting — federation handles cross-server comms.
        
        Returns:
            The created Vox ID string.
        
        Raises:
            Exception: If registration fails (username taken, server down, etc.)
        """
        server = homeserver or VOX_HOMESERVER
        vox_id = f"vox_{username}" if username else f"vox_{secrets.token_hex(4)}"
        password = secrets.token_urlsafe(32)
        
        # Step 1: Real Matrix registration
        register_url = f"{server.rstrip('/')}/_matrix/client/v3/register"
        
        payload = {
            "username": vox_id,
            "password": password,
            "auth": {
                "type": "m.login.dummy",
            },
            "inhibit_login": False,
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(register_url, json=payload) as resp:
                data = await resp.json()
                
                if resp.status == 200:
                    # Registration successful
                    access_token = data["access_token"]
                    user_id = data["user_id"]
                    device_id = data["device_id"]
                elif resp.status == 400 and data.get("errcode") == "M_USER_IN_USE":
                    # Username taken — try to login instead
                    access_token, user_id, device_id = await self._login(
                        server, vox_id, password
                    )
                else:
                    error = data.get("error", f"HTTP {resp.status}")
                    raise Exception(f"Registration failed: {error}")
        
        # Step 2: Save config with real credentials
        self.config = Config(
            vox_id=vox_id,
            homeserver=server,
            access_token=access_token,
            device_id=device_id,
            user_id=user_id,
        )
        
        self.config.save()
        
        return vox_id
    
    async def _login(
        self, homeserver: str, username: str, password: str
    ) -> tuple:
        """Login to existing Matrix account."""
        login_url = f"{homeserver.rstrip('/')}/_matrix/client/v3/login"
        
        payload = {
            "type": "m.login.password",
            "identifier": {
                "type": "m.id.user",
                "user": username,
            },
            "password": password,
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(login_url, json=payload) as resp:
                data = await resp.json()
                
                if resp.status == 200:
                    return data["access_token"], data["user_id"], data["device_id"]
                else:
                    error = data.get("error", f"HTTP {resp.status}")
                    raise Exception(f"Login failed: {error}")
    
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
            "contacts": len(contacts),
            "user_id": config.user_id,
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
        backend = self._ensure_backend()
        
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
