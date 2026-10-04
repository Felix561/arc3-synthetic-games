# Source-informed AI-agent trajectories

Dataset ID: **`arc3-source-informed-agent-20261002-v1`**. Recorded experience from
30 Studio games and 25 NVIDIA DreamTeam synthetic games, frozen on October 2, 2026.
There are 55 completed game runs, 410 solved levels and 415 level-attempt segments.
No human trajectories or official ARC3 training/evaluation games are included.

## Collection method and assistance

One dedicated Codex gameplay agent was assigned to each game. Agents could read
mechanics, level definitions and game source, then select legal actions in a real,
isolated native runtime. They could plan short action chunks and inspect actual
observations between them. Sixteen agents ran concurrently after a session restart.
This is privileged, source-informed experience rather than source-blind discovery.

The requested session configuration was **GPT-6.1-sol / ultra**. Subagents inherited
the session configuration; effective per-action model identity and effort were
not independently recorded. These fields are configuration provenance, not
verified model telemetry.

Actors were instructed not to invoke bespoke solvers, search algorithms, bundled
solutions or test action lists. Their source views removed recognised solution
definitions, but some unexpectedly named planning helpers and design guidance
remained visible. The actors reported not using those helpers. SG18 received an
additional read-only explanation of ordinary reflection, occupancy and click
rules; its original gameplay agent still chose all actions. Replay checks real
execution, not an actor's internal reasoning or the claimed non-use of visible
planning information. The public manifest retains these assistance limitations.

All runs reached native WIN at seed 0. Independently replaying every recorded
response checked pixels, states, available actions and level progression against
the exact native packages. This establishes the recorded paths, not optimality,
human discoverability, source-blind success or all-seed solvability.

## Two source partitions

| Partition | Native environments | Levels per game | License |
| --- | --- | ---: | --- |
| `trajectories/studio/` | SG01–SG30 in `environment_files/` | 7 | [MIT](LICENSE) |
| `trajectories/nvidia/` | 25 unchanged packages in `third_party/nvidia/environment_files/` | 8 | [Apache-2.0 and retained notices](third_party/nvidia/LICENSE) |

