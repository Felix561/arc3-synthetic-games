# ARC3 Synthetic Games

**30 independent games · 210 levels · native 64×64 ARC3 environments**

An open-source collection of abstract, turn-based games for human exploration
and reasoning-agent research. Each game has its own mechanics and seven fixed
levels. The collection uses the ARC3 engine and environment format; it is an
independent synthetic dataset, not an official ARC Prize benchmark.

![Six representative initial boards](media/overview.png)

## Play locally

Use **Python 3.12**. From this repository's directory:

```bash
python -m pip install -e .
arc3-synthetic-games play
```

The browser opens at **http://127.0.0.1:8780**. No Docker, API key, account or
internet connection is needed to play after installation. You can select any
of the seven levels, reset a level, or restart a game. Available controls are
arrows, Space, clicking and Undo (`Z`), depending on the game.

Mechanics explanations and human-played demonstrations are hidden until you
request them. Gameplay stays in memory: the player has no recorder, telemetry,
accounts or persistent action log. It executes the curated Python game sources
locally; it is not an execution sandbox or a service intended for public hosting.

```bash
arc3-synthetic-games play --port 8781 --no-browser
arc3-synthetic-games verify
arc3-synthetic-games list
# Equivalent module entry point:
python -m arc3_synthetic_games play
```

## Use the native environments

The `environment_files/` directory has the same native package arrangement as
public ARC3 environments: one game/version directory with Python source and
`metadata.json`. Copy that directory into an existing offline ARC3 project, or
use it directly with the official SDK. No player or custom Studio adapter is
required by the games.

For native-only use, install the validated dependencies on Python 3.12:

```bash
python -m pip install arc-agi==0.9.8 arcengine==0.9.3 numpy==2.5.3
```

From the repository directory:

```python
import json
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

with open("catalog.json", encoding="utf-8") as file:
    catalog = json.load(file)

arcade = Arcade(
    operation_mode=OperationMode.OFFLINE,
    environments_dir="environment_files",
)
game_id = catalog["games"][0]["game_id"]  # Exact SG01 native version
game = arcade.make(game_id, seed=0, save_recording=False)
assert game is not None
observation = game.reset()
observation = game.step(GameAction.ACTION1)
```

Use the exact `game_id` values in the catalog to bind experiments to this release.
The catalog supplies file SHA-256 hashes and human-facing descriptions; learner
inputs can remain limited to native observations and available actions. These
environments have no measured official human-efficiency baselines. SDK scorecard
values must not be interpreted as comparable official benchmark scores.

## Browse the collection

See [the game index](GAMES.md) for short discovery-first descriptions, and the
[dataset card](DATASET_CARD.md) for composition, validation and limitations.
Native metadata keeps the stable SG labels; descriptive titles live in the
catalog and player.

<details>
<summary>Show six human-played demonstrations — contains early-level spoilers</summary>

The following excerpts show real current-version gameplay. Only native game
pixels are included; pauses are shortened. Raw trajectories and identifying
recording metadata are not distributed.

| SG01 | SG06 | SG08 |
| --- | --- | --- |
| ![SG01 human gameplay](media/demos/sg01.gif) | ![SG06 human gameplay](media/demos/sg06.gif) | ![SG08 human gameplay](media/demos/sg08.gif) |

| SG24 | SG26 | SG28 |
| --- | --- | --- |
| ![SG24 human gameplay](media/demos/sg24.gif) | ![SG26 human gameplay](media/demos/sg26.gif) | ![SG28 human gameplay](media/demos/sg28.gif) |

</details>

## Development

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
```

Native tests execute game Python. Run them in an isolated development/CI
environment. No raw human trajectories or solutions are required by the tests.
Use `arc3-synthetic-games verify` for data-only integrity checks.

Original games, player, documentation and demonstration assets are available
under the [MIT license](LICENSE). The [official ARC-AGI toolkit](https://github.com/arcprize/ARC-AGI)
and ARC engine are separate dependencies; see [third-party acknowledgments](THIRD_PARTY_NOTICES.md).
Citation metadata is in [CITATION.cff](CITATION.cff).

## AI disclosure

This repository was created with substantial assistance from AI coding agents,
including game design, implementation, the local player and documentation.
Human feedback, gameplay and iterative review informed the collection. The GIF
demonstrations show actual human gameplay; they are not AI-generated playthroughs.
AI assistance and technical validation do not establish that every level has
been independently human-reviewed or that the collection is free of errors.
