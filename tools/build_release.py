"""Assemble release ZIPs from a clean, committed tree and a built static preview."""

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

from build_preview import ROOT, write_zip
from build_trajectory_release import build as build_trajectory_archive


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args])


PUBLIC_DOCS = {"README.md", "DATASET_CARD.md", "GAMES.md", "VALIDATION.md", "PUBLICATION.md",
               "THIRD_PARTY_NOTICES.md", "CHANGELOG.md", "TRAJECTORIES.md", "STATISTICS.md"}


def check_public_docs(paths):
    unexpected = [name for name in paths if name.lower().endswith(".md") and name not in PUBLIC_DOCS]
    if unexpected:
        raise ValueError(f"Unexpected Markdown in publication source: {unexpected}")


def native_archive_readme(version):
    """An environments-only archive describes only the assets it actually contains."""
    return f"""# ARC3 Synthetic Games native environments · v{version}

This archive contains the unchanged SG01–SG30 native environments: 30 games and
210 levels, with exact game IDs and SHA-256 hashes in `catalog.json`. It also
contains initial-board previews, six human-played GIF excerpts and reader-facing
documentation. The GIFs are presentation assets, not human trajectory data.

There is no player application or AI-agent trajectory dataset in this archive.
The separate source, browser-preview and agent-trajectory packages are available
from https://github.com/Felix561/arc3-synthetic-games/releases . NVIDIA environments
are separate from these 30 games and are not included here.

## Use the native environments

Use Python 3.12 and the validated native dependencies:

```bash
python -m pip install arc-agi==0.9.8 arcengine==0.9.3 numpy==2.5.3
```

From the extracted archive directory:

```python
import json
from arc_agi import Arcade, OperationMode

with open("catalog.json", encoding="utf-8") as file:
    catalog = json.load(file)

arcade = Arcade(operation_mode=OperationMode.OFFLINE,
                environments_dir="environment_files")
game = arcade.make(catalog["games"][0]["game_id"], seed=0, save_recording=False)
assert game is not None
observation = game.reset()
```

These game sources execute Python; use an isolated environment for untrusted
experiments. No official human-efficiency baseline or comparable ARC Prize score
is provided. Original Studio content is MIT-licensed; see `LICENSE` and
`THIRD_PARTY_NOTICES.md`. `GAMES.md` describes the included game collection.
""".encode()


def native_archive_validation():
    return b"""# Native environment validation

This archive contains only the 30 Studio native environments and their public
presentation assets. At packaging time, all 60 native source/metadata files are
checked against `catalog.json`. Native initialization, controls and player tests
are documented in the source repository:
https://github.com/Felix561/arc3-synthetic-games/blob/main/VALIDATION.md

The pinned native runtime is Python 3.12, arcengine 0.9.3, arc-agi 0.9.8 and NumPy
2.5.3. Runtime compatibility is distinct from human discoverability or independent
proof of solvability under every possible state. Tests and recorded successful
runs provide finite evidence, not a universal solvability guarantee.

Source-informed AI-agent recordings and their fresh-runtime replay verification
are a separate dataset/package, documented here:
https://github.com/Felix561/arc3-synthetic-games/blob/main/TRAJECTORIES.md
They are not human playthroughs, blind-agent evaluations or official benchmark
scores. No raw trajectory data or NVIDIA game source is included in this archive.
"""


