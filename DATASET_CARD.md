# Dataset card

## Contents

ARC3 Synthetic Games 1.0.3 contains one current version of each SG01–SG30 game:
30 native Python environments with seven fixed levels each, 210 levels in total.
Observations use the native 64×64 grid and 16-color ARC3 palette. Depending on
the environment, actions use arrows, Space, clicks and Undo. Exact action masks
are provided by the native engine.

The release contains native source/metadata, a checksum catalog, local and browser players,
30 initial-board previews and six anonymous human-played GIF excerpts. It contains
no raw human trajectories, historical replacements, generation pipeline,
learning scripts, private solution witnesses or official ARC3 game sources.

## Design and intended use

These synthetic environments were developed through AI-assisted programming,
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

`catalog.json` is the release inventory. Each entry binds a stable SG identifier,
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
3.12 runtime above for reproducible SDK experiments. Release 1.0.3 changes no
native game versions or file hashes from 1.0.0.

Use exact native IDs and release hashes when reporting results. Changes to
mechanics require a new game version and release inventory; this release remains
an immutable reference. All 30 environments are available without a prescribed
training split or sampling quota. Researchers choose and document their own
evaluation protocol.

## Validation and human data

Technical validation is documented in [VALIDATION.md](VALIDATION.md). Native
compatibility, level initialization, player behavior and data integrity are
distinct from human usability or proof that every level was solved by a human.
Human playtesting coverage is incomplete and is not asserted as full approval.

GIFs show excerpts from genuine human runs on the included versions, with reading
pauses shortened. They contain only game pixels and no personal labels, IDs or
timestamps. They are presentation assets, not a trajectory dataset. No human
action-efficiency baseline or official RHAE score is supplied or inferred.

## License and attribution

Original collection content is MIT-licensed, credited to ARC3 Synthetic Games
contributors. The engine and SDK are separate MIT-licensed dependencies of the
ARC Prize Foundation. This project is independently maintained and does not
claim ARC Prize endorsement. See the license and third-party notices.
