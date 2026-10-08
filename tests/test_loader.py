"""Portable loading checks use small data fixtures and never import game code."""

import gzip
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("public_dataset_loader", ROOT / "tools/load_dataset.py")
loader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(loader)


def fixture(root, sources=("studio", "studio_v2", "nvidia")):
    path = root / "trajectories"
    path.mkdir()
    (path / "manifest.json").write_text(json.dumps({"sources": {source: {} for source in sources}}))
    for source in sources:
        folder = path / source
        folder.mkdir()
        with gzip.open(folder / "trajectories.jsonl.gz", "wt", encoding="utf-8") as out:
            out.write(json.dumps({"source": source, "is_solved": True, "actions": [1]}) + "\n")


def test_loader_reads_all_partitions_once_and_can_select_v2(tmp_path):
    fixture(tmp_path)
    assert [row["source"] for row in loader.iter_trajectories(tmp_path)] == list(loader.SOURCES)
    rows = list(loader.iter_trajectories(tmp_path, ("studio_v2",)))
    assert len(rows) == 1 and rows[0]["source"] == "studio_v2"
    with pytest.raises(ValueError, match="only once"):
        list(loader.iter_trajectories(tmp_path, ("studio_v2", "studio_v2")))


def test_loader_preserves_earlier_two_partition_datasets(tmp_path):
    fixture(tmp_path, ("studio", "nvidia"))
    assert [row["source"] for row in loader.iter_trajectories(tmp_path)] == ["studio", "nvidia"]
    with pytest.raises(ValueError, match="Unknown source"):
        list(loader.iter_trajectories(tmp_path, ("studio_v2",)))


def test_loader_rejects_unknown_partition(tmp_path):
    fixture(tmp_path, ("studio", "studio_v2", "nvidia", "unknown"))
    with pytest.raises(ValueError, match="Unknown or missing"):
        list(loader.iter_trajectories(tmp_path))
