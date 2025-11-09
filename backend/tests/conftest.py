"""Pytest configuration and fixtures."""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.session_manager import SessionManager


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def session_manager():
    """Create a fresh session manager for each test."""
    return SessionManager()


@pytest.fixture
def empty_board():
    """Return an empty 3x3 board."""
    return [["", "", ""], ["", "", ""], ["", "", ""]]


@pytest.fixture
def sample_board_x_wins():
    """Return a board where X wins (top row)."""
    return [["X", "X", "X"], ["O", "O", ""], ["", "", ""]]


@pytest.fixture
def sample_board_o_wins():
    """Return a board where O wins (diagonal)."""
    return [["O", "X", "X"], ["X", "O", ""], ["", "", "O"]]


@pytest.fixture
def sample_board_draw():
    """Return a board that results in a draw."""
    return [["X", "O", "X"], ["X", "O", "O"], ["O", "X", "X"]]


@pytest.fixture
def sample_board_in_progress():
    """Return a board with a game in progress."""
    return [["X", "O", ""], ["O", "X", ""], ["", "", ""]]

