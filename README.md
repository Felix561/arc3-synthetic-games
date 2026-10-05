# ARC3 Synthetic Games & Agent Trajectories

**30 independently created synthetic games · 55 games with agent demonstrations · 410 recorded level solves**

Abstract, turn-based ARC3-compatible games and compact source-informed AI-agent
trajectories for studying environment models, planning and learning.

**[Play the 30 Studio games](https://felix561.github.io/arc3-synthetic-games/)** ·
[Game index](docs/GAMES.md) · [Trajectory format](docs/TRAJECTORIES.md) ·
[Statistics](docs/STATISTICS.md) · [Player releases](https://github.com/Felix561/arc3-synthetic-games/releases/latest)

<table>
<tr>
<td><img src="media/agent-demos/studio/sg07-level-07.gif" width="180" alt="Studio SG07 level 7, recorded source-informed AI-agent solution"></td>
<td><img src="media/agent-demos/studio/sg18-level-07.gif" width="180" alt="Studio SG18 level 7, recorded source-informed AI-agent solution"></td>
<td><img src="media/agent-demos/studio/sg24-level-06.gif" width="180" alt="Studio SG24 level 6, recorded source-informed AI-agent solution"></td>
<td><img src="media/agent-demos/studio/sg25-level-07.gif" width="180" alt="Studio SG25 level 7, recorded source-informed AI-agent solution"></td>
</tr>
<tr>
<td align="center"><sub>Studio SG07 · level 7</sub></td>
<td align="center"><sub>Studio SG18 · level 7</sub></td>
<td align="center"><sub>Studio SG24 · level 6</sub></td>
<td align="center"><sub>Studio SG25 · level 7</sub></td>
</tr>
<tr>
<td><img src="media/agent-demos/nvidia/cc2048-level-07.gif" width="180" alt="NVIDIA CC2048 level 7, recorded source-informed AI-agent solution"></td>
<td><img src="media/agent-demos/nvidia/df4821-level-07.gif" width="180" alt="NVIDIA DF4821 level 7, recorded source-informed AI-agent solution"></td>
<td><img src="media/agent-demos/nvidia/ss6041-level-07.gif" width="180" alt="NVIDIA SS6041 level 7, recorded source-informed AI-agent solution"></td>
<td><img src="media/agent-demos/nvidia/fw4821-level-07.gif" width="180" alt="NVIDIA FW4821 level 7, recorded source-informed AI-agent solution"></td>
</tr>
<tr>
<td align="center"><sub>NVIDIA CC2048 · level 7</sub></td>
<td align="center"><sub>NVIDIA DF4821 · level 7</sub></td>
<td align="center"><sub>NVIDIA SS6041 · level 7</sub></td>
<td align="center"><sub>NVIDIA FW4821 · level 7</sub></td>
</tr>
</table>

<sub><b>AI-agent gameplay, with source access.</b> Eight complete solved-level excerpts; these previews reveal solutions. Playback timing is illustrative. Source, level, actions and provenance are in the <a href="media/agent-demos/manifest.json">media manifest</a>.</sub>

Play the Studio synthetic games, or use the trajectory dataset spanning Studio and
25 synthetic environments from
[NVIDIA DreamTeam](https://github.com/NVIDIA/dream-team/tree/main/arc_agi_3).
The two sources stay in separate, attributed partitions.

## What's included

| Source | Games | Levels | Recorded level attempts | Solved / unsolved | Policy actions |
| --- | ---: | ---: | ---: | ---: | ---: |
| [Studio](trajectories/studio) — SG01–SG30 synthetic games | 30 | 210 | 210 | 210 / 0 | 2,344 |
| [NVIDIA DreamTeam](trajectories/nvidia) — third-party synthetic games | 25 | 200 | 205 | 200 / 5 | 3,667 |
| **Total** | **55** | **410** | **415** | **410 / 5** | **6,011** |

Each game has one recorded agent run through all its levels. All 55 runs reached
native WIN and passed fresh replay on the exact package versions and recorded seed.
The five unsolved attempts were interrupted by current-level resets and are
retained. These counts describe this collected experience, not blind benchmark
performance, optimality or human-efficiency scores.

**These trajectories are AI-played, not human-played.** Dedicated Codex agents
could inspect mechanics and game source before choosing actions. The collection
configuration was **GPT-6.1-sol / ultra**; effective model
identity was not independently captured. Assistance and source-exposure limits
are documented in [the trajectory card](docs/TRAJECTORIES.md). All demonstrations were
collected for this project; NVIDIA authored its environments, not these agent runs.

## Download the dataset

**[Download all 55 synthetic environments and AI trajectories (ZIP)](https://github.com/Felix561/arc3-synthetic-games/releases/download/v1.1.2/arc3-synthetic-games-v1.1.2-dataset.zip)**

Extract into an empty folder and run `python tools/load_dataset.py`. No installation
is needed to read the data. The archive includes exact native game packages,
compact palette-grid training rows, Recorder-style native replays, checksums and
separate Studio/NVIDIA licenses. See [download and loading guide](docs/DOWNLOADS.md).

| Download | Contents |
| --- | --- |
| [Complete dataset](https://github.com/Felix561/arc3-synthetic-games/releases/download/v1.1.2/arc3-synthetic-games-v1.1.2-dataset.zip) | All 55 environments and their AI recordings |
| [Trajectories only](https://github.com/Felix561/arc3-synthetic-games/releases/download/v1.1.2/arc3-synthetic-games-v1.1.2-agent-trajectories.zip) | AI recordings, manifests and statistics; no game code |
| [Studio environments only](https://github.com/Felix561/arc3-synthetic-games/releases/download/v1.1.2/arc3-synthetic-games-v1.1.2-environments.zip) | 30 Studio games in native ARC3-compatible layout |
| [Source and player](https://github.com/Felix561/arc3-synthetic-games/releases/download/v1.1.2/arc3-synthetic-games-v1.1.2-source.zip) | Local player, code, data and documentation |

These are independent synthetic games, **not official ARC Prize training games**.
Native replay envelopes follow the Recorder style; segmented training rows use our
[documented schema](docs/TRAJECTORIES.md), so check your loader's field expectations.

## Use the trajectory data

The two partitions contain 415 segments in total. Load both for the complete dataset.

```python
import gzip
import json
from pathlib import Path

for source in ("studio", "nvidia"):
    path = Path("trajectories") / source / "trajectories.jsonl.gz"
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        for line in stream:
            episode = json.loads(line)
            # Palette observations: [actions + 1, 64, 64], integer values 0–15.
            observations = episode["observations"]
            actions = episode["actions"]
            solved = episode["is_solved"]
```

Canonical rows contain observations, actions, valid-action information and
outcome flags. Native per-game recordings additionally preserve every animation
frame in the ARC Prize Recorder-style `timestamp` / `data` JSONL envelope.
Everything is losslessly gzip-compressed; RGB images are not the training format.
Unknown recording times remain `null`.

Start with [TRAJECTORIES.md](docs/TRAJECTORIES.md) for loading, resets, coordinate
conventions, provenance and license scope. [Machine-readable statistics](trajectories/statistics.json)
and CSVs support independent analysis. The player wheel and environments-only
release contain only Studio content; use this repository or the separate
trajectory archive for the agent data and NVIDIA dependencies.

## Explore the statistics

![Actions per recorded level attempt, separated by source](media/trajectory-stats/action-distribution.svg)

<sub><b>Figure 1.</b> Policy-action counts in five-action bins, on common scales: Studio has 210 attempts (median 6 actions); NVIDIA has 205 (median 15). All 415 attempts are included: 410 solved and five reset-interrupted. Reset controls are counted separately.</sub>

<sub><b>Interpretation.</b> One source-informed AI-agent run per game, with retries retained. These are descriptive action lengths, not blind success rates, human-efficiency scores or optimal solution lengths.</sub>

The [statistics page](docs/STATISTICS.md) includes per-game attempts, outcomes, total
actions and segment-length distributions.

## Play locally

Use **Python 3.12**. From this repository, or an extracted Studio source release:

```bash
python -m pip install -e .
arc3-synthetic-games play
```

The browser opens at **http://127.0.0.1:8780**. No Docker, API key, account or
internet connection is needed to play after installation. Select any of the
seven levels, reset a level, or restart a game. Controls are arrows, Space,
clicking and Undo (`Z`), depending on the game.

```bash
arc3-synthetic-games play --port 8781 --no-browser
arc3-synthetic-games verify
arc3-synthetic-games list
```

The local and GitHub Pages players currently cover **Studio's 30 games**.
Mechanics explanations and human gameplay GIFs are opt-in. Gameplay stays in
memory; neither player records or uploads actions.

The browser demo runs the native Python games through WebAssembly, without an
account or API key. Its first runtime download needs internet access. GitHub and
the runtime CDN handle ordinary asset requests under their own privacy policies.

## Use the native environments

Studio's `environment_files/` uses the public ARC3 package arrangement: one
game/version directory with Python source and `metadata.json`. Use exact IDs and
hashes in `catalog.json`; the trajectory manifest binds the same native versions.
For reproducible native use, the validated dependencies are:

```bash
python -m pip install arc-agi==0.9.8 arcengine==0.9.3 numpy==2.5.3
```

```python
import json
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

with open("catalog.json", encoding="utf-8") as file:
    catalog = json.load(file)
arcade = Arcade(operation_mode=OperationMode.OFFLINE,
                environments_dir="environment_files")
game = arcade.make(catalog["games"][0]["game_id"], seed=0, save_recording=False)
observation = game.reset()
observation = game.step(GameAction.ACTION1)
```

NVIDIA's unchanged packages are separate under
[`third_party/nvidia/environment_files/`](third_party/nvidia/environment_files).
Their pinned runtime support, upstream revision, checksums and licenses are
included; they have **eight levels**, rather than Studio's seven. See the
[NVIDIA setup](docs/TRAJECTORIES.md#nvidia-environments) before replaying them.
Native code executes Python; run unfamiliar environments in isolation.

## Validation and limitations

Recorded trajectories were independently replayed to native WIN for all 55 exact
game versions and seed 0. Pixel/action alignment, completion boundaries, retries
and dataset accounting were checked. [Validation](docs/VALIDATION.md) distinguishes
this evidence from player compatibility and human playtesting.

The dataset is small and source-informed, with one actor per game. It does not
measure source-blind exploration, human discoverability, optimal solutions,
all-seed solvability or generalization. Official ARC3 human baselines and scores
are not supplied. Keep source, mechanics and provenance out of a learner's
observation inputs unless deliberately studying privileged information.

## Development and hosting

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
python tools/build_preview.py  # Static Studio site in _site/
```

Native tests execute game Python; run them in an isolated development/CI
environment. Data-only trajectory checks do not require executing games.
[Publishing instructions](docs/PUBLICATION.md) describe package scopes and GitHub Pages.

## License and citation

Original Studio games, player, documentation, Studio agent data and original
presentation assets are [MIT-licensed](LICENSE). NVIDIA game code, runtime support,
NVIDIA-based agent recordings and derived presentation assets are distributed
with [Apache-2.0 and applicable retained third-party notices](third_party/nvidia/LICENSE).
The repository's MIT license does not replace NVIDIA's license or attribution.
See [third-party acknowledgments](THIRD_PARTY_NOTICES.md) and [CITATION.cff](CITATION.cff).

This is an independent research dataset, with no NVIDIA or ARC Prize endorsement.
No official ARC3 environments or human trajectory dataset are redistributed.

## AI disclosure

AI assisted the design, implementation and documentation of the Studio games,
with human feedback and playtesting. The trajectory dataset and eight agent replay
GIFs show **source-informed AI-agent gameplay**. The six human gameplay GIFs are
labelled separately; no raw human trajectories are included.
