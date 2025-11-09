"""Tests for FastAPI endpoints."""
import pytest
from fastapi.testclient import TestClient
from app.models import GameMode, MoveRequest, GameResponse


@pytest.mark.integration
class TestHealthEndpoint:
    """Test health check endpoint."""

    def test_health_check(self, client: TestClient):
        """Test health endpoint returns correct response."""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "message" in data


@pytest.mark.integration
class TestCreateGameEndpoint:
    """Test game creation endpoint."""

    def test_create_game_algorithmic(self, client: TestClient):
        """Test creating a game with algorithmic mode."""
        response = client.post("/api/game/new", json={"mode": GameMode.ALGORITHMIC.value})
        assert response.status_code == 200
        data = response.json()
        assert "session_id" in data
        assert data["state"]["mode"] == GameMode.ALGORITHMIC.value
        assert data["message"] == "New game created with algorithmic mode"

    def test_create_game_grok_ai(self, client: TestClient):
        """Test creating a game with Grok AI mode."""
        response = client.post("/api/game/new", json={"mode": GameMode.GROK_AI.value})
        assert response.status_code == 200
        data = response.json()
        assert "session_id" in data
        assert data["state"]["mode"] == GameMode.GROK_AI.value
        assert data["message"] == "New game created with grok_ai mode"

    def test_create_game_default_mode(self, client: TestClient):
        """Test creating a game without specifying mode (default)."""
        response = client.post("/api/game/new", json={})
        assert response.status_code == 200
        data = response.json()
        assert "session_id" in data
        assert data["state"]["mode"] in [GameMode.ALGORITHMIC.value, GameMode.GROK_AI.value]

    def test_create_game_invalid_mode(self, client: TestClient):
        """Test creating a game with invalid mode."""
        response = client.post("/api/game/new", json={"mode": "invalid_mode"})
        assert response.status_code == 422  # Validation error


@pytest.mark.integration
class TestGetGameStateEndpoint:
    """Test get game state endpoint."""

    def test_get_game_state(self, client: TestClient, new_game_session_id: str):
        """Test getting game state for existing session."""
        response = client.get(f"/api/game/{new_game_session_id}/state")
        assert response.status_code == 200
        data = response.json()
        assert "state" in data
        assert "session_id" in data

    def test_get_nonexistent_game_state(self, client: TestClient):
        """Test getting game state for nonexistent session."""
        response = client.get("/api/game/nonexistent-id/state")
        assert response.status_code == 404


@pytest.mark.integration
class TestMakeMoveEndpoint:
    """Test make move endpoint."""

    def test_make_valid_move(self, client: TestClient):
        """Test making a valid move."""
        # Create new game
        create_response = client.post("/api/game/new", json={"mode": GameMode.ALGORITHMIC.value})
        session_id = create_response.json()["session_id"]
        
        # Make a move
        move = MoveRequest(row=0, col=0)
        response = client.post(f"/api/game/{session_id}/move", json=move.model_dump())
        assert response.status_code == 200
        data = response.json()
        assert data["state"]["board"][0][0] == "X"

    def test_make_move_occupied_cell(self, client: TestClient):
        """Test making a move on occupied cell."""
        create_response = client.post("/api/game/new", json={"mode": GameMode.ALGORITHMIC.value})
        session_id = create_response.json()["session_id"]
        
        # First move
        move = MoveRequest(row=0, col=0)
        client.post(f"/api/game/{session_id}/move", json=move.model_dump())
        
        # Try same cell again
        response = client.post(f"/api/game/{session_id}/move", json=move.model_dump())
        assert response.status_code in [400, 422]  # Error expected

    def test_make_move_invalid_coordinates(self, client: TestClient):
        """Test making a move with invalid coordinates."""
        create_response = client.post("/api/game/new", json={"mode": GameMode.ALGORITHMIC.value})
        session_id = create_response.json()["session_id"]
        
        move = {"row": 5, "col": 5}
        response = client.post(f"/api/game/{session_id}/move", json=move)
        assert response.status_code == 422  # Validation error

    def test_make_move_nonexistent_game(self, client: TestClient):
        """Test making a move on nonexistent game."""
        move = MoveRequest(row=0, col=0)
        response = client.post("/api/game/nonexistent-id/move", json=move.model_dump())
        assert response.status_code == 404

    def test_game_completion(self, client: TestClient):
        """Test that game completes correctly."""
        create_response = client.post("/api/game/new", json={"mode": GameMode.ALGORITHMIC.value})
        session_id = create_response.json()["session_id"]
        
        # Make moves until game over
        moves_made = 0
        max_moves = 10
        
        while moves_made < max_moves:
            state_response = client.get(f"/api/game/{session_id}/state")
            game_state = state_response.json()["state"]
            
            if game_state["game_over"]:
                break
            
            # Find first available cell
            for row in range(3):
                for col in range(3):
                    if game_state["board"][row][col] == "" and game_state["current_turn"] == "X":
                        move = MoveRequest(row=row, col=col)
                        move_response = client.post(f"/api/game/{session_id}/move", json=move.model_dump())
                        if move_response.status_code == 200:
                            moves_made += 1
                            break
                else:
                    continue
                break
            else:
                break
        
        # Verify game eventually ends
        final_state = client.get(f"/api/game/{session_id}/state").json()["state"]
        assert final_state["game_over"] or moves_made >= max_moves


@pytest.mark.integration
class TestDeleteGameEndpoint:
    """Test delete game endpoint."""

    def test_delete_existing_game(self, client: TestClient):
        """Test deleting an existing game."""
        create_response = client.post("/api/game/new", json={"mode": GameMode.ALGORITHMIC.value})
        session_id = create_response.json()["session_id"]
        
        response = client.delete(f"/api/game/{session_id}")
        assert response.status_code == 200
        
        # Verify game is deleted
        get_response = client.get(f"/api/game/{session_id}/state")
        assert get_response.status_code == 404

    def test_delete_nonexistent_game(self, client: TestClient):
        """Test deleting a nonexistent game."""
        response = client.delete("/api/game/nonexistent-id")
        assert response.status_code == 404


@pytest.mark.integration
class TestCORSHeaders:
    """Test CORS configuration."""

    def test_cors_headers_present(self, client: TestClient):
        """Test that CORS headers are present."""
        # Test with a regular GET request with Origin header
        response = client.get("/api/health", headers={"Origin": "http://localhost:3000"})
        assert response.status_code == 200
        # FastAPI/Starlette CORS middleware should add these headers
        # Check for either lowercase or capitalized version
        headers_lower = {k.lower(): v for k, v in response.headers.items()}
        assert "access-control-allow-origin" in headers_lower
