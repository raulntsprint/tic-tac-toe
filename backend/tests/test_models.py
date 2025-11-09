"""Tests for Pydantic models."""
import pytest
from pydantic import ValidationError
from app.models import (
    GameMode,
    Player,
    MoveRequest,
    GameState,
    NewGameRequest,
    GameResponse,
)


class TestGameMode:
    """Test GameMode enum."""

    def test_game_mode_values(self):
        """Test that GameMode has correct values."""
        assert GameMode.ALGORITHMIC == "algorithmic"
        assert GameMode.GROK_AI == "grok_ai"


class TestPlayer:
    """Test Player enum."""

    def test_player_values(self):
        """Test that Player has correct values."""
        assert Player.X == "X"
        assert Player.O == "O"


class TestMoveRequest:
    """Test MoveRequest model."""

    def test_valid_move_request(self):
        """Test creating a valid move request."""
        move = MoveRequest(row=0, col=1)
        assert move.row == 0
        assert move.col == 1

    def test_invalid_row_negative(self):
        """Test that negative row is rejected."""
        with pytest.raises(ValidationError):
            MoveRequest(row=-1, col=0)

    def test_invalid_row_too_large(self):
        """Test that row > 2 is rejected."""
        with pytest.raises(ValidationError):
            MoveRequest(row=3, col=0)

    def test_invalid_col_negative(self):
        """Test that negative col is rejected."""
        with pytest.raises(ValidationError):
            MoveRequest(row=0, col=-1)

    def test_invalid_col_too_large(self):
        """Test that col > 2 is rejected."""
        with pytest.raises(ValidationError):
            MoveRequest(row=0, col=3)

    def test_missing_fields(self):
        """Test that missing fields are rejected."""
        with pytest.raises(ValidationError):
            MoveRequest(row=0)


class TestGameState:
    """Test GameState model."""

    def test_valid_game_state(self):
        """Test creating a valid game state."""
        board = [["X", "O", ""], ["", "", ""], ["", "", ""]]
        state = GameState(
            board=board,
            current_turn="X",
            winner=None,
            is_draw=False,
            game_over=False,
            mode="algorithmic",
        )
        assert state.board == board
        assert state.current_turn == "X"
        assert state.winner is None
        assert state.is_draw is False
        assert state.game_over is False
        assert state.mode == "algorithmic"

    def test_game_state_with_winner(self):
        """Test game state with a winner."""
        state = GameState(
            board=[["X", "X", "X"], ["O", "O", ""], ["", "", ""]],
            current_turn="O",
            winner="X",
            is_draw=False,
            game_over=True,
            mode="algorithmic",
        )
        assert state.winner == "X"
        assert state.game_over is True

    def test_invalid_board_size(self):
        """Test that invalid board size is rejected."""
        with pytest.raises(ValidationError):
            GameState(
                board=[["X", "O"]],  # Wrong size
                current_turn="X",
                winner=None,
                is_draw=False,
                game_over=False,
                mode="algorithmic",
            )


class TestNewGameRequest:
    """Test NewGameRequest model."""

    def test_valid_algorithmic_mode(self):
        """Test creating new game with algorithmic mode."""
        request = NewGameRequest(mode=GameMode.ALGORITHMIC)
        assert request.mode == GameMode.ALGORITHMIC

    def test_valid_grok_ai_mode(self):
        """Test creating new game with grok_ai mode."""
        request = NewGameRequest(mode=GameMode.GROK_AI)
        assert request.mode == GameMode.GROK_AI

    def test_default_mode(self):
        """Test that default mode is algorithmic."""
        request = NewGameRequest()
        assert request.mode == GameMode.ALGORITHMIC


class TestGameResponse:
    """Test GameResponse model."""

    def test_valid_game_response(self):
        """Test creating a valid game response."""
        state = GameState(
            board=[["", "", ""], ["", "", ""], ["", "", ""]],
            current_turn="X",
            winner=None,
            is_draw=False,
            game_over=False,
            mode="algorithmic",
        )
        response = GameResponse(
            session_id="test-123",
            state=state,
            message="Game created",
        )
        assert response.session_id == "test-123"
        assert response.state == state
        assert response.message == "Game created"

    def test_game_response_without_message(self):
        """Test game response without message."""
        state = GameState(
            board=[["", "", ""], ["", "", ""], ["", "", ""]],
            current_turn="X",
            winner=None,
            is_draw=False,
            game_over=False,
            mode="algorithmic",
        )
        response = GameResponse(session_id="test-123", state=state)
        assert response.message is None

