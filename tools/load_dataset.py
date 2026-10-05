"""Read compact palette trajectories without installing or executing game code."""

import argparse
import gzip
import json
from pathlib import Path


def iter_trajectories(root, sources=("studio", "nvidia")):
    """Stream one level-attempt dict at a time from selected source partitions."""
    for source in sources:
        if source not in {"studio", "nvidia"}:
            raise ValueError(f"Unknown source: {source}")
        path = Path(root) / "trajectories" / source / "trajectories.jsonl.gz"
        with gzip.open(path, "rt", encoding="utf-8") as stream:
            for line in stream:
                yield json.loads(line)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--source", choices=("studio", "nvidia", "all"), default="all")
    args = parser.parse_args()
    sources = ("studio", "nvidia") if args.source == "all" else (args.source,)
    attempts = solved = actions = 0
    for row in iter_trajectories(args.root, sources):
        attempts += 1
        solved += bool(row["is_solved"])
        actions += len(row["actions"])
    print(json.dumps({"level_attempts": attempts, "solved": solved, "policy_actions": actions}))


if __name__ == "__main__":
    main()
