import pytest
from fastapi.testclient import TestClient

from arc3_synthetic_games.server import create_app


@pytest.fixture
def client():
    with TestClient(create_app(), base_url="http://127.0.0.1:8780") as c:
        c.headers["x-csrf-token"] = c.get("/api/bootstrap").json()["csrf_token"]
        yield c


def test_player_session_flow_and_optional_reveals(client):
    games = client.get("/api/games").json()
    assert len(games) == 30 and all("mechanics" not in g for g in games)
    assert "text" in client.get("/api/games/sg01/mechanics").json()
    start = client.post("/api/sessions", json={"game_id": "sg01", "level": 0}).json()
    token = start["session_id"]
    path = "/api/sessions/" + token
    first = start["observation"]["frames"][-1]
    assert client.post(path + "/action", json={"action_id": 4}).status_code == 200
    assert client.post(path + "/reset", json={}).json()["frames"][-1] == first
    assert client.post(path + "/level", json={"level": 6}).json()["level_index"] == 6
    assert client.post(path + "/restart", json={}).json()["level_index"] == 0
    assert client.request("DELETE", path, json={}).json() == {"closed": True}
    assert client.post(path + "/action", json={"action_id": 4}).status_code == 409


def test_local_request_boundary_and_known_game_allowlist(client):
    assert client.post("/api/sessions", json={"game_id": "../unknown"}).status_code == 409
    assert client.post("/api/sessions", json={"game_id": "sg01", "level": True}).status_code == 422
    assert (
        client.post(
            "/api/sessions", json={"game_id": "sg01"}, headers={"origin": "https://example.org"}
        ).status_code
        == 403
    )
    assert client.get("/api/games", headers={"host": "example.org"}).status_code == 403
    assert (
        client.post("/api/sessions", json={"game_id": "sg01"}, headers={"x-csrf-token": "wrong"}).status_code
        == 403
    )


def test_independent_tabs_and_real_click_coordinates(client):
    left = client.post("/api/sessions", json={"game_id": "sg06"}).json()
    right = client.post("/api/sessions", json={"game_id": "sg06"}).json()
    assert left["session_id"] != right["session_id"]
    response = client.post(
        "/api/sessions/" + left["session_id"] + "/action", json={"action_id": 6, "data": {"x": 32, "y": 32}}
    )
    assert response.status_code == 200
    right_reset = client.post("/api/sessions/" + right["session_id"] + "/reset", json={}).json()
    assert right_reset["frames"][-1] == right["observation"]["frames"][-1]


def test_static_assets_and_no_recording_endpoints(client):
    assert client.get("/").status_code == 200
    assert client.get("/media/previews/sg01.png").headers["content-type"] == "image/png"
    assert client.get("/api/recordings").status_code == 404
    assert client.get("/static/app.js").headers["content-security-policy"].startswith("default-src 'self'")