NVIDIA source: [DreamTeam](https://github.com/NVIDIA/dream-team), revision
[`bffef22f3e50fb7dcd6b2dc20005e6986e1479e9`](https://github.com/NVIDIA/dream-team/tree/bffef22f3e50fb7dcd6b2dc20005e6986e1479e9).
Its generated games are distinct from the official ARC Prize public environments.
All agent demonstrations were collected for this project; NVIDIA supplied the
environment source, not these recorded solutions.
The root Studio player catalog remains a 30-game catalog; it does not mix NVIDIA
IDs into Studio's browser or Python player.

Load each partition once to use the complete dataset. No combined file duplicates
the two partitions. All recorded policy segments are retained, including retries
and short sequences. The canonical `train` label is an ingestion convenience;
researchers choose and report their own experimental protocols.

## Canonical level-attempt JSONL

Each partition provides `trajectories.jsonl.gz`. Read one JSON object per line:

```python
import gzip
import json

with gzip.open("trajectories/studio/trajectories.jsonl.gz", "rt", encoding="utf-8") as stream:
    for line in stream:
        trajectory = json.loads(line)
        assert len(trajectory["observations"]) == len(trajectory["actions"]) + 1
```

| Field | Meaning |
| --- | --- |
| `game_id`, `level_id`, `seed` | Exact native version, one-based level and recorded seed |
| `trajectory_id`, `episode_id` | Deterministic public source/game/level/attempt identifier |
| `actor_type` | `online_agent`; never `human` |
| `observations` | Initial observation plus one settled frame per policy action; each is a 64×64 grid of palette integers 0–15 |
| `actions` | Native action ID, canonical type, parameters and valid-action information |
| `is_solved`, `is_terminal`, `is_truncated`, `terminal_reason` | Actual segment outcome and boundary, including interrupted attempts |
| `rewards` | `null`; no runtime rewards were fabricated |
| `scores` | Native completed-level-count sequence; not an official benchmark score or human-efficiency measure |
| `source_metadata` | Public source/assistance labels, package/runtime identity and measured completion-frame provenance |

Arrow IDs are 1–4 (up, down, left, right), Space is 5, click is 6 and Undo is 7.
For canonical clicks, `parameters.row` is native pixel **y** and
`parameters.column` is native pixel **x**, both 0–63. Native recordings retain the
original `action_input` representation. Use the available-action information;
not every game supports every action.

The final solved observation belongs to the completed level, even when the
response also contains the next level's initial frame. Selection was based on
worker-measured level attribution. The complete native recording preserves all
response frames, including animation and transitions.

Reset ID 0 is a control, not a policy action. A current-level reset ends the
previous attempt and begins a new one. Undo stays a policy action. The five
unsolved segments ended at reset boundaries; their native state was
`NOT_FINISHED`, not `GAME_OVER`. Initial game resets are separate from retries.

## Native per-game recordings

The partitions also contain one `*.recording.jsonl.gz` per game. These use the
[ARC Prize Recorder](https://github.com/arcprize/ARC-AGI-3-Agents/blob/main/agents/recorder.py)
JSONL envelope, with native FrameData from the
[SDK wrapper](https://github.com/arcprize/ARC-AGI/blob/main/arc_agi/wrapper.py):

```json
{"timestamp": null, "data": {"game_id": "…", "frame": "…", "action_input": "…"}}
```

The example abbreviates fields; `frame` in the real files is an array of integer
palette grids, not a string or RGB image. All 6,784 native frames and 6,071
responses are preserved. Recording times were not captured and remain `null`;
do not infer wall-clock duration or latency from them. GIF playback timing is
presentation pacing only.

Native recordings include reset controls and next-level transitions. Use the
canonical files for already segmented training data; do not assume every native
response's last frame belongs to the preceding level. Provenance sidecars and the
manifest are additional dataset metadata, not fields added to the native envelope.
Some native headers use a game's logical alias rather than its package-version
ID. Bind recordings to exact environments through the manifest and canonical
`game_id`; do not infer a package version from the raw header alone.

## NVIDIA environments

Native Python packages and runtime support are source-checkout assets; they are
omitted from the data-only trajectory ZIP, which includes their license notices
and exact-version bindings. Obtain the source repository to execute the games.

The third-party subtree retains the exact 25 native packages, original license,
NOTICE, third-party notices and required `runtime_support`. No entire game
generation framework or model dependency is needed for these packaged games.
In an isolated environment with the pinned native dependencies, from the repository
root, make the support import root visible before constructing the offline SDK:

```python
import json
import sys
from pathlib import Path
from arc_agi import Arcade, OperationMode

sys.path.insert(0, str(Path("third_party/nvidia/runtime_support").resolve()))
arcade = Arcade(operation_mode=OperationMode.OFFLINE,
                environments_dir="third_party/nvidia/environment_files")
with open("trajectories/nvidia/manifest.json", encoding="utf-8") as stream:
    collection = json.load(stream)
game_id = collection["games"][0]["native_game_id"]
game = arcade.make(game_id, seed=0, save_recording=False)
```

Keep Studio and NVIDIA registries and provenance separate. NVIDIA's eight-level
games must not be forced into a seven-level assumption. Metadata baseline action
values are not measured human baselines for this dataset.

## Integrity, privacy and reuse

The manifest and SHA-256 inventories bind compressed records, native packages,
runtime support and derived statistics. Public identifiers replace private actor,
run and request IDs. Private journals, machine paths, credentials, reasoning
transcripts, collection configuration and human trajectories are excluded.
The public verification summary describes the saved independent replay evidence;
it does not claim a newly published collection is a separate blind evaluation.

The dataset is intended for testing, imitation learning, planning and environment
model research. Supply observations/actions and appropriate outcome targets to
learners; source code and privileged mechanism/provenance information are separate.
Report exact versions, assistance conditions and any data filtering.

Original Studio data and tools are MIT-licensed. NVIDIA-derived recordings and
renderings are distributed with Apache-2.0, retaining upstream copyright and
relevant notices. Third-party rights are preserved; the root MIT license does not
replace them. This project is independent of NVIDIA and ARC Prize.
