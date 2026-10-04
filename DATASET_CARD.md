# Dataset card

## Contents

Release 1.1.0 contains one current version of each SG01–SG30 game, unchanged from 1.0.3:
30 native Python environments with seven fixed levels each, 210 levels in total.
Observations use the native 64×64 grid and 16-color ARC3 palette. Depending on
the environment, actions use arrows, Space, clicks and Undo. Exact action masks
are provided by the native engine.

The Studio player release contains native source/metadata, a checksum catalog, local and browser players,
30 initial-board previews and six anonymous human-played GIF excerpts. It contains
no raw human trajectories, historical replacements, generation pipeline,
learning scripts, private solution witnesses or official ARC3 game sources.

This repository additionally provides the separately versioned
`arc3-source-informed-agent-20261002-v1` trajectory dataset: 55 source-informed
AI-agent runs across those 30 Studio games and 25 NVIDIA DreamTeam synthetic
games. It contains 415 level-attempt segments, 410 solved levels and 6,011 policy
actions. The two sources have separate compressed partitions, native version
bindings and license scopes. NVIDIA's 25 unchanged eight-level packages and
their required runtime support are under `third_party/nvidia/`, outside the
Studio player and its 30-game catalog. Eight additional GIF excerpts show actual
AI-agent experience. They are distinct from the older human GIF excerpts.

## Agent trajectory dataset

Dedicated agents could read mechanics and source before acting in a real native
runtime. This collection requested GPT-6.1-sol / ultra through an inherited Codex
session; effective per-action model metadata was not independently recorded.
It is privileged agent experience, not human data or a source-blind evaluation.
Some planning helpers remained visible in source views; actors reported non-use.
SG18 also received a read-only explanation of ordinary mechanics. See
[TRAJECTORIES.md](TRAJECTORIES.md) for the complete assistance statement.

All 55 game runs reached native WIN and passed independent fresh replay for the
exact native packages and seed 0. The five unsuccessful segments are genuine
reset-interrupted attempts, not native GAME_OVER events. All 103 segments shorter
than six actions are retained. Resets are separate controls; undo is a policy
action. The 55 native recordings retain every response/animation frame, using
64×64 integer palette grids and lossless JSONL gzip. Recording timestamps remain
null because timing was not captured. Public records exclude private actor IDs,
machine paths, collection credentials, journals and reasoning transcripts.

[Statistics](STATISTICS.md) describe coverage and action distributions. One
recorded actor per game and source access do not support estimates of human
discoverability, generalization, unbiased model success or official efficiency.
All data is available without a prescribed synthetic sampling quota. Keep source
and privileged metadata separate from ordinary learner observations.

## Design and intended use

The original Studio environments were developed through AI-assisted programming,
visual/mechanical inspection and iterative human playtesting. Designs draw on
abstract object, spatial, quantitative and causal relationships. They are meant
for exploration, environment-model learning, planning and reasoning research,
and for people to play.

Novelty and out-of-distribution difficulty are design intentions, not measured
guarantees. This collection has not established equivalence to the official ARC3
benchmark, difficulty calibration against a human population, or resistance to
training contamination. The native source is public and explains the mechanics;
blind evaluations should expose only frames and valid actions to the agent.
The optional descriptions and GIFs can reveal mechanics or early solutions.

## Versions and compatibility

`catalog.json` is the Studio environment inventory. Each entry binds a stable SG identifier,
an exact versioned native ID, source/metadata checksums, controls, preview and
optional demonstration. All descriptive titles are catalog aliases; native
metadata retains its original SG label. Two development-only module comments
were replaced with neutral comments, without changing executable mechanics.

The validated runtime is Python 3.12, arcengine 0.9.3, arc-agi 0.9.8 and
NumPy 2.5.3. This is a compatibility pin, not a claim of support for every future
SDK release. Custom environments are used in offline mode without an API key.

The optional browser preview uses Pyodide 314.0.7 (Python 3.14), arcengine 0.9.3
and Pyodide's NumPy 2.4.6/Pydantic 2.12.5 builds. It is a convenience demo, with
native-frame parity checks documented in VALIDATION.md. Use the pinned Python
3.12 runtime above for reproducible SDK experiments. Release 1.1.0 changes no
native game versions or file hashes from 1.0.0.

Use exact native IDs and release hashes when reporting results. Changes to
mechanics require a new game version and release inventory; this release remains
an immutable reference. `trajectories/manifest.json` separately binds the agent
dataset and NVIDIA packages; original environment files are not revised by this
addition. All 30 Studio environments are available without a prescribed
training split or sampling quota. Researchers choose and document their own
evaluation protocol.

## Validation and human data

Technical validation is documented in [VALIDATION.md](VALIDATION.md). Native
compatibility, level initialization, player behavior and data integrity are
distinct from human usability or proof that every level was solved by a human.
Human playtesting coverage is incomplete and is not asserted as full approval.

The six older GIFs in `media/demos/` show genuine human runs on the included versions, with reading
pauses shortened. They contain only game pixels and no personal labels, IDs or
timestamps. They are presentation assets, not the agent trajectory dataset. New
GIFs in `media/agent-demos/` show AI-agent level attempts at presentation-paced
timing and identify their native game/version and level. No human
action-efficiency baseline or official RHAE score is supplied or inferred.

## License and attribution

Original Studio environments, player, Studio recordings/renderings and project
tools/documentation are MIT-licensed, credited to ARC3 Synthetic Games
contributors. NVIDIA's environment code, support, NVIDIA-derived recordings and
renderings are distributed separately with Apache-2.0 and retained applicable
third-party notices. The root MIT license does not replace these rights.
The engine and SDK are separate MIT-licensed dependencies of the ARC Prize
Foundation. This project claims neither NVIDIA nor ARC Prize endorsement.
See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for exact source attribution.
