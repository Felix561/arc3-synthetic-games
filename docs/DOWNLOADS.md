# Download and use the dataset

Download **`arc3-synthetic-games-v2.0.0-dataset.zip`** from the
[version 2.0.0 release](https://github.com/Felix561/arc3-synthetic-games/releases/tag/v2.0.0)
and extract it into an empty directory. It contains 75 synthetic environments,
exact-version AI data, compact training rows and source-specific licenses.
No official ARC Prize games or raw human trajectories are included.

| Path | Contents |
| --- | --- |
| `environment_files/` | 50 Studio games, one Python/metadata pair per native version |
| `third_party/nvidia/environment_files/` | 25 unchanged NVIDIA synthetic games |
| `third_party/nvidia/runtime_support/` | Pinned NVIDIA runtime support |
| `trajectories/{studio,studio_v2,nvidia}/trajectories.jsonl.gz` | Canonical level-attempt training rows |
| `trajectories/{studio,nvidia}/recordings/` | Complete native game recordings and public sidecars |
| `trajectories/studio_v2/recordings/` | Seven successful native response excerpts per game and public sidecars |
| `trajectories/manifest.json` | Dataset identity, partition paths and checksums |
| `SHA256SUMS.txt` | SHA-256 inventory of archive contents |

## Read without installation

Python 3.12 and its standard library are enough. From the extracted directory:

```bash
python tools/load_dataset.py
python tools/load_dataset.py --source studio_v2
python tools/load_dataset.py --source nvidia
```

The complete dataset has **555 attempts, 550 solved segments and 7,751 policy
actions**. Load each partition once; per-game native files are another
representation of the same recorded experience, not additional training episodes.

```python
from tools.load_dataset import iter_trajectories

for episode in iter_trajectories("."):
    observations = episode["observations"]  # [actions + 1, 64, 64], integers 0–15
    actions = episode["actions"]
    solved = episode["is_solved"]
```

Canonical rows use the documented level-attempt schema. The native files use the
ARC Prize Recorder-style `timestamp` / `data` envelope and palette frames;
gzip is lossless. An official human-data loader may need field mapping.

Earlier partitions include complete native game runs. V2 preserves successful
per-level response excerpts, including the actual preceding observation.
These excerpts are not independently replayable full-game files: they may start
mid-run, and neighboring excerpts can repeat a boundary response.
No RESET is fabricated. Unknown timestamps remain null.
See [trajectory format and coordinates](TRAJECTORIES.md).

## Run the native environments

Use an isolated Python 3.12 environment with:

```bash
python -m pip install arc-agi==0.9.8 arcengine==0.9.3 numpy==2.5.3
```

```python
import json
from arc_agi import Arcade, OperationMode

with open("catalog.json", encoding="utf-8") as stream:
    catalog = json.load(stream)
arcade = Arcade(operation_mode=OperationMode.OFFLINE,
                environments_dir="environment_files")
game = arcade.make(catalog["games"][0]["game_id"], seed=0, save_recording=False)
observation = game.reset()
```

NVIDIA uses its own environment directory and support import path;
follow [NVIDIA setup](TRAJECTORIES.md#nvidia-environments).
Keep exact native IDs, versions and recorded seeds when reproducing trajectories.

Use the source/player package for interactive play of the 50 Studio games.
The trajectories-only ZIP omits game Python; the Studio environments-only ZIP
omits agent data and NVIDIA environments. Every release asset has an external
checksum; archives also contain checksums for their own files.
