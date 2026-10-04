# Validation

The Studio environment collection contains 30 games, 210 levels and 60 native source/metadata files.
Catalog IDs and SHA-256 hashes bind each game to its exact native version.
Release 1.1.0 preserves all native game files from 1.0.0.

## Native runtime and player

The validated runtime is Python 3.12, arcengine 0.9.3, arc-agi 0.9.8 and
NumPy 2.5.3. Source and installed-wheel suites passed 73 tests for release 1.0.2;
the current suite is rerun in CI. Checks cover offline SDK discovery, reset and
representative actions for all 30 games, initialization of all 210 levels,
action validation, independent player sessions, level selection and packaging.
Native validation runs in isolated development/CI environments. Container
checks use no network, read-only mounts, an unprivileged user and resource limits.

## Browser preview

The preview runs the same game files through Pyodide 314.0.7, Python 3.14,
NumPy 2.4.6 and Pydantic 2.12.5. Edge and CI Chromium checks matched 1,381
observations against the native runtime, including every pixel, state, level,
available action and reset flag. They cover all 210 initial boards and
representative actions, Undo, reset and restart.

UI checks include keyboard controls, scaled clicks, level selection, opt-in
explanations/GIFs and a 390-pixel layout. Corrupt runtime downloads are rejected
and can be retried. Gameplay sends no HTTP requests and uses no persistent
browser storage. GitHub and the runtime CDN receive ordinary asset requests.

## Release integrity

Release packages are checked for native file hashes, licenses, document links,
credentials, personal paths and unwanted internal files. The 31 PNGs and six
human-played GIFs contain only game pixels, without identifying media metadata.
The Studio player/browser/environments releases remain separate from the agent
trajectory dataset. Neither includes private human trajectories, the generation
pipeline or private solution witnesses. The repository additionally contains
NVIDIA's unchanged native packages with their original public source, including
upstream helper definitions, under their retained licenses.

## Source-informed agent recordings

The October 2 frozen collection contains 55 completed game runs: 30 Studio games
(210 levels) and 25 NVIDIA games (200 levels). All 55 saved runs passed independent
fresh replay to native WIN using Python 3.12.10, arcengine 0.9.3, arc-agi 0.9.8,
NumPy 2.5.3 and the pinned native packages/support. Replays compared every native
response and animation frame, not just final completion flags.

Independent content checks validated recorded action order, palette pixels,
click coordinates, the 355 measured old-level completion targets, resets and
segment accounting. The private collection has 6,011 policy actions, 6,071
responses and 6,784 native frames. Its 415 canonical segments include 410 solved
and five reset-interrupted attempts; all 103 short segments are retained.
Recorded timestamps remain null. Current-level resets are separate from policy
actions; native GAME_OVER was not observed in these recordings.

The public preparation preserves native recording bytes and gameplay content
while replacing private IDs/provenance with a public allowlist. Public inventories
bind the new compressed canonical files and retained exact native files.
The verification summary reports the saved replay evidence; preparing the public
package does not constitute new source-blind evaluation or human approval.
Public tools can verify checksums and record structure without executing games.

## Reproduce

```bash
arc3-synthetic-games verify
python -m pytest -q
```

The first command reads data only. The second executes native game code; use an
isolated development/CI environment. Browser checks are in `tools/check_browser.py`
and `.github/workflows/checks.yml`. Native reference generation also executes
game code and belongs in an isolated environment.

Recorded paths establish solvability for these exact packages and seed, while
human discoverability, source-blind performance, optimality, all-seed solvability
and calibrated human-efficiency baselines remain unverified.
