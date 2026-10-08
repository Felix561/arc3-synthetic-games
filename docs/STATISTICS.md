# Agent dataset statistics

Snapshot: **`arc3-source-informed-agent-v2.0.0`**, recorded seed 0.
These are source-informed AI-agent demonstrations, not human trials,
source-blind results or official benchmark scores.

## Coverage and observed outcomes

| Measure | Studio | Studio V2 | NVIDIA DreamTeam | Total |
| --- | ---: | ---: | ---: | ---: |
| Games with recorded full-run solutions | 30 | 20 | 25 | 75 |
| Distinct levels | 210 | 140 | 200 | 550 |
| Public level-attempt segments | 210 | 140 | 205 | 555 |
| Solved segments | 210 | 140 | 200 | 550 |
| Reset-interrupted segments | 0 | 0 | 5 | 5 |
| Policy actions, including Undo | 2,344 | 1,740 | 3,667 | 7,751 |
| Click actions | 736 | 340 | 1,809 | 2,885 |
| Undo actions | 7 | 78 | 0 | 85 |
| Unique original-run responses | 2,374 | 1,760 | 3,697 | 7,831 |
| Unique original-run native frames | 2,912 | 2,451 | 3,872 | 9,235 |
| Short segments, fewer than 6 actions | 95 | 60 | 8 | 163 |

Each game has one completed source-informed agent run. Earlier Studio and NVIDIA
data retain recorded retries; V2 retains successful segments only. Its private
failed attempts and full audit histories are outside the public collection.
Consequently, combined completion fractions do not estimate a model success rate.

The five public interrupted segments occurred in NE4172 and TD4826. They ended
at current-level resets with native state `NOT_FINISHED`, not `GAME_OVER`.
They are five interrupted attempts, not five failed games.

Public segment completion is **550 / 555 (99.1%)**, and every included game has a
recorded successful path through its levels. These counts describe a deliberately
completed, source-informed collection with distinct retention policies.
No measured human baseline or efficiency score is supplied.

## Action-count distributions

All public attempts, including the five interrupted ones, contribute to these
lengths. Resets are controls, not policy actions; Undo and blocked moves count.

| Policy actions per segment | Studio | Studio V2 | NVIDIA DreamTeam | Total |
| --- | ---: | ---: | ---: | ---: |
| Minimum | 1 | 1 | 2 | 1 |
| Median | 6 | 6 | 15 | 10 |
| Mean | 11.2 | 12.4 | 17.9 | 14.0 |
| Maximum | 86 | 166 | 78 | 166 |

![Recorded policy actions per level attempt, separated by collection](../media/trajectory-stats/action-distribution.svg)

<sub><b>Figure 1.</b> Recorded action lengths for 210 Studio, 140 Studio V2 and 205 NVIDIA attempts. All 555 public attempts are included. Five NVIDIA attempts ended at reset; V2 is a successful-segment-only collection.</sub>

<sub><b>Interpretation.</b> Descriptive lengths of source-informed AI experience. They are not human baselines, minimum solutions or calibrated game difficulty. Presentation timing, tokens and solver compute are not actions.</sub>

![Minimum, median and maximum recorded attempt lengths by game](../media/trajectory-stats/actions-by-game.svg)

<sub><b>Figure 2.</b> Each row shows one game's observed minimum, median and maximum attempt length. Studio games have seven solved levels; NVIDIA games have eight, with five interrupted attempts retained across its collection.</sub>

<sub><b>Interpretation.</b> Ranges are observed lengths, not confidence intervals. Long sequences can contain exploration, blocked actions and Undo. Length alone does not establish reasoning depth or necessary work.</sub>

## Per-game and per-level data

The [per-game CSV](../trajectories/per-game.csv) covers all 75 games with
attempts, outcomes, total actions and min/median/mean/max lengths.
The [per-segment CSV](../trajectories/per-segment.csv) covers 555 public
source/game/level/attempt identities and outcome flags.
Neither CSV contains palette frames or private actor identifiers.

[Machine-readable statistics](../trajectories/statistics.json) provide definitions
and native-storage counts. A native response can contain multiple animation
frames. Earlier partitions preserve complete game recordings; V2 native files
are successful per-level excerpts whose boundary responses can overlap.
V2's 140 excerpt files store 1,880 response lines and 3,189 frames, including
repeated boundaries. These storage counts must not be confused with its 1,760
unique original-run responses and 2,451 frames. They are not extra episodes.

