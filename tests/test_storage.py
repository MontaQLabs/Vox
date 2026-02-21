"""Tests for Vox storage."""

import pytest
import tempfile
from pathlib import Path
from vox.storage import Storage, Contact, Message, Conversation


class TestStorage:
    """Test cases for Storage class."""
    
    def setup_method(self):
        """Set up test storage."""
        self.temp_dir = tempfile.mkdtemp()
        self.storage = Storage(Path(self.temp_dir))
    
    def test_add_contact(self):
        """Test adding a contact."""
        self.storage.add_contact("test_user", "vox_test123")
        
        contacts = self.storage.get_contacts()
        assert contacts["test_user"] == "vox_test123"
    
    def test_get_contact(self):
        """Test getting a specific contact."""
        self.storage.add_contact("test_user", "vox_test123")
        
        vox_id = self.storage.get_contact("test_user")
        assert vox_id == "vox_test123"
        
        # Test non-existent contact
        vox_id = self.storage.get_contact("nonexistent")
        assert vox_id is None
    
    def test_remove_contact(self):
        """Test removing a contact."""
        self.storage.add_contact("test_user", "vox_test123")
        
        # Remove existing contact
        result = self.storage.remove_contact("test_user")
        assert result is True
        assert "test_user" not in self.storage.get_contacts()
        
        # Remove non-existent contact
        result = self.storage.remove_contact("nonexistent")
        assert result is False
    
    def test_sync_token(self):
        """Test sync token management."""
        # Initially no token
        token = self.storage.get_sync_token()
        assert token is None
        
        # Set token
        self.storage.set_sync_token("test_token_123")
        token = self.storage.get_sync_token()
        assert token == "test_token_123"
        
        # Clear token
        self.storage.clear_sync_token()
        token = self.storage.get_sync_token()
        assert token is None
    
    def test_message_models(self):
        """Test message and conversation models."""
        message = Message(
            from_vox_id="vox_user1",
            to_vox_id="vox_user2",
            timestamp="2025-01-01T12:00:00Z",
            conversation_id="conv_abc123",
            body="Hello, world!"
        )
        
        assert message.from_vox_id == "vox_user1"
        assert message.to_vox_id == "vox_user2"
        assert message.body == "Hello, world!"
        
        conversation = Conversation(
            conversation_id="conv_abc123",
            with_contact="user2",
            messages=[message]
        )
        
        assert conversation.conversation_id == "conv_abc123"
        assert conversation.with_contact == "user2"
        assert len(conversation.messages) == 1
        assert conversation.messages[0].body == "Hello, world!"
