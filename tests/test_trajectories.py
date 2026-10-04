"""Data-only trajectory checks. No test imports or executes generated games."""

from __future__ import annotations

import copy
import gzip
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("public_trajectory_preparation", ROOT / "tools/prepare_trajectories.py")
assert spec and spec.loader
tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tool)


def frame(color):
    return [[color] * 64 for _ in range(64)]


def identity():
    return {"bytes": 1, "files": 1, "content_sha256": "a" * 64, "file_sha256": {"sg01.py": "b" * 64}}


def metadata(event):
    return {
        "source_collection": "studio", "source_informed": True, "bundled_solutions_used": False,
        "content_sha256": "a" * 64, "source_files": identity(), "native_level_index": 0,
        "response_event_indices": [event], "response_frame_indices": [0],
        "agent": {
            "requested_model": "gpt-6.1-sol", "requested_effort": "ultra",
            "task": "/root/private_agent", "credential": "secret-agent-token",
        },
        "runtime_identity": {
            "backend": "docker", "python": "3.12.10", "sha256": "c" * 64,
            "dependencies": {"arc-agi": "0.9.8", "arcengine": "0.9.3", "numpy": "2.5.3"},
            "image_id": "sha256:" + "d" * 64, "package_identity": identity(), "support_identity": None,
            "worker_files": {"worker.py": "e" * 64}, "adapter_files": {"adapter.py": "f" * 64},
            "private_config": "C:/Users/private-user/private-file",
        },
        "run_id": "agent-private-run", "request_ids": ["private-request"],
        "raw_journal": "audit/private.jsonl.gz", "notes": "secret-owner-conversation",
    }


def native_record(color, action, *, full_reset=False, state="NOT_FINISHED"):
    return {
        "timestamp": None, "data": {
            "action_input": {"id": action, "data": {"x": 2, "y": 3} if action == 6 else {}, "reasoning": None},
            "available_actions": list(range(1, 8)), "frame": [frame(color)], "full_reset": full_reset,
            "game_id": "sg01-v1", "guid": None, "levels_completed": int(state == "WIN"),
            "state": state, "win_levels": 1,
        },
    }


def raw_row(start, end, action, event, solved):
    return {
        "schema_version": 1, "provider": "arc3_meta_informed_agent", "dataset_version": "private-export",
        "split": "train", "game_id": "sg01-abc123", "level_id": "1", "episode_id": "private-run-episode",
        "trajectory_id": "private-run-trajectory", "task_id": "/root/private-task", "actor_type": "online_agent",
        "color_space": "arc3_0_15", "observations": [frame(start), frame(end)],
        "actions": [{
            "type": tool.ACTION_NAMES[action], "parameters": {"row": 3, "column": 2} if action == 6 else
            {"subtype": "ARC3_ACTION5"} if action == 5 else {}, "provider_raw_action": action,
            "valid_action_types": list(tool.ACTION_NAMES.values()), "settled_frame_known": True,
            "outcome_target": None, "private_debug": "secret-action-note",
        }],
        "selection_masks": None, "rewards": None, "scores": [0.0, float(solved)], "is_solved": solved,
        "is_terminal": solved, "is_truncated": not solved,
        "terminal_reason": "level_solved" if solved else "native_level_reset", "seed": 0,
        "source_metadata": metadata(event), "private_owner": "secret-owner-email",
    }


@pytest.fixture
def reset_attempts():
    native = [
        native_record(0, 0, full_reset=True), native_record(1, 6),
        native_record(2, 0), native_record(3, 5, state="WIN"),
    ]
    events = {1: 0, 3: 1, 5: 2, 7: 3}
    failed = tool.sanitize_row(raw_row(0, 1, 6, 3, False), "studio", "sg01", 1, events, native)
    solved = tool.sanitize_row(raw_row(2, 3, 5, 7, True), "studio", "sg01", 2, events, native)
    return native, [failed, solved]


def test_public_projection_keeps_attempts_without_private_provenance(reset_attempts):
    native, rows = reset_attempts
    assert rows[0]["trajectory_id"] == "studio/sg01/level-01/attempt-01"
    assert rows[1]["trajectory_id"] == "studio/sg01/level-01/attempt-02"
    assert rows[0]["is_truncated"] and not rows[0]["is_terminal"] and not rows[0]["is_solved"]
    assert rows[1]["observations"][0] == native[2]["data"]["frame"][-1]
    assert rows[0]["source_metadata"]["native_response_indices"] == [1]
    assert rows[1]["source_metadata"]["native_response_indices"] == [3]
    public = json.dumps(rows)
    for private in ("private-", "secret-", "/root/", "C:/Users/", "raw_journal", "request_ids", "run_id"):
        assert private not in public
    assert "inherited_session_not_independently_measured" in public


