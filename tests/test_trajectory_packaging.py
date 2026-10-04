"""Data-only publication boundaries; native game code is never imported."""

import hashlib
import importlib.util
import json
import sys
import tomllib
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("trajectory_builder", ROOT / "tools/build_trajectory_release.py")
builder = importlib.util.module_from_spec(spec)
sys.path.insert(0, str(ROOT / "tools"))
try:
    spec.loader.exec_module(builder)
finally:
    sys.path.pop(0)


def json_bytes(value):
    return (json.dumps(value, sort_keys=True, indent=2) + "\n").encode()


def digest(content):
    return hashlib.sha256(content).hexdigest()


def fixture(root):
    files = {}
    sources = {}
    for source in ("studio", "nvidia"):
        prefix = f"trajectories/{source}/"
        canonical = prefix + "trajectories.jsonl.gz"
        files[canonical] = b"test compressed data bytes; not imported or executed"
        files[prefix + "verification.json"] = json_bytes({"source_collection": source})
        game = "sg01" if source == "studio" else "nv01"
        recording = prefix + "recordings/" + game + ".recording.jsonl.gz"
        files[recording] = b"native recording test bytes"
        files[prefix + "recordings/" + game + ".metadata.json"] = json_bytes(
            {"source_collection": source, "actor_type": "online_agent", "source_informed": True})
        environment_prefix = "environment_files/" if source == "studio" else "third_party/nvidia/environment_files/"
        partition = {"schema_version": builder.SCHEMA, "source_collection": source,
                     "canonical_path": canonical, "canonical_sha256": digest(files[canonical]),
                     "license_path": "LICENSE" if source == "studio" else "third_party/nvidia/LICENSE",
                     "license": "MIT" if source == "studio" else "Apache-2.0",
                     "actor_type": "online_agent", "source_informed": True, "human_trajectories_included": False,
                     "games": [{"game": game, "source_collection": source,
                                "environment_path": environment_prefix + game + "/fixture",
                                "recording_path": recording, "recording_sha256": digest(files[recording])}]}
        files[prefix + "manifest.json"] = json_bytes(partition)
        files[prefix + "SHA256SUMS.txt"] = "".join(
            f"{digest(content)}  {name.removeprefix(prefix)}\n" for name, content in sorted(files.items())
            if name.startswith(prefix)).encode()
        sources[source] = {"manifest_path": prefix + "manifest.json", "canonical_path": canonical,
                           "license": "MIT" if source == "studio" else "Apache-2.0",
                           "game_count": 1,
                           "license_path": "LICENSE" if source == "studio" else "third_party/nvidia/LICENSE"}
    files["trajectories/statistics.json"] = json_bytes({"game_count": 2})
    files["trajectories/per-game.csv"] = b"source,game\nstudio,studio01\nnvidia,nvidia01\n"
    files["trajectories/per-segment.csv"] = b"source,game,level,attempt\n"
    manifest = {"schema_version": builder.SCHEMA, "dataset_version": "fixture-v1", "sources": sources,
                "actor_type": "online_agent", "source_informed": True, "human_trajectories_included": False,
                "totals": {"game_count": 2},
                "files_sha256": {name: digest(content) for name, content in files.items()}}
    files["trajectories/manifest.json"] = json_bytes(manifest)
    files["trajectories/SHA256SUMS.txt"] = "".join(
        f"{digest(content)}  {name.removeprefix('trajectories/')}\n"
        for name, content in sorted(files.items())).encode()
    for name in builder.DOCS | builder.LICENSES:
        files[name] = f"Public documentation or license: {name}\n".encode()
    for name, content in files.items():
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
    return files


def test_trajectory_zip_is_deterministic_self_checking_and_separate(tmp_path):
    root = tmp_path / "source"
    fixture(root)
    first, second = tmp_path / "first.zip", tmp_path / "second.zip"
    first_result = builder.build(first, root)
    second_result = builder.build(second, root)
    assert first.read_bytes() == second.read_bytes()
    assert first_result["sha256"] == second_result["sha256"]
    with zipfile.ZipFile(first) as archive:
        assert archive.testzip() is None
        assert "trajectories/studio/trajectories.jsonl.gz" in archive.namelist()
        assert "trajectories/nvidia/trajectories.jsonl.gz" in archive.namelist()
        assert builder.LICENSES <= set(archive.namelist())
        assert not any(name.endswith(".py") or name.startswith("environment_files/")
                       for name in archive.namelist())
        sums = builder.parse_sums(archive.read("SHA256SUMS.txt"))
        assert set(sums) == set(archive.namelist()) - {"SHA256SUMS.txt"}
        assert all(digest(archive.read(name)) == expected for name, expected in sums.items())
        assert all(info.date_time == (1980, 1, 1, 0, 0, 0) for info in archive.infolist())
        assert b"not human players" in archive.read("README.md")
    with pytest.raises(ValueError, match="overwrite"):
        builder.build(first, root)


