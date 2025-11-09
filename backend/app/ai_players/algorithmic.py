"""Algorithmic AI player using Minimax algorithm with alpha-beta pruning."""
from typing import List, Tuple, Optional
import math


class MinimaxPlayer:
    """AI player using Minimax algorithm with alpha-beta pruning."""

    def __init__(self, player: str = "O") -> None:
        """
        Initialize the Minimax player.

        Args:
            player: The player symbol ('X' or 'O')
        """
        self.player = player
        self.opponent = "X" if player == "O" else "O"

    def get_best_move(self, board: List[List[str]]) -> Optional[Tuple[int, int]]:
        """
        Get the best move using Minimax algorithm.

        Args:
            board: Current board state

        Returns:
            Optional[Tuple[int, int]]: Best move as (row, col) or None
        """
        best_score = -math.inf
        best_move = None

        for row in range(3):
            for col in range(3):
                if board[row][col] == "":
                    board[row][col] = self.player
                    score = self._minimax(
                        board, 0, False, -math.inf, math.inf
                    )
                    board[row][col] = ""

                    if score > best_score:
                        best_score = score
                        best_move = (row, col)

        return best_move

    def _minimax(  # noqa: C901
        self,
        board: List[List[str]],
        depth: int,
        is_maximizing: bool,
        alpha: float,
        beta: float,
    ) -> float:
        """
        Minimax algorithm with alpha-beta pruning.

        Args:
            board: Current board state
            depth: Current depth in the game tree
            is_maximizing: Whether it's maximizing player's turn
            alpha: Alpha value for pruning
            beta: Beta value for pruning

        Returns:
            float: Score of the position
        """
        winner = self._check_winner(board)

        if winner == self.player:
            return 10 - depth
        elif winner == self.opponent:
            return depth - 10
        elif self._is_full(board):
            return 0

        if is_maximizing:
            max_score = -math.inf
            for row in range(3):
                for col in range(3):
                    if board[row][col] == "":
                        board[row][col] = self.player
                        score = self._minimax(
                            board, depth + 1, False, alpha, beta
                        )
                        board[row][col] = ""
                        max_score = max(score, max_score)
                        alpha = max(alpha, score)
                        if beta <= alpha:
                            break
            return max_score
        else:
            min_score = math.inf
            for row in range(3):
                for col in range(3):
                    if board[row][col] == "":
                        board[row][col] = self.opponent
                        score = self._minimax(
                            board, depth + 1, True, alpha, beta
                        )
                        board[row][col] = ""
                        min_score = min(score, min_score)
                        beta = min(beta, score)
                        if beta <= alpha:
                            break
            return min_score

    def _check_winner(self, board: List[List[str]]) -> Optional[str]:
        """
        Check if there's a winner.

        Args:
            board: Current board state

        Returns:
            Optional[str]: Winner ('X' or 'O') or None
        """
        # Check rows
        for row in board:
            if row[0] == row[1] == row[2] != "":
                return row[0]

        # Check columns
        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col] != "":
                return board[0][col]

        # Check diagonals
        if board[0][0] == board[1][1] == board[2][2] != "":
            return board[0][0]

        if board[0][2] == board[1][1] == board[2][0] != "":
            return board[0][2]

        return None

    def _is_full(self, board: List[List[str]]) -> bool:
        """
        Check if the board is full.

        Args:
            board: Current board state

        Returns:
            bool: True if board is full, False otherwise
        """
        for row in board:
            for cell in row:
                if cell == "":
                    return False
        return True
