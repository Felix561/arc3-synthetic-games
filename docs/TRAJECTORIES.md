# Source-informed AI-agent trajectories

Dataset ID: **`arc3-source-informed-agent-v2.0.0`**.
The collection covers 75 synthetic games and 550 levels, with **555 recorded
level-attempt segments: 550 solved and five reset-interrupted**.
No raw human trajectories or official ARC3 training/evaluation games are included.

## Collection method and assistance

One dedicated Codex gameplay agent was assigned to each game. Agents could read
mechanics, level definitions and source, choose legal actions in an isolated native
runtime, and inspect actual observations between short action chunks.
This is privileged source-informed experience, not source-blind discovery.

The requested model was **GPT-6.1-sol**. The original Studio/NVIDIA collection
requested ultra reasoning. V201–V207 requested ultra; V208–V220 requested xhigh.
Effective model identity and per-action effort were not independently measured.
Public model labels describe dispatch configuration rather than verified telemetry.

Earlier actors were instructed not to invoke bespoke solvers, search algorithms,
bundled solutions or test action lists. Source views removed recognized solution
definitions, but some unexpectedly named planning helpers and design guidance
remained visible. Actors reported non-use. SG18 also received a read-only
explanation of ordinary reflection, occupancy and click rules. V2 actors had
source and design information. Replay checks execution, not internal reasoning
or the claimed non-use of visible information.

The original complete runs reached native WIN at recorded seed 0 and passed
independent fresh replay on exact packages, comparing response frames and game
progression. This establishes recorded paths, not human discoverability,
optimality, source-blind success or all-seed solvability.

## Three partitions

| Partition | Environments | Levels per game | Native records | License |
| --- | --- | ---: | --- | --- |
| `studio` | SG01–SG30 in `environment_files/` | 7 | 30 complete game recordings | [MIT](../LICENSE) |
| `studio_v2` | V201–V220 in `environment_files/` | 7 | 140 successful level response excerpts | [MIT](../LICENSE) |
| `nvidia` | 25 packages in `third_party/nvidia/environment_files/` | 8 | 25 complete game recordings | [Apache-2.0 and retained notices](../third_party/nvidia/LICENSE) |

Studio and NVIDIA's existing partition dataset IDs are unchanged.
V2 adds a new partition and leaves older native versions and recordings intact.
The Studio catalog/player includes 50 games; NVIDIA remains outside that catalog.

