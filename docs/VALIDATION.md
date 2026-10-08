# Validation

The Studio catalog covers **50 games and 350 levels**, with one native
Python/metadata pair per exact version. Catalog and trajectory hashes bind
source bytes and normalized package metadata.

## Native runtime and player

The native compatibility pins are Python 3.12, arcengine 0.9.3, arc-agi 0.9.8 and
NumPy 2.5.3. Automatic checks cover offline SDK discovery, level initialization,
reset, representative actions, available controls, sessions and packaging.
Native execution belongs in isolation; secured checks use no network, read-only
mounts, an unprivileged user and resource limits.

Version 2.0.0 passed **105 isolated native/SDK/dataset tests** covering the
50 Studio games, plus **four server tests**. Technical validation is separate
from gameplay recording and visual/mechanical review. Reviews are
AI/source-informed inspection, not human approval.

## Browser preview

The browser runs the same native Studio files through Pyodide 314.0.7, Python 3.14,
NumPy 2.4.6 and Pydantic 2.12.5. Browser checks compare palette pixels, game state,
level counts, available actions and reset flags against native reference data.

The earlier 30-game collection's Edge/Chromium comparison covered 1,381
observations, including all 210 initial boards and representative actions, Undo,
reset and restart. This historical number describes that collection, not a
count for the expanded V2 browser.

Version 2.0.0 passed browser/native comparison for **all 50 games, 350 levels
and 2,325 exact native observations**, including every initial board and
representative transitions. The optional mechanics routes were checked for all
50 games. Checksum rejection and retry, keyboard controls, scaled clicks,
reset/restart, mobile layout and absence of gameplay uploads or persistent
browser storage also passed.

UI checks cover keyboard controls, scaled clicks, level selection, optional
explanations/GIFs and compact layouts. Runtime download hashes are checked.
Gameplay creates no recordings or persistent browser history. GitHub and the
runtime CDN receive ordinary asset requests.

## Release integrity

Release checks cover native identities, metadata structure, license notices,
documentation links, archive contents, credential patterns, personal paths and
unwanted internal files. The release passed **40 data-only tests**, **two nested
provenance/privacy-guard regressions** and **three publication-documentation tests**.
Media contain native game pixels without personal labels or identifying metadata.

Studio player/browser/environments-only packages exclude AI trajectory files,
private human recordings, generation tools and private solution witnesses.
NVIDIA source and support are separately packaged with retained upstream
licenses and notices. Public data use neutral identifiers and portable relative
paths; no private collection receipts or reasoning transcripts are distributed.

## Agent data

The original 55-game collection has 410 solved levels and five reset-interrupted
attempts. Fresh native replay compared every response and animation frame on the
exact packages and seed 0. It contains 6,011 policy actions, 6,071 responses and
6,784 frames. All original short/retry segments remain unchanged.

V2 adds 20 games, 140 successful level segments and 1,740 policy actions.
Fresh replay against the **cleaned public packages passed for all 20 V2 games**,
each reaching native WIN after seven levels. Across those runs, **1,760 responses
and 2,451 native frames** matched every recorded native field and all animation
frames, including action inputs, palette pixels, state, level progression and
available actions.

Public native files are
per-level successful response excerpts, including actual preceding observations;
they may share boundary responses and are not standalone full-game replays.
Its 140 excerpt files store 1,880 response lines and 3,189 frames, including
repeated boundaries. Canonical training rows count each successful segment once.

Content checks distinguish settled training observations, animation frames,
completed-level targets and next-level frames. They validate action order, legal
controls, click coordinates, completion boundaries and accounting.
Recording timestamps remain null. Reset controls are separate from policy
actions; Undo is included.

SHA-256 inventories permit data integrity checks without executing games.
The combined public collection has **555 attempts, 550 solved segments and 7,751
policy actions**. Collection labels are source-informed AI, never human.

## Reproduce

```bash
arc3-synthetic-games verify
python tools/load_dataset.py
python -m pytest -q
```

The first two commands read data. Tests execute game Python; use an isolated
development/CI environment. Browser checks are in `tools/check_browser.py`
and `.github/workflows/checks.yml`; native reference generation also requires
isolation.

These checks establish recorded paths and consistency. Complete solvability of
every possible state or seed, human discoverability, source-blind performance,
optimality, calibrated human efficiency and learner improvement are not verified.
