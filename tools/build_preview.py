"""Build a static GitHub Pages demo; reads game files without executing them."""

import argparse
import hashlib
import json
import re
import shutil
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE_NAME = "arcengine-0.9.3-py3-none-any.whl"
ENGINE_SHA256 = "5f9739d6d0055780a4581fd6fe09066bb08775c4c8212c9adcca2eb008aef59c"
ENGINE_URL = (
    "https://files.pythonhosted.org/packages/49/ce/efc5dcb66cacfe4c6ada2ba07ed7a6d9971110c9fd6d540793ed6748a12c/"
    + ENGINE_NAME
)


def write_zip(path, files):
    """Stable paths and timestamps; never inherit a workstation's ZIP metadata."""
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, content in sorted(files.items()):
            info = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, content)


def build(output, engine_wheel=None):
    output = Path(output).resolve()
    if output == ROOT or output in ROOT.parents:
        raise ValueError("Choose a separate output directory")
    output.mkdir(parents=True, exist_ok=True)
    if any(output.iterdir()):
        raise ValueError("Preview output must be empty; choose a new directory")
    data = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    native = {}
    media = {"media/overview.png"}
    for game in data["games"]:
        media.add(game["preview"])
        if game.get("demo"):
            media.add(game["demo"])
        for relative, digest in game["files_sha256"].items():
            name = f"{game['environment_path']}/{relative}"
            source = ROOT / name
            if not source.resolve().is_relative_to(ROOT) or source.is_symlink():
                raise ValueError("Unexpected native path")
            content = source.read_bytes()
            if hashlib.sha256(content).hexdigest() != digest:
                raise ValueError(f"Native checksum mismatch: {game['id']}")
            native["arc3_synthetic_games/data/" + name] = content
    if len(data["games"]) != 30 or len(native) != 60:
        raise ValueError("Expected the complete 30-game collection")
    for name in sorted(media | {"LICENSE", "THIRD_PARTY_NOTICES.md", "catalog.json"}):
        source = ROOT / name
        if not source.resolve().is_relative_to(ROOT) or source.is_symlink():
            raise ValueError("Unexpected asset path")
        target = output / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    static = ROOT / "src/arc3_synthetic_games/static"
    (output / "static").mkdir()
    for name in ("app.js", "style.css", "icon.svg"):
        shutil.copyfile(static / name, output / "static" / name)
    html = (static / "index.html").read_text(encoding="utf-8")
    html = html.replace(
        '<script src="static/app.js" defer></script>',
        '<script src="browser/client.js" defer></script>\n    <script src="static/app.js" defer></script>',
    )
    html = re.sub(r"Independent collection · v[0-9.]+", f"Browser demo · v{data['version']}", html, count=1)
    html = html.replace("Choose a world, try an action, and see what changes.",
                        "Choose a world and play without installing anything. "
                        "The first game downloads a browser runtime; an internet connection is needed.")
    html = html.replace("Local play · No accounts · No telemetry", "In-browser play · No accounts · No telemetry")
    html = html.replace("In-browser play · No accounts · No telemetry",
                        'In-browser play · No accounts · No telemetry · <a href="THIRD_PARTY_NOTICES.md">Licenses</a>')
    (output / "index.html").write_text(html, encoding="utf-8")
    (output / ".nojekyll").write_bytes(b"")
    (output / "browser").mkdir()
    for name in ("client.js", "worker.mjs"):
        shutil.copyfile(ROOT / "web" / name, output / "browser" / name)
    runtime = dict(native)
    for name in ("__init__.py", "dataset.py", "native.py"):
        runtime["arc3_synthetic_games/" + name] = (ROOT / "src/arc3_synthetic_games" / name).read_bytes()
    runtime["arc3_synthetic_games/data/catalog.json"] = (ROOT / "catalog.json").read_bytes()
    runtime["arc3_synthetic_games/data/THIRD_PARTY_NOTICES.md"] = (ROOT / "THIRD_PARTY_NOTICES.md").read_bytes()
    runtime["LICENSE"] = (ROOT / "LICENSE").read_bytes()
    runtime["browser_bridge.py"] = (ROOT / "web/bridge.py").read_bytes()
    write_zip(output / "browser/runtime.zip", runtime)
    if engine_wheel:
        engine = Path(engine_wheel).read_bytes()
    else:
        with urllib.request.urlopen(ENGINE_URL, timeout=60) as response:
            engine = response.read(1_000_000)
    if hashlib.sha256(engine).hexdigest() != ENGINE_SHA256:
        raise ValueError("ARC engine wheel checksum mismatch")
    (output / "browser" / ENGINE_NAME).write_bytes(engine)
    manifest = {
        "version": data["version"],
        "pyodide": "314.0.7",
        "files": [
            {"path": name, "sha256": hashlib.sha256((output / "browser" / name).read_bytes()).hexdigest()}
            for name in (ENGINE_NAME, "runtime.zip")
        ],
    }
    (output / "browser/runtime.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "_site")
    parser.add_argument("--engine-wheel", type=Path, help="Reuse a checksum-verified engine download")
    args = parser.parse_args()
    print(json.dumps(build(args.output, args.engine_wheel), indent=2))
