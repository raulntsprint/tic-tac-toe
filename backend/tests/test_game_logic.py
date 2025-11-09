"""Tests for game logic."""
import pytest
from app.game_logic import TicTacToeGame


class TestTicTacToeGame:
    """Test TicTacToeGame class."""

    def test_initial_state(self):
        """Test that game initializes with correct state."""
        game = TicTacToeGame()
        assert game.board == [["", "", ""], ["", "", ""], ["", "", ""]]
        assert game.current_turn == "X"
        assert game.winner is None
        assert game.is_draw is False
        assert game.game_over is False

    def test_make_valid_move(self):
        """Test making a valid move."""
        game = TicTacToeGame()
        result = game.make_move(0, 0, "X")
        assert result is True
        assert game.board[0][0] == "X"
        assert game.current_turn == "O"

    def test_make_move_occupied_cell(self):
        """Test that making a move on occupied cell fails."""
        game = TicTacToeGame()
        game.make_move(0, 0, "X")
        result = game.make_move(0, 0, "O")
        assert result is False
        assert game.board[0][0] == "X"

    def test_make_move_out_of_bounds(self):
        """Test that out of bounds move fails."""
        game = TicTacToeGame()
        result = game.make_move(3, 3, "X")
        assert result is False

    def test_make_move_after_game_over(self):
        """Test that moves cannot be made after game is over."""
        game = TicTacToeGame()
        # Create winning condition
        game.make_move(0, 0, "X")
        game.make_move(1, 0, "O")
        game.make_move(0, 1, "X")
        game.make_move(1, 1, "O")
        game.make_move(0, 2, "X")  # X wins
        
        assert game.game_over is True
        result = game.make_move(2, 2, "O")
        assert result is False

    def test_check_winner_row(self):
        """Test winning condition for a row."""
        game = TicTacToeGame()
        game.board = [["X", "X", "X"], ["O", "O", ""], ["", "", ""]]
        game._check_winner()
        assert game.winner == "X"
        assert game.game_over is True

    def test_check_winner_column(self):
        """Test winning condition for a column."""
        game = TicTacToeGame()
        game.board = [["O", "X", ""], ["O", "X", ""], ["O", "", ""]]
        game._check_winner()
        assert game.winner == "O"
        assert game.game_over is True

    def test_check_winner_diagonal_main(self):
        """Test winning condition for main diagonal."""
        game = TicTacToeGame()
        game.board = [["X", "O", "O"], ["", "X", ""], ["", "", "X"]]
        game._check_winner()
        assert game.winner == "X"
        assert game.game_over is True

    def test_check_winner_diagonal_anti(self):
        """Test winning condition for anti-diagonal."""
        game = TicTacToeGame()
        game.board = [["X", "X", "O"], ["X", "O", ""], ["O", "", ""]]
        game._check_winner()
        assert game.winner == "O"
        assert game.game_over is True

    def test_check_draw(self):
        """Test draw condition."""
        game = TicTacToeGame()
        game.board = [["X", "O", "X"], ["X", "O", "O"], ["O", "X", "X"]]
        game._check_winner()
        assert game.winner is None
        assert game.is_draw is True
        assert game.game_over is True

    def test_full_game_x_wins(self):
        """Test a full game where X wins."""
        game = TicTacToeGame()
        moves = [
            (0, 0, "X"),  # X
            (1, 0, "O"),  # O
            (0, 1, "X"),  # X
            (1, 1, "O"),  # O
            (0, 2, "X"),  # X wins
        ]
        
        for row, col, player in moves:
            game.make_move(row, col, player)
        
        assert game.winner == "X"
        assert game.game_over is True

    def test_full_game_draw(self):
        """Test a full game that results in a draw."""
        game = TicTacToeGame()
        moves = [
            (0, 0, "X"),
            (0, 1, "O"),
            (0, 2, "X"),
            (1, 0, "X"),
            (1, 1, "O"),
            (1, 2, "O"),
            (2, 0, "O"),
            (2, 1, "X"),
            (2, 2, "X"),
        ]
        
        for row, col, player in moves:
            game.make_move(row, col, player)
        
        assert game.winner is None
        assert game.is_draw is True
        assert game.game_over is True

    def test_alternating_turns(self):
        """Test that turns alternate correctly."""
        game = TicTacToeGame()
        assert game.current_turn == "X"
        
        game.make_move(0, 0, "X")
        assert game.current_turn == "O"
        
        game.make_move(1, 1, "O")
        assert game.current_turn == "X"
        
        game.make_move(2, 2, "X")
        assert game.current_turn == "O"

