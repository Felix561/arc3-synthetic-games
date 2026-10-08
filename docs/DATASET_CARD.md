# Dataset card

## Contents

Version **2.0.0** contains 50 independently created Studio environments:
SG01–SG30 and V201–V220. Each has seven fixed levels, for 350 Studio levels.
The separate NVIDIA DreamTeam collection contains 25 unchanged synthetic games
with eight levels each. Together, the dataset covers **75 games and 550 levels**.

Observations use native 64×64 integer grids and the 16-color ARC3 palette.
Depending on the game, actions use arrows, Space, clicks and Undo. Native
available-action masks describe legal controls; advertised controls are not a
claim of equal use across the collection.

The local and browser players cover the 50 Studio games. They provide level
selection, native controls, initial-board previews and optional explanations.
They do not record or upload gameplay. NVIDIA code stays in its separately
attributed package, outside the Studio player catalog.

The agent dataset `arc3-source-informed-agent-v2.0.0` contains three partitions:

| Partition | Games | Levels | Recorded attempts | Solved / interrupted | Policy actions |
| --- | ---: | ---: | ---: | ---: | ---: |
| `studio` | 30 | 210 | 210 | 210 / 0 | 2,344 |
| `studio_v2` | 20 | 140 | 140 | 140 / 0 | 1,740 |
| `nvidia` | 25 | 200 | 205 | 200 / 5 | 3,667 |
| **Total** | **75** | **550** | **555** | **550 / 5** | **7,751** |

Twelve GIF excerpts show source-informed AI gameplay. Six separately labelled
GIFs show human gameplay on earlier Studio games. No raw human trajectories,
official ARC3 source/recordings, private journals, reasoning transcripts,
generation pipeline or learning scripts are included.

## Agent collection and assistance

Dedicated agents could read mechanics, level definitions and game source before
choosing legal actions in an isolated native runtime. They could inspect observed
states between action chunks. This is privileged agent experience, not human
data or a source-blind evaluation.

The requested model was GPT-6.1-sol. Earlier partitions requested ultra reasoning;
V201–V207 requested ultra; V208–V220 requested xhigh. Effective model identity and
per-action effort were not independently measured. The label describes collection
configuration, not verified model telemetry.

Some planning helpers remained visible in earlier source views; actors reported
non-use. SG18 received an additional read-only explanation of ordinary mechanics.
V2 actors also had source and design information. Replay verifies execution,
not the actor's reasoning or source blindness.
See [TRAJECTORIES.md](TRAJECTORIES.md) for assistance and exact-version bindings.

The original full game runs reached native WIN and passed fresh replay at their
recorded seed. Earlier partitions retain complete native recordings and all
recorded segments, including five reset-interrupted NVIDIA attempts. V2 contains
140 successful level segments and their native response excerpts; failures and
full audit histories are excluded. An excerpt is not an independently replayable
full-game file. Original complete V2 runs were replayed before excerpt export.

Canonical rows preserve settled palette observations and actions. Separate native
files retain response animation frames using lossless JSONL/gzip. Unknown recording
times remain null; GIF timing is presentation pacing, not measured latency.

## Design and intended use

The Studio games explore object continuity, containment, contact, spatial
relations, visible quantities, memory and goal-directed change. They are intended
for environment-model learning, planning, imitation learning, reasoning research
and play. Earlier designs received human feedback; full human playtesting is not
asserted for V2.

V2 uses an independently implemented functional construction scaffold inspired by
[NVIDIA DreamTeam](https://github.com/NVIDIA/dream-team/tree/main/arc_agi_3).
Public ARC3 games were consulted for abstract design references; their source and
trajectories are not redistributed.

Novelty and out-of-distribution difficulty are design intentions, not measured
guarantees. The dataset does not establish official benchmark equivalence,
population-calibrated human difficulty, contamination resistance or learner gains.
Source, explanations and GIFs reveal privileged information or solutions.
Keep them separate from ordinary observation inputs for blind evaluations.

## Versions and compatibility

`catalog.json` inventories the 50 Studio games. Each entry binds a stable display
ID, exact native game/version ID, source/metadata checksums, controls and preview.
`trajectories/manifest.json` inventories all three data partitions and their native
bindings. Existing Studio and NVIDIA partition identities are retained; V2 is an
added partition. No fixed train/test split is supplied.

The validated native dependency pins are Python 3.12, arcengine 0.9.3, arc-agi
0.9.8 and NumPy 2.5.3. They are compatibility pins, not promises about future SDKs.
Custom games use offline mode without an API key.

The browser preview uses Pyodide 314.0.7 (Python 3.14), arcengine 0.9.3 and
Pyodide's NumPy 2.4.6/Pydantic 2.12.5 builds. It is a convenience demo;
use pinned native Python for reproducible SDK experiments.

Exact source bytes and IDs matter. Do not substitute a different native revision
or seed for a saved recording. Metadata action baselines are not measured human
baselines for these synthetic environments.

## Validation and limitations

Automatic technical checks, native initialization and replay checks are distinct
from human approval. Saved successful paths establish those paths, not complete
solvability of all possible states or seeds. Source-blind performance, human
discoverability, optimality and generalization remain unverified.
See [VALIDATION.md](VALIDATION.md).

The six human GIFs contain only game pixels, with reading pauses shortened and
no personal labels or timestamps. They are presentation assets, not a human
trajectory dataset. No official human-efficiency or RHAE score is supplied.

## License and attribution

Studio environments, player, Studio data/renderings and project documentation
are MIT-licensed. NVIDIA game code, runtime support, NVIDIA-derived recordings
and renderings retain Apache-2.0 and applicable upstream notices.
The root MIT license does not replace third-party rights.

ARC Prize SDK/engine dependencies are separately MIT-licensed.
This independent project claims no NVIDIA or ARC Prize endorsement.
See [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md) and
[CITATION.cff](../CITATION.cff).
