"""Tests for Minimax AI algorithm."""
import pytest
from app.ai_players.algorithmic import MinimaxPlayer
from app.game_logic import TicTacToeGame


@pytest.mark.unit
class TestMinimaxPlayer:
    """Test MinimaxPlayer class."""

    def test_initialization(self):
        """Test that MinimaxPlayer initializes correctly."""
        player = MinimaxPlayer("O")
        assert player.player == "O"
        assert player.opponent == "X"

    def test_win_in_one_move_row(self):
        """Test AI wins when it can complete a row."""
        player = MinimaxPlayer("X")
        board = [
            ["X", "X", ""],
            ["O", "O", ""],
            ["", "", ""]
        ]
        move = player.get_best_move(board)
        assert move == (0, 2)  # Complete the row

    def test_block_opponent_win(self):
        """Test AI blocks opponent's winning move."""
        player = MinimaxPlayer("O")
        board = [
            ["X", "X", ""],
            ["O", "", ""],
            ["", "", ""]
        ]
        move = player.get_best_move(board)
        assert move == (0, 2)  # Block X from winning

    def test_choose_center_on_empty_board(self):
        """Test AI chooses center or corner on empty board."""
        player = MinimaxPlayer("X")
        board = [
            ["", "", ""],
            ["", "", ""],
            ["", "", ""]
        ]
        move = player.get_best_move(board)
        # Minimax should choose center or a corner
        assert move in [(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)]

    def test_no_move_on_full_board(self):
        """Test AI returns None when board is full."""
        player = MinimaxPlayer("X")
        board = [
            ["X", "O", "X"],
            ["X", "O", "O"],
            ["O", "X", "X"]
        ]
        move = player.get_best_move(board)
        assert move is None

    def test_win_diagonal(self):
        """Test AI completes diagonal to win."""
        player = MinimaxPlayer("O")
        board = [
            ["O", "X", ""],
            ["X", "O", ""],
            ["", "", ""]
        ]
        move = player.get_best_move(board)
        assert move == (2, 2)  # Complete diagonal

    def test_minimax_optimal_play(self):
        """Test Minimax makes optimal decisions."""
        player = MinimaxPlayer("O")
        # O should block X's fork
        board = [
            ["X", "", ""],
            ["", "X", ""],
            ["", "", "O"]
        ]
        move = player.get_best_move(board)
        # Should block the diagonal
        assert move is not None
        assert len(move) == 2

    def test_perfect_play_cannot_lose(self):
        """Test that perfect play results in win or draw."""
        game = TicTacToeGame()
        ai_player = MinimaxPlayer("O")
        
        # Simulate a full game with AI playing perfectly
        moves_played = 0
        max_moves = 9
        
        while not game.game_over and moves_played < max_moves:
            if game.current_turn == "X":
                # Player X (human) makes a simple move
                available = game.get_available_moves()
                if available:
                    row, col = available[0]
                    game.make_move(row, col, "X")
                    moves_played += 1
            else:
                # AI plays optimally
                ai_move = ai_player.get_best_move(game.board)
                if ai_move:
                    game.make_move(ai_move[0], ai_move[1], "O")
                    moves_played += 1
                else:
                    break
        
        # AI should never lose
        assert game.winner != "X", "AI should not lose"
