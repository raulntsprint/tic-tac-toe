"""FastAPI main application for Tic Tac Toe game."""
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import (
    NewGameRequest,
    GameResponse,
    GameState,
)
from .session_manager import SessionManager


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Tic Tac Toe API",
    description="A Tic Tac Toe game with algorithmic and AI-powered opponents",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize session manager
session_manager = SessionManager()


@app.get("/api/health")
async def health_check() -> dict:
    """
    Health check endpoint.

    Returns:
        dict: Health status
    """
    return {"status": "healthy", "message": "Tic Tac Toe API is running"}


@app.post("/api/game/new", response_model=GameResponse)
async def create_game(request: NewGameRequest) -> GameResponse:
    """
    Create a new game session.

    Args:
        request: New game request with mode selection

    Returns:
        GameResponse: New game state with session ID
    """
    try:
        session_id = session_manager.create_session(request.mode)
        session = session_manager.get_session(session_id)
        game = session["game"]

        state = GameState(
            board=game.board,
            current_turn=game.current_turn,
            winner=game.winner,
            is_draw=game.is_draw,
            game_over=game.game_over,
            mode=request.mode,
        )

        logger.info(
            f"Created new game session: {session_id} with mode: {request.mode}"
        )

        return GameResponse(
            session_id=session_id,
            state=state,
            message=f"New game created with {request.mode.value} mode",
        )
    except Exception as e:
        logger.error(f"Error creating game: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/game/{session_id}/state", response_model=GameResponse)
async def get_game_state(session_id: str) -> GameResponse:
    """
    Get the current game state.

    Args:
        session_id: Session ID

    Returns:
        GameResponse: Current game state
    """
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    game = session["game"]
    mode = session["mode"]

    state = GameState(
        board=game.board,
        current_turn=game.current_turn,
        winner=game.winner,
        is_draw=game.is_draw,
        game_over=game.game_over,
        mode=mode,
    )

    return GameResponse(session_id=session_id, state=state)


@app.delete("/api/game/{session_id}")
async def delete_game(session_id: str) -> dict:
    """
    Delete a game session.

    Args:
        session_id: Session ID

    Returns:
        dict: Deletion confirmation
    """
    if session_manager.delete_session(session_id):
        logger.info(f"Deleted session: {session_id}")
        return {"message": "Game session deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Session not found")

