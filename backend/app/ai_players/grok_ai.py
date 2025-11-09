"""AI player using Groq API."""
from typing import List, Tuple, Optional
import httpx
import json
import os
import logging
from .algorithmic import MinimaxPlayer


logger = logging.getLogger(__name__)


class GrokAIPlayer:
    """AI player using Groq API (renamed from Grok for compatibility)."""

    def __init__(self, api_key: Optional[str] = None) -> None:
        """
        Initialize the Groq AI player.

        Args:
            api_key: Groq API key (if None, reads from environment)
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.api_url = os.getenv(
            "GROQ_API_URL", "https://api.groq.com/openai/v1/chat/completions"
        )
        self.fallback_player = MinimaxPlayer("O")

    async def get_best_move(
        self, board: List[List[str]]
    ) -> Optional[Tuple[int, int]]:
        """
        Get the best move using Groq API.

        Args:
            board: Current board state

        Returns:
            Optional[Tuple[int, int]]: Best move as (row, col) or None
        """
        if not self.api_key:
            logger.warning("Groq API key not found, using fallback algorithm")
            return self.fallback_player.get_best_move(board)

        try:
            move = await self._query_groq(board)
            if move and self._is_valid_move(board, move):
                logger.info(f"✅ Using Groq AI - move: {move}")
                return move
            else:
                logger.warning(
                    "Invalid move from Groq, using fallback algorithm"
                )
                return self.fallback_player.get_best_move(board)
        except Exception as e:
            logger.error(f"Error querying Groq API: {e}")
            return self.fallback_player.get_best_move(board)

    async def _query_groq(
        self, board: List[List[str]]
    ) -> Optional[Tuple[int, int]]:
        """
        Query the Groq API for the best move.

        Args:
            board: Current board state

        Returns:
            Optional[Tuple[int, int]]: Best move or None
        """
        prompt = self._create_prompt(board)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": "llama-3.1-70b-versatile",  # Groq's fast model
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are an expert Tic Tac Toe player. "
                        "You play as 'O'. Analyze the board and respond "
                        "with ONLY a JSON object in this exact format: "
                        '{"row": <number>, "col": <number>}. '
                        "Row and col must be 0, 1, or 2. "
                        "No additional text or explanation."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.3,
            "max_tokens": 50,
        }

        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(
                self.api_url, headers=headers, json=payload
            )
            response.raise_for_status()
            data = response.json()

            content = data["choices"][0]["message"]["content"].strip()
            logger.info(f"Groq response: {content}")

            # Try to extract JSON even if there's extra text
            if "{" in content and "}" in content:
                start = content.index("{")
                end = content.rindex("}") + 1
                json_str = content[start:end]
                move_data = json.loads(json_str)
            else:
                move_data = json.loads(content)

            row = int(move_data["row"])
            col = int(move_data["col"])

            return (row, col)

    def _create_prompt(self, board: List[List[str]]) -> str:
        """
        Create a prompt for the Groq API.

        Args:
            board: Current board state

        Returns:
            str: Prompt string
        """
        board_str = ""
        for i, row in enumerate(board):
            row_str = " | ".join([cell if cell else " " for cell in row])
            board_str += f"Row {i}: {row_str}\n"

        prompt = f"""
Current Tic Tac Toe board (you are 'O'):

{board_str}

Analyze the board and make the best move. Consider:
1. Can you win in this move?
2. Must you block opponent's winning move?
3. Strategic position (center, corners, edges)

Respond with JSON: {{"row": <0-2>, "col": <0-2>}}
"""
        return prompt

    def _is_valid_move(
        self, board: List[List[str]], move: Tuple[int, int]
    ) -> bool:
        """
        Validate if a move is legal.

        Args:
            board: Current board state
            move: Move to validate (row, col)

        Returns:
            bool: True if move is valid, False otherwise
        """
        row, col = move
        if row < 0 or row > 2 or col < 0 or col > 2:
            return False
        return board[row][col] == ""
