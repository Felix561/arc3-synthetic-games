"""Render public demonstration clips and charts from saved trajectory data only.

No game module is imported or executed. Requires Pillow and matplotlib, which are
optional authoring dependencies rather than dependencies of the game player.
Run from the repository root: python tools/render_trajectory_media.py
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from statistics import median

# ARC3 palette, copied verbatim from the trusted collection player's renderer.
PALETTE = [
    "FFFFFF", "CCCCCC", "999999", "666666", "333333", "000000", "E53AA3", "FF7BCC",
    "F93C31", "FF8B7F", "FFDC00", "FF851B", "921231", "4FCC30", "0074D9", "8E70D6",
]
SOURCES = {"studio": {"label": "Studio", "color": "#E43AA2"},
           "nvidia": {"label": "NVIDIA DreamTeam", "color": "#1E93FF"}}
CLIPS = [("studio", "sg07", 7), ("studio", "sg18", 7), ("studio", "sg24", 6),
         ("studio", "sg25", 7), ("nvidia", "cc2048", 7), ("nvidia", "df4821", 7),
         ("nvidia", "ss6041", 7), ("nvidia", "fw4821", 7)]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def rows_from_partitions(data_root: Path) -> list[tuple[str, dict]]:
    rows = []
    for source in SOURCES:
        with gzip.open(data_root / source / "trajectories.jsonl.gz", "rt", encoding="utf-8") as stream:
            for line in stream:
                row = json.loads(line)
                assert row["actor_type"] == "online_agent", "Only explicitly agent-labelled data is permitted"
                assert row["color_space"] == "arc3_0_15"
                assert len(row["observations"]) == len(row["actions"]) + 1
                rows.append((source, row))
    return rows


def grid_bytes(grid: list) -> bytes:
    assert len(grid) == 64 and all(len(row) == 64 for row in grid)
    assert all(type(pixel) is int and 0 <= pixel <= 15 for row in grid for pixel in row)
    return bytes(pixel for row in grid for pixel in row)


def action_label(action: dict) -> str:
    names = {"MOVE_UP": "Up", "MOVE_DOWN": "Down", "MOVE_LEFT": "Left", "MOVE_RIGHT": "Right",
             "SPECIAL": "Action 5", "UNDO": "Undo"}
    if action["type"] == "CLICK":
        params = action["parameters"]
        # Canonical coordinates are row/column; native ARC3 clicks use x/y.
        return f"Click (x={params['column']}, y={params['row']})"
    return names.get(action["type"], action["type"])


def draw_clips(rows: list[tuple[str, dict]], data_root: Path, output: Path) -> list[dict]:
    from PIL import GifImagePlugin, Image

    palette = [channel for color in PALETTE for channel in bytes.fromhex(color)]
    palette += [0] * (768 - len(palette))
    clips = []
    for source, short_id, level in CLIPS:
        selected = [r for s, r in rows if s == source and r["game_id"].split("-")[0] == short_id
                    and int(r["level_id"]) == level and r["is_solved"]]
        assert len(selected) == 1, f"Expected exactly one solved selected level: {source}/{short_id}/{level}"
        row = selected[0]
        total = len(row["actions"])
        canonical = data_root / source / "trajectories.jsonl.gz"
        native = data_root / source / "recordings" / f"{row['game_id']}.recording.jsonl.gz"
        if not native.exists():
            candidates = list((data_root / source / "recordings").glob(f"{short_id}*.recording.jsonl.gz"))
            assert len(candidates) == 1, f"Cannot resolve public native recording: {source}/{short_id}"
            native = candidates[0]
        with gzip.open(native, "rt", encoding="utf-8") as stream:
            responses = [json.loads(line)["data"] for line in stream]
        native_indices = row["source_metadata"]["native_response_indices"]
        native_frame_indices = row["source_metadata"]["response_frame_indices"]
        assert len(native_indices) == len(native_frame_indices) == total
        for i, action in enumerate(row["actions"]):
            recorded = responses[native_indices[i]]
            assert recorded["action_input"]["id"] == action["provider_raw_action"]
            if action["type"] == "CLICK":
                assert recorded["action_input"]["data"]["x"] == action["parameters"]["column"]
                assert recorded["action_input"]["data"]["y"] == action["parameters"]["row"]
            assert recorded["frame"][native_frame_indices[i]] == row["observations"][i + 1]
        step_ms = max(180, min(750, (16000 // max(total, 1)) // 10 * 10))
        durations = [1200] + [step_ms] * max(total - 1, 0) + [2800]
        frames = []
        frame_hashes = []
        for grid in row["observations"]:
            raw = grid_bytes(grid)
            frame_hashes.append(hashlib.sha256(raw).hexdigest())
            board = Image.frombytes("P", (64, 64), raw)
            board.putpalette(palette)
            board = board.resize((320, 320), Image.Resampling.NEAREST)
            frames.append(board)
        relative = Path("agent-demos") / source / f"{short_id}-level-{level:02d}.gif"
        path = output / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        # Pillow's usual save_all combines identical neighboring boards. Encode
        # each frame explicitly so even no-op actions keep their own observation.
        header, _ = GifImagePlugin.getheader(frames[0], info={"loop": 0, "optimize": False})
        with path.open("wb") as stream:
            for block in header:
                stream.write(block)
            for frame, duration in zip(frames, durations, strict=True):
                for block in GifImagePlugin.getdata(frame, duration=duration, disposal=2):
                    stream.write(block)
            stream.write(b";")
        # Verify the final GIF's game pixels survived the indexed conversion exactly.
        with Image.open(path) as check:
            assert check.info.get("loop") == 0, "The README previews must loop automatically"
            assert check.size == (320, 320), "The replay must contain only the native board"
            assert check.n_frames == len(frames)
            for i, grid in enumerate(row["observations"]):
                check.seek(i)
                board_rgb = check.convert("RGB")
                restored = board_rgb.resize((64, 64), Image.Resampling.NEAREST)
                expected = b"".join(bytes.fromhex(PALETTE[v]) for rr in grid for v in rr)
                assert restored.tobytes() == expected, "GIF changed native palette pixels"
        clips.append({
            "path": relative.as_posix(),
            "source": source, "game_id": row["game_id"], "level_id": str(level),
            "trajectory_id": row["trajectory_id"], "is_solved": row["is_solved"],
            "policy_actions": total, "canonical_observation_indices": list(range(total + 1)),
            "native_response_indices_per_action": native_indices,
            "native_animation_frame_indices_per_action": native_frame_indices,
            "canonical_observation_sha256_uint8_row_major": frame_hashes,
            "canonical_data_path": f"trajectories/{source}/trajectories.jsonl.gz",
            "canonical_data_sha256": sha256(canonical),
            "native_recording_path": f"trajectories/{source}/recordings/{native.name}",
            "native_recording_sha256": sha256(native), "gif_sha256": sha256(path),
            "bytes": path.stat().st_size, "duration_ms": sum(durations),
            "frame_durations_ms": durations, "native_size": [64, 64], "display_scale": 5,
            "display_size": [320, 320], "loop": "infinite", "in_image_labels": False,
            "game_pixel_annotation": "none", "presentation": "complete solved level excerpt; settled observations",
        })
    return clips


def draw_charts(rows: list[tuple[str, dict]], output: Path, stats: dict) -> list[dict]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.ticker import MaxNLocator

    # ARC Prize's human-dataset figures inform the presentation, not the data or scoring.
    # Scope, interpretation and limitations belong below each chart in the Markdown docs.
    background = "#0E0C0C"
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "axes.titlesize": 15,
                         "figure.facecolor": background, "axes.facecolor": background,
                         "savefig.facecolor": background, "axes.labelcolor": "#FFFFFF",
                         "text.color": "#FFFFFF", "xtick.color": "#FFFFFF", "ytick.color": "#FFFFFF",
                         "axes.edgecolor": "#FFFFFF", "axes.linewidth": 0.8,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "svg.hashsalt": "arc3-agent-trajectories-v1"})
    target = output / "trajectory-stats"
    target.mkdir(parents=True, exist_ok=True)
    assets = []
    by_source = {s: [len(r["actions"]) for ss, r in rows if ss == s] for s in SOURCES}
    assert len(rows) == stats["totals"]["segments"]
    assert sum(sum(v) for v in by_source.values()) == stats["totals"]["policy_actions"]
    assert sum(bool(r["is_solved"]) for _, r in rows) == stats["totals"]["solved_segments"]
    assert max(max(v) for v in by_source.values()) < 90, "The authored histogram must include all attempts"
    bins = np.arange(0, 91, 5)
    fig, axes = plt.subplots(1, 2, figsize=(12, 6.2), sharex=True, sharey=True)
    for ax, (source, info) in zip(axes, SOURCES.items(), strict=True):
        values = by_source[source]
        ax.hist(values, bins=bins, color=info["color"], edgecolor=background, linewidth=0.7)
        ax.set_title(info["label"], loc="left", pad=14)
        ax.set_xlim(0, 90)
        ax.set_xticks(np.arange(0, 91, 15))
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set_axisbelow(True)
        ax.grid(axis="y", color="#595959", linewidth=0.8, linestyle=(0, (1, 3)))
        ax.set_xlabel("Policy actions per level attempt", labelpad=10)
    axes[0].set_ylabel("Recorded attempts", labelpad=10)
    fig.suptitle("Actions per level attempt", x=0.08, y=0.96, ha="left", fontsize=19)
    fig.subplots_adjust(left=0.08, right=0.98, bottom=0.15, top=0.81, wspace=0.15)
    assets.append(save_chart(fig, target / "action-distribution", plt))
    grouped = defaultdict(list)
    for source, row in rows:
        grouped[(source, row["game_id"].split("-")[0])].append(len(row["actions"]))
    fig, axes = plt.subplots(1, 2, figsize=(12, 12), sharex=True)
    for ax, (source, info) in zip(axes, SOURCES.items(), strict=True):
        games = sorted(game for ss, game in grouped if ss == source)
        yy = np.arange(len(games))
        lo = [min(grouped[(source, g)]) for g in games]
        hi = [max(grouped[(source, g)]) for g in games]
        mid = [median(grouped[(source, g)]) for g in games]
        ax.hlines(yy, lo, hi, color=info["color"], linewidth=2, alpha=0.65)
        ax.scatter(lo, yy, facecolors=background, edgecolors=info["color"], s=23, linewidths=1.3, zorder=3)
        ax.scatter(hi, yy, facecolors=background, edgecolors=info["color"], s=23, linewidths=1.3, zorder=3)
        ax.scatter(mid, yy, color=info["color"], s=40, zorder=4)
        for y, number in zip(yy, mid, strict=True):
            ax.text(1.04, y, f"{number:g}", transform=ax.get_yaxis_transform(),
                    va="center", fontsize=10, color="#FFFFFF")
        ax.set_yticks(yy, [g.upper() for g in games])
        ax.set_ylim(29.8, -1.5)
        ax.set_title(info["label"], loc="left", pad=12)
        ax.text(1.04, -1, "Median", transform=ax.get_yaxis_transform(), ha="left", fontsize=10)
        ax.set_xlim(0, 90)
        ax.set_xticks([0, 20, 40, 60, 80])
        ax.set_xlabel("Policy actions per level attempt", labelpad=10)
        ax.grid(axis="x", color="#595959", linewidth=0.8, linestyle=(0, (1, 3)))
        ax.set_axisbelow(True)
        ax.tick_params(axis="y", length=0, pad=7)
        ax.spines["left"].set_visible(False)
        ax.spines["bottom"].set_bounds(0, 90)
    fig.suptitle("Recorded actions by game", x=0.08, y=0.985, ha="left", fontsize=19)
    fig.subplots_adjust(left=0.08, right=0.925, bottom=0.065, top=0.915, wspace=0.42)
    assets.append(save_chart(fig, target / "actions-by-game", plt))
    return assets


def save_chart(fig: object, stem: Path, plt: object) -> dict:
    svg, png = stem.with_suffix(".svg"), stem.with_suffix(".png")
    fig.savefig(svg, metadata={"Date": None, "Creator": "ARC3 trajectory media renderer"})
    fig.savefig(png, dpi=130, metadata={"Software": "ARC3 trajectory media renderer"})
    plt.close(fig)
    return {"svg": "trajectory-stats/" + svg.name, "png": "trajectory-stats/" + png.name,
            "svg_sha256": sha256(svg), "png_sha256": sha256(png)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", type=Path, default=Path("trajectories"))
    parser.add_argument("--output", type=Path, default=Path("media"))
    parser.add_argument("--only", choices=("all", "clips", "charts"), default="all",
                        help="Refresh only the selected media family (default: all).")
    args = parser.parse_args()
    rows = rows_from_partitions(args.data_root)
    stats = json.loads((args.data_root / "statistics.json").read_text(encoding="utf-8"))
    clips = []
    charts = []
    if args.only in ("all", "clips"):
        clips = draw_clips(rows, args.data_root, args.output)
        write_json(args.output / "agent-demos/manifest.json", {
            "schema_version": 1, "actor_type": "online_agent", "source_informed": True,
            "selection": "Eight illustrative solved level excerpts: four Studio and four NVIDIA games; not a random sample or a performance comparison.",
            "timing": "Replay-paced display. Native response timestamps were not recorded; no wall-clock speed is claimed.",
            "frame_policy": "Canonical initial plus every settled post-action observation, including the old-level completion frame.",
            "animation_policy": "Intermediate animation frames are preserved in native recordings, but omitted from settled-observation clips.",
            "rendering": "Native 64x64 ARC3 palette pixels scaled 5x by nearest-neighbor into board-only 320x320 looping GIFs; captions and notices are below the README gallery.",
            "documentation": "TRAJECTORIES.md", "attribution_and_licensing": "THIRD_PARTY_NOTICES.md",
            "regenerate": "python tools/render_trajectory_media.py --only clips; optional authoring dependency: Pillow",
            "palette": PALETTE, "clips": clips,
        })
    if args.only in ("all", "charts"):
        charts = draw_charts(rows, args.output, stats)
        write_json(args.output / "trajectory-stats/manifest.json", {
            "schema_version": 1, "statistics_path": "trajectories/statistics.json",
            "statistics_sha256": sha256(args.data_root / "statistics.json"), "charts": charts,
            "grain": "One recorded level attempt per canonical segment; all 415 attempts included.",
            "limitations": "One source-informed AI-agent playthrough per game. No human or optimal-policy comparison.",
            "policy_actions": "Current-level reset controls are excluded; unsuccessful reset-truncated attempts remain included.",
            "definitions": "STATISTICS.md", "authoritative_values": "trajectories/statistics.json",
            "style_reference": "https://arcprize.org/blog/arc-agi-3-human-dataset",
            "presentation": "ARC Prize-inspired dark figures; interpretation captions are below charts in README.md and STATISTICS.md.",
        })
    print(json.dumps({"clips": len(clips), "gif_bytes": sum(c["bytes"] for c in clips), "charts": len(charts)}))


if __name__ == "__main__":
    main()