def native_archive_notices():
    notices = (ROOT / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8")
    marker = "## Studio player dependencies"
    if marker not in notices:
        raise ValueError("Missing complete Studio dependency notices")
    return ("""# Third-party notices for the native environment archive

The original Studio games and presentation assets in this archive use the MIT
license supplied in `LICENSE`. The dependency acknowledgments and full MIT notices
below are preserved from the source repository.

No NVIDIA game source or trajectory data is included in this archive. The full
repository has additional, separately licensed datasets and retains their notices:
https://github.com/Felix561/arc3-synthetic-games/blob/main/THIRD_PARTY_NOTICES.md

This independent collection does not claim ARC Prize or NVIDIA endorsement.

""" + notices[notices.index(marker):]).encode()


def native_archive_citation(version):
    return f"""cff-version: 1.2.0
message: "Please cite this collection when using its native environments."
type: dataset
title: "ARC3 Synthetic Games"
version: "{version}"
license: MIT
authors:
  - name: "ARC3 Synthetic Games contributors"
abstract: "Thirty independent ARC3-compatible native games with seven fixed levels each."
repository-code: "https://github.com/Felix561/arc3-synthetic-games"
keywords:
  - interactive reasoning
  - synthetic environments
  - ARC3
  - planning
""".encode()


def build(output, preview, packages):
    if git("status", "--porcelain").strip():
        raise ValueError("Commit the reviewed source before creating release packages")
    check_public_docs(git("ls-files", "-z").decode().split("\0")[:-1])
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    if any(output.iterdir()):
        raise ValueError("Release output must be empty")
    data = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    version = data["version"]
    stem = f"arc3-synthetic-games-v{version}"
    # Git archive contains tracked source only, including no repository metadata.
    subprocess.run(["git", "-C", str(ROOT), "archive", "--format=zip", "--output",
                    str(output / f"{stem}-source.zip"), "HEAD"], check=True)
    names = {"catalog.json", "LICENSE", "GAMES.md", "media/overview.png"}
    for entry in data["games"]:
        names.add(entry["preview"])
        if entry.get("demo"):
            names.add(entry["demo"])
        for relative, expected in entry["files_sha256"].items():
            name = f"{entry['environment_path']}/{relative}"
            if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != expected:
                raise ValueError("Native release checksum mismatch")
            names.add(name)
    files = {name: (ROOT / name).read_bytes() for name in names}
    files["README.md"] = native_archive_readme(version)
    files["VALIDATION.md"] = native_archive_validation()
    files["THIRD_PARTY_NOTICES.md"] = native_archive_notices()
    files["CITATION.cff"] = native_archive_citation(version)
    write_zip(output / f"{stem}-environments.zip", files)
    manifest = json.loads((preview / "browser/runtime.json").read_text())
    if manifest["version"] != version:
        raise ValueError("Preview version does not match release")
    for entry in manifest["files"]:
        if hashlib.sha256((preview / "browser" / entry["path"]).read_bytes()).hexdigest() != entry["sha256"]:
            raise ValueError("Preview checksum mismatch")
    allowed = {"index.html", ".nojekyll", "LICENSE", "THIRD_PARTY_NOTICES.md", "catalog.json",
               "static/app.js", "static/style.css", "static/icon.svg", "browser/client.js",
               "browser/worker.mjs", "browser/runtime.json"}
    allowed.update("browser/" + entry["path"] for entry in manifest["files"])
    allowed.update(name for name in names if name.startswith("media/"))
    actual = {p.relative_to(preview).as_posix() for p in preview.rglob("*") if p.is_file()}
    if actual != allowed or any(p.is_symlink() for p in preview.rglob("*")):
        raise ValueError("Unexpected static preview files")
    write_zip(output / f"{stem}-browser-preview.zip", {name: (preview / name).read_bytes() for name in allowed})
    for name in (f"arc3_synthetic_games-{version}-py3-none-any.whl", f"arc3_synthetic_games-{version}.tar.gz"):
        shutil.copyfile(packages / name, output / name)
    if (ROOT / "trajectories/manifest.json").is_file():
        build_trajectory_archive(output / f"{stem}-agent-trajectories.zip")
    sums = "".join(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n"
                   for path in sorted(output.iterdir()))
    (output / "SHA256SUMS.txt").write_text(sums, encoding="utf-8")
    print(sums, end="")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--preview", required=True, type=Path)
    parser.add_argument("--packages", required=True, type=Path)
    args = parser.parse_args()
    build(args.output, args.preview, args.packages)