def test_trajectory_zip_rejects_corruption_and_private_extras(tmp_path):
    root = tmp_path / "source"
    fixture(root)
    recording = root / "trajectories/studio/trajectories.jsonl.gz"
    recording.write_bytes(b"tampered")
    with pytest.raises(ValueError, match="checksum mismatch"):
        builder.build(tmp_path / "corrupt.zip", root)
    fixture(root)
    (root / "trajectories/server.json").write_text('{"token": "private"}')
    with pytest.raises(ValueError, match="Unexpected or unlisted"):
        builder.build(tmp_path / "private.zip", root)


@pytest.mark.parametrize("change,message", [
    ("human", "explicitly label"), ("license", "source-specific license"),
    ("cross_source", "within their source collection"),
])
def test_public_data_requires_honest_actor_labels_and_source_license_split(tmp_path, change, message):
    root = tmp_path / "source"
    files = fixture(root)
    name = "trajectories/manifest.json"
    manifest = json.loads(files[name])
    if change == "human":
        manifest["actor_type"] = "human"
    elif change == "license":
        manifest["sources"]["nvidia"]["license"] = "MIT"
    else:
        manifest["sources"]["nvidia"]["canonical_path"] = "trajectories/studio/trajectories.jsonl.gz"
    files[name] = json_bytes(manifest)
    (root / name).write_bytes(files[name])
    (root / "trajectories/SHA256SUMS.txt").write_bytes("".join(
        f"{digest(content)}  {path.removeprefix('trajectories/')}\n"
        for path, content in sorted(files.items())
        if path.startswith("trajectories/") and path != "trajectories/SHA256SUMS.txt").encode())
    with pytest.raises(ValueError, match=message):
        builder.build(tmp_path / "invalid.zip", root)


@pytest.mark.parametrize("name", ["../secret", "/private", "C:/private", "trajectories\\studio\\x",
                                 "trajectories//studio/x", "trajectories/./studio/x"])
def test_trajectory_manifest_rejects_unsafe_paths(name):
    with pytest.raises(ValueError, match="Unsafe"):
        builder.checked_name(name)


def test_wheel_and_sdist_keep_nvidia_and_agent_bulk_separate():
    config = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    wheel = config["tool"]["hatch"]["build"]["targets"]["wheel"]
    assert set(wheel["force-include"]) == {
        "environment_files", "catalog.json", "media/overview.png", "media/previews", "media/demos",
        "THIRD_PARTY_NOTICES.md",
    }
    exclusions = set(config["tool"]["hatch"]["build"]["targets"]["sdist"]["exclude"])
    assert {"/trajectories", "/third_party", "/media/agent-demos"} <= exclusions


def test_data_only_document_links_preserve_data_and_point_to_omitted_source():
    document = (b"[Data](trajectories/studio/manifest.json) [Native](environment_files/sg01/game.py) "
                b"![Agent GIF](media/agent-demos/nvidia.gif) [Details](TRAJECTORIES.md#format)")
    result = builder.scope_document_links(document, {"trajectories/studio/manifest.json", "TRAJECTORIES.md"})
    assert b"[Data](trajectories/studio/manifest.json)" in result
    assert b"blob/main/environment_files/sg01/game.py" in result
    assert b"raw.githubusercontent.com/Felix561/arc3-synthetic-games/main/media/agent-demos/nvidia.gif" in result
    assert b"[Details](TRAJECTORIES.md#format)" in result


def test_official_release_requires_clean_committed_source(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location("official_release", ROOT / "tools/build_release.py")
    official = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(ROOT / "tools"))
    try:
        spec.loader.exec_module(official)
    finally:
        sys.path.pop(0)
    monkeypatch.setattr(official, "git", lambda *args: b" M README.md\n")
    with pytest.raises(ValueError, match="Commit the reviewed source"):
        official.build(tmp_path / "release", tmp_path / "preview", tmp_path / "packages")
    assert not (tmp_path / "release").exists()
    readme = official.native_archive_readme("1.0.3")
    assert b"no player application or AI-agent trajectory" in readme
    assert b"NVIDIA environments" in readme
    notices = official.native_archive_notices()
    assert b"Copyright (c) 2026 ARC Prize Foundation" in notices
    assert b"The 16-color palette" in notices
    assert b"THE SOFTWARE IS PROVIDED" in notices
    assert b"## NVIDIA" not in notices
    citation = official.native_archive_citation("1.0.3")
    assert b"license: MIT" in citation and b"Apache-2.0" not in citation
