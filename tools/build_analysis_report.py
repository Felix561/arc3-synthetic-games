"""Build a self-contained public report from allowlisted, reviewed summary data."""

import argparse
import base64
import csv
import hashlib
import io
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs" / "analysis"
SOURCE = ROOT / "tools" / "report"
SYNTHETIC = {"Studio V1", "Studio V2", "NVIDIA"}
FIELDS = {
    "coverage": "collection source games nativeLevels recordedPlays actions segments median mean lateMedian lateShort lateN",
    "distribution": "collection band count levelShare n",
    "profile": "collection level median n",
    "mix": "collection mode actions actionShare denominator",
    "weighted_mix": "collection mode meanGameShare games",
    "by_level_mix": "collection level mode actions actionShare denominator",
    "modes": "collection mode games gameShare",
    "synthetic_heat": "collection game level actions",
    "game_reviews": "source game title levels segments actions successful_actions median_level_actions late_mean_actions tutorial_actions late_short_le10 advertised_modes observed_modes planning discovery decoding family silhouette review_note challenge_band",
    "official_games": "game plays solves completionRate wilsonLow wilsonHigh levels actions median_completed_visit",
    "official_levels": "game level median upperMedian completed plays completionRate conditionalCompletionRate n",
    "families": "collection family games gameShare",
    "silhouettes": "collection family games gameShare",
    "divergence": "collection coding jsDivergence",
    "visuals": "collection game level modal_palette nonmodal_share palette_count edge_share palette_entropy",
    "visual_summary": "collection games median_nonmodal_share median_palette_count median_edge_share",
    "click_map": "collection x y count clickShare",
    "recipes": "collection game earlier_level later_level actions exact_ids_and_parameters",
    "progress": "game collection actions completed",
    "sequence": "collection game distinct_parameter_sequences levels all_lengths_equal",
    "input_detail": "collection input actions inputShare",
    "game_input": "collection game input actions inputShare",
}
FIGURES = (
    "01-length-distribution", "02-level-progression", "03-control-mix",
    "04-all-synthetic-levels", "05-actions-per-game", "06-official-human-completion",
    "07-human-level-reach", "08-mechanic-families", "09-visual-grammars",
    "10-opening-visual-structure", "11-action-progression", "12-click-spatial-distribution",
    "13-provisional-planning-bands", "14-v2-cohorts", "15-seven-input-mix", "16-game-control-mix",
)
REPORT_NAMES = {"index.html", "summary.json", "README.md", "LICENSE"}
REPORT_NAMES |= {f"tables/{name}.csv" for name in FIELDS}
REPORT_NAMES |= {f"figures/{name}.{suffix}" for name in FIGURES for suffix in ("png", "svg")}
REFERENCE_URLS = [
    "https://arcprize.org/blog/arc-agi-3-human-dataset",
    "https://docs.arcprize.org/methodology",
    "https://arcprize.org/media/ARC_AGI_3_Technical_Report.pdf",
    "https://arcprize.org/blog/arc-agi-3-preview-30-day-learnings",
    "https://github.com/NVIDIA/dream-team/tree/bffef22f3e50fb7dcd6b2dc20005e6986e1479e9/arc_agi_3",
]


def digest(content):
    return hashlib.sha256(content).hexdigest()


def normalize_svg(content):
    """Keep generated vector files readable and consistent across platforms."""
    return ("\n".join(line.rstrip() for line in content.decode("utf-8").splitlines()) + "\n").encode("utf-8")


def report_files(root=REPORT):
    """Read an exact hash-bound report inventory; refuse extras or unsafe paths."""
    root = Path(root)
    if root.is_symlink():
        raise ValueError("Unsafe analysis asset path")
    root = root.resolve()
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("schema") != "arc3-synthetic-analysis-files/1":
        raise ValueError("Unexpected analysis manifest schema")
    if set(manifest["files_sha256"]) != REPORT_NAMES:
        raise ValueError("Unexpected analysis asset inventory")
    files = {}
    for name, expected in manifest["files_sha256"].items():
        path = root / name
        if path.is_symlink() or not path.resolve().is_relative_to(root):
            raise ValueError("Unsafe analysis asset path")
        content = path.read_bytes()
        if digest(content) != expected:
            raise ValueError(f"Analysis checksum mismatch: {name}")
        files[name] = content
    files["manifest.json"] = (root / "manifest.json").read_bytes()
    actual = {path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file()}
    if set(files) != actual or any(path.is_symlink() for path in root.rglob("*")):
        raise ValueError("Unexpected analysis assets")
    return files


