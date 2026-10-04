"""Build a deterministic, data-only agent trajectory ZIP from reviewed local files.

This draft builder never commits, pushes, tags, deploys or executes game Python.
Official source/player releases still require a clean committed tree.
"""

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path, PurePosixPath

from build_preview import ROOT, write_zip

SCHEMA = "arc3-public-agent-trajectories/1"
SOURCES = {"studio", "nvidia"}
DOCS = {"TRAJECTORIES.md", "STATISTICS.md"}
LICENSES = {"LICENSE", "third_party/nvidia/LICENSE", "third_party/nvidia/NOTICE",
            "third_party/nvidia/THIRD_PARTY_NOTICES"}
ROOT_DATA = {"manifest.json", "statistics.json", "per-game.csv", "per-segment.csv", "SHA256SUMS.txt"}
PARTITION_DATA = {"manifest.json", "trajectories.jsonl.gz", "verification.json", "SHA256SUMS.txt"}
RECORDING = re.compile(r"[a-z][a-z0-9]*\.(?:recording\.jsonl\.gz|metadata\.json)")
DIGEST = re.compile(r"[0-9a-f]{64}")
MARKDOWN_LINK = re.compile(r"(!?\[[^\]]*\]\()([^\s)]+)(\))")
STATISTICS_MEDIA = {"media/trajectory-stats/action-distribution.svg", "media/trajectory-stats/action-distribution.png",
                   "media/trajectory-stats/actions-by-game.svg", "media/trajectory-stats/actions-by-game.png",
                   "media/trajectory-stats/manifest.json"}


def sha256(content):
    return hashlib.sha256(content).hexdigest()


def checked_name(name):
    """ZIP and manifest names use safe, unambiguous repository-relative POSIX paths."""
    if not isinstance(name, str) or "\\" in name or ":" in name:
        raise ValueError("Unsafe publication path")
    path = PurePosixPath(name)
    if path.is_absolute() or not path.parts or any(part in {".", ".."} for part in path.parts):
        raise ValueError("Unsafe publication path")
    if path.as_posix() != name:
        raise ValueError("Unsafe publication path")
    return name


def is_data_path(name):
    checked_name(name)
    parts = PurePosixPath(name).parts
    if len(parts) == 2 and parts[0] == "trajectories":
        return parts[1] in ROOT_DATA
    if len(parts) == 3 and parts[0] == "trajectories" and parts[1] in SOURCES:
        return parts[2] in PARTITION_DATA
    return (len(parts) == 4 and parts[0] == "trajectories" and parts[1] in SOURCES
            and parts[2] == "recordings" and bool(RECORDING.fullmatch(parts[3])))


def read_public(root, name):
    checked_name(name)
    source = root / name
    if not source.resolve().is_relative_to(root.resolve()):
        raise ValueError("Publication path leaves repository")
    if any(path.is_symlink() for path in [source, *source.parents] if path != root.parent):
        raise ValueError("Publication files must not be symlinks")
    if not source.is_file():
        raise ValueError(f"Missing publication file: {name}")
    return source.read_bytes()


