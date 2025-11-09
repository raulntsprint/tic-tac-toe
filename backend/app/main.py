"""FastAPI main application for Tic Tac Toe game."""
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import (
    NewGameRequest,
    GameResponse,
    MoveRequest,
    GameState,
)
from .session_manager import SessionManager
from .ai_players.algorithmic import MinimaxPlayer
from .ai_players.grok_ai import GrokAIPlayer
from .models import GameMode


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


@app.post("/api/game/{session_id}/move", response_model=GameResponse)
async def make_move(session_id: str, move: MoveRequest) -> GameResponse:
    """
    Make a move in the game.

    Args:
        session_id: Session ID
        move: Move request with row and column

    Returns:
        GameResponse: Updated game state
    """
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    game = session["game"]
    mode = session["mode"]

    # Player's move
    if not game.make_move(move.row, move.col, "X"):
        raise HTTPException(status_code=400, detail="Invalid move")

    logger.info(
        f"Player move: ({move.row}, {move.col}) in session {session_id}"
    )

    # Check if game is over after player's move
    if game.game_over:
        state = GameState(
            board=game.board,
            current_turn=game.current_turn,
            winner=game.winner,
            is_draw=game.is_draw,
            game_over=game.game_over,
            mode=mode,
        )
        return GameResponse(
            session_id=session_id,
            state=state,
            message="Game over" if game.winner else "It's a draw!",
        )

    # AI's move - choose based on game mode
    try:
        if mode == GameMode.GROK_AI:
            ai_player = GrokAIPlayer()
            ai_move = await ai_player.get_best_move(game.board)
        else:  # GameMode.ALGORITHMIC
            ai_player = MinimaxPlayer("O")
            ai_move = ai_player.get_best_move(game.board)

        if ai_move:
            game.make_move(ai_move[0], ai_move[1], "O")
            logger.info(
                f"AI move: {ai_move} (mode: {mode.value}) in session {session_id}"
            )
        else:
            logger.warning(f"No AI move available in session {session_id}")

    except Exception as e:
        logger.error(f"Error making AI move: {e}")
        raise HTTPException(status_code=500, detail="AI move failed")

    state = GameState(
        board=game.board,
        current_turn=game.current_turn,
        winner=game.winner,
        is_draw=game.is_draw,
        game_over=game.game_over,
        mode=mode,
    )

    message = None
    if game.game_over:
        if game.winner:
            message = f"Game over! {game.winner} wins!"
        else:
            message = "It's a draw!"

    return GameResponse(session_id=session_id, state=state, message=message)


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

