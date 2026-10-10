"""Check the public analysis boundary and denominators without loading games."""

import csv
import importlib.util
import json
import shutil
import statistics
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("analysis_builder", ROOT / "tools/build_analysis_report.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def test_report_has_only_declared_summary_columns_and_synthetic_progress():
    files = builder.report_files()
    assert set(files) == builder.REPORT_NAMES | {"manifest.json"}
    data = json.loads(files["summary.json"])
    assert set(data) == {"schema", "as_of", "dataset_release", "source_commit", "reference_urls", "queries"}
    assert data["schema"] == "arc3-synthetic-analysis/1"
    assert set(data["queries"]) == set(builder.FIELDS)
    for name, rows in data["queries"].items():
        assert all(set(row) == set(builder.FIELDS[name].split()) for row in rows), name
        reader = csv.DictReader(files[f"tables/{name}.csv"].decode("utf-8").splitlines())
        assert reader.fieldnames == builder.FIELDS[name].split()
        assert list(reader) == [{key: str(value) for key, value in row.items()} for row in rows]
    q = data["queries"]
    synthetic_ids = {row["game"] for row in q["game_reviews"]}
    assert len(synthetic_ids) == 75
    assert all(row["game"] in synthetic_ids and row["collection"] in builder.SYNTHETIC
               for row in q["progress"])


def test_report_coverage_and_completed_length_denominators_reconcile():
    q = json.loads(builder.report_files()["summary.json"])["queries"]
    coverage = {row["collection"]: row for row in q["coverage"]}
    assert sum(coverage[name]["nativeLevels"] for name in builder.SYNTHETIC) == 550
    assert sum(coverage[name]["segments"] for name in builder.SYNTHETIC) == 555
    assert sum(coverage[name]["actions"] for name in builder.SYNTHETIC) == 7751
    for name in builder.SYNTHETIC:
        completed = [row["actions"] for row in q["synthetic_heat"] if row["collection"] == name]
        assert len(completed) == coverage[name]["nativeLevels"]
        assert statistics.median(completed) == coverage[name]["median"]
    assert sum(row["actions"] for row in q["synthetic_heat"] if row["collection"] == "NVIDIA") == 3611
    assert len(q["official_games"]) == 25
    assert len(q["official_levels"]) == 183
    assert sum(row["plays"] for row in q["official_games"]) == 340
    assert sum(row["solves"] for row in q["official_games"]) == 144
    assert sum(row["actions"] for row in q["official_games"]) == 178422
    assert len(q["recipes"]) == 20


def test_report_inventory_rejects_extra_files_corruption_and_path_traversal(tmp_path):
    report = tmp_path / "report"
    shutil.copytree(builder.REPORT, report)
    extra = report / "private-notes.txt"
    extra.write_text("excluded", encoding="utf-8")
    with pytest.raises(ValueError, match="Unexpected analysis assets"):
        builder.report_files(report)
    extra.unlink()
    index = report / "index.html"
    original = index.read_bytes()
    index.write_bytes(original + b"corrupt")
    with pytest.raises(ValueError, match="checksum mismatch"):
        builder.report_files(report)
    index.write_bytes(original)
    manifest_path = report / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["files_sha256"]["../private.txt"] = "0" * 64
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(ValueError, match="Unexpected analysis asset inventory"):
        builder.report_files(report)


def test_rebuild_refuses_unreviewed_summary_fields_and_extra_assets(tmp_path, monkeypatch):
    report = tmp_path / "report"
    shutil.copytree(builder.REPORT, report)
    monkeypatch.setattr(builder, "REPORT", report)
    summary_path = report / "summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    summary["queries"]["progress"][0]["participant"] = "unreviewed"
    summary_path.write_text(json.dumps(summary), encoding="utf-8")
    with pytest.raises(ValueError, match="Unexpected public fields: progress"):
        builder.build()
    (report / "figures/private.svg").write_text("excluded", encoding="utf-8")
    with pytest.raises(ValueError, match="Unexpected analysis assets"):
        builder.build()
