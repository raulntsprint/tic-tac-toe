"""Tests for session manager."""
import pytest
from app.session_manager import SessionManager
from app.models import GameMode


class TestSessionManager:
    """Test SessionManager class."""

    def test_session_manager_creation(self):
        """Test that SessionManager can be created."""
        manager = SessionManager()
        assert manager is not None
        assert hasattr(manager, 'sessions')

    def test_create_session_algorithmic(self):
        """Test creating a session with algorithmic mode."""
        manager = SessionManager()
        session_id = manager.create_session(GameMode.ALGORITHMIC)
        
        assert session_id is not None
        assert isinstance(session_id, str)
        assert len(session_id) > 0

    def test_create_session_grok_ai(self):
        """Test creating a session with grok_ai mode."""
        manager = SessionManager()
        session_id = manager.create_session(GameMode.GROK_AI)
        
        assert session_id is not None
        assert isinstance(session_id, str)

    def test_get_existing_session(self):
        """Test retrieving an existing session."""
        manager = SessionManager()
        session_id = manager.create_session(GameMode.ALGORITHMIC)
        
        session = manager.get_session(session_id)
        assert session is not None
        assert "game" in session
        assert "mode" in session
        assert session["mode"] == GameMode.ALGORITHMIC

    def test_get_nonexistent_session(self):
        """Test that getting non-existent session returns None."""
        manager = SessionManager()
        session = manager.get_session("nonexistent-id")
        assert session is None

    def test_delete_existing_session(self):
        """Test deleting an existing session."""
        manager = SessionManager()
        session_id = manager.create_session(GameMode.ALGORITHMIC)
        
        result = manager.delete_session(session_id)
        assert result is True
        
        # Verify it's deleted
        session = manager.get_session(session_id)
        assert session is None

    def test_delete_nonexistent_session(self):
        """Test that deleting non-existent session returns False."""
        manager = SessionManager()
        result = manager.delete_session("nonexistent-id")
        assert result is False

    def test_multiple_sessions(self):
        """Test managing multiple sessions."""
        manager = SessionManager()
        
        session_id1 = manager.create_session(GameMode.ALGORITHMIC)
        session_id2 = manager.create_session(GameMode.GROK_AI)
        
        assert session_id1 != session_id2
        
        session1 = manager.get_session(session_id1)
        session2 = manager.get_session(session_id2)
        
        assert session1 is not None
        assert session2 is not None
        assert session1["mode"] == GameMode.ALGORITHMIC
        assert session2["mode"] == GameMode.GROK_AI

    def test_session_isolation(self):
        """Test that sessions are isolated from each other."""
        manager = SessionManager()
        
        session_id1 = manager.create_session(GameMode.ALGORITHMIC)
        session_id2 = manager.create_session(GameMode.ALGORITHMIC)
        
        session1 = manager.get_session(session_id1)
        session2 = manager.get_session(session_id2)
        
        # Make a move in session1
        session1["game"].make_move(0, 0, "X")
        
        # Verify session2 is unaffected
        assert session2["game"].board[0][0] == ""

    def test_session_game_state_persistence(self):
        """Test that game state persists in session."""
        manager = SessionManager()
        session_id = manager.create_session(GameMode.ALGORITHMIC)
        
        # Get session and make moves
        session = manager.get_session(session_id)
        session["game"].make_move(0, 0, "X")
        session["game"].make_move(1, 1, "O")
        
        # Retrieve session again and verify state
        session_retrieved = manager.get_session(session_id)
        assert session_retrieved["game"].board[0][0] == "X"
        assert session_retrieved["game"].board[1][1] == "O"

