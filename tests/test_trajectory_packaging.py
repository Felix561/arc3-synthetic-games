"""Data-only publication boundaries; native game code is never imported."""

import gzip
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


def canonical_bytes(agent):
    line = json.dumps({"source_metadata": {"agent": agent}}, sort_keys=True, separators=(",", ":")) + "\n"
    return gzip.compress(line.encode(), mtime=0)


def fixture(root, *, include_v2=False, v2_change=None):
    files = {}
    sources = {}
    for source in (("studio", "studio_v2", "nvidia") if include_v2 else ("studio", "nvidia")):
        prefix = f"trajectories/{source}/"
        canonical = prefix + "trajectories.jsonl.gz"
        files[canonical] = canonical_bytes({
            "requested_model": "gpt-6.1-sol", "requested_effort": "xhigh",
            "effective_model_metadata": "unmeasured"})
        files[prefix + "verification.json"] = json_bytes({"source_collection": source})
        game = {"studio": "sg01", "studio_v2": "v201", "nvidia": "nv01"}[source]
        recordings = []
        for level in (range(1, 8) if source == "studio_v2" else (None,)):
            stem = prefix + "recordings/" + game + (f"-level-{level:02}" if level else "")
            recording, metadata = stem + ".recording.jsonl.gz", stem + ".metadata.json"
            files[recording] = b"native recording test bytes"
            sidecar = {"source_collection": source, "actor_type": "online_agent", "source_informed": True}
            if source == "studio_v2":
                sidecar.update({"level_id": str(level), "recording_scope": "successful_level_excerpt",
                                "human_approval": False, "standalone_full_run": False})
                if v2_change and level == 1:
                    sidecar.update(v2_change)
            files[metadata] = json_bytes(sidecar)
            record = {"recording_path": recording, "recording_sha256": digest(files[recording])}
            if level:
                record.update({"level_id": str(level), "metadata_path": metadata,
                               "metadata_sha256": digest(files[metadata])})
            recordings.append(record)
        environment_prefix = "third_party/nvidia/environment_files/" if source == "nvidia" else "environment_files/"
        game_info = {"game": game, "source_collection": source,
                     "environment_path": environment_prefix + game + "/fixture"}
        if source == "studio_v2":
            game_info.update({"levels": 7, "recording_scope": "successful_level_excerpt", "recordings": recordings})
        else:
            game_info.update(recordings[0])
        partition = {"schema_version": builder.SCHEMA, "source_collection": source,
                     "canonical_path": canonical, "canonical_sha256": digest(files[canonical]),
                     "license_path": "third_party/nvidia/LICENSE" if source == "nvidia" else "LICENSE",
                     "license": "Apache-2.0" if source == "nvidia" else "MIT",
                     "actor_type": "online_agent", "source_informed": True, "human_trajectories_included": False,
                     "games": [game_info]}
        files[prefix + "manifest.json"] = json_bytes(partition)
        files[prefix + "SHA256SUMS.txt"] = "".join(
            f"{digest(content)}  {name.removeprefix(prefix)}\n" for name, content in sorted(files.items())
            if name.startswith(prefix)).encode()
        sources[source] = {"manifest_path": prefix + "manifest.json", "canonical_path": canonical,
                           "license": "Apache-2.0" if source == "nvidia" else "MIT",
                           "game_count": 1,
                           "license_path": "third_party/nvidia/LICENSE" if source == "nvidia" else "LICENSE"}
    files["trajectories/statistics.json"] = json_bytes({"game_count": len(sources)})
    files["trajectories/per-game.csv"] = b"source,game\nstudio,studio01\nnvidia,nvidia01\n"
    files["trajectories/per-segment.csv"] = b"source,game,level,attempt\n"
    manifest = {"schema_version": builder.SCHEMA, "dataset_version": "fixture-v1", "sources": sources,
                "actor_type": "online_agent", "source_informed": True, "human_trajectories_included": False,
                "totals": {"game_count": len(sources)},
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


def test_v2_excerpts_remain_separate_and_do_not_claim_full_runs(tmp_path):
    root = tmp_path / "source"
    fixture(root, include_v2=True)
    result = tmp_path / "v2.zip"
    builder.build(result, root)
    with zipfile.ZipFile(result) as archive:
        assert "trajectories/studio_v2/trajectories.jsonl.gz" in archive.namelist()
        names = [name for name in archive.namelist() if name.startswith("trajectories/studio_v2/recordings/")]
        assert len(names) == 14
        assert "trajectories/studio_v2/recordings/v201.recording.jsonl.gz" not in archive.namelist()
        assert b"not independent reset-to-WIN" in archive.read("README.md")


@pytest.mark.parametrize("change", [{"standalone_full_run": True}, {"human_approval": True},
                                    {"level_id": "2"}, {"recording_scope": "complete_game_run"}])
def test_v2_excerpts_reject_false_scope_and_level_provenance(tmp_path, change):
    root = tmp_path / "source"
    fixture(root, include_v2=True, v2_change=change)
    with pytest.raises(ValueError, match="excerpt provenance"):
        builder.build(tmp_path / "false-scope.zip", root)


@pytest.mark.parametrize("location", ["canonical", "sidecar"])
def test_public_agent_metadata_rejects_nested_worker_even_with_rebound_checksums(tmp_path, location):
    root = tmp_path / "source"
    files = fixture(root, include_v2=True)
    prefix = "trajectories/studio_v2/"
    partition_name = prefix + "manifest.json"
    partition = json.loads(files[partition_name])
    private_agent = {"requested_model": "gpt-6.1-sol", "requested_effort": "xhigh",
                     "effective_model_metadata": {"actual_worker_id": "private-worker"}}
    if location == "canonical":
        name = prefix + "trajectories.jsonl.gz"
        files[name] = canonical_bytes(private_agent)
        partition["canonical_sha256"] = digest(files[name])
    else:
        name = prefix + "recordings/v201-level-01.metadata.json"
        sidecar = json.loads(files[name])
        sidecar["agent"] = private_agent
        files[name] = json_bytes(sidecar)
        partition["games"][0]["recordings"][0]["metadata_sha256"] = digest(files[name])
    files[partition_name] = json_bytes(partition)
    source_sums = prefix + "SHA256SUMS.txt"
    files[source_sums] = "".join(
        f"{digest(content)}  {name.removeprefix(prefix)}\n" for name, content in sorted(files.items())
        if name.startswith(prefix) and name != source_sums).encode()
    manifest_name = "trajectories/manifest.json"
    manifest = json.loads(files[manifest_name])
    manifest["files_sha256"] = {
        name: digest(content) for name, content in files.items()
        if name.startswith("trajectories/") and name not in {manifest_name, "trajectories/SHA256SUMS.txt"}}
    files[manifest_name] = json_bytes(manifest)
    files["trajectories/SHA256SUMS.txt"] = "".join(
        f"{digest(content)}  {name.removeprefix('trajectories/')}\n" for name, content in sorted(files.items())
        if name.startswith("trajectories/") and name != "trajectories/SHA256SUMS.txt").encode()
    for name, content in files.items():
        (root / name).write_bytes(content)
    with pytest.raises(ValueError, match="exactly three scalar string fields"):
        builder.checked_data(root)


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
                b"![Agent GIF](media/agent-demos/nvidia.gif) [Details](docs/TRAJECTORIES.md#format)")
    result = builder.scope_document_links(document, {"trajectories/studio/manifest.json", "docs/TRAJECTORIES.md"})
    assert b"[Data](trajectories/studio/manifest.json)" in result
    assert b"blob/main/environment_files/sg01/game.py" in result
    assert b"raw.githubusercontent.com/Felix561/arc3-synthetic-games/main/media/agent-demos/nvidia.gif" in result
    assert b"[Details](docs/TRAJECTORIES.md#format)" in result


def test_nested_document_links_resolve_relative_to_the_document():
    document = b"[Data](../trajectories/manifest.json) [Guide](TRAJECTORIES.md) [Player](../src/app.py)"
    result = builder.scope_document_links(
        document, {"trajectories/manifest.json", "docs/TRAJECTORIES.md"}, "docs/STATISTICS.md")
    assert b"[Data](../trajectories/manifest.json)" in result
    assert b"[Guide](TRAJECTORIES.md)" in result
    assert b"blob/main/src/app.py" in result


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
