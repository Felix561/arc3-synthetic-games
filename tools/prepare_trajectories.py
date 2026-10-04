"""Prepare a public, source-separated projection of an already verified collection.

This is a data-only operation. It never imports environments, executes gameplay,
re-solves levels, or contacts a service. The private source directory is an input,
never a value in a public output. Native recordings are copied byte for byte;
canonical provenance is rebuilt from an explicit allowlist.
"""

from __future__ import annotations

import argparse
import copy
import csv
import gzip
import hashlib
import json
import math
import re
import statistics
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath
from typing import Any

VERSION = "arc3-source-informed-agent-20261002-v1"
SCHEMA = "arc3-public-agent-trajectories/1"
SOURCES = ("studio", "nvidia")
NVIDIA_REPOSITORY = "https://github.com/NVIDIA/dream-team"
NVIDIA_COMMIT = "bffef22f3e50fb7dcd6b2dc20005e6986e1479e9"
EXPECTED_TOTALS = {
    "games": 55, "levels": 410, "segments": 415, "solved_segments": 410,
    "unsolved_segments": 5, "short_segments": 103, "policy_actions": 6011,
    "native_responses": 6071, "native_palette_frames": 6784,
    "current_level_resets": 5, "initialisation_resets": 55,
    "clicks": 2545, "undo_actions": 7, "game_wins": 55,
}
ROW_FIELDS = (
    "schema_version", "provider", "dataset_version", "split", "game_id", "level_id",
    "episode_id", "trajectory_id", "task_id", "actor_type", "color_space", "observations",
    "actions", "selection_masks", "rewards", "scores", "is_solved", "is_terminal",
    "is_truncated", "terminal_reason", "seed", "source_metadata",
)
ACTION_FIELDS = (
    "type", "parameters", "provider_raw_action", "valid_action_types",
    "settled_frame_known", "outcome_target",
)
ACTION_NAMES = {
    1: "MOVE_UP", 2: "MOVE_DOWN", 3: "MOVE_LEFT", 4: "MOVE_RIGHT",
    5: "SPECIAL", 6: "CLICK", 7: "UNDO",
}
NATIVE_FIELDS = {
    "frame", "state", "action_input", "game_id", "guid", "levels_completed",
    "win_levels", "full_reset", "available_actions",
}
DEFINITIONS = {
    "games": "Distinct exact-version environments with one complete recorded game run each.",
    "levels": "Distinct source/game/level identities, not attempts or observation frames.",
    "segments": "Recorded nonempty level attempts; a level can have more than one segment.",
    "solved_segments": "Segments that completed their level through legal recorded actions.",
    "unsolved_segments": "Segments interrupted by a native current-level reset; not native GAME_OVER.",
    "terminal_segments": "Canonical is_terminal flags, including solved-level boundaries.",
    "truncated_segments": "Canonical is_truncated flags; retained unsuccessful reset-interrupted attempts.",
    "short_segments": "Segments with fewer than six policy actions; none were discarded.",
    "policy_actions": "Actions 1–7, including mistakes and undo; excludes initialization/current-level resets.",
    "actions_per_segment": "Min/median/arithmetic mean/max of policy-action counts over all segments.",
    "clicks": "Policy actions with native action ID 6; coordinates use canonical row/column.",
    "undo_actions": "Policy actions with native action ID 7.",
    "native_responses": "Native recording lines, including initialization and current-level reset responses.",
    "native_palette_frames": "All animation frames in native responses, represented by 64×64 palette indices.",
    "current_level_resets": "Native action ID 0 after initialization; outside canonical policy segments.",
    "initialisation_resets": "First native action ID 0 of each game run.",
    "game_wins": "Complete recorded game runs whose final native state is WIN.",
    "native_game_over_responses": "Recorded responses whose native state is GAME_OVER; not inferred from reset.",
    "terminal_reasons": "Counts of canonical segment terminal_reason strings.",
    "unknown_native_timestamps": "Native recording lines with timestamp null; original time was not captured.",
    "success_rate": "Solved segments divided by all recorded segments; descriptive collection statistic only.",
    "first_attempt_solved_levels": "Distinct levels solved in their first recorded nonempty attempt.",
    "attempts": "Alias of segments; exactly the recorded attempts, not hypothetical solver trials.",
    "replay_scope": "Fresh native replay verifies these recorded runs, not optimality or cognitive strategy.",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def safe_relative(value: str) -> str:
    if not isinstance(value, str) or "\\" in value or ":" in value:
        raise ValueError("Expected a portable relative path")
    path = PurePosixPath(value)
    if path.is_absolute() or not path.parts or any(p in (".", "..") for p in path.parts):
        raise ValueError("Unsafe relative path")
    return path.as_posix()


def checked_hash(value: str) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
        raise ValueError("Expected a SHA-256 digest")
    return value


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(json_bytes(value))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_jsonl_gzip(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as raw, gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as out:
        for row in rows:
            out.write((json.dumps(row, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode())


def verify_input(source: Path) -> dict[str, Any]:
    manifest = json.loads((source / "manifest.json").read_text(encoding="utf-8"))
    checksums = (source / "SHA256SUMS.txt").read_text(encoding="utf-8")
    entries = {}
    for line in checksums.splitlines():
        digest, name = line.split("  ", 1)
        relative = safe_relative(name)
        if relative in entries:
            raise ValueError("Duplicate input checksum path")
        entries[relative] = checked_hash(digest)
        if sha256(source / relative) != digest:
            raise ValueError(f"Input checksum mismatch: {relative}")
    needed = {"manifest.json", "trajectories/all.jsonl", "verification/collection-audit.json"}
    if not needed.issubset(entries):
        raise ValueError("Input checksum list does not cover required collection files")
    audit = json.loads((source / "verification/collection-audit.json").read_text(encoding="utf-8"))
    if not audit.get("complete") or manifest.get("final_export_fresh_replays") != 55:
        raise ValueError("The source must be the complete, final-replay-checked collection")
    return manifest


def validate_frame(frame: Any) -> None:
    if not isinstance(frame, list) or len(frame) != 64:
        raise ValueError("Expected a native 64×64 palette frame")
    for row in frame:
        if not isinstance(row, list) or len(row) != 64:
            raise ValueError("Expected a native 64×64 palette frame")
        if any(type(pixel) is not int or not 0 <= pixel <= 15 for pixel in row):
            raise ValueError("Frame contains non-palette pixels")


def validate_native(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Reject unsafe envelope additions rather than silently copy unknown metadata."""
    if not rows:
        raise ValueError("Empty native recording")
    counts = Counter()
    native_ids = set()
    for index, row in enumerate(rows):
        if set(row) != {"timestamp", "data"} or row["timestamp"] is not None:
            raise ValueError("Unexpected native envelope/timestamp; review required")
        data = row["data"]
        if set(data) != NATIVE_FIELDS or data["guid"] is not None:
            raise ValueError("Unexpected native data/opaque identifier; review required")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)+", data["game_id"]):
            raise ValueError("Unexpected native game identifier")
        native_ids.add(data["game_id"])
        action = data["action_input"]
        if set(action) != {"id", "data", "reasoning"} or action["reasoning"] is not None:
            raise ValueError("Unexpected native action metadata/reasoning; review required")
        if type(action["id"]) is not int or action["id"] not in range(8):
            raise ValueError("Invalid native action ID")
        if action["id"] == 6:
            if set(action["data"]) != {"x", "y"}:
                raise ValueError("Unexpected native click data")
            if any(type(v) is not int or not 0 <= v <= 63 for v in action["data"].values()):
                raise ValueError("Invalid native click coordinate")
        elif action["data"]:
            raise ValueError("Unexpected native non-click parameters")
        if data["state"] not in ("NOT_FINISHED", "WIN", "GAME_OVER"):
            raise ValueError("Unexpected native state")
        if not isinstance(data["frame"], list) or not data["frame"]:
            raise ValueError("No native response frames")
        for frame in data["frame"]:
            validate_frame(frame)
        if type(data["full_reset"]) is not bool:
            raise ValueError("Invalid reset indicator")
        for key in ("levels_completed", "win_levels"):
            if type(data[key]) is not int or data[key] < 0:
                raise ValueError("Invalid native level count")
        if any(type(a) is not int or a not in range(1, 8) for a in data["available_actions"]):
            raise ValueError("Invalid native available actions")
        counts["native_responses"] += 1
        counts["native_palette_frames"] += len(data["frame"])
        counts["unknown_native_timestamps"] += 1
        counts["native_game_over_responses"] += data["state"] == "GAME_OVER"
        if action["id"] == 0:
            counts["initialisation_resets" if index == 0 else "current_level_resets"] += 1
        else:
            counts["native_policy_actions"] += 1
    if len(native_ids) != 1 or rows[0]["data"]["action_input"]["id"] != 0:
        raise ValueError("Native recording must be a single initialized game run")
    counts["game_wins"] = int(rows[-1]["data"]["state"] == "WIN")
    return {key: counts[key] for key in (
        "native_responses", "native_palette_frames", "unknown_native_timestamps",
        "native_game_over_responses", "initialisation_resets", "current_level_resets",
        "game_wins", "native_policy_actions",
    )}


def safe_identity(value: dict[str, Any]) -> dict[str, Any]:
    return {
        "bytes": int(value["bytes"]), "files": int(value["files"]),
        "content_sha256": checked_hash(value["content_sha256"]),
        "file_sha256": {safe_relative(k): checked_hash(v) for k, v in value["file_sha256"].items()},
    }


def safe_runtime(value: dict[str, Any]) -> dict[str, Any]:
    dependencies = value["dependencies"]
    if dependencies != {"arc-agi": "0.9.8", "arcengine": "0.9.3", "numpy": "2.5.3"}:
        raise ValueError("Unexpected runtime dependency pins")
    if value["python"] != "3.12.10" or value["backend"] != "docker":
        raise ValueError("Unexpected native runtime")
    image = value["image_id"]
    checked_hash(image.removeprefix("sha256:"))
    return {
        "backend": "docker", "python": "3.12.10", "dependencies": dependencies.copy(),
        "image_id": image, "identity_sha256": checked_hash(value["sha256"]),
        "package_identity": safe_identity(value["package_identity"]),
        "support_identity": safe_identity(value["support_identity"]) if value["support_identity"] else None,
        "worker_files": {safe_relative(k): checked_hash(v) for k, v in value["worker_files"].items()},
        "adapter_files": {safe_relative(k): checked_hash(v) for k, v in value["adapter_files"].items()},
    }


def source_note(source: str) -> dict[str, Any]:
    if source == "studio":
        return {"license": "MIT", "repository": "https://github.com/Felix561/arc3-synthetic-games"}
    return {
        "license": "Apache-2.0", "repository": NVIDIA_REPOSITORY, "commit": NVIDIA_COMMIT,
        "original_environments": f"{NVIDIA_REPOSITORY}/tree/{NVIDIA_COMMIT}/arc_agi_3",
    }


def sanitize_row(
    row: dict[str, Any], source: str, game: str, attempt: int,
    event_to_response: dict[int, int], native: list[dict[str, Any]],
) -> dict[str, Any]:
    if source not in SOURCES or not re.fullmatch(r"[a-z0-9]+", game):
        raise ValueError("Invalid source/game partition")
    metadata = row["source_metadata"]
    if metadata["source_collection"] != source or not metadata["source_informed"]:
        raise ValueError("Invalid agent source provenance")
    if (
        row["schema_version"] != 1 or row["provider"] != "arc3_meta_informed_agent"
        or row["split"] != "train" or row["actor_type"] != "online_agent"
        or row["color_space"] != "arc3_0_15"
    ):
        raise ValueError("Only source-informed palette agent rows may be exported")
    if not re.fullmatch(re.escape(game) + r"-[a-z0-9]+", row["game_id"]):
        raise ValueError("Unexpected canonical environment identifier")
    if not isinstance(row["level_id"], str) or not re.fullmatch(r"[1-8]", row["level_id"]):
        raise ValueError("Unexpected canonical level identifier")
    if row["seed"] != 0 or metadata["bundled_solutions_used"] is not False:
        raise ValueError("Unexpected collection seed or solution policy")
    agent = metadata["agent"]
    if agent["requested_model"] != "gpt-6.1-sol" or agent["requested_effort"] != "ultra":
        raise ValueError("Unexpected requested agent settings")
    public_id = f"{source}/{game}/level-{int(row['level_id']):02d}/attempt-{attempt:02d}"
    out = {key: copy.deepcopy(row[key]) for key in ROW_FIELDS if key != "source_metadata"}
    out.update({
        "dataset_version": VERSION, "episode_id": public_id, "trajectory_id": public_id,
        "task_id": f"{source}/{game}/level-{int(row['level_id']):02d}",
    })
    indices = [event_to_response[i] for i in metadata["response_event_indices"]]
    out["actions"] = [{key: copy.deepcopy(action[key]) for key in ACTION_FIELDS} for action in row["actions"]]
    out["source_metadata"] = {
        "source_collection": source, "source_informed": True, "actor_type": "online_agent",
        "native_game_id": row["game_id"], "content_sha256": checked_hash(metadata["content_sha256"]),
        "seed": 0, "policy_mode": "source_informed_direct_play",
        "agent": {
            "requested_model": "gpt-6.1-sol", "requested_effort": "ultra",
            "effective_model_metadata": "inherited_session_not_independently_measured",
        },
        "bundled_solutions_used_reported": False,
        "strategy_verification_scope": "actor_report_not_independently_measured_cognitive_fact",
        "runtime_identity": safe_runtime(metadata["runtime_identity"]),
        "source_files": safe_identity(metadata["source_files"]), "source_provenance": source_note(source),
        "native_recording_path": f"trajectories/{source}/recordings/{game}.recording.jsonl.gz",
        "native_response_indices": indices,
        "response_frame_indices": list(metadata["response_frame_indices"]),
        "native_level_index": metadata["native_level_index"],
        "source_run_end_reason": "complete_native_win",
        "all_animation_frames_preserved_in_native_recording": True,
        "completion_boundary_policy": "last_worker_measured_old_level_frame",
        "reward_policy": "not_recorded_no_reward_invented", "human_approval": False,
    }
    validate_segment(out, native)
    return out


def validate_segment(row: dict[str, Any], native: list[dict[str, Any]]) -> None:
    actions = row["actions"]
    if not actions or len(row["observations"]) != len(actions) + 1:
        raise ValueError("Canonical segments require N actions and N+1 observations")
    if row["scores"] is not None and len(row["scores"]) != len(actions) + 1:
        raise ValueError("Invalid score alignment")
    if row["scores"] is not None and any(
        type(score) not in (int, float) or not math.isfinite(score) for score in row["scores"]
    ):
        raise ValueError("Scores must remain finite numeric native level counts")
    if any(type(row[key]) is not bool for key in ("is_solved", "is_terminal", "is_truncated")):
        raise ValueError("Invalid canonical boundary flags")
    if row["rewards"] is not None or row["selection_masks"] is not None:
        raise ValueError("Unexpected invented reward or selection mask")
    if row["is_solved"]:
        if row["is_truncated"] or not row["is_terminal"] or row["terminal_reason"] not in ("level_solved", "win"):
            raise ValueError("Invalid solved-level flags")
    elif not row["is_truncated"] or row["is_terminal"] or row["terminal_reason"] != "native_level_reset":
        raise ValueError("Unsolved reset segment must remain nonterminal and truncated")
    metadata = row["source_metadata"]
    indices = metadata["native_response_indices"]
    frame_indices = metadata["response_frame_indices"]
    if len(indices) != len(actions) or len(frame_indices) != len(actions):
        raise ValueError("Missing native response/frame mapping")
    if indices != sorted(set(indices)):
        raise ValueError("Canonical actions are not in native response order")
    if indices[0] <= 0 or row["observations"][0] != native[indices[0] - 1]["data"]["frame"][-1]:
        raise ValueError("Canonical initial observation differs from native boundary")
    for index, action in enumerate(actions):
        identifier = action["provider_raw_action"]
        if identifier not in ACTION_NAMES or action["type"] != ACTION_NAMES[identifier]:
            raise ValueError("Canonical action type/ID mismatch")
        if not isinstance(action["valid_action_types"], list) or any(
            action_type not in ACTION_NAMES.values() for action_type in action["valid_action_types"]
        ) or type(action["settled_frame_known"]) is not bool:
            raise ValueError("Unexpected canonical action metadata")
        parameters = action["parameters"]
        if identifier == 6:
            if set(parameters) != {"row", "column"}:
                raise ValueError("Unexpected canonical click parameters")
            if any(type(value) is not int or not 0 <= value <= 63 for value in parameters.values()):
                raise ValueError("Invalid canonical click coordinate")
            expected = {"x": parameters["column"], "y": parameters["row"]}
        elif identifier == 5:
            if parameters != {"subtype": "ARC3_ACTION5"}:
                raise ValueError("Unexpected canonical special action")
            expected = {}
        else:
            if parameters:
                raise ValueError("Unexpected canonical non-click parameters")
            expected = {}
        data = native[indices[index]]["data"]
        if data["action_input"]["id"] != identifier or data["action_input"]["data"] != expected:
            raise ValueError("Canonical action differs from actual native request")
        if row["observations"][index + 1] != data["frame"][frame_indices[index]]:
            raise ValueError("Canonical selected observation differs from native frame")
        if action["outcome_target"] is not None:
            validate_frame(action["outcome_target"])
        validate_frame(row["observations"][index])
    validate_frame(row["observations"][-1])


def segment_stat(row: dict[str, Any]) -> dict[str, Any]:
    parts = row["trajectory_id"].split("/")
    actions = row["actions"]
    return {
        "source": parts[0], "game": parts[1], "game_id": row["game_id"],
        "level_id": int(row["level_id"]), "attempt": int(parts[3].removeprefix("attempt-")),
        "trajectory_id": row["trajectory_id"], "policy_actions": len(actions),
        "is_solved": row["is_solved"], "is_terminal": row["is_terminal"],
        "is_truncated": row["is_truncated"], "terminal_reason": row["terminal_reason"],
        "clicks": sum(a["type"] == "CLICK" for a in actions),
        "undo_actions": sum(a["type"] == "UNDO" for a in actions), "short": len(actions) < 6,
    }


def summarize(segments: list[dict[str, Any]], games: list[dict[str, Any]]) -> dict[str, Any]:
    lengths = [s["policy_actions"] for s in segments]
    first = [s for s in segments if s["attempt"] == 1]
    solved = sum(s["is_solved"] for s in segments)
    result = {
        "games": len(games), "levels": len({(s["source"], s["game"], s["level_id"]) for s in segments}),
        "segments": len(segments), "attempts": len(segments), "solved_segments": solved,
        "unsolved_segments": len(segments) - solved,
        "truncated_segments": sum(s["is_truncated"] for s in segments),
        "terminal_segments": sum(s["is_terminal"] for s in segments),
        "short_segments": sum(s["short"] for s in segments), "policy_actions": sum(lengths),
        "actions_per_segment": {
            "min": min(lengths), "median": statistics.median(lengths),
            "mean": round(statistics.mean(lengths), 6), "max": max(lengths),
        },
        "clicks": sum(s["clicks"] for s in segments), "undo_actions": sum(s["undo_actions"] for s in segments),
        "terminal_reasons": dict(sorted(Counter(s["terminal_reason"] for s in segments).items())),
        "success_rate": solved / len(segments),
        "first_attempt_solved_levels": sum(s["is_solved"] for s in first),
    }
    for key in (
        "native_responses", "native_palette_frames", "unknown_native_timestamps",
        "native_game_over_responses", "initialisation_resets", "current_level_resets", "game_wins",
    ):
        result[key] = sum(g["native_statistics"][key] for g in games)
    return result


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def exposure_notes(source: str) -> list[dict[str, Any]]:
    notes = {
        "studio": [
            {"game": "sg24", "planning_helpers_visible": ["search"]},
            {"game": "sg27", "planning_helpers_visible": ["explore", "path_to"]},
            {"game": "sg29", "planning_helpers_visible": ["explore", "path_to", "min_switches"]},
            {
                "game": "sg18", "additional_assistance": "Normal rules clarified by a separate read-only reviewer: "
                "reflection, occupancy, parity, click coordinates, and undo. No solution path or reviewer gameplay.",
            },
        ],
        "nvidia": [
            {"game": "ll4821", "planning_helpers_visible": [
                "_bfs_first_action", "_distance_to_goals", "_candidate_fire_cells", "_best_safe_move",
            ]},
            {"game": "ps1842", "design_guidance_visible": "Design metadata included switch-count guidance."},
        ],
    }
    return [note | {
        "source_collection": source, "bundled_solver_or_solution_path_use_reported": False,
        "assistance_verification_scope": "Actor reports; replay does not independently measure reasoning strategy.",
    } for note in notes[source]]


def verification_receipt(
    receipt: dict[str, Any], game: str, game_manifest: dict[str, Any], input_receipt_hash: str,
) -> dict[str, Any]:
    required_true = (
        "verified", "all_animation_frames_compared", "all_levels_completed", "complete_run", "native_win",
    )
    if any(receipt.get(key) is not True for key in required_true) or receipt.get("prefix_only") is not False:
        raise ValueError("Source receipt does not establish a complete final fresh replay")
    if receipt["content_sha256"] != game_manifest["content_sha256"]:
        raise ValueError("Replay receipt environment identity mismatch")
    return {
        "game": game, "native_game_id": game_manifest["native_game_id"],
        "environment_content_sha256": checked_hash(receipt["content_sha256"]),
        "source_receipt_sha256": input_receipt_hash,
        "reported_fresh_native_replay": {key: receipt[key] for key in required_true} | {
            "prefix_only": False, "responses_compared": int(receipt["responses_compared"]),
        },
        "public_projection": "Data-only provenance sanitization; gameplay was not rerun for publication.",
        "scope": "Original fresh replay checked the unchanged native requests and every animation frame. "
        "Public native recording bytes are preserved; canonical pixels/actions/boundaries are checked against them.",
        "human_playtest_or_approval": False,
    }


def checksum_file(directory: Path, prefix: str = "") -> None:
    paths = sorted(p for p in directory.rglob("*") if p.is_file() and p != directory / "SHA256SUMS.txt")
    lines = [f"{sha256(p)}  {prefix}{p.relative_to(directory).as_posix()}\n" for p in paths]
    (directory / "SHA256SUMS.txt").write_bytes("".join(lines).encode())


def expected_files(manifest: dict[str, Any]) -> set[str]:
    expected = {"manifest.json", "statistics.json", "per-game.csv", "per-segment.csv", "SHA256SUMS.txt"}
    for source_name in SOURCES:
        expected.update(f"{source_name}/{name}" for name in (
            "manifest.json", "trajectories.jsonl.gz", "verification.json", "SHA256SUMS.txt",
        ))
    for item in manifest["games"]:
        source_name = item["source_collection"]
        game = item["native_game_id"].split("-", 1)[0]
        if source_name not in SOURCES or not re.fullmatch(r"[a-z0-9]+", game):
            raise ValueError("Unexpected source/game identity")
        expected.update((f"{source_name}/recordings/{game}.recording.jsonl.gz", f"{source_name}/recordings/{game}.metadata.json"))
    return expected


def prepare(source: Path, destination: Path) -> dict[str, Any]:
    source, destination = source.resolve(), destination.resolve()
    if source == destination or source in destination.parents or destination in source.parents:
        raise ValueError("Input and public destination must be separate trees")
    manifest = verify_input(source)
    allowed = expected_files(manifest)
    if destination.exists():
        existing = {path.relative_to(destination).as_posix() for path in destination.rglob("*") if path.is_file()}
        if not existing.issubset(allowed):
            raise ValueError("Destination contains files outside the strict public-data allowlist")
    rows = read_jsonl(source / "trajectories/all.jsonl")
    grouped = defaultdict(list)
    for row in rows:
        grouped[(row["source_metadata"]["source_collection"], row["game_id"])].append(row)
    games_by_source = defaultdict(list)
    rows_by_source = defaultdict(list)
    segments = []
    public_checks = defaultdict(list)
    destination.mkdir(parents=True, exist_ok=True)
    for item in manifest["games"]:
        source_name, game_id = item["source_collection"], item["native_game_id"]
        if source_name not in SOURCES:
            raise ValueError("Unexpected source partition")
        game, version = game_id.split("-", 1)
        if not re.fullmatch(r"[a-z0-9]+", game) or not re.fullmatch(r"[a-z0-9]+", version):
            raise ValueError("Unexpected environment identifier")
        native_path = source / safe_relative(item["recording_path"])
        native = read_jsonl(native_path)
        native_stats = validate_native(native)
        if sha256(native_path) != item["recording_sha256"]:
            raise ValueError("Native recording manifest mismatch")
        if not native_stats["game_wins"]:
            raise ValueError("Expected a completed native game run")
        # The journals remain private. Only response ordinals are carried forward.
        audit_path = source / safe_relative(item["audit_path"])
        audit = read_jsonl(audit_path)
        responses = [event for event in audit if event["kind"] == "response"]
        event_to_response = {event["event_index"]: i for i, event in enumerate(responses)}
        if len(responses) != len(native):
            raise ValueError("Native recording/journal response count mismatch")
        public_rows = []
        attempts = Counter()
        for row in grouped[(source_name, game_id)]:
            attempts[row["level_id"]] += 1
            public_rows.append(sanitize_row(row, source_name, game, attempts[row["level_id"]], event_to_response, native))
        if sum(len(row["actions"]) for row in public_rows) != native_stats["native_policy_actions"]:
            raise ValueError("Canonical segments lose native policy actions")
        if len({row["level_id"] for row in public_rows if row["is_solved"]}) != item["levels"]:
            raise ValueError("Canonical solved-level coverage mismatch")
        partition = destination / source_name
        recording_path = partition / "recordings" / f"{game}.recording.jsonl.gz"
        recording_path.parent.mkdir(parents=True, exist_ok=True)
        recording_path.write_bytes(native_path.read_bytes())
        first = public_rows[0]["source_metadata"]
        public_environment = (
            f"environment_files/{game}/{version}" if source_name == "studio"
            else f"third_party/nvidia/environment_files/{game}/{version}"
        )
        game_info = {
            "game": game, "native_game_id": game_id, "version": version,
            "native_recording_game_id": native[0]["data"]["game_id"],
            "source_collection": source_name, "levels": item["levels"], "seed": 0,
            "environment_path": public_environment, "environment_content_sha256": item["content_sha256"],
            "environment_files_sha256": first["source_files"]["file_sha256"],
            "recording_path": f"trajectories/{source_name}/recordings/{game}.recording.jsonl.gz",
            "recording_sha256": sha256(recording_path), "native_statistics": native_stats,
            "source_provenance": source_note(source_name),
        }
        write_json(partition / "recordings" / f"{game}.metadata.json", {
            "schema_version": SCHEMA, "dataset_version": VERSION, "game": game, "native_game_id": game_id,
            "native_recording_game_id": native[0]["data"]["game_id"],
            "source_collection": source_name, "actor_type": "online_agent", "source_informed": True,
            "agent": first["agent"], "runtime_identity": first["runtime_identity"],
            "recording_sha256": game_info["recording_sha256"], "native_statistics": native_stats,
            "timestamp_policy": "null: original response times were not recorded",
            "format": "ARC Prize Recorder timestamp/data/native FrameData envelope",
            "format_reference": "https://github.com/arcprize/ARC-AGI-3-Agents/blob/main/agents/recorder.py",
            "timing_or_human_actor_compatibility_claimed": False, "all_animation_frames_preserved": True,
        })
        receipt_path = source / "verification" / f"{item['key']}.fresh-replay.json"
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        public_checks[source_name].append(verification_receipt(receipt, game, item, sha256(receipt_path)))
        games_by_source[source_name].append(game_info)
        rows_by_source[source_name].extend(public_rows)
        segments.extend(segment_stat(row) for row in public_rows)
        del audit, responses, native
    all_games = [game for source_name in SOURCES for game in games_by_source[source_name]]
    totals = summarize(segments, all_games)
    if any(totals.get(key) != value for key, value in EXPECTED_TOTALS.items()):
        raise ValueError("Public projection totals differ from the frozen collection")
    input_identity = {
        "dataset_version": manifest["dataset_version"],
        "manifest_sha256": sha256(source / "manifest.json"),
        "checksums_sha256": sha256(source / "SHA256SUMS.txt"),
        "projection": "Immutable verified input; no native environment modifications or new gameplay.",
    }
    by_source = {}
    source_index = {}
    for source_name in SOURCES:
        partition = destination / source_name
        canonical = partition / "trajectories.jsonl.gz"
        write_jsonl_gzip(canonical, rows_by_source[source_name])
        source_segments = [segment for segment in segments if segment["source"] == source_name]
        by_source[source_name] = summarize(source_segments, games_by_source[source_name])
        write_json(partition / "verification.json", {
            "schema_version": "arc3-public-replay-verification/1", "dataset_version": VERSION,
            "source_collection": source_name, "input_identity": input_identity,
            "canonical_sha256": sha256(canonical), "games": public_checks[source_name],
            "native_recordings_byte_preserved": True, "canonical_pixels_actions_boundaries_checked": True,
            "publication_preparation_performed_native_replays": False,
        })
        license_name = "MIT" if source_name == "studio" else "Apache-2.0"
        license_path = "LICENSE" if source_name == "studio" else "third_party/nvidia/LICENSE"
        part_manifest = {
            "schema_version": SCHEMA, "dataset_version": VERSION, "source_collection": source_name,
            "license": license_name, "license_path": license_path,
            "canonical_path": f"trajectories/{source_name}/trajectories.jsonl.gz",
            "canonical_sha256": sha256(canonical), "statistics": by_source[source_name],
            "input_identity": input_identity, "agent": {
                "requested_model": "gpt-6.1-sol", "requested_effort": "ultra",
                "effective_model_metadata": "inherited_session_not_independently_measured",
            },
            "actor_type": "online_agent", "source_informed": True, "human_trajectories_included": False,
            "assistance_and_context_notes": exposure_notes(source_name),
            "interpretation": "Privileged source-informed direct-agent gameplay. Actors reported no bundled "
            "solver/search/solution-path use; replay proves recorded execution, not their mental process.",
            "games": games_by_source[source_name],
        }
        if source_name == "nvidia":
            part_manifest["runtime_support_path"] = "third_party/nvidia/runtime_support"
            part_manifest["runtime_support_content_sha256"] = rows_by_source[source_name][0][
                "source_metadata"
            ]["runtime_identity"]["support_identity"]["content_sha256"]
        write_json(partition / "manifest.json", part_manifest)
        checksum_file(partition)
        source_index[source_name] = {
            "manifest_path": f"trajectories/{source_name}/manifest.json",
            "canonical_path": part_manifest["canonical_path"], "license": license_name,
            "license_path": license_path, "game_count": by_source[source_name]["games"],
            "level_count": by_source[source_name]["levels"], "segment_count": by_source[source_name]["segments"],
        }
    write_json(destination / "statistics.json", {
        "schema_version": "arc3-agent-trajectory-statistics/1", "dataset_version": VERSION,
        "totals": totals, "by_source": by_source, "metric_definitions": DEFINITIONS,
        "interpretation": "Descriptive statistics of one source-informed agent run per game, with retained retries. "
        "Not blind-agent evaluation, human performance, an optimality score, or an independent benchmark.",
    })
    write_csv(destination / "per-segment.csv", segments)
    game_stats = []
    for game in all_games:
        gs = summarize([s for s in segments if s["source"] == game["source_collection"] and s["game"] == game["game"]], [game])
        flat = {"source": game["source_collection"], "game": game["game"], "game_id": game["native_game_id"]}
        for key, value in gs.items():
            if key == "actions_per_segment":
                flat.update({f"actions_per_segment_{k}": v for k, v in value.items()})
            elif key == "terminal_reasons":
                flat["level_solved_segments"] = value.get("level_solved", 0)
                flat["win_segments"] = value.get("win", 0)
                flat["native_level_reset_segments"] = value.get("native_level_reset", 0)
            else:
                flat[key] = value
        game_stats.append(flat)
    write_csv(destination / "per-game.csv", game_stats)
    prepared_files = {path.relative_to(destination).as_posix() for path in destination.rglob("*") if path.is_file()}
    if not prepared_files.issubset(allowed):
        raise ValueError("Unexpected file appeared in the public data tree")
    file_map = {
        f"trajectories/{path.relative_to(destination).as_posix()}": sha256(path)
        for path in sorted(destination.rglob("*")) if path.is_file()
        and path not in (destination / "manifest.json", destination / "SHA256SUMS.txt")
    }
    root_manifest = {
        "schema_version": SCHEMA, "publication_id": VERSION, "dataset_version": VERSION,
        "actor_type": "online_agent", "source_informed": True, "human_trajectories_included": False,
        "sources": source_index, "statistics_path": "trajectories/statistics.json", "totals": totals,
        "input_identity": input_identity, "files_sha256": file_map,
        "canonical_format": "TrajectoryExport schema version 1, gzip JSONL, N+1 palette observations for N actions",
        "source_separation": "Two disjoint source partitions; load one or both once, with no union duplicate.",
        "privacy_projection": "Allowlisted public provenance and stable source/game/level/attempt IDs. "
        "No actor/task/run/request IDs, journals, decisions, local paths, credentials, or human trajectories.",
    }
    write_json(destination / "manifest.json", root_manifest)
    checksum_file(destination)
    return root_manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path, help="Private verified export (not embedded in outputs)")
    parser.add_argument("--destination", type=Path, default=Path(__file__).resolve().parents[1] / "trajectories")
    args = parser.parse_args()
    result = prepare(args.source, args.destination)
    print(json.dumps({"dataset_version": VERSION, "totals": result["totals"]}, indent=2))


if __name__ == "__main__":
    main()
