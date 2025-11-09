"""Core game logic for Tic Tac Toe."""
from typing import List, Optional, Tuple


class TicTacToeGame:
    """Tic Tac Toe game logic implementation."""

    def __init__(self) -> None:
        """Initialize a new game with an empty board."""
        self.board: List[List[str]] = [["", "", ""], ["", "", ""], ["", "", ""]]
        self.current_turn: str = "X"
        self.winner: Optional[str] = None
        self.is_draw: bool = False
        self.game_over: bool = False

    def make_move(self, row: int, col: int, player: str) -> bool:
        """
        Make a move on the board.

        Args:
            row: Row index (0-2)
            col: Column index (0-2)
            player: Player making the move ('X' or 'O')

        Returns:
            bool: True if move was successful, False otherwise
        """
        if self.game_over:
            return False

        if row < 0 or row > 2 or col < 0 or col > 2:
            return False

        if self.board[row][col] != "":
            return False

        if player != self.current_turn:
            return False

        self.board[row][col] = player
        self.check_winner()

        if not self.game_over:
            self.current_turn = "O" if self.current_turn == "X" else "X"

        return True

    def check_winner(self) -> Optional[str]:
        """
        Check if there's a winner or draw.

        Returns:
            Optional[str]: Winner ('X' or 'O') or None
        """
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] != "":
                self.winner = row[0]
                self.game_over = True
                return self.winner

        # Check columns
        for col in range(3):
            if (
                self.board[0][col]
                == self.board[1][col]
                == self.board[2][col]
                != ""
            ):
                self.winner = self.board[0][col]
                self.game_over = True
                return self.winner

        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            self.winner = self.board[0][0]
            self.game_over = True
            return self.winner

        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            self.winner = self.board[0][2]
            self.game_over = True
            return self.winner

        # Check for draw
        if self.is_full():
            self.is_draw = True
            self.game_over = True

        return self.winner

    def is_full(self) -> bool:
        """
        Check if the board is full.

        Returns:
            bool: True if board is full, False otherwise
        """
        for row in self.board:
            for cell in row:
                if cell == "":
                    return False
        return True

    def get_available_moves(self) -> List[Tuple[int, int]]:
        """
        Get all available moves on the board.

        Returns:
            List[Tuple[int, int]]: List of (row, col) tuples
        """
        moves = []
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == "":
                    moves.append((row, col))
        return moves

    def get_state(self) -> dict:
        """
        Get the current game state.

        Returns:
            dict: Dictionary containing game state
        """
        return {
            "board": self.board,
            "current_turn": self.current_turn,
            "winner": self.winner,
            "is_draw": self.is_draw,
            "game_over": self.game_over,
        }

    def copy_board(self) -> List[List[str]]:
        """
        Create a copy of the current board.

        Returns:
            List[List[str]]: Copy of the board
        """
        return [row[:] for row in self.board]
