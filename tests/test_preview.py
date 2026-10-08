"""Static packaging checks; no native game code is imported or executed here."""

import hashlib
import importlib.util
import json
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("preview_builder", ROOT / "tools/build_preview.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def test_preview_contains_exact_native_bytes_and_only_public_assets(tmp_path, monkeypatch):
    dependency = tmp_path / "dependency.whl"
    dependency.write_bytes(b"stub for data-only packaging test")
    monkeypatch.setattr(builder, "ENGINE_SHA256", hashlib.sha256(dependency.read_bytes()).hexdigest())
    first, second = tmp_path / "first", tmp_path / "second"
    manifest = builder.build(first, dependency)
    builder.build(second, dependency)
    assert (first / "browser/runtime.zip").read_bytes() == (second / "browser/runtime.zip").read_bytes()
    catalog = json.loads((first / "catalog.json").read_text(encoding="utf-8"))
    with zipfile.ZipFile(first / "browser/runtime.zip") as archive:
        native = [name for name in archive.namelist() if "/environment_files/" in name]
        assert len(native) == 100
        for entry in catalog["games"]:
            for relative, digest in entry["files_sha256"].items():
                name = f"arc3_synthetic_games/data/{entry['environment_path']}/{relative}"
                assert hashlib.sha256(archive.read(name)).hexdigest() == digest
        assert "browser_bridge.py" in archive.namelist()
        assert "arc3_synthetic_games/data/THIRD_PARTY_NOTICES.md" in archive.namelist()
    expected_media = {"media/overview.png"}
    for entry in catalog["games"]:
        expected_media.add(entry["preview"])
        if entry.get("demo"):
            expected_media.add(entry["demo"])
    assert {p.relative_to(first).as_posix() for p in (first / "media").rglob("*") if p.is_file()} == expected_media
    for entry in manifest["files"]:
        assert hashlib.sha256((first / "browser" / entry["path"]).read_bytes()).hexdigest() == entry["sha256"]
    html = (first / "index.html").read_text(encoding="utf-8")
    assert html.index("browser/client.js") < html.index("static/app.js")
    assert 'src="/static/' not in html


def test_preview_rejects_corrupt_dependency_and_existing_output(tmp_path):
    dependency = tmp_path / "bad.whl"
    dependency.write_bytes(b"not the pinned dependency")
    with pytest.raises(ValueError, match="wheel checksum"):
        builder.build(tmp_path / "site", dependency)
    with pytest.raises(ValueError, match="must be empty"):
        builder.build(tmp_path / "site", dependency)
