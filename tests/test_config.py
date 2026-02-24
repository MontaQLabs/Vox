"""Tests for Vox configuration."""

import pytest
import tempfile
import toml
from pathlib import Path
from vox.config import Config, VOX_HOMESERVER


class TestConfig:
    """Test cases for Config class."""
    
    def test_config_creation(self):
        """Test creating a new config."""
        config = Config(
            vox_id="test_user",
            homeserver="http://test.com:3338",
            access_token="test_token",
            device_id="test_device",
            user_id="@test_user:test.com"
        )
        
        assert config.vox_id == "test_user"
        assert config.homeserver == "http://test.com:3338"
        assert config.access_token == "test_token"
        assert config.device_id == "test_device"
        assert config.user_id == "@test_user:test.com"
    
    def test_config_save_and_load(self):
        """Test saving and loading config."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.toml"
            
            # Create and save config
            config = Config(
                vox_id="test_user",
                homeserver="http://test.com:3338",
                access_token="test_token"
            )
            config.save(config_path)
            
            # Load config
            loaded_config = Config.load(config_path)
            
            assert loaded_config.vox_id == "test_user"
            assert loaded_config.homeserver == "http://test.com:3338"
            assert loaded_config.access_token == "test_token"
    
    def test_config_load_file_not_found(self):
        """Test loading config when file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            Config.load(Path("/nonexistent/config.toml"))
    
    def test_config_defaults(self):
        """Test config default values."""
        config = Config(vox_id="test_user")
        
        assert config.vox_id == "test_user"
        assert config.homeserver == "http://80.225.209.87:3338"
        assert config.access_token is None
        assert config.device_id is None
        assert config.user_id is None
    
    def test_config_roundtrip_preserves_all_fields(self):
        """Test that save -> load roundtrip preserves all fields."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.toml"
            
            config = Config(
                vox_id="roundtrip_test",
                homeserver=VOX_HOMESERVER,
                access_token="tok_abc123",
                device_id="dev_xyz",
                user_id="@roundtrip_test:vox.pm"
            )
            config.save(config_path)
            
            loaded = Config.load(config_path)
            assert loaded.vox_id == config.vox_id
            assert loaded.homeserver == config.homeserver
            assert loaded.access_token == config.access_token
            assert loaded.device_id == config.device_id
            assert loaded.user_id == config.user_id
