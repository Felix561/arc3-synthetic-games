"""Local, memory-only browser player. No recording or scorecard service."""

import secrets
import time
from contextlib import asynccontextmanager
from pathlib import Path
from threading import RLock

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field, StrictInt

from .dataset import catalog, dataset_root, find_game, verify_dataset
from .native import NativeGame


class Body(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class Start(Body):
    game_id: str = Field(max_length=80)
    level: StrictInt = Field(default=0, ge=0, le=6)


class Select(Body):
    level: StrictInt = Field(ge=0, le=6)


class Action(Body):
    action_id: StrictInt = Field(ge=0, le=7)
    data: dict = Field(default_factory=dict)


def create_app(port=8780):
    verify_dataset()
    sessions, lock, csrf = {}, RLock(), secrets.token_urlsafe(32)

    @asynccontextmanager
    async def lifespan(app):
        yield
        sessions.clear()

    app = FastAPI(
        title="ARC3 Synthetic Games", docs_url=None, redoc_url=None, openapi_url=None, lifespan=lifespan
    )
    static = Path(__file__).parent / "static"

    @app.middleware("http")
    async def local_boundary(request: Request, call_next):
        hosts = {f"127.0.0.1:{port}", f"localhost:{port}"}
        if request.headers.get("host") not in hosts:
            return JSONResponse({"detail": "Use the local player address"}, 403)
        origin = request.headers.get("origin")
        if (origin and origin not in {f"http://{h}" for h in hosts}) or request.headers.get(
            "sec-fetch-site"
        ) == "cross-site":
            return JSONResponse({"detail": "Same-origin requests only"}, 403)
        if request.method not in ("GET", "HEAD"):
            if not secrets.compare_digest(request.headers.get("x-csrf-token", ""), csrf):
                return JSONResponse({"detail": "Reload the player to reconnect"}, 403)
            if request.headers.get("content-type", "").split(";")[0] != "application/json":
                return JSONResponse({"detail": "JSON body required"}, 415)
            if len(await request.body()) > 4096:
                return JSONResponse({"detail": "Request too large"}, 413)
        response = await call_next(request)
        response.headers.update(
            {
                "Cache-Control": "no-store",
                "X-Content-Type-Options": "nosniff",
                "Referrer-Policy": "no-referrer",
                "Content-Security-Policy": "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'",
            }
        )
        return response

    @app.exception_handler(ValueError)
    async def invalid(request, exc):
        return JSONResponse({"detail": str(exc)}, 409)

    def prune():
        now = time.monotonic()
        for token, (_, seen) in list(sessions.items()):
            if now - seen > 1800:
                del sessions[token]

    def perform(token, callback):
        # Per-session locking serializes state changes; no frame/action journal is stored.
        with lock:
            prune()
            if token not in sessions:
                raise ValueError("Session expired; choose a game again")
            game, _ = sessions[token]
            sessions[token] = (game, time.monotonic())
        with game.lock:
            return callback(game)

    @app.get("/api/bootstrap")
    def bootstrap():
        return {"csrf_token": csrf, "version": catalog()["version"]}

    @app.get("/api/games")
    def games():
        return [
            {
                k: v
                for k, v in g.items()
                if k
                in {
                    "id",
                    "game_id",
                    "title",
                    "teaser",
                    "controls",
                    "levels",
                    "preview",
                    "demo",
                    "default_fps",
                }
            }
            for g in catalog()["games"]
        ]

    @app.get("/api/games/{identity}/mechanics")
    def mechanics(identity: str):
        return {"text": find_game(identity)["mechanics"]}

    @app.post("/api/sessions")
    def start(body: Start):
        with lock:
            prune()
            if len(sessions) >= 16:
                raise ValueError("Close an unused game tab before starting another")
            game = NativeGame(body.game_id, body.level)
            token = secrets.token_urlsafe(32)
            sessions[token] = (game, time.monotonic())
        return {"session_id": token, "observation": game.observation}

    @app.post("/api/sessions/{token}/action")
    def action(token: str, body: Action):
        return perform(token, lambda g: g.act(body.action_id, body.data))

    @app.post("/api/sessions/{token}/level")
    def select(token: str, body: Select):
        return perform(token, lambda g: g.select_level(body.level))

    @app.post("/api/sessions/{token}/reset")
    def reset(token: str, body: Body):
        return perform(token, lambda g: g.reset())

    @app.post("/api/sessions/{token}/restart")
    def restart(token: str, body: Body):
        return perform(token, lambda g: g.restart())

    @app.delete("/api/sessions/{token}")
    def close(token: str, body: Body):
        with lock:
            sessions.pop(token, None)
        return {"closed": True}

    @app.get("/")
    def index():
        return FileResponse(static / "index.html")

    app.mount("/static", StaticFiles(directory=static), name="static")
    app.mount("/media", StaticFiles(directory=dataset_root() / "media"), name="media")
    return app
