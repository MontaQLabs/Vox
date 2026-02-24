"""Tests for Vox CLI."""

import pytest
import tempfile
import json
import os
from pathlib import Path
from click.testing import CliRunner
from vox.cli import cli


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
    
    def test_init_command(self):
        """Test vox init command with explicit username."""
        with self.runner.isolated_filesystem():
            self._set_vox_home()
            
            result = self.runner.invoke(cli, ["init", "--username", "test_user"])
            assert result.exit_code == 0
            assert "✅ Vox ID: vox_test_user" in result.output
    
    def test_init_command_random_username(self):
        """Test vox init command without username generates random ID."""
        with self.runner.isolated_filesystem():
            self._set_vox_home()
            
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
    
    def test_whoami_after_init(self):
        """Test vox whoami after initialization."""
        with self.runner.isolated_filesystem():
            self._set_vox_home()
            
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
    
    def test_status_after_init(self):
        """Test vox status after initialization."""
        with self.runner.isolated_filesystem():
            self._set_vox_home()
            
            self.runner.invoke(cli, ["init", "--username", "test_user"])
            result = self.runner.invoke(cli, ["status"])
            assert result.exit_code == 0
            assert "vox_test_user" in result.output
            assert "Contacts: 0" in result.output
    
    def test_contact_commands(self):
        """Test contact management commands."""
        with self.runner.isolated_filesystem():
            self._set_vox_home()
            
            # Initialize first
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
    
    def test_contact_remove_not_found(self):
        """Test removing non-existent contact."""
        with self.runner.isolated_filesystem():
            self._set_vox_home()
            
            # Initialize first
            self.runner.invoke(cli, ["init", "--username", "test_user"])
            
            # Try to remove non-existent contact
            result = self.runner.invoke(cli, ["contact", "remove", "nonexistent"])
            assert result.exit_code == 3
            assert "Contact 'nonexistent' not found" in result.output
    
    def test_contact_add_multiple(self):
        """Test adding multiple contacts."""
        with self.runner.isolated_filesystem():
            self._set_vox_home()
            
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
