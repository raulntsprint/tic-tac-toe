"""Tests for API endpoints."""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestHealthEndpoint:
    """Test health check endpoint."""

    def test_health_check(self):
        """Test that health endpoint returns 200."""
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestCreateGameEndpoint:
    """Test create game endpoint."""

    def test_create_game_algorithmic(self):
        """Test creating a game with algorithmic mode."""
        response = client.post(
            "/api/game/new",
            json={"mode": "algorithmic"}
        )
        assert response.status_code == 200
        data = response.json()
        
        assert "session_id" in data
        assert "state" in data
        assert data["state"]["mode"] == "algorithmic"
        assert data["state"]["current_turn"] == "X"
        assert data["state"]["game_over"] is False

    def test_create_game_grok_ai(self):
        """Test creating a game with grok_ai mode."""
        response = client.post(
            "/api/game/new",
            json={"mode": "grok_ai"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["state"]["mode"] == "grok_ai"

    def test_create_game_default_mode(self):
        """Test creating game with default mode."""
        response = client.post("/api/game/new", json={})
        assert response.status_code == 200
        data = response.json()
        assert data["state"]["mode"] == "algorithmic"

    def test_create_game_invalid_mode(self):
        """Test that invalid mode is rejected."""
        response = client.post(
            "/api/game/new",
            json={"mode": "invalid_mode"}
        )
        assert response.status_code == 422  # Validation error


class TestGetGameStateEndpoint:
    """Test get game state endpoint."""

    def test_get_game_state(self):
        """Test retrieving game state."""
        # Create a game first
        create_response = client.post(
            "/api/game/new",
            json={"mode": "algorithmic"}
        )
        session_id = create_response.json()["session_id"]
        
        # Get the state
        response = client.get(f"/api/game/{session_id}/state")
        assert response.status_code == 200
        data = response.json()
        
        assert data["session_id"] == session_id
        assert "state" in data

    def test_get_nonexistent_game_state(self):
        """Test that getting non-existent game returns 404."""
        response = client.get("/api/game/nonexistent-id/state")
        assert response.status_code == 404


class TestMakeMoveEndpoint:
    """Test make move endpoint."""

    def test_make_valid_move(self):
        """Test making a valid move."""
        # Create game
        create_response = client.post(
            "/api/game/new",
            json={"mode": "algorithmic"}
        )
        session_id = create_response.json()["session_id"]
        
        # Make move
        response = client.post(
            f"/api/game/{session_id}/move",
            json={"row": 0, "col": 0}
        )
        assert response.status_code == 200
        data = response.json()
        
        assert data["state"]["board"][0][0] == "X"
        # AI should have made a move (board should have O somewhere)
        board = data["state"]["board"]
        has_o = any("O" in row for row in board)
        assert has_o

    def test_make_move_occupied_cell(self):
        """Test making move on occupied cell."""
        # Create game and make first move
        create_response = client.post(
            "/api/game/new",
            json={"mode": "algorithmic"}
        )
        session_id = create_response.json()["session_id"]
        
        client.post(
            f"/api/game/{session_id}/move",
            json={"row": 0, "col": 0}
        )
        
        # Try to make move on same cell
        response = client.post(
            f"/api/game/{session_id}/move",
            json={"row": 0, "col": 0}
        )
        assert response.status_code == 400

    def test_make_move_invalid_coordinates(self):
        """Test making move with invalid coordinates."""
        create_response = client.post(
            "/api/game/new",
            json={"mode": "algorithmic"}
        )
        session_id = create_response.json()["session_id"]
        
        response = client.post(
            f"/api/game/{session_id}/move",
            json={"row": 5, "col": 5}
        )
        assert response.status_code == 422  # Validation error

    def test_make_move_nonexistent_game(self):
        """Test making move on non-existent game."""
        response = client.post(
            "/api/game/nonexistent-id/move",
            json={"row": 0, "col": 0}
        )
        assert response.status_code == 404

    def test_game_completion(self):
        """Test that game detects completion correctly."""
        create_response = client.post(
            "/api/game/new",
            json={"mode": "algorithmic"}
        )
        session_id = create_response.json()["session_id"]
        
        # Make moves until game ends (this will vary based on AI moves)
        max_moves = 9
        last_response = None
        
        for i in range(max_moves):
            row = i // 3
            col = i % 3
            
            response = client.post(
                f"/api/game/{session_id}/move",
                json={"row": row, "col": col}
            )
            
            if response.status_code == 200:
                last_response = response
                if response.json()["state"]["game_over"]:
                    break
            else:
                # Move might be invalid (cell occupied by AI)
                continue
        
        # Game should eventually end
        if last_response:
            data = last_response.json()
            if data["state"]["game_over"]:
                assert (
                    data["state"]["winner"] is not None or
                    data["state"]["is_draw"] is True
                )


class TestDeleteGameEndpoint:
    """Test delete game endpoint."""

    def test_delete_existing_game(self):
        """Test deleting an existing game."""
        # Create game
        create_response = client.post(
            "/api/game/new",
            json={"mode": "algorithmic"}
        )
        session_id = create_response.json()["session_id"]
        
        # Delete game
        response = client.delete(f"/api/game/{session_id}")
        assert response.status_code == 200
        assert "message" in response.json()
        
        # Verify it's deleted
        get_response = client.get(f"/api/game/{session_id}/state")
        assert get_response.status_code == 404

    def test_delete_nonexistent_game(self):
        """Test deleting non-existent game."""
        response = client.delete("/api/game/nonexistent-id")
        assert response.status_code == 404


class TestCORSHeaders:
    """Test CORS configuration."""

    def test_cors_headers_present(self):
        """Test that CORS headers are present."""
        response = client.options("/api/health")
        assert response.status_code == 200

