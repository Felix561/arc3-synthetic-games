# Synthetic ARC3: difficulty, controls and diversity

Analysis snapshot: 10 October 2026. Dataset inputs: released v2.0.0, source commit
[`86bdcda`](https://github.com/Felix561/arc3-synthetic-games/tree/86bdcda30ce9f21606146c0796671b07220a50e8).

[Read the interactive report](https://felix561.github.io/arc3-synthetic-games/analysis/).
[Download the offline report bundle (ZIP)](https://github.com/Felix561/arc3-synthetic-games/releases/download/v2.0.0/arc3-analysis-20261010.zip)
for the HTML, summary tables, figures and checksums.
Download `index.html` and open it directly for an offline copy. The HTML embeds
its charts, reviewed summary data and original presentation code. No account,
installation, server or internet connection is required to read it or export
embedded data. Reference links are optional outbound navigation.

## Scope and findings

The report covers 75 synthetic environments, 550 native levels, 555 recorded
level-attempt segments and 7,751 policy inputs. It compares Studio V1, Studio V2
and NVIDIA DreamTeam with aggregate statistics computed from 340 official public
human replays across 25 games.

Studio V1 and V2 have six-input median completed levels; NVIDIA has fifteen.
The official human reference has a 54-input median first completion, under a
different conditions. Synthetic actors could inspect source; humans
learned the rules. The counts do not identify an intrinsic difficulty ratio.
The report examines compact later paths, exact repeated recipes, control
semantics, visual structure and provisional mechanical families.

## Included files

| File | Contents |
| --- | --- |
| `index.html` | Self-contained interactive report, including all summary rows used by its charts |
| `summary.json` | Twenty-two explicitly selected summary tables, schema `arc3-synthetic-analysis/1` |
| `tables/*.csv` | The same tables as UTF-8 CSVs with header rows |
| `figures/*.png`, `figures/*.svg` | Sixteen independently generated statistical figures in raster and editable vector formats |
| `manifest.json` | SHA-256 inventory of the report, data, figures and notices |
| `LICENSE` | MIT notice for the original report code, narrative and independently drawn statistical graphics |

Every source table is an analysis product, not a replacement for the underlying
game/trajectory dataset. `progress.csv` contains only synthetic progression;
official data are limited to aggregate summaries. No official environment source,
game imagery, individual human replay paths or personal identifiers are included.
The recipe table contains game/level pairs and lengths, not solution actions.
Per-game assessments contain mechanic spoilers and subjective AI judgments.

## Rebuild

From the repository root, with Python 3.12:

```bash
python tools/build_analysis_report.py
```

The normal build uses Python's standard library and the checked-in summaries,
figures and project-authored template under `tools/report/`. It does not load
games, request an API, download software or require the original human archive.
It deterministically regenerates the HTML, CSVs and checksums.

To build a standalone report bundle, choose a new output filename:

```bash
python tools/build_analysis_report.py --archive dist/arc3-analysis-20261010.zip
```

The report bundle contains only the files listed above. It is independent of the
environment, trajectory and player packages; dataset release v2.0.0 remains the
frozen input version. The standard static-site build includes the report under
`analysis/`.

## Definitions and limitations

- Policy inputs are ACTION1–7, including blocked inputs and Undo. RESET controls,
  animation frames and model/tool operations are separate.
- Level length means a completed synthetic segment or a human first-completion
  visit. Whole human input totals also include unfinished work.
- V2 retains successful segments only; earlier synthetic partitions retain five
  interrupted NVIDIA segments. Collection completion fractions are not blind
  success probabilities.
- Per-game planning, discovery and decoding ratings are separate, source-informed
  1–3 ordinal judgments. They are not calibrated human difficulty or a composite
  score. Primary-family labels simplify hybrids.
- Nonmodal pixel share, palette size and edge share are image descriptors, not
  segmented object coverage, semantic novelty or perceptual difficulty.
- The analyzed official archive contains 340 plays/144 WINs. The official article
  reports 342/145; G50T accounts for the difference. No observations are imputed.
- No new human study, fresh game execution, optimality proof, random-resistance
  test or learner-training experiment was performed for the report.

The full methods and primary references are in the report. This analysis uses
AI assistance, with inspectable reductions and explicitly provisional qualitative
assessments. Dataset source exposure and licenses are described in
[the trajectory card](../TRAJECTORIES.md) and
[third-party notices](../../THIRD_PARTY_NOTICES.md). Engine licenses do not imply
redistribution rights for official competition environments.
