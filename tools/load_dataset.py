"""Read compact palette trajectories without installing or executing game code."""

import argparse
import gzip
import json
from pathlib import Path

SOURCES = ("studio", "studio_v2", "nvidia")


def iter_trajectories(root, sources=None):
    """Stream one level-attempt dict at a time from selected source partitions."""
    root = Path(root)
    manifest = json.loads((root / "trajectories" / "manifest.json").read_text(encoding="utf-8"))
    available = manifest["sources"]
    if set(available) not in ({"studio", "nvidia"}, set(SOURCES)):
        raise ValueError("Unknown or missing trajectory source partitions")
    sources = tuple(source for source in SOURCES if source in available) if sources is None else sources
    if len(set(sources)) != len(sources):
        raise ValueError("Load each source partition only once")
    for source in sources:
        if source not in available:
            raise ValueError(f"Unknown source: {source}")
        path = root / "trajectories" / source / "trajectories.jsonl.gz"
        with gzip.open(path, "rt", encoding="utf-8") as stream:
            for line in stream:
                yield json.loads(line)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--source", choices=(*SOURCES, "all"), default="all")
    args = parser.parse_args()
    sources = None if args.source == "all" else (args.source,)
    attempts = solved = actions = 0
    for row in iter_trajectories(args.root, sources):
        attempts += 1
        solved += bool(row["is_solved"])
        actions += len(row["actions"])
    print(json.dumps({"level_attempts": attempts, "solved": solved, "policy_actions": actions}))


if __name__ == "__main__":
    main()