def test_native_boundary_corruption_is_detected(reset_attempts):
    native, rows = reset_attempts
    corrupted = copy.deepcopy(rows[1])
    corrupted["observations"][0] = frame(1)  # A failed attempt's ending must not replace the reset observation.
    with pytest.raises(ValueError, match="initial observation"):
        tool.validate_segment(corrupted, native)
    corrupted = copy.deepcopy(rows[1])
    corrupted["observations"][1][0][0] = 9
    with pytest.raises(ValueError, match="selected observation"):
        tool.validate_segment(corrupted, native)


def test_click_swap_is_not_silently_accepted(reset_attempts):
    native, rows = reset_attempts
    corrupted = copy.deepcopy(rows[0])
    corrupted["actions"][0]["parameters"] = {"row": 2, "column": 3}
    with pytest.raises(ValueError, match="actual native request"):
        tool.validate_segment(corrupted, native)


@pytest.mark.parametrize("field,value", [("guid", "opaque-session-id"), ("state", "invented")])
def test_native_private_or_invalid_state_rejected(reset_attempts, field, value):
    native, _ = reset_attempts
    corrupted = copy.deepcopy(native)
    corrupted[0]["data"][field] = value
    with pytest.raises(ValueError):
        tool.validate_native(corrupted)


def test_native_reasoning_and_nonpalette_data_rejected(reset_attempts):
    native, _ = reset_attempts
    corrupted = copy.deepcopy(native)
    corrupted[1]["data"]["action_input"]["reasoning"] = "private model text"
    with pytest.raises(ValueError, match="reasoning"):
        tool.validate_native(corrupted)
    corrupted = copy.deepcopy(native)
    corrupted[1]["data"]["frame"][0][0][0] = 16
    with pytest.raises(ValueError, match="non-palette"):
        tool.validate_native(corrupted)


def test_statistics_distinguish_failed_attempt_from_native_game_over(reset_attempts):
    native, rows = reset_attempts
    games = [{"native_statistics": tool.validate_native(native)}]
    summary = tool.summarize([tool.segment_stat(row) for row in rows], games)
    assert summary["segments"] == 2 and summary["levels"] == 1
    assert summary["solved_segments"] == summary["unsolved_segments"] == 1
    assert summary["policy_actions"] == 2 and summary["current_level_resets"] == 1
    assert summary["initialisation_resets"] == 1 and summary["native_responses"] == 4
    assert summary["native_game_over_responses"] == 0
    assert summary["first_attempt_solved_levels"] == 0
    assert summary["clicks"] == 1 and summary["short_segments"] == 2
    assert summary["actions_per_segment"]["median"] == 1


def test_gzip_is_reproducible_and_lossless(tmp_path, reset_attempts):
    _, rows = reset_attempts
    first, second = tmp_path / "first.jsonl.gz", tmp_path / "second.jsonl.gz"
    tool.write_jsonl_gzip(first, rows)
    tool.write_jsonl_gzip(second, rows)
    assert first.read_bytes() == second.read_bytes()
    with gzip.open(first, "rt") as handle:
        assert [json.loads(line) for line in handle] == rows


@pytest.mark.parametrize("path", ["../secret", "/absolute/file", "C:/Users/private", "folder\\private"])
def test_unsafe_public_paths_rejected(path):
    with pytest.raises(ValueError, match="relative path"):
        tool.safe_relative(path)


def test_prepared_partitions_have_no_duplicate_union_or_missing_file_hashes():
    root = ROOT / "trajectories"
    if not (root / "manifest.json").exists():
        pytest.skip("Public data has not been prepared")
    manifest = json.loads((root / "manifest.json").read_text())
    assert set(manifest["sources"]) == {"studio", "nvidia"}
    assert not (root / "all.jsonl").exists()
    actual = {
        "trajectories/" + path.relative_to(root).as_posix()
        for path in root.rglob("*") if path.is_file() and path not in (root / "manifest.json", root / "SHA256SUMS.txt")
    }
    assert actual == set(manifest["files_sha256"])
    assert all(tool.sha256(ROOT / path) == digest for path, digest in manifest["files_sha256"].items())
    stats = json.loads((root / "statistics.json").read_text())
    assert all(stats["totals"][key] == value for key, value in tool.EXPECTED_TOTALS.items())
    assert stats["by_source"]["studio"]["unsolved_segments"] == 0
    assert stats["by_source"]["nvidia"]["unsolved_segments"] == 5
