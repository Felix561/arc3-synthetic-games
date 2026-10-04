import hashlib
import json

from arc3_synthetic_games.dataset import catalog, dataset_root, find_game, verify_dataset


def test_exact_native_inventory_and_assets():
    assert verify_dataset() == {
        "verified": True,
        "version": "1.1.0",
        "games": 30,
        "levels": 210,
        "native_files": 60,
    }
    data = catalog()
    assert len({g["game_id"] for g in data["games"]}) == 30
    root = dataset_root()
    for game in data["games"]:
        assert game["preview"].startswith("media/previews/")
        assert (root / game["preview"]).read_bytes().startswith(b"\x89PNG")
        assert find_game(game["id"]) == find_game(game["game_id"])
    demos = [g for g in data["games"] if g.get("demo")]
    assert {g["id"] for g in demos} == {"sg01", "sg06", "sg08", "sg24", "sg26", "sg28"}
    for game in demos:
        assert (root / game["demo"]).read_bytes().startswith(b"GIF89a")


def test_metadata_is_standard_and_contains_no_private_fields():
    root = dataset_root()
    for game in catalog()["games"]:
        metadata = json.loads((root / game["environment_path"] / "metadata.json").read_text())
        assert set(metadata) == {"class_name", "default_fps", "game_id", "tags", "title", "version"}
        for relative, digest in game["files_sha256"].items():
            assert (
                hashlib.sha256((root / game["environment_path"] / relative).read_bytes()).hexdigest()
                == digest
            )