Recording times were not measured and remain null. Duration, latency and cost
statistics are unavailable.

## Per-game inventory

Median and range describe actions per public level-attempt segment, not full-game
length or optimal solutions.

### Studio - SG01-SG30

| Game | Attempts | Solved / unsolved | Total actions | Median | Min-max |
| --- | ---: | ---: | ---: | ---: | ---: |
| SG01 | 7 | 7 / 0 | 355 | 51 | 6-86 |
| SG02 | 7 | 7 / 0 | 83 | 8 | 2-26 |
| SG03 | 7 | 7 / 0 | 19 | 2 | 1-5 |
| SG04 | 7 | 7 / 0 | 40 | 4 | 2-14 |
| SG05 | 7 | 7 / 0 | 23 | 3 | 2-5 |
| SG06 | 7 | 7 / 0 | 39 | 4 | 4-8 |
| SG07 | 7 | 7 / 0 | 68 | 8 | 1-20 |
| SG08 | 7 | 7 / 0 | 63 | 10 | 1-15 |
| SG09 | 7 | 7 / 0 | 189 | 31 | 6-38 |
| SG10 | 7 | 7 / 0 | 60 | 10 | 2-15 |
| SG11 | 7 | 7 / 0 | 67 | 9 | 2-18 |
| SG12 | 7 | 7 / 0 | 81 | 10 | 6-19 |
| SG13 | 7 | 7 / 0 | 120 | 16 | 2-38 |
| SG14 | 7 | 7 / 0 | 154 | 17 | 2-49 |
| SG15 | 7 | 7 / 0 | 29 | 4 | 1-8 |
| SG16 | 7 | 7 / 0 | 23 | 3 | 1-6 |
| SG17 | 7 | 7 / 0 | 100 | 12 | 2-34 |
| SG18 | 7 | 7 / 0 | 106 | 7 | 1-33 |
| SG19 | 7 | 7 / 0 | 44 | 5 | 1-14 |
| SG20 | 7 | 7 / 0 | 52 | 7 | 1-16 |
| SG21 | 7 | 7 / 0 | 35 | 6 | 1-8 |
| SG22 | 7 | 7 / 0 | 53 | 7 | 1-16 |
| SG23 | 7 | 7 / 0 | 31 | 4 | 1-8 |
| SG24 | 7 | 7 / 0 | 199 | 31 | 12-44 |
| SG25 | 7 | 7 / 0 | 53 | 4 | 1-21 |
| SG26 | 7 | 7 / 0 | 29 | 4 | 1-8 |
| SG27 | 7 | 7 / 0 | 84 | 8 | 2-25 |
| SG28 | 7 | 7 / 0 | 55 | 5 | 2-26 |
| SG29 | 7 | 7 / 0 | 66 | 7 | 3-19 |
| SG30 | 7 | 7 / 0 | 24 | 3 | 1-7 |


### NVIDIA DreamTeam - 25 synthetic games

