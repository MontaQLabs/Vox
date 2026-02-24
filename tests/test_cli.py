"""Tests for Vox CLI."""

import pytest
import tempfile
import json
import os
from pathlib import Path
from unittest.mock import patch, AsyncMock, MagicMock
from click.testing import CliRunner
from vox.cli import cli


def _mock_initialize(username=None, homeserver=None):
    """Create a mock for VoxClient.initialize that writes real config."""
    import secrets
    from vox.config import Config, VOX_HOMESERVER
    
    vox_id = f"vox_{username}" if username else f"vox_{secrets.token_hex(4)}"
    config = Config(
        vox_id=vox_id,
        homeserver=homeserver or VOX_HOMESERVER,
        access_token="mock_token_abc123",
        device_id="mock_device_01",
        user_id=f"@{vox_id}:your.vps.ip",
    )
    config.save()
    return vox_id


class TestCLI:
    """Test cases for Vox CLI."""
    
    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.runner = CliRunner()
    
    def _set_vox_home(self):
        """Set VOX_HOME to a temporary directory."""
        vox_home = tempfile.mkdtemp()
        os.environ["VOX_HOME"] = vox_home
        return vox_home
    
    @patch("vox.client.VoxClient.initialize")
    @patch("vox.client.VoxClient.close")
    def test_init_command(self, mock_close, mock_init):
        """Test vox init command with explicit username."""
        with self.runner.isolated_filesystem():
            self._set_vox_home()
            
            async def side_effect(username=None, homeserver=None):
                return _mock_initialize(username, homeserver)
            
            mock_init.side_effect = side_effect
            mock_close.return_value = None
            
            result = self.runner.invoke(cli, ["init", "--username", "test_user"])
            assert result.exit_code == 0
            assert "✅ Vox ID: vox_test_user" in result.output
    
    @patch("vox.client.VoxClient.initialize")
    @patch("vox.client.VoxClient.close")
    def test_init_command_random_username(self, mock_close, mock_init):
        """Test vox init command without username generates random ID."""
        with self.runner.isolated_filesystem():
            self._set_vox_home()
            
            async def side_effect(username=None, homeserver=None):
                return _mock_initialize(username, homeserver)
            
            mock_init.side_effect = side_effect
            mock_close.return_value = None
            
            result = self.runner.invoke(cli, ["init"])
            assert result.exit_code == 0
            assert "✅ Vox ID: vox_" in result.output
    
    def test_whoami_not_initialized(self):
        """Test vox whoami when not initialized."""
        with self.runner.isolated_filesystem():
            self._set_vox_home()
            
            result = self.runner.invoke(cli, ["whoami"])
            assert result.exit_code == 4
            assert "Not initialized" in result.output
    
    @patch("vox.client.VoxClient.initialize")
    @patch("vox.client.VoxClient.close")
    def test_whoami_after_init(self, mock_close, mock_init):
        """Test vox whoami after initialization."""
        with self.runner.isolated_filesystem():
            self._set_vox_home()
            
            async def side_effect(username=None, homeserver=None):
                return _mock_initialize(username, homeserver)
            
            mock_init.side_effect = side_effect
            mock_close.return_value = None
            
            self.runner.invoke(cli, ["init", "--username", "test_user"])
            result = self.runner.invoke(cli, ["whoami"])
            assert result.exit_code == 0
            assert "vox_test_user" in result.output
    
    def test_status_not_initialized(self):
        """Test vox status when not initialized."""
        with self.runner.isolated_filesystem():
            self._set_vox_home()
            
            result = self.runner.invoke(cli, ["status"])
            assert result.exit_code == 4
            assert "Not initialized" in result.output
    
    @patch("vox.client.VoxClient.initialize")
    @patch("vox.client.VoxClient.close")
    def test_status_after_init(self, mock_close, mock_init):
        """Test vox status after initialization."""
        with self.runner.isolated_filesystem():
            self._set_vox_home()
            
            async def side_effect(username=None, homeserver=None):
                return _mock_initialize(username, homeserver)
            
            mock_init.side_effect = side_effect
            mock_close.return_value = None
            
            self.runner.invoke(cli, ["init", "--username", "test_user"])
            result = self.runner.invoke(cli, ["status"])
            assert result.exit_code == 0
            assert "vox_test_user" in result.output
            assert "Contacts: 0" in result.output
    
    @patch("vox.client.VoxClient.initialize")
    @patch("vox.client.VoxClient.close")
    def test_contact_commands(self, mock_close, mock_init):
        """Test contact management commands."""
        with self.runner.isolated_filesystem():
            self._set_vox_home()
            
            async def side_effect(username=None, homeserver=None):
                return _mock_initialize(username, homeserver)
            
            mock_init.side_effect = side_effect
            mock_close.return_value = None
            
            self.runner.invoke(cli, ["init", "--username", "test_user"])
            
            # Add contact
            result = self.runner.invoke(cli, ["contact", "add", "test_contact", "vox_test123"])
            assert result.exit_code == 0
            assert "✅ Contact 'test_contact' added" in result.output
            
            # List contacts
            result = self.runner.invoke(cli, ["contact", "list"])
            assert result.exit_code == 0
            assert "test_contact" in result.output
            assert "vox_test123" in result.output
            
            # Remove contact
            result = self.runner.invoke(cli, ["contact", "remove", "test_contact"])
            assert result.exit_code == 0
            assert "✅ Contact 'test_contact' removed" in result.output
            
            # Verify removed
            result = self.runner.invoke(cli, ["contact", "list"])
            assert result.exit_code == 0
            assert "No contacts found" in result.output
    
    @patch("vox.client.VoxClient.initialize")
    @patch("vox.client.VoxClient.close")
    def test_contact_remove_not_found(self, mock_close, mock_init):
        """Test removing non-existent contact."""
        with self.runner.isolated_filesystem():
            self._set_vox_home()
            
            async def side_effect(username=None, homeserver=None):
                return _mock_initialize(username, homeserver)
            
            mock_init.side_effect = side_effect
            mock_close.return_value = None
            
            self.runner.invoke(cli, ["init", "--username", "test_user"])
            
            result = self.runner.invoke(cli, ["contact", "remove", "nonexistent"])
            assert result.exit_code == 3
            assert "Contact 'nonexistent' not found" in result.output
    
    @patch("vox.client.VoxClient.initialize")
    @patch("vox.client.VoxClient.close")
    def test_contact_add_multiple(self, mock_close, mock_init):
        """Test adding multiple contacts."""
        with self.runner.isolated_filesystem():
            self._set_vox_home()
            
            async def side_effect(username=None, homeserver=None):
                return _mock_initialize(username, homeserver)
            
            mock_init.side_effect = side_effect
            mock_close.return_value = None
            
            self.runner.invoke(cli, ["init", "--username", "test_user"])
            
            self.runner.invoke(cli, ["contact", "add", "alice", "vox_alice"])
            self.runner.invoke(cli, ["contact", "add", "bob", "vox_bob"])
            
            result = self.runner.invoke(cli, ["contact", "list"])
            assert result.exit_code == 0
            assert "alice" in result.output
            assert "bob" in result.output
    
    def test_version_flag(self):
        """Test --version flag."""
        result = self.runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output
