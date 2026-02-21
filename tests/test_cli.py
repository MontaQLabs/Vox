"""Tests for Vox CLI."""

import pytest
import tempfile
import json
from pathlib import Path
from click.testing import CliRunner
from vox.cli import cli


class TestCLI:
    """Test cases for Vox CLI."""
    
    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.runner = CliRunner()
    
    def test_init_command(self):
        """Test vox init command."""
        with self.runner.isolated_filesystem():
            # Mock the home directory
            import os
            os.environ["VOX_HOME"] = tempfile.mkdtemp()
            
            result = self.runner.invoke(cli, ["init", "--username", "test_user"])
            assert result.exit_code == 0
            assert "✅ Vox ID: vox_test_user" in result.output
    
    def test_init_command_random_username(self):
        """Test vox init command without username."""
        with self.runner.isolated_filesystem():
            import os
            os.environ["VOX_HOME"] = tempfile.mkdtemp()
            
            result = self.runner.invoke(cli, ["init"])
            assert result.exit_code == 0
            assert "✅ Vox ID: vox_" in result.output
    
    def test_whoami_not_initialized(self):
        """Test vox whoami when not initialized."""
        with self.runner.isolated_filesystem():
            import os
            os.environ["VOX_HOME"] = tempfile.mkdtemp()
            
            result = self.runner.invoke(cli, ["whoami"])
            assert result.exit_code == 4
            assert "Not initialized" in result.output
    
    def test_status_not_initialized(self):
        """Test vox status when not initialized."""
        with self.runner.isolated_filesystem():
            import os
            os.environ["VOX_HOME"] = tempfile.mkdtemp()
            
            result = self.runner.invoke(cli, ["status"])
            assert result.exit_code == 4
            assert "Not initialized" in result.output
    
    def test_contact_commands(self):
        """Test contact management commands."""
        with self.runner.isolated_filesystem():
            import os
            os.environ["VOX_HOME"] = tempfile.mkdtemp()
            
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
    
    def test_contact_remove_not_found(self):
        """Test removing non-existent contact."""
        with self.runner.isolated_filesystem():
            import os
            os.environ["VOX_HOME"] = tempfile.mkdtemp()
            
            # Initialize first
            self.runner.invoke(cli, ["init", "--username", "test_user"])
            
            # Try to remove non-existent contact
            result = self.runner.invoke(cli, ["contact", "remove", "nonexistent"])
            assert result.exit_code == 3
            assert "Contact 'nonexistent' not found" in result.output
