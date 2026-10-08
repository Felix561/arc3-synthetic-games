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
import math
from collections import defaultdict
from pathlib import Path, PurePosixPath
from statistics import median

# ARC3 palette, copied verbatim from the trusted collection player's renderer.
PALETTE = [
    "FFFFFF", "CCCCCC", "999999", "666666", "333333", "000000", "E53AA3", "FF7BCC",
    "F93C31", "FF8B7F", "FFDC00", "FF851B", "921231", "4FCC30", "0074D9", "8E70D6",
]
SOURCES = {"studio": {"label": "Studio V1", "color": "#E43AA2"},
           "studio_v2": {"label": "Studio V2", "color": "#F9D143"},
           "nvidia": {"label": "NVIDIA DreamTeam", "color": "#1E93FF"}}
CLIPS = [("studio", "sg07", 7), ("studio", "sg18", 7), ("studio", "sg24", 6),
         ("studio", "sg25", 7), ("studio_v2", "v201", 7), ("studio_v2", "v214", 7),
         ("studio_v2", "v217", 7), ("studio_v2", "v219", 7),
         ("nvidia", "cc2048", 7), ("nvidia", "df4821", 7),
         ("nvidia", "ss6041", 7), ("nvidia", "fw4821", 7)]
DEMO_FOLDERS = {"studio": "studio", "studio_v2": "studio-v2", "nvidia": "nvidia"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((json.dumps(obj, indent=2, sort_keys=True) + "\n").encode("utf-8"))


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


def native_recording_path(data_root: Path, row: dict) -> Path:
    relative = PurePosixPath(row["source_metadata"]["native_recording_path"])
    assert not relative.is_absolute() and ".." not in relative.parts
    assert relative.parts and relative.parts[0] == data_root.name
    assert "\\" not in str(relative) and ":" not in str(relative)
    native = data_root.parent.joinpath(*relative.parts)
    assert native.is_file(), f"Missing public native recording: {relative}"
    return native


def verify_gif(path: Path, observations: list, durations: list[int]) -> None:
    from PIL import Image

    with Image.open(path) as check:
        assert check.info.get("loop") == 0, "The README previews must loop automatically"
        assert check.size == (320, 320), "The replay must contain only the native board"
        assert check.n_frames == len(observations)
        for i, grid in enumerate(observations):
            check.seek(i)
            assert check.info["duration"] == durations[i], "GIF changed playback timing"
            restored = check.convert("RGB").resize((64, 64), Image.Resampling.NEAREST)
            expected = b"".join(bytes.fromhex(PALETTE[v]) for rr in grid for v in rr)
            assert restored.tobytes() == expected, "GIF changed native palette pixels"


def draw_clips(rows: list[tuple[str, dict]], data_root: Path, output: Path,
               overwrite_existing: bool = False) -> list[dict]:
    from PIL import GifImagePlugin, Image

    palette = [channel for color in PALETTE for channel in bytes.fromhex(color)]
    palette += [0] * (768 - len(palette))
    manifest_path = output / "agent-demos/manifest.json"
    previous = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
    previous_clips = {entry["path"]: entry for entry in previous.get("clips", [])}
    clips = []
    for source, short_id, level in CLIPS:
        selected = [r for s, r in rows if s == source and r["game_id"].split("-")[0] == short_id
                    and int(r["level_id"]) == level and r["is_solved"]]
        assert len(selected) == 1, f"Expected exactly one solved selected level: {source}/{short_id}/{level}"
        row = selected[0]
        total = len(row["actions"])
        canonical = data_root / source / "trajectories.jsonl.gz"
        native = native_recording_path(data_root, row)
        with gzip.open(native, "rt", encoding="utf-8") as stream:
            responses = [json.loads(line)["data"] for line in stream]
        native_indices = row["source_metadata"]["native_response_indices"]
        native_frame_indices = row["source_metadata"]["response_frame_indices"]
        assert len(native_indices) == len(native_frame_indices) == total
        if source == "studio_v2":
            assert native_indices == list(range(1, total + 1))
            assert len(responses) == total + 1
            assert responses[0]["frame"][-1] == row["observations"][0]
        for i, action in enumerate(row["actions"]):
            recorded = responses[native_indices[i]]
            assert recorded["action_input"]["id"] == action["provider_raw_action"]
            if action["type"] == "CLICK":
                assert recorded["action_input"]["data"]["x"] == action["parameters"]["column"]
                assert recorded["action_input"]["data"]["y"] == action["parameters"]["row"]
            assert recorded["frame"][native_frame_indices[i]] == row["observations"][i + 1]
        step_ms = max(180, min(750, (16000 // max(total, 1)) // 10 * 10))
        durations = [1200] + [step_ms] * max(total - 1, 0) + [2800]
        # GIF delays have 10 ms precision. Round cumulative half-duration timing
        # to avoid accumulating per-frame rounding error.
        elapsed = 0
        previous = 0
        accelerated = []
        for duration in durations:
            elapsed += duration
            rounded = (elapsed + 10) // 20 * 10
            accelerated.append(rounded - previous)
            previous = rounded
        durations = accelerated
        gif_grids = row["observations"]
        native_animation = source == "studio_v2" and short_id == "v219"
        gif_native_indices = []
        gif_native_frame_indices = []
        if native_animation:
            gif_grids = []
            settled_durations = durations
            durations = []
            for response_index, response in enumerate(responses):
                received_frames = response["frame"]
                assert received_frames
                for frame_index, grid in enumerate(received_frames):
                    # The excerpt's preceding response may include the previous
                    # level's closing animation. Begin at this level's measured
                    # initial board, then retain every actual action-response frame.
                    if response_index == 0 and frame_index < len(received_frames) - 1:
                        continue
                    gif_grids.append(grid)
                    gif_native_indices.append(response_index)
                    gif_native_frame_indices.append(frame_index)
                    # Native cycles show causal motion that settled boards omit.
                    # Every action-response frame is retained; no motion is synthesized.
                    durations.append(20 if frame_index < len(received_frames) - 1
                                     else settled_durations[response_index])
        frames = []
        frame_hashes = [hashlib.sha256(grid_bytes(grid)).hexdigest() for grid in row["observations"]]
        gif_frame_hashes = []
        for grid in gif_grids:
            raw = grid_bytes(grid)
            gif_frame_hashes.append(hashlib.sha256(raw).hexdigest())
            board = Image.frombytes("P", (64, 64), raw)
            board.putpalette(palette)
            board = board.resize((320, 320), Image.Resampling.NEAREST)
            frames.append(board)
        relative = Path("agent-demos") / DEMO_FOLDERS[source] / f"{short_id}-level-{level:02d}.gif"
        path = output / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        preserved = previous_clips.get(relative.as_posix())
        public_native_path = native.relative_to(data_root.parent).as_posix()
        if preserved is not None and path.exists() and not overwrite_existing:
            assert preserved["source"] == source and preserved["game_id"] == row["game_id"]
            assert preserved["trajectory_id"] == row["trajectory_id"]
            assert preserved["canonical_data_sha256"] == sha256(canonical)
            assert preserved["native_recording_path"] == public_native_path
            assert preserved["native_recording_sha256"] == sha256(native)
            assert preserved["canonical_observation_sha256_uint8_row_major"] == frame_hashes
            assert preserved["native_response_indices_per_action"] == native_indices
            assert preserved["native_animation_frame_indices_per_action"] == native_frame_indices
            assert preserved["frame_durations_ms"] == durations
            assert preserved["gif_sha256"] == sha256(path)
            if native_animation:
                assert preserved["gif_native_response_indices"] == gif_native_indices
                assert preserved["gif_native_animation_frame_indices"] == gif_native_frame_indices
                assert preserved["gif_frame_sha256_uint8_row_major"] == gif_frame_hashes
            verify_gif(path, gif_grids, durations)
            clips.append(preserved)
            continue
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
        verify_gif(path, gif_grids, durations)
        clip = {
            "path": relative.as_posix(),
            "source": source, "game_id": row["game_id"], "level_id": str(level),
            "trajectory_id": row["trajectory_id"], "is_solved": row["is_solved"],
            "policy_actions": total, "canonical_observation_indices": list(range(total + 1)),
            "native_response_indices_per_action": native_indices,
            "native_animation_frame_indices_per_action": native_frame_indices,
            "canonical_observation_sha256_uint8_row_major": frame_hashes,
            "canonical_data_path": f"trajectories/{source}/trajectories.jsonl.gz",
            "canonical_data_sha256": sha256(canonical),
            "native_recording_path": public_native_path,
            "native_recording_sha256": sha256(native), "gif_sha256": sha256(path),
            "bytes": path.stat().st_size, "duration_ms": sum(durations),
            "frame_durations_ms": durations, "native_size": [64, 64], "display_scale": 5,
            "display_size": [320, 320], "loop": "infinite", "in_image_labels": False,
            "game_pixel_annotation": "none", "presentation": "complete solved level excerpt; settled observations",
        }
        if native_animation:
            clip.update({
                "presentation": "complete solved level excerpt; canonical initial observation and all native action-response animation frames",
                "gif_frame_policy": "Canonical initial observation plus every received frame of this level's action responses, in original order; no interpolation or invented motion.",
                "initial_native_response_index": 0,
                "initial_native_frame_index": len(responses[0]["frame"]) - 1,
                "gif_native_response_indices": gif_native_indices,
                "gif_native_animation_frame_indices": gif_native_frame_indices,
                "gif_frame_sha256_uint8_row_major": gif_frame_hashes,
                "native_frames_per_response": [len(response["frame"]) for response in responses],
                "gif_frames_per_response": [1] + [len(response["frame"]) for response in responses[1:]],
                "native_animation_frame_duration_ms": 20,
                "timing_policy": "Intermediate native frames use illustrative 20 ms delays; each response's final frame uses the settled-observation presentation delay.",
            })
        clips.append(clip)
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
                         "svg.hashsalt": "arc3-agent-trajectories-v2"})
    target = output / "trajectory-stats"
    target.mkdir(parents=True, exist_ok=True)
    assets = []
    by_source = {s: [len(r["actions"]) for ss, r in rows if ss == s] for s in SOURCES}
    assert len(rows) == stats["totals"]["segments"]
    assert sum(sum(v) for v in by_source.values()) == stats["totals"]["policy_actions"]
    assert sum(bool(r["is_solved"]) for _, r in rows) == stats["totals"]["solved_segments"]
    max_actions = max(max(values) for values in by_source.values())
    assert max_actions == stats["totals"]["actions_per_segment"]["max"]
    axis_limit = max(20, math.ceil(max_actions / 20) * 20)
    bins = np.arange(0, axis_limit + 1, 5)
    tick_step = 30 if axis_limit > 120 else 20
    fig, axes = plt.subplots(1, len(SOURCES), figsize=(18, 6.2), sharex=True, sharey=True)
    for ax, (source, info) in zip(axes, SOURCES.items(), strict=True):
        values = by_source[source]
        counts, _, _ = ax.hist(values, bins=bins, color=info["color"], edgecolor=background, linewidth=0.7)
        assert int(sum(counts)) == len(values), "Histogram omitted recorded attempts"
        ax.set_title(info["label"], loc="left", pad=14)
        ax.set_xlim(0, axis_limit)
        ax.set_xticks(np.arange(0, axis_limit + 1, tick_step))
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
    largest_source = max(sum(ss == source for ss, _ in grouped) for source in SOURCES)
    fig, axes = plt.subplots(1, len(SOURCES), figsize=(18, max(8, largest_source * 0.34 + 2.1)), sharex=True)
    for ax, (source, info) in zip(axes, SOURCES.items(), strict=True):
        games = sorted(game for ss, game in grouped if ss == source)
        yy = np.arange(len(games))
        lo = [min(grouped[(source, g)]) for g in games]
        hi = [max(grouped[(source, g)]) for g in games]
        mid = [median(grouped[(source, g)]) for g in games]
        assert max(hi) <= axis_limit
        ax.hlines(yy, lo, hi, color=info["color"], linewidth=2, alpha=0.65)
        ax.scatter(lo, yy, facecolors=background, edgecolors=info["color"], s=23, linewidths=1.3, zorder=3)
        ax.scatter(hi, yy, facecolors=background, edgecolors=info["color"], s=23, linewidths=1.3, zorder=3)
        ax.scatter(mid, yy, color=info["color"], s=40, zorder=4)
        for y, number in zip(yy, mid, strict=True):
            ax.text(1.04, y, f"{number:g}", transform=ax.get_yaxis_transform(),
                    va="center", fontsize=10, color="#FFFFFF")
        ax.set_yticks(yy, [g.upper() for g in games])
        ax.set_ylim(largest_source - 0.2, -1.5)
        ax.set_title(info["label"], loc="left", pad=12)
        ax.text(1.04, -1, "Median", transform=ax.get_yaxis_transform(), ha="left", fontsize=10)
        ax.set_xlim(0, axis_limit)
        ax.set_xticks(np.arange(0, axis_limit + 1, tick_step))
        ax.set_xlabel("Policy actions per level attempt", labelpad=10)
        ax.grid(axis="x", color="#595959", linewidth=0.8, linestyle=(0, (1, 3)))
        ax.set_axisbelow(True)
        ax.tick_params(axis="y", length=0, pad=7)
        ax.spines["left"].set_visible(False)
        ax.spines["bottom"].set_bounds(0, axis_limit)
    fig.suptitle("Recorded actions by game", x=0.08, y=0.985, ha="left", fontsize=19)
    fig.subplots_adjust(left=0.08, right=0.925, bottom=0.065, top=0.915, wspace=0.42)
    assets.append(save_chart(fig, target / "actions-by-game", plt))
    return assets


def save_chart(fig: object, stem: Path, plt: object) -> dict:
    svg, png = stem.with_suffix(".svg"), stem.with_suffix(".png")
    fig.savefig(svg, metadata={"Date": None, "Creator": "ARC3 trajectory media renderer"})
    svg.write_bytes(("\n".join(line.rstrip() for line in svg.read_text(encoding="utf-8").splitlines())
                     + "\n").encode("utf-8"))
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
    parser.add_argument("--overwrite-existing", action="store_true",
                        help="Regenerate existing GIFs instead of preserving verified matching files.")
    args = parser.parse_args()
    rows = rows_from_partitions(args.data_root)
    stats = json.loads((args.data_root / "statistics.json").read_text(encoding="utf-8"))
    clips = []
    charts = []
    if args.only in ("all", "clips"):
        clips = draw_clips(rows, args.data_root, args.output, args.overwrite_existing)
        write_json(args.output / "agent-demos/manifest.json", {
            "schema_version": 1, "actor_type": "online_agent", "source_informed": True,
            "selection": "Twelve illustrative solved level excerpts: four Studio V1, four Studio V2 and four NVIDIA games; not a random sample or a performance comparison.",
            "timing": "Illustrative playback timing; recording timestamps are unavailable.",
            "frame_policy": "Eleven clips show the canonical initial plus every settled post-action observation; V219 shows its canonical initial plus every received action-response animation frame.",
            "animation_policy": "All intermediate frames are preserved in native recordings. V219's GIF includes this level's action-response frames to show motion; other clips show settled observations. Its preceding response is shown only at the measured initial observation.",
            "rendering": "Native 64x64 ARC3 palette pixels scaled 5x by nearest-neighbor into board-only 320x320 looping GIFs; captions and notices are below the README gallery.",
            "documentation": "docs/TRAJECTORIES.md", "attribution_and_licensing": "THIRD_PARTY_NOTICES.md",
            "regenerate": "python tools/render_trajectory_media.py --only clips; optional authoring dependency: Pillow",
            "palette": PALETTE, "clips": clips,
        })
    if args.only in ("all", "charts"):
        charts = draw_charts(rows, args.output, stats)
        write_json(args.output / "trajectory-stats/manifest.json", {
            "schema_version": 1, "statistics_path": "trajectories/statistics.json",
            "statistics_sha256": sha256(args.data_root / "statistics.json"), "charts": charts,
            "grain": f"One recorded level attempt per canonical segment; all {len(rows)} attempts included.",
            "limitations": "One source-informed AI-agent playthrough per game. No human or optimal-policy comparison.",
            "policy_actions": "Current-level reset controls are excluded; unsuccessful reset-truncated attempts remain included.",
            "definitions": "docs/STATISTICS.md", "authoritative_values": "trajectories/statistics.json",
            "style_reference": "https://arcprize.org/blog/arc-agi-3-human-dataset",
            "presentation": "ARC Prize-inspired dark figures; interpretation captions are below charts in README.md and STATISTICS.md.",
        })
    print(json.dumps({"clips": len(clips), "gif_bytes": sum(c["bytes"] for c in clips), "charts": len(charts)}))


if __name__ == "__main__":
    main()
