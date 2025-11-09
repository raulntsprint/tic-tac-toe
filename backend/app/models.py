"""Pydantic models for the Tic Tac Toe game."""
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field


class GameMode(str, Enum):
    """Game mode enumeration."""

    ALGORITHMIC = "algorithmic"
    GROK_AI = "grok_ai"  # Now using Groq API (kept name for compatibility)


class Player(str, Enum):
    """Player enumeration."""

    X = "X"
    O = "O"  # noqa: E741
    EMPTY = ""


class MoveRequest(BaseModel):
    """Request model for making a move."""

    row: int = Field(..., ge=0, le=2, description="Row index (0-2)")
    col: int = Field(..., ge=0, le=2, description="Column index (0-2)")


class GameState(BaseModel):
    """Model representing the current game state."""

    board: List[List[str]] = Field(
        default_factory=lambda: [["", "", ""], ["", "", ""], ["", "", ""]]
    )
    current_turn: str = Field(default="X", description="Current player's turn")
    winner: Optional[str] = Field(default=None, description="Winner of the game")
    is_draw: bool = Field(default=False, description="Whether the game is a draw")
    game_over: bool = Field(default=False, description="Whether the game is over")
    mode: GameMode = Field(default=GameMode.ALGORITHMIC, description="AI mode")


class NewGameRequest(BaseModel):
    """Request model for creating a new game."""

    mode: GameMode = Field(
        default=GameMode.ALGORITHMIC, description="AI mode to use"
    )


class GameResponse(BaseModel):
    """Response model for game operations."""

    session_id: str = Field(..., description="Unique session identifier")
    state: GameState = Field(..., description="Current game state")
    message: Optional[str] = Field(
        default=None, description="Additional information"
    )
