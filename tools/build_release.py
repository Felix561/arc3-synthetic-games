"""Assemble release ZIPs from a clean, committed tree and a built static preview."""

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

from build_preview import ROOT, write_zip


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args])


def build(output, preview, packages):
    if git("status", "--porcelain").strip():
        raise ValueError("Commit the reviewed source before creating release packages")
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
    names = {"catalog.json", "LICENSE", "THIRD_PARTY_NOTICES.md", "DATASET_CARD.md", "GAMES.md",
             "VALIDATION.md", "CITATION.cff", "CHANGELOG.md", "media/overview.png"}
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
    # An environments-only archive must not suggest its missing player is installed here.
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme = readme[:readme.index("## Play locally")] + readme[readme.index("## Use the native environments"):]
    readme = readme[:readme.index("## Development and hosting")] + readme[readme.index("## License and citation"):]
    files["README.md"] = readme.encode("utf-8")
    # Validation links to the historical audit, so retain that public document too.
    files["PUBLICATION_AUDIT.md"] = (ROOT / "PUBLICATION_AUDIT.md").read_bytes()
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
