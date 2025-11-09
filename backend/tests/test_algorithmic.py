"""Tests for Minimax AI algorithm."""
import pytest
from app.ai_players.algorithmic import MinimaxPlayer


class TestMinimaxPlayer:
    """Test MinimaxPlayer class."""

    def test_initialization(self):
        """Test that MinimaxPlayer initializes correctly."""
        player = MinimaxPlayer("O")
        assert player.symbol == "O"

    def test_win_in_one_move_row(self):
        """Test AI wins when it can complete a row."""
        player = MinimaxPlayer("O")
        board = [["O", "O", ""], ["X", "X", ""], ["", "", ""]]
        move = player.get_best_move(board)
        assert move == (0, 2)  # Complete the row

    def test_block_opponent_win(self):
        """Test AI blocks opponent's winning move."""
        player = MinimaxPlayer("O")
        board = [["X", "X", ""], ["O", "", ""], ["", "", ""]]
        move = player.get_best_move(board)
        assert move == (0, 2)  # Block X from winning

    def test_choose_center_on_empty_board(self):
        """Test AI prefers center on empty board."""
        player = MinimaxPlayer("O")
        board = [["", "", ""], ["", "", ""], ["", "", ""]]
        move = player.get_best_move(board)
        # Center or corner should be chosen (optimal first move)
        assert move in [(1, 1), (0, 0), (0, 2), (2, 0), (2, 2)]

    def test_no_move_on_full_board(self):
        """Test AI returns None when board is full."""
        player = MinimaxPlayer("O")
        board = [["X", "O", "X"], ["X", "O", "O"], ["O", "X", "X"]]
        move = player.get_best_move(board)
        assert move is None

    def test_win_diagonal(self):
        """Test AI completes a diagonal win."""
        player = MinimaxPlayer("O")
        board = [["O", "X", ""], ["X", "O", ""], ["", "", ""]]
        move = player.get_best_move(board)
        assert move == (2, 2)  # Complete diagonal

    def test_minimax_optimal_play(self):
        """Test that minimax makes optimal moves."""
        player = MinimaxPlayer("O")
        
        # Scenario: O can win or block, should win
        board = [
            ["O", "X", "X"],
            ["O", "X", ""],
            ["", "", ""]
        ]
        move = player.get_best_move(board)
        assert move == (2, 0)  # Win by completing column

    def test_is_terminal_state_win(self):
        """Test terminal state detection for win."""
        player = MinimaxPlayer("O")
        board = [["X", "X", "X"], ["O", "O", ""], ["", "", ""]]
        assert player._is_terminal(board) is True

    def test_is_terminal_state_draw(self):
        """Test terminal state detection for draw."""
        player = MinimaxPlayer("O")
        board = [["X", "O", "X"], ["X", "O", "O"], ["O", "X", "X"]]
        assert player._is_terminal(board) is True

    def test_is_not_terminal_state(self):
        """Test non-terminal state."""
        player = MinimaxPlayer("O")
        board = [["X", "O", ""], ["", "", ""], ["", "", ""]]
        assert player._is_terminal(board) is False

    def test_evaluate_win_for_o(self):
        """Test evaluation when O wins."""
        player = MinimaxPlayer("O")
        board = [["O", "O", "O"], ["X", "X", ""], ["", "", ""]]
        score = player._evaluate(board)
        assert score == 1

    def test_evaluate_win_for_x(self):
        """Test evaluation when X wins."""
        player = MinimaxPlayer("O")
        board = [["X", "X", "X"], ["O", "O", ""], ["", "", ""]]
        score = player._evaluate(board)
        assert score == -1

    def test_evaluate_draw(self):
        """Test evaluation for draw."""
        player = MinimaxPlayer("O")
        board = [["X", "O", "X"], ["X", "O", "O"], ["O", "X", "X"]]
        score = player._evaluate(board)
        assert score == 0

    def test_get_available_moves(self):
        """Test getting available moves."""
        player = MinimaxPlayer("O")
        board = [["X", "", ""], ["", "O", ""], ["", "", ""]]
        moves = player._get_available_moves(board)
        expected = [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]
        assert sorted(moves) == sorted(expected)

    def test_perfect_play_cannot_lose(self):
        """Test that minimax never loses when playing optimally."""
        player_o = MinimaxPlayer("O")
        player_x = MinimaxPlayer("X")
        
        board = [["", "", ""], ["", "", ""], ["", "", ""]]
        current_player = "X"
        
        # Simulate full game with both using minimax
        for _ in range(9):
            if current_player == "X":
                move = player_x.get_best_move(board)
            else:
                move = player_o.get_best_move(board)
            
            if move is None:
                break
            
            row, col = move
            board[row][col] = current_player
            
            # Check for winner
            winner = player_o._check_winner(board)
            if winner:
                # With perfect play, neither should win
                pytest.fail(f"Player {winner} won with perfect play!")
            
            current_player = "O" if current_player == "X" else "X"
        
        # Should end in draw
        assert player_o._check_winner(board) is None

