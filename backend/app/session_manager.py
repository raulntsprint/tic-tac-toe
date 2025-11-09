"""Session management for Tic Tac Toe games."""
from typing import Dict, Optional
import uuid
from .game_logic import TicTacToeGame
from .models import GameMode


class SessionManager:
    """Manage game sessions in memory."""

    def __init__(self) -> None:
        """Initialize the session manager."""
        self.sessions: Dict[str, Dict] = {}

    def create_session(self, mode: GameMode) -> str:
        """
        Create a new game session.

        Args:
            mode: Game mode (ALGORITHMIC or GROK_AI)

        Returns:
            str: Unique session ID
        """
        session_id = str(uuid.uuid4())
        game = TicTacToeGame()
        self.sessions[session_id] = {"game": game, "mode": mode}
        return session_id

    def get_session(self, session_id: str) -> Optional[Dict]:
        """
        Get a game session by ID.

        Args:
            session_id: Session ID

        Returns:
            Optional[Dict]: Session data or None if not found
        """
        return self.sessions.get(session_id)

    def delete_session(self, session_id: str) -> bool:
        """
        Delete a game session.

        Args:
            session_id: Session ID

        Returns:
            bool: True if session was deleted, False if not found
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False

    def session_exists(self, session_id: str) -> bool:
        """
        Check if a session exists.

        Args:
            session_id: Session ID

        Returns:
            bool: True if session exists, False otherwise
        """
        return session_id in self.sessions