def parse_sums(content):
    result = {}
    for line in content.decode("utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        if not match:
            raise ValueError("Invalid trajectory checksum inventory")
        digest, name = match.groups()
        checked_name(name)
        if name in result:
            raise ValueError("Duplicate trajectory checksum entry")
        result[name] = digest
    return result


def checked_data(root):
    """Validate the complete data allowlist and both independently licensed partitions."""
    manifest_name = "trajectories/manifest.json"
    sums_name = "trajectories/SHA256SUMS.txt"
    manifest = json.loads(read_public(root, manifest_name))
    if manifest.get("schema_version") != SCHEMA:
        raise ValueError("Unsupported public trajectory manifest schema")
    if set(manifest.get("sources", {})) != SOURCES:
        raise ValueError("Expected distinct Studio and NVIDIA partitions")
    if (manifest.get("actor_type") != "online_agent" or manifest.get("source_informed") is not True
            or manifest.get("human_trajectories_included") is not False):
        raise ValueError("Publication must explicitly label source-informed AI-agent data")
    expected = manifest.get("files_sha256")
    if not isinstance(expected, dict) or not expected:
        raise ValueError("Missing public trajectory checksums")
    files = {manifest_name: read_public(root, manifest_name), sums_name: read_public(root, sums_name)}
    for name, digest in expected.items():
        if not is_data_path(name) or name in files or not isinstance(digest, str) or not DIGEST.fullmatch(digest):
            raise ValueError("Unexpected trajectory manifest file")
        content = read_public(root, name)
        if sha256(content) != digest:
            raise ValueError(f"Trajectory checksum mismatch: {name}")
        files[name] = content
    actual = {path.relative_to(root).as_posix() for path in (root / "trajectories").rglob("*")
              if path.is_file() or path.is_symlink()}
    if actual != set(files):
        raise ValueError("Unexpected or unlisted trajectory files")
    sums = {"trajectories/" + name: digest for name, digest in parse_sums(files[sums_name]).items()}
    if set(sums) != set(files) - {sums_name}:
        raise ValueError("Incomplete trajectory checksum inventory")
    if any(sha256(files[name]) != digest for name, digest in sums.items()):
        raise ValueError("Trajectory checksum inventory mismatch")
    for source in sorted(SOURCES):
        entry = manifest["sources"][source]
        prefix = f"trajectories/{source}/"
        partition_name = prefix + "manifest.json"
        canonical_name = prefix + "trajectories.jsonl.gz"
        expected_license = "LICENSE" if source == "studio" else "third_party/nvidia/LICENSE"
        license_name = "MIT" if source == "studio" else "Apache-2.0"
        if entry.get("manifest_path") != partition_name or entry.get("canonical_path") != canonical_name:
            raise ValueError("Partition files must stay within their source collection")
        if entry.get("license_path") != expected_license or entry.get("license") != license_name:
            raise ValueError("Missing source-specific license coverage")
        partition = json.loads(files[partition_name])
        if partition.get("schema_version") != SCHEMA or partition.get("source_collection") != source:
            raise ValueError("Partition provenance mismatch")
        if partition.get("license_path") != expected_license or partition.get("license") != license_name:
            raise ValueError("Partition license mismatch")
        if (partition.get("actor_type") != "online_agent" or partition.get("source_informed") is not True
                or partition.get("human_trajectories_included") is not False):
            raise ValueError("Partition must explicitly label source-informed AI-agent data")
        if partition.get("canonical_path") != canonical_name:
            raise ValueError("Partition canonical path mismatch")
        if partition.get("canonical_sha256") != sha256(files[canonical_name]):
            raise ValueError("Partition canonical checksum mismatch")
        if not partition.get("games"):
            raise ValueError("Empty public trajectory partition")
        games = partition["games"]
        if len(games) != entry.get("game_count"):
            raise ValueError("Partition game inventory mismatch")
        declared_recordings = set()
        environment_prefix = "environment_files/" if source == "studio" else "third_party/nvidia/environment_files/"
        game_names = set()
        for game in games:
            short_id = game["game"]
            if (not isinstance(short_id, str) or not re.fullmatch(r"[a-z][a-z0-9]*", short_id)
                    or short_id in game_names or game.get("source_collection") != source):
                raise ValueError("Game must belong to exactly one source partition")
            game_names.add(short_id)
            checked_name(game["environment_path"])
            if not game["environment_path"].startswith(environment_prefix + short_id + "/"):
                raise ValueError("Native source binding leaves its collection")
            recording_name = prefix + "recordings/" + short_id + ".recording.jsonl.gz"
            sidecar_name = prefix + "recordings/" + short_id + ".metadata.json"
            if game.get("recording_path") != recording_name:
                raise ValueError("Recording binding leaves its collection")
            if game.get("recording_sha256") != sha256(files[recording_name]):
                raise ValueError("Native recording binding checksum mismatch")
            sidecar = json.loads(files[sidecar_name])
            if (sidecar.get("source_collection") != source or sidecar.get("actor_type") != "online_agent"
                    or sidecar.get("source_informed") is not True):
                raise ValueError("Recording provenance mismatch")
            declared_recordings.update({recording_name, sidecar_name})
        actual_recordings = {name for name in files if name.startswith(prefix + "recordings/")}
        if declared_recordings != actual_recordings:
            raise ValueError("Recording inventory differs from the declared games")
        source_sums_name = prefix + "SHA256SUMS.txt"
        source_sums = {prefix + name: digest for name, digest
                       in parse_sums(files[source_sums_name]).items()}
        source_names = {name for name in files if name.startswith(prefix)} - {source_sums_name}
        if set(source_sums) != source_names:
            raise ValueError("Incomplete source-partition checksum inventory")
        if any(sha256(files[name]) != digest for name, digest in source_sums.items()):
            raise ValueError("Source-partition checksum inventory mismatch")
    return manifest, files


def archive_readme(manifest):
    counts = manifest.get("totals", {})
    games = counts.get("games", counts.get("game_count", 55))
    return f"""# Source-informed AI-agent trajectories

This data-only archive contains two separate collections covering {games} native
games: Studio synthetic games and NVIDIA Dream Team synthetic games. The records
were produced by source-informed AI agents, not human players. Source access and
mechanics information were available; this is not a blind benchmark result.

See [TRAJECTORIES.md](TRAJECTORIES.md) for formats, provenance and limitations, and
[STATISTICS.md](STATISTICS.md) for attempts, outcomes and action counts. The
`trajectories/` manifests bind every data file to its SHA-256 hash. `SHA256SUMS.txt`
at this archive's root additionally covers the documentation and license files.

No original game source, player application or raw human trajectories are in this
archive. Obtain the exact native environments from the source repository and
follow the manifests when replaying records:
https://github.com/Felix561/arc3-synthetic-games

Studio material uses [MIT](LICENSE). NVIDIA material retains its separate
[Apache-2.0 license](third_party/nvidia/LICENSE),
[notice](third_party/nvidia/NOTICE) and
[third-party notices](third_party/nvidia/THIRD_PARTY_NOTICES). There is no claim of
NVIDIA or ARC Prize endorsement. These datasets are intended for research and
testing, with no prescribed sampling quota.
""".encode()


def scope_document_links(content, archive_names):
    """Keep the data ZIP useful without implying it contains the playable source."""
    def replace(match):
        prefix, target, suffix = match.groups()
        if target.startswith(("https://", "http://", "#", "mailto:")):
            return match.group(0)
        path = target.split("#", 1)[0]
        checked_name(path)
        if path in archive_names:
            return match.group(0)
        host = ("https://raw.githubusercontent.com/Felix561/arc3-synthetic-games/main/"
                if prefix.startswith("!") else
                "https://github.com/Felix561/arc3-synthetic-games/blob/main/")
        return prefix + host + target + suffix
    return MARKDOWN_LINK.sub(replace, content.decode("utf-8")).encode()


def build(output, root=ROOT):
    root = Path(root).resolve()
    output = Path(output).resolve()
    if output.exists():
        raise ValueError("Trajectory archive must not overwrite an existing artifact")
    if output.is_relative_to(root / "trajectories") or output == root:
        raise ValueError("Choose an output outside the trajectory source tree")
    manifest, files = checked_data(root)
    for name in LICENSES:
        files[name] = read_public(root, name)
    for name in STATISTICS_MEDIA:
        if (root / name).is_file():
            files[name] = read_public(root, name)
    included_media = set(files) & STATISTICS_MEDIA
    if included_media:
        if included_media != STATISTICS_MEDIA:
            raise ValueError("Incomplete public statistics graphics")
        media_manifest = json.loads(files["media/trajectory-stats/manifest.json"])
        if media_manifest.get("statistics_sha256") != sha256(files["trajectories/statistics.json"]):
            raise ValueError("Statistics graphics refer to different source data")
        declared_media = set()
        for chart in media_manifest.get("charts", []):
            for extension in ("svg", "png"):
                name = "media/" + chart[extension]
                if name not in STATISTICS_MEDIA or chart[extension + "_sha256"] != sha256(files[name]):
                    raise ValueError("Statistics graphic checksum mismatch")
                declared_media.add(name)
        if declared_media != STATISTICS_MEDIA - {"media/trajectory-stats/manifest.json"}:
            raise ValueError("Statistics graphics manifest is incomplete")
    archive_names = set(files) | DOCS | {"README.md", "SHA256SUMS.txt"}
    for name in DOCS:
        files[name] = scope_document_links(read_public(root, name), archive_names)
    files["README.md"] = archive_readme(manifest)
    files["SHA256SUMS.txt"] = "".join(f"{sha256(content)}  {name}\n"
                                          for name, content in sorted(files.items())).encode("utf-8")
    output.parent.mkdir(parents=True, exist_ok=True)
    write_zip(output, files)
    with zipfile.ZipFile(output) as archive:
        if archive.testzip() is not None:
            raise ValueError("Trajectory ZIP failed its CRC check")
    result = {"path": str(output), "sha256": sha256(output.read_bytes()), "bytes": output.stat().st_size,
              "dataset_version": manifest["dataset_version"], "files": len(files)}
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(build(args.output), indent=2))
