"""Tests for Tic Tac Toe game logic."""
import pytest
from app.game_logic import TicTacToeGame


@pytest.mark.unit
class TestTicTacToeGame:
    """Test TicTacToeGame class."""

    def test_initial_state(self):
        """Test initial game state."""
        game = TicTacToeGame()
        assert game.current_turn == "X"
        assert game.winner is None
        assert not game.is_draw
        assert not game.game_over
        assert len(game.board) == 3
        assert all(len(row) == 3 for row in game.board)

    def test_make_valid_move(self):
        """Test making a valid move."""
        game = TicTacToeGame()
        result = game.make_move(0, 0, "X")
        assert result is True
        assert game.board[0][0] == "X"
        assert game.current_turn == "O"

    def test_make_move_occupied_cell(self):
        """Test making a move on an occupied cell."""
        game = TicTacToeGame()
        game.make_move(0, 0, "X")
        result = game.make_move(0, 0, "O")
        assert result is False
        assert game.board[0][0] == "X"

    def test_make_move_out_of_bounds(self):
        """Test making a move out of bounds."""
        game = TicTacToeGame()
        result = game.make_move(3, 3, "X")
        assert result is False

    def test_make_move_after_game_over(self):
        """Test that moves cannot be made after game over."""
        game = TicTacToeGame()
        # Create winning condition for X
        game.board = [["X", "X", "X"], ["O", "O", ""], ["", "", ""]]
        game.check_winner()
        
        assert game.game_over is True
        result = game.make_move(2, 2, "O")
        assert result is False

    def test_check_winner_row(self):
        """Test winning condition for a row."""
        game = TicTacToeGame()
        game.board = [["X", "X", "X"], ["O", "O", ""], ["", "", ""]]
        game.check_winner()
        assert game.winner == "X"
        assert game.game_over is True

    def test_check_winner_column(self):
        """Test winning condition for a column."""
        game = TicTacToeGame()
        game.board = [["O", "X", ""], ["O", "X", ""], ["O", "", ""]]
        game.check_winner()
        assert game.winner == "O"
        assert game.game_over is True

    def test_check_winner_diagonal_main(self):
        """Test winning condition for main diagonal."""
        game = TicTacToeGame()
        game.board = [["X", "O", "O"], ["", "X", ""], ["", "", "X"]]
        game.check_winner()
        assert game.winner == "X"
        assert game.game_over is True

    def test_check_winner_diagonal_anti(self):
        """Test winning condition for anti-diagonal."""
        game = TicTacToeGame()
        game.board = [["X", "X", "O"], ["X", "O", ""], ["O", "", ""]]
        game.check_winner()
        assert game.winner == "O"
        assert game.game_over is True

    def test_check_draw(self):
        """Test draw condition."""
        game = TicTacToeGame()
        game.board = [["X", "O", "X"], ["X", "O", "O"], ["O", "X", "X"]]
        game.check_winner()
        assert game.winner is None
        assert game.is_draw is True
        assert game.game_over is True

    def test_full_game_x_wins(self):
        """Test a full game where X wins."""
        game = TicTacToeGame()
        moves = [
            (0, 0, "X"),
            (0, 1, "O"),
            (1, 1, "X"),
            (0, 2, "O"),
            (2, 2, "X"),  # X wins with diagonal
        ]
        
        for row, col, player in moves:
            game.make_move(row, col, player)
        
        assert game.winner == "X"
        assert game.game_over is True

    def test_full_game_draw(self):
        """Test a full game that ends in a draw."""
        game = TicTacToeGame()
        # Specific sequence to produce a draw:
        # X | O | X
        # X | O | O
        # O | X | X
        # This guarantees no winner
        moves_coords = [
            (0, 0),  # X
            (0, 1),  # O
            (0, 2),  # X
            (1, 0),  # O (Block X at 1,0) - No wait, this needs to be X
        ]
        
        # Let me use the exact sequence from the fixture draw_board
        # X | O | X
        # X | O | O  
        # O | X | O
        moves_coords = [
            (0, 0),  # X
            (0, 1),  # O
            (0, 2),  # X
            (1, 2),  # O
            (1, 0),  # X
            (1, 1),  # O
            (2, 1),  # X
            (2, 0),  # O
            (2, 2),  # O - But wait, it should be X's turn!
        ]
        
        # Correct: alternate properly
        game.make_move(0, 0, "X")  # X
        game.make_move(0, 1, "O")  # O
        game.make_move(0, 2, "X")  # X
        game.make_move(1, 2, "O")  # O
        game.make_move(1, 0, "X")  # X
        game.make_move(1, 1, "O")  # O
        game.make_move(2, 1, "X")  # X
        game.make_move(2, 0, "O")  # O
        game.make_move(2, 2, "X")  # X - Last move
        
        # Result should be:
        # X | O | X
        # X | O | O
        # O | X | X
        
        assert game.winner is None
        assert game.is_draw is True
        assert game.game_over is True

    def test_alternating_turns(self):
        """Test that turns alternate correctly."""
        game = TicTacToeGame()
        assert game.current_turn == "X"
        
        game.make_move(0, 0, "X")
        assert game.current_turn == "O"
        
        game.make_move(0, 1, "O")
        assert game.current_turn == "X"