def prepare(snapshot_path, figures_dir):
    """One-time data refresh: select columns, never copy source/provenance blobs."""
    snapshot = json.loads(Path(snapshot_path).read_text(encoding="utf-8"))
    queries = {}
    for name, fields in FIELDS.items():
        rows = snapshot["queries"][name]["rows"]
        if name == "progress":
            rows = [row for row in rows if row["collection"] in SYNTHETIC]
        queries[name] = [{key: row[key] for key in fields.split()} for row in rows]
    payload = {
        "schema": "arc3-synthetic-analysis/1",
        "as_of": "2026-10-10",
        "dataset_release": "v2.0.0",
        "source_commit": "86bdcda30ce9f21606146c0796671b07220a50e8",
        "reference_urls": REFERENCE_URLS,
        "queries": queries,
    }
    REPORT.mkdir(parents=True, exist_ok=True)
    (REPORT / "summary.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    figures = REPORT / "figures"
    figures.mkdir(exist_ok=True)
    # Figure 11 in the private report contains individual human paths. Rebuild
    # that figure from synthetic data only; all other charts use aggregate data.
    for name in FIGURES:
        if name == "11-action-progression":
            continue
        for suffix in ("png", "svg"):
            path = Path(figures_dir) / f"{name}.{suffix}"
            if path.is_symlink():
                raise ValueError("Unsafe reviewed figure path")
            content = path.read_bytes()
            if suffix == "svg":
                # Deterministic public metadata: no workstation timestamps.
                content = re.sub(rb"<dc:date>.*?</dc:date>", b"<dc:date>2026-10-10</dc:date>", content)
                content = normalize_svg(content)
            (figures / path.name).write_bytes(content)
    render_progress_figure(queries["progress"], figures)


def render_progress_figure(rows, output):
    """Optional refresh dependency only; the normal report build uses stdlib."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MaxNLocator

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                         "figure.facecolor": "#0e0c0c", "axes.facecolor": "#0e0c0c",
                         "savefig.facecolor": "#0e0c0c", "text.color": "white",
                         "axes.labelcolor": "white", "xtick.color": "#cccccc",
                         "ytick.color": "#cccccc", "axes.edgecolor": "#595959",
                         "svg.fonttype": "none"})
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    for ax, game in zip(axes.ravel(), ("sg01", "v220", "v208", "ps7413")):
        points = [row for row in rows if row["game"] == game]
        ax.step([row["actions"] for row in points], [row["completed"] for row in points],
                where="post", color="#e43aa2", linewidth=2)
        ax.set_title(game.upper() + " · source-informed AI")
        ax.set_xlabel("Cumulative policy inputs")
        ax.set_ylabel("Completed levels")
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set_xlim(left=0)
        ax.set_ylim(bottom=0)
        ax.grid(color="#393535", linewidth=.6)
    fig.suptitle("Synthetic playthroughs reveal concentrated costs", x=.06, ha="left", fontsize=20)
    fig.text(.06, .025, "Independent x scales. Studio V2 concatenates selected successful level excerpts.\n"
             "Recovery and transit remain counted; these are not optimal paths.", fontsize=10, color="#c3bbbb")
    fig.subplots_adjust(top=.89, bottom=.17, left=.09, right=.97, hspace=.45, wspace=.3)
    for suffix in ("png", "svg"):
        metadata = {"Date": "2026-10-10"} if suffix == "svg" else {"Software": "ARC3 Synthetic Games analysis"}
        fig.savefig(output / f"11-action-progression.{suffix}", dpi=170, metadata=metadata)
        if suffix == "svg":
            path = output / "11-action-progression.svg"
            path.write_bytes(normalize_svg(path.read_bytes()))
    plt.close(fig)


def build(archive=None):
    if REPORT.is_symlink() or any(path.is_symlink() for path in REPORT.rglob("*")):
        raise ValueError("Unsafe analysis asset path")
    actual = {path.relative_to(REPORT).as_posix() for path in REPORT.rglob("*") if path.is_file()}
    if actual - REPORT_NAMES - {"manifest.json"}:
        raise ValueError("Unexpected analysis assets")
    data = json.loads((REPORT / "summary.json").read_text(encoding="utf-8"))
    metadata = {"schema", "as_of", "dataset_release", "source_commit", "reference_urls", "queries"}
    if set(data) != metadata or data["schema"] != "arc3-synthetic-analysis/1":
        raise ValueError("Unexpected public summary schema")
    if not re.fullmatch(r"[0-9a-f]{40}", data["source_commit"]) or data["reference_urls"] != REFERENCE_URLS:
        raise ValueError("Unexpected public source metadata")
    queries = data["queries"]
    if set(queries) != set(FIELDS):
        raise ValueError("Unexpected report query set")
    for name, rows in queries.items():
        if any(set(row) != set(FIELDS[name].split()) for row in rows):
            raise ValueError(f"Unexpected public fields: {name}")
    if any(row["collection"] not in SYNTHETIC for row in queries["progress"]):
        raise ValueError("Public progression data must be synthetic only")
    tables = REPORT / "tables"
    tables.mkdir(exist_ok=True)
    for name, rows in queries.items():
        text = io.StringIO(newline="")
        writer = csv.DictWriter(text, fieldnames=FIELDS[name].split(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
        (tables / f"{name}.csv").write_text(text.getvalue(), encoding="utf-8", newline="\n")
    template = (SOURCE / "index.template.html").read_text(encoding="utf-8")
    assets = {"STYLE": (SOURCE / "report.css").read_text(encoding="utf-8"),
              "SCRIPT": (SOURCE / "report.js").read_text(encoding="utf-8"),
              "DATA": json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")}
    for key, value in assets.items():
        template = template.replace("{{" + key + "}}", value)
    for match in re.findall(r"\{\{FIGURE:([a-z0-9-]+)\}\}", template):
        content = (REPORT / "figures" / f"{match}.png").read_bytes()
        template = template.replace("{{FIGURE:" + match + "}}", "data:image/png;base64," + base64.b64encode(content).decode())
    if "{{" in template:
        raise ValueError("Unresolved report placeholder")
    (REPORT / "index.html").write_text(template, encoding="utf-8", newline="\n")
    allowlist = [REPORT / name for name in sorted(REPORT_NAMES)]
    inventory = {str(path.relative_to(REPORT)).replace("\\", "/"): digest(path.read_bytes()) for path in allowlist}
    manifest = {"schema": "arc3-synthetic-analysis-files/1", "as_of": data["as_of"],
                "dataset_release": data["dataset_release"], "files_sha256": inventory,
                "excluded": ["official game source and pixels", "individual human replay paths",
                             "account/context identifiers", "private generation and learning notes",
                             "third-party report runtime"]}
    (REPORT / "manifest.json").write_text(json.dumps(manifest, indent=2)+"\n", encoding="utf-8", newline="\n")
    if archive:
        archive = Path(archive)
        if archive.exists():
            raise ValueError("Choose a new archive path")
        archive.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as output:
            for path in allowlist + [REPORT / "manifest.json"]:
                info = zipfile.ZipInfo("arc3-analysis/" + path.relative_to(REPORT).as_posix(), (1980, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                output.writestr(info, path.read_bytes())
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reviewed-snapshot", type=Path)
    parser.add_argument("--reviewed-figures", type=Path)
    parser.add_argument("--archive", type=Path)
    args = parser.parse_args()
    if bool(args.reviewed_snapshot) != bool(args.reviewed_figures):
        parser.error("Refreshing requires both reviewed inputs")
    if args.reviewed_snapshot:
        prepare(args.reviewed_snapshot, args.reviewed_figures)
    result = build(args.archive)
    print(json.dumps({"files": len(result["files_sha256"]), "index_sha256": result["files_sha256"]["index.html"]}))
