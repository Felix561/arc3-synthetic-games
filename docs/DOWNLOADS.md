# Download and use the dataset

Download **`arc3-synthetic-games-v1.1.1-dataset.zip`** from the
[release](https://github.com/Felix561/arc3-synthetic-games/releases/tag/v1.1.1)
and extract it into an empty directory. It includes all 55 synthetic environments,
their exact-version AI recordings, compact training rows and source-specific licenses.
It contains no official ARC Prize games or human demonstration dataset.

| Path | Contents |
| --- | --- |
| `environment_files/` | 30 Studio games, one Python/metadata pair per game version |
| `third_party/nvidia/environment_files/` | 25 unchanged NVIDIA synthetic games |
| `third_party/nvidia/runtime_support/` | Pinned NVIDIA runtime support |
| `trajectories/{studio,nvidia}/trajectories.jsonl.gz` | Streaming level-attempt training rows |
| `trajectories/{studio,nvidia}/recordings/` | Native per-game gzip JSONL replays and provenance sidecars |
| `trajectories/manifest.json` | Dataset identity, partition paths and checksums |
| `SHA256SUMS.txt` | Every archive file's SHA-256 |

## Read the data without installing anything

Python 3.12 and its standard library are enough. From the extracted directory:

```bash
python tools/load_dataset.py
python tools/load_dataset.py --source nvidia
```

The first command reports **415 attempts, 410 solved, 6,011 policy actions**.
To stream individual rows:

```python
from tools.load_dataset import iter_trajectories

for episode in iter_trajectories("."):
    observations = episode["observations"]  # [actions + 1, 64, 64], integers 0–15
    actions = episode["actions"]
    solved = episode["is_solved"]
```

Native replay files preserve the ARC Prize Recorder-style `timestamp` / `data`
JSONL envelope and palette frames. Gzip is lossless; these are not RGB images.
The canonical training rows are our documented level-attempt schema, not a claim
of byte-for-byte interchangeability with every official human-data loader.
Unknown timestamps remain `null`. All actors are source-informed AI agents.
See [formats and coordinate conventions](TRAJECTORIES.md) before training.

## Run the exact environments

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

NVIDIA requires its separate environment directory and support import path;
follow [NVIDIA setup](TRAJECTORIES.md#nvidia-environments). Studio and NVIDIA remain
separate registries and separately licensed sources. Saved trajectories bind exact
native versions and seed 0; do not silently substitute other versions or seeds.

For the browser/local player, use the separate source or player package from the
same release. The player supports the 30 Studio games. The data-only trajectory ZIP
is available if you already have the environments; the Studio environments-only
ZIP is available if you do not need agent data or NVIDIA environments.
