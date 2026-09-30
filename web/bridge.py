"""Browser-only, in-memory adapter to the same native player used locally."""

import json
import re

from arc3_synthetic_games.dataset import verify_dataset
from arc3_synthetic_games.native import NativeGame

verify_dataset()
_sessions = {}
_serial = 0


def request(payload):
    global _serial
    message = json.loads(payload)
    path, method, body = message["path"], message["method"], message["body"]
    if path == "/api/sessions" and method == "POST":
        if len(_sessions) >= 16:
            raise ValueError("Close a game before opening another")
        game = NativeGame(body["game_id"], body.get("level", 0))
        _serial += 1
        identity = f"browser-{_serial}"
        _sessions[identity] = game
        result = {"session_id": identity, "observation": game.observation}
    else:
        match = re.fullmatch(r"/api/sessions/(browser-\d+)(?:/(action|level|reset|restart))?", path)
        if not match or match[1] not in _sessions:
            raise ValueError("Unknown game session")
        identity, operation = match.groups()
        game = _sessions[identity]
        if method == "DELETE" and operation is None:
            del _sessions[identity]
            result = {"closed": True}
        elif method != "POST":
            raise ValueError("Unsupported operation")
        elif operation == "action":
            result = game.act(body["action_id"], body.get("data", {}))
        elif operation == "level":
            result = game.select_level(body["level"])
        elif operation == "reset":
            result = game.reset()
        elif operation == "restart":
            result = game.restart()
        else:
            raise ValueError("Unsupported operation")
    return json.dumps(result, separators=(",", ":"))
