"""Configuration management for Vox."""

import os
from pathlib import Path
from typing import Optional
import toml
from pydantic import BaseModel, Field


# Canonical homeserver — Conduit instance
VOX_HOMESERVER = "http://80.225.209.87:3338"
VOX_DOMAIN = "your.vps.ip"


class Config(BaseModel):
    """Vox configuration model."""
    
    vox_id: str
    homeserver: str = Field(default=VOX_HOMESERVER)
    access_token: Optional[str] = None
    device_id: Optional[str] = None
    user_id: Optional[str] = None
    
    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> "Config":
        """Load configuration from file."""
        if config_path is None:
            vox_home = Path(os.environ.get("VOX_HOME", Path.home() / ".vox"))
            config_path = vox_home / "config.toml"
        
        if not config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {config_path}. "
                "Run 'vox init' first."
            )
        
        with open(config_path, "r") as f:
            data = toml.load(f)
        
        return cls(**data)
    
    def save(self, config_path: Optional[Path] = None) -> None:
        """Save configuration to file."""
        if config_path is None:
            vox_home = Path(os.environ.get("VOX_HOME", Path.home() / ".vox"))
            vox_home.mkdir(parents=True, exist_ok=True)
            config_path = vox_home / "config.toml"
        
        with open(config_path, "w") as f:
            toml.dump(self.model_dump(), f)
