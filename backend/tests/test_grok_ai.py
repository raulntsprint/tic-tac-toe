"""Tests for Groq AI player."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.ai_players.grok_ai import GrokAIPlayer


class TestGrokAIPlayer:
    """Test GrokAIPlayer class."""

    def test_initialization_with_api_key(self):
        """Test initialization with API key."""
        player = GrokAIPlayer(api_key="test-key")
        assert player.api_key == "test-key"

    def test_initialization_without_api_key(self):
        """Test initialization without API key falls back to env."""
        with patch.dict("os.environ", {}, clear=True):
            player = GrokAIPlayer()
            assert player.api_key is None

    @pytest.mark.asyncio
    async def test_fallback_when_no_api_key(self):
        """Test that AI falls back to Minimax when no API key."""
        player = GrokAIPlayer(api_key=None)
        board = [["X", "O", ""], ["", "", ""], ["", "", ""]]
        
        move = await player.get_best_move(board)
        assert move is not None
        assert isinstance(move, tuple)
        assert len(move) == 2

    @pytest.mark.asyncio
    async def test_successful_groq_api_call(self):
        """Test successful Groq API call."""
        player = GrokAIPlayer(api_key="test-key")
        board = [["X", "O", ""], ["", "", ""], ["", "", ""]]
        
        # Mock the HTTP response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": '{"row": 1, "col": 1}'
                    }
                }
            ]
        }
        mock_response.raise_for_status = MagicMock()
        
        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(
                return_value=mock_response
            )
            
            move = await player.get_best_move(board)
            assert move == (1, 1)

    @pytest.mark.asyncio
    async def test_groq_api_returns_invalid_move(self):
        """Test fallback when Groq returns invalid move."""
        player = GrokAIPlayer(api_key="test-key")
        board = [["X", "", ""], ["", "", ""], ["", "", ""]]
        
        # Mock response with occupied cell
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": '{"row": 0, "col": 0}'  # Already occupied by X
                    }
                }
            ]
        }
        mock_response.raise_for_status = MagicMock()
        
        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(
                return_value=mock_response
            )
            
            move = await player.get_best_move(board)
            # Should fall back to Minimax
            assert move is not None
            assert move != (0, 0)  # Should not return the invalid move

    @pytest.mark.asyncio
    async def test_groq_api_exception(self):
        """Test fallback when Groq API raises exception."""
        player = GrokAIPlayer(api_key="test-key")
        board = [["X", "", ""], ["", "", ""], ["", "", ""]]
        
        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(
                side_effect=Exception("API Error")
            )
            
            move = await player.get_best_move(board)
            # Should fall back to Minimax
            assert move is not None

    def test_is_valid_move(self):
        """Test move validation."""
        player = GrokAIPlayer(api_key="test-key")
        board = [["X", "O", ""], ["", "", ""], ["", "", ""]]
        
        # Valid moves
        assert player._is_valid_move(board, (0, 2)) is True
        assert player._is_valid_move(board, (1, 1)) is True
        
        # Invalid moves (occupied)
        assert player._is_valid_move(board, (0, 0)) is False
        assert player._is_valid_move(board, (0, 1)) is False
        
        # Invalid moves (out of bounds)
        assert player._is_valid_move(board, (3, 0)) is False
        assert player._is_valid_move(board, (0, 3)) is False
        assert player._is_valid_move(board, (-1, 0)) is False

    def test_create_prompt(self):
        """Test prompt creation."""
        player = GrokAIPlayer(api_key="test-key")
        board = [["X", "O", ""], ["", "X", ""], ["", "", "O"]]
        
        prompt = player._create_prompt(board)
        
        assert "Row 0: X | O |" in prompt
        assert "Row 1:   | X |" in prompt
        assert "Row 2:   |   | O" in prompt
        assert "you are 'O'" in prompt
        assert "best move" in prompt

    @pytest.mark.asyncio
    async def test_groq_response_with_extra_text(self):
        """Test handling Groq response with extra text."""
        player = GrokAIPlayer(api_key="test-key")
        board = [["X", "", ""], ["", "", ""], ["", "", ""]]
        
        # Mock response with extra text
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": 'The best move is {"row": 1, "col": 1} because...'
                    }
                }
            ]
        }
        mock_response.raise_for_status = MagicMock()
        
        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(
                return_value=mock_response
            )
            
            move = await player.get_best_move(board)
            assert move == (1, 1)

    @pytest.mark.asyncio
    async def test_groq_malformed_json(self):
        """Test fallback when Groq returns malformed JSON."""
        player = GrokAIPlayer(api_key="test-key")
        board = [["X", "", ""], ["", "", ""], ["", "", ""]]
        
        # Mock response with malformed JSON
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": 'Not a JSON response'
                    }
                }
            ]
        }
        mock_response.raise_for_status = MagicMock()
        
        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(
                return_value=mock_response
            )
            
            move = await player.get_best_move(board)
            # Should fall back to Minimax
            assert move is not None

