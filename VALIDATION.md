# Validation

The collection contains 30 games, 210 levels and 60 native source/metadata files.
Catalog IDs and SHA-256 hashes bind each game to its exact native version.
Release 1.0.3 preserves all native game files from 1.0.0.

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
The releases include no raw trajectories, generation pipeline or solution files.

## Reproduce

```bash
arc3-synthetic-games verify
python -m pytest -q
```

The first command reads data only. The second executes native game code; use an
isolated development/CI environment. Browser checks are in `tools/check_browser.py`
and `.github/workflows/checks.yml`. Native reference generation also executes
game code and belongs in an isolated environment.

These checks do not prove complete solvability of every level or establish
calibrated human-efficiency baselines.