NVIDIA source: [DreamTeam](https://github.com/NVIDIA/dream-team), revision
[`bffef22f3e50fb7dcd6b2dc20005e6986e1479e9`](https://github.com/NVIDIA/dream-team/tree/bffef22f3e50fb7dcd6b2dc20005e6986e1479e9).
Its synthetic games are distinct from official ARC Prize environments.
NVIDIA supplied environment code, not these agent demonstrations.

Load each partition once. No combined training file duplicates those partitions.
Earlier partitions retain retries and short segments; V2 retains all successful
replay-verified segments and excludes private failed attempts. The canonical
`train` label is an ingestion convenience, not a prescribed experimental split.

## Canonical level-attempt JSONL

Each partition provides `trajectories.jsonl.gz`, one JSON object per line:

```python
import gzip
import json

with gzip.open("trajectories/studio_v2/trajectories.jsonl.gz", "rt", encoding="utf-8") as stream:
    for line in stream:
        trajectory = json.loads(line)
        assert len(trajectory["observations"]) == len(trajectory["actions"]) + 1
```

| Field | Meaning |
| --- | --- |
| `game_id`, `level_id`, `seed` | Exact native version, one-based level and recorded seed |
| `trajectory_id`, `episode_id` | Deterministic public source/game/level/attempt identifier |
| `actor_type` | `online_agent`; never `human` |
| `observations` | Initial observation plus one settled frame per policy action; 64×64 palette integers 0–15 |
| `actions` | Native action ID, canonical type, parameters and valid-action information |
| `is_solved`, `is_terminal`, `is_truncated`, `terminal_reason` | Actual outcome and completion/reset boundary |
| `rewards` | `null`; no rewards are fabricated |
| `scores` | Native completed-level counts, not official benchmark or efficiency scores |
| `source_metadata` | Public source/assistance labels, package/runtime identity and completion-frame provenance |

Action IDs 1–4 are up, down, left and right; 5 is Space, 6 click and 7 Undo.
For canonical clicks, `parameters.row` is native pixel **y** and
`parameters.column` is pixel **x**, both 0–63. Native files retain the original
`action_input` representation. Use available-action masks: games support
different controls.

A solved observation belongs to its completed level even if the same response
also contains the next level's initial frame. Selection uses measured level
attribution, not an assumption that the final response frame is the solved one.
Native files retain response animation and transition frames.

Reset ID 0 is a control, not a policy action. A current-level reset splits an
attempt. Undo is a policy action. The five unsolved NVIDIA segments ended with
`NOT_FINISHED` at resets, not native `GAME_OVER`.

## Native recordings and V2 excerpts

Files use the
[ARC Prize Recorder](https://github.com/arcprize/ARC-AGI-3-Agents/blob/main/agents/recorder.py)
`timestamp` / `data` JSONL envelope with native FrameData:

```json
{"timestamp": null, "data": {"game_id": "…", "frame": "…", "action_input": "…"}}
```

The example abbreviates fields; actual `frame` values are arrays of integer
palette grids. Timestamps were not captured and remain null. GIF pacing does not
measure elapsed time, latency or collection cost.

Across all 75 original complete runs, 7,831 unique responses contain 9,235 native
frames. V2 contributes 1,760 unique responses and 2,451 frames. These original-run
counts are distinct from overlapping public excerpt storage.

Original `studio` and `nvidia` partitions have one complete
`*.recording.jsonl.gz` file per game, including resets and next-level transitions.
Their 6,071 responses contain 6,784 native frames.

V2 has files such as
`recordings/v201-level-01.recording.jsonl.gz`, with a corresponding
`v201-level-01.metadata.json` sidecar. They contain the successful level's
responses plus its actual preceding observation. They can start mid-run;
the preserved preceding action is not replaced with a fabricated RESET.
The 140 V2 excerpt files store 1,880 response lines and 3,189 frames, including
repeated boundary responses. Sidecars explicitly mark
`excerpt_only: true` and `standalone_native_game_replay: false`.

**V2 excerpts are not standalone full-game replay files.** The original complete
runs were freshly replayed before successful segments were exported. Use canonical
rows for segmented training, and preserve exact versions when reconstructing native
execution. Do not sum overlapping excerpt responses as unique original-run
responses or treat excerpt copies as extra episodes.

Manifest and sidecars are additional public metadata, not fields inserted into the
native envelope. Some earlier native headers use logical aliases rather than
package-version IDs; exact bindings come from manifests and canonical
`game_id`, not the raw header alone.

## NVIDIA environments

The complete dataset/source packages contain 25 unchanged native NVIDIA packages,
retained licenses/notices and required `runtime_support`.
They are omitted from the trajectories-only ZIP. No complete game-generation
framework or model dependency is needed to run these packages.

From an isolated environment with pinned native dependencies:

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
game = arcade.make(collection["games"][0]["native_game_id"], seed=0,
                   save_recording=False)
```

Keep NVIDIA's eight-level assumption distinct from Studio's seven levels.
Metadata action baselines are not measured human baselines for this dataset.

## Integrity, privacy and reuse

SHA-256 inventories bind compressed records, native packages, runtime support and
derived statistics. Public identifiers replace private actor/run/request IDs.
Machine paths, credentials, personal identifiers, journals, reasoning transcripts,
generation configuration and human trajectories are excluded.

Use observations, actions and appropriate outcome targets for testing, imitation
learning, planning and environment modeling. Source and privileged mechanics
metadata are separate inputs. Report exact versions, assistance and filtering.

Studio data/tools are MIT-licensed. NVIDIA-derived recordings and renderings
retain Apache-2.0, upstream copyright and relevant notices. The root MIT license
does not replace third-party rights. This independent project has no NVIDIA
or ARC Prize endorsement.
