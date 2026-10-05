"""Package exact synthetic environments and agent records together, without execution."""

import argparse
import json
from pathlib import Path

from build_preview import ROOT, write_zip
from build_trajectory_release import (
    STATISTICS_MEDIA,
    checked_data,
    parse_sums,
    read_public,
    scope_document_links,
    sha256,
)


def build(output, root=ROOT):
    root, output = Path(root).resolve(), Path(output).resolve()
    if output.exists():
        raise ValueError("Dataset archive must not overwrite an existing artifact")
    if output.is_relative_to(root / "trajectories"):
        raise ValueError("Choose an output outside the trajectory source tree")
    manifest, files = checked_data(root)
    catalog = json.loads(read_public(root, "catalog.json"))
    for game in catalog["games"]:
        for relative, expected in game["files_sha256"].items():
            name = game["environment_path"] + "/" + relative
            content = read_public(root, name)
            if sha256(content) != expected:
                raise ValueError(f"Native checksum mismatch: {name}")
            files[name] = content
    upstream_sums = read_public(root, "third_party/nvidia/SHA256SUMS.txt")
    files["third_party/nvidia/SHA256SUMS.txt"] = upstream_sums
    nvidia = json.loads(files["trajectories/nvidia/manifest.json"])
    allowed = {"LICENSE", "NOTICE", "THIRD_PARTY_NOTICES", "runtime_support/LICENSE",
               "runtime_support/NOTICE", "runtime_support/THIRD_PARTY_NOTICES",
               "runtime_support/arc_agi_3/game_creator/arcengine_adapter.py"}
    for game in nvidia["games"]:
        for relative in game["environment_files_sha256"]:
            allowed.add(game["environment_path"].removeprefix("third_party/nvidia/") + "/" + relative)
    inventory = parse_sums(upstream_sums)
    if set(inventory) != allowed:
        raise ValueError("Unexpected NVIDIA archive files")
    for relative, expected in inventory.items():
        name = "third_party/nvidia/" + relative
        content = read_public(root, name)
        if sha256(content) != expected:
            raise ValueError(f"NVIDIA checksum mismatch: {name}")
        files[name] = content
    # Bind the native packages in the replay manifests to the bytes just collected.
    for source in ("studio", "nvidia"):
        partition = json.loads(files[f"trajectories/{source}/manifest.json"])
        for game in partition["games"]:
            for relative, expected in game["environment_files_sha256"].items():
                name = game["environment_path"] + "/" + relative
                if name not in files or sha256(files[name]) != expected:
                    raise ValueError(f"Replay/source binding mismatch: {name}")
    for name in ("catalog.json", "LICENSE", "THIRD_PARTY_NOTICES.md", "tools/load_dataset.py",
                 "docs/DOWNLOADS.md", "docs/TRAJECTORIES.md", "docs/GAMES.md", "docs/STATISTICS.md",
                 "docs/VALIDATION.md", "docs/DATASET_CARD.md", *sorted(STATISTICS_MEDIA)):
        files[name] = read_public(root, name)
    files["README.md"] = b"""# Synthetic ARC3 environments and AI-agent trajectories

30 independently created Studio games + 25 NVIDIA synthetic environments.
No official ARC Prize games or official human demonstrations are included.

Read docs/DOWNLOADS.md for layout and native environment setup; read
docs/TRAJECTORIES.md for schemas, source-informed AI provenance and limitations.
Load all 415 palette-grid level attempts without any dependencies:

    python tools/load_dataset.py

Native recordings retain Recorder-style timestamp/data JSONL, compressed with
gzip. They are AI gameplay, not human recordings; unknown timestamps stay null.
Studio content uses MIT. NVIDIA content retains its Apache-2.0 license and notices
under third_party/nvidia/. Game sources execute Python: isolate native execution.
SHA256SUMS.txt covers every file in this ZIP. No player, GIFs or generation setup
is included; obtain the player separately from the repository releases.
"""
    for name in list(files):
        if name.startswith("docs/") and name.endswith(".md"):
            files[name] = scope_document_links(files[name], set(files), name)
    files["SHA256SUMS.txt"] = "".join(f"{sha256(b)}  {n}\n" for n, b in sorted(files.items())).encode()
    output.parent.mkdir(parents=True, exist_ok=True)
    write_zip(output, files)
    return {"bytes": output.stat().st_size, "sha256": sha256(output.read_bytes()),
            "dataset_version": manifest["dataset_version"], "files": len(files)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(build(args.output), indent=2))
