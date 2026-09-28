"""Public inventory and portable package paths; no native imports."""

import hashlib
import json
from pathlib import Path


def dataset_root():
    bundled = Path(__file__).parent / "data"
    return bundled if (bundled / "catalog.json").is_file() else Path(__file__).resolve().parents[2]


def catalog():
    return json.loads((dataset_root() / "catalog.json").read_text(encoding="utf-8"))


def find_game(identity):
    for game in catalog()["games"]:
        if identity in (game["id"], game["game_id"]):
            return game
    raise ValueError("Unknown game")


def verify_dataset():
    data = catalog()
    games = data["games"]
    if len(games) != 30 or {g["id"] for g in games} != {f"sg{i:02}" for i in range(1, 31)}:
        raise ValueError("Expected exactly SG01–SG30")
    root = dataset_root().resolve()
    expected = set()
    for game in games:
        folder = root / game["environment_path"]
        for relative, digest in game["files_sha256"].items():
            path = folder / relative
            if path.is_symlink() or not path.resolve().is_relative_to(root):
                raise ValueError("Unexpected dataset link")
            if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                raise ValueError(f"Checksum mismatch in {game['id']}")
            expected.add(path.relative_to(root).as_posix())
        metadata = json.loads((folder / "metadata.json").read_text(encoding="utf-8"))
        if metadata["game_id"] != game["game_id"] or game["levels"] != 7:
            raise ValueError("Native identity mismatch")
    actual = {
        p.relative_to(root).as_posix()
        for p in (root / "environment_files").rglob("*")
        if p.is_file() and "__pycache__" not in p.parts
    }
    if expected != actual:
        raise ValueError("Missing or unexpected native files")
    return {
        "verified": True,
        "version": data["version"],
        "games": len(games),
        "levels": 210,
        "native_files": len(expected),
    }