| Game | Attempts | Solved / unsolved | Total actions | Median | Min-max |
| --- | ---: | ---: | ---: | ---: | ---: |
| AL7306 | 8 | 8 / 0 | 174 | 21 | 9-37 |
| CC2048 | 8 | 8 / 0 | 158 | 20 | 16-21 |
| CG1842 | 8 | 8 / 0 | 177 | 21 | 15-33 |
| CL0426 | 8 | 8 / 0 | 74 | 10 | 6-12 |
| DF4821 | 8 | 8 / 0 | 182 | 22 | 14-38 |
| DL4827 | 8 | 8 / 0 | 226 | 29 | 12-37 |
| FL5273 | 8 | 8 / 0 | 200 | 23 | 9-48 |
| FW4821 | 8 | 8 / 0 | 79 | 9 | 8-15 |
| GC4721 | 8 | 8 / 0 | 119 | 15 | 7-21 |
| HR2048 | 8 | 8 / 0 | 124 | 15.5 | 10-19 |
| LL4821 | 8 | 8 / 0 | 118 | 15 | 8-22 |
| MA4173 | 8 | 8 / 0 | 111 | 13.5 | 10-19 |
| MB2741 | 8 | 8 / 0 | 112 | 15 | 10-17 |
| ML2048 | 8 | 8 / 0 | 128 | 14.5 | 8-23 |
| MT4926 | 8 | 8 / 0 | 93 | 10 | 6-20 |
| NE4172 | 9 | 8 / 1 | 373 | 51 | 15-76 |
| OS1842 | 8 | 8 / 0 | 61 | 7.5 | 4-10 |
| PS1842 | 8 | 8 / 0 | 63 | 6.5 | 2-14 |
| PS7413 | 8 | 8 / 0 | 345 | 40.5 | 8-78 |
| RL2048 | 8 | 8 / 0 | 130 | 14 | 10-24 |
| RS0427 | 8 | 8 / 0 | 133 | 13.5 | 8-37 |
| SF2048 | 8 | 8 / 0 | 102 | 12.5 | 7-21 |
| SL4821 | 8 | 8 / 0 | 52 | 6.5 | 3-9 |
| SS6041 | 8 | 8 / 0 | 145 | 19 | 13-21 |
| TD4826 | 12 | 8 / 4 | 188 | 14.5 | 5-37 |

### Studio V2 — V201–V220

| Game | Attempts | Solved / interrupted | Total actions | Median | Min–max |
| --- | ---: | ---: | ---: | ---: | ---: |
| V201 | 7 | 7 / 0 | 35 | 4 | 3–9 |
| V202 | 7 | 7 / 0 | 36 | 5 | 2–9 |
| V203 | 7 | 7 / 0 | 35 | 4 | 3–10 |
| V204 | 7 | 7 / 0 | 162 | 21 | 3–48 |
| V205 | 7 | 7 / 0 | 154 | 21 | 4–45 |
| V206 | 7 | 7 / 0 | 45 | 8 | 1–10 |
| V207 | 7 | 7 / 0 | 29 | 4 | 2–7 |
| V208 | 7 | 7 / 0 | 58 | 7 | 1–17 |
| V209 | 7 | 7 / 0 | 29 | 4 | 2–7 |
| V210 | 7 | 7 / 0 | 35 | 5 | 2–10 |
| V211 | 7 | 7 / 0 | 16 | 1 | 1–6 |
| V212 | 7 | 7 / 0 | 33 | 3 | 3–9 |
| V213 | 7 | 7 / 0 | 34 | 5 | 3–8 |
| V214 | 7 | 7 / 0 | 89 | 16 | 2–21 |
| V215 | 7 | 7 / 0 | 105 | 12 | 4–40 |
| V216 | 7 | 7 / 0 | 109 | 17 | 1–38 |
| V217 | 7 | 7 / 0 | 133 | 23 | 4–28 |
| V218 | 7 | 7 / 0 | 181 | 31 | 3–47 |
| V219 | 7 | 7 / 0 | 152 | 16 | 6–49 |
| V220 | 7 | 7 / 0 | 270 | 9 | 2–166 |


## Definitions and interpretation

- **Game run:** a source-informed session through one exact game version.
- **Level:** a distinct source/game/level identity, independent of retries.
- **Attempt / segment:** a nonempty sequence on one level ending at completion
  or reset. The reset itself is outside its policy-action sequence.
- **Solved segment:** `is_solved=true`; 475 end with `level_solved` and 75 with `win`.
- **Interrupted segment:** one of five NVIDIA attempts with
  `is_truncated=true`, `is_terminal=false` and
  `terminal_reason=native_level_reset`.
- **Policy action:** native IDs 1–7. Reset ID 0 is a control; Undo ID 7 is a policy action.
- **Short segment:** fewer than six policy actions, retained without a length filter.
- **V2 excerpt:** native responses from a successful level, plus its actual preceding
  observation; not an independently replayable complete game.

The presentation draws on ARC Prize's
[Measuring Human Performance on ARC-AGI-3](https://arcprize.org/blog/arc-agi-3-human-dataset).
Its human protocol and action-efficiency baselines differ from these privileged
synthetic demonstrations. No official human data, figures or scores are copied.

For collection assistance, formats and licenses, see [TRAJECTORIES.md](TRAJECTORIES.md).
