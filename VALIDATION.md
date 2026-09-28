# Release validation

Version 1.0.0 was checked on 2026-09-28 with Python 3.12, arcengine 0.9.3,
arc-agi 0.9.8 and NumPy 2.5.3.

## Data and native compatibility

- The inventory contains exactly SG01–SG30, one current native version each:
  60 source/metadata files and 210 fixed levels.
- Catalog identities and SHA-256 checksums match the included files.
- All 30 environments were discovered, reset and stepped through the official
  SDK in offline mode, without a Studio adapter.
- All 210 levels were selected and initialized through the player; available
  actions, representative inputs, current-level resets and independent sessions
  were checked.
- Two development-only module strings were replaced by neutral comments.
  Executable Python syntax trees are unchanged; the other 58 native files
  retain their original bytes.

## Player and installation

The test suite passed **69 tests**, both from the source checkout and from an
installed wheel. Native execution took place in a network-isolated, read-only,
unprivileged container with limited resources and no credentials or user data.

An installed wheel also passed a real local HTTP server startup check, including
catalog retrieval, game creation, level selection, actions, reset, restart and
packaged preview retrieval. Windows wheel installation and the data-only
`verify`, `list` and module entry points were checked outside the source tree.

A headless Edge browser exercised the real player against that isolated native
backend. Checks covered all 30 gallery cards and their previews, arrow keys,
Space, Undo, automatic native level progression, level 7 selection, current-level
reset, whole-game restart, keyboard focus, scaled click coordinates, opt-in
mechanics explanations, on-demand GIF loading and a 390-pixel mobile layout.
No browser JavaScript errors were observed. Gallery and player screenshots were
visually inspected.

There was one dependency deprecation warning concerning the test client's HTTP
transport. It did not affect the passing tests or the installed HTTP server.

## Presentation and privacy

All 30 previews were rendered from the included native versions. The six GIFs
were made from genuine recorded play on those versions. They are 10–21-second
excerpts showing game pixels only, with reading pauses shortened. Media metadata
was inspected for identifying fields.

The release was audited for personal names, local paths, credentials, private
logs, raw trajectories, solution witnesses and Studio/generation dependencies.
Git history starts with a fresh, neutral contributor identity.

## Limits of these checks

These are technical and presentation checks, not a new full human playthrough
of every level. They do not establish population difficulty, official human
efficiency baselines, universal solvability or complete human approval.

For reproducible checks, use the pinned runtime and run:

```bash
arc3-synthetic-games verify
python -m pytest -q
```

The second command executes native Python; use an isolated development/CI
environment.
