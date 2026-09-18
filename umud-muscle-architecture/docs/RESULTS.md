# UMUD results ledger

Terse decision-driver, exported from the project's working state on 2026-09-17. Rule: a claim may
drive a decision only if it carries a code `file:line` or an exact leaderboard number. Everything else
is a hypothesis.

## Best score

**Confirmed public best: `0.45615`** = fascicle mask threshold 0.30 with apo at the default 0.50
(`results/submission_thr_a0.50_f0.30.csv`, 2026-07-01). The threshold submissions were generated on the
old `0.46041` lineage by `benchmark_lab/generate_threshold_sweep.py`.

Isolation is clean: `0.45615` (fasc-only) > `0.45669` (apo 0.60 + fasc 0.30) > `0.47200` (apo-only
0.60/0.50). So the July 1 win is **entirely** the fascicle threshold recovering faint fascicles. The
apo/MT knob is dead both ways: MT x0.95 lost hard (`0.53395`), and raising MT via a thinner apo mask
also lost (`0.47200`). Live leaderboard search is now one-dimensional: push the **fascicle**
binarization threshold lower at apo 0.50.

The reproducible one-run pipeline (`local_infer.py`, median FL) is still `0.47473`
(`submission_reproduced.csv`). Older docs that say `0.52570`, `0.55075`, or `0.46041` as the best are
stale.

## Leaderboard ledger (the only proven oracle)

| change | public |
|---|---:|
| scale router + inner-edge MT + fragment FL | 0.61918 |
| temporal smoothing | 0.60961 |
| shape-neighbor fallback scale | 0.58910 |
| PA +2.0 / +2.5 / +3.0 flat | 0.55075 / 0.55033 / 0.55168 |
| FL x1.05 on PA+2.5 | 0.52570 |
| family_b scale 134.5 -> 147 px/cm (41 rows) | ~0.488 |
| aponeurosis band fix | 0.46076 |
| band fix + FL x1.05 | 0.46041 |
| PA -1.5 on the 0.46041 file | 0.46686 (lost) |
| family route: pos-weight | 0.46314 (lost) |
| family route: top robust triangle | 0.48730 (lost) |
| family route: curved deep apo | 0.51435 (lost) |
| apo 0.60 only (`submission_thr_a0.60_f0.50.csv`) | 0.47200 (lost) |
| apo 0.60 + fasc 0.30 (`submission_thr_a0.60_f0.30.csv`) | 0.45669 |
| fasc 0.30 only (`submission_thr_a0.50_f0.30.csv`) | **0.45615** |
| median pipeline, one run (`submission_reproduced.csv`) | 0.47473 |
| min_extrap_top3 FL (`submission_minextrap.csv`) | 0.49983 (refuted) |
| MT x0.95 on best (`submission_mtx095_on_best.csv`) | 0.53395 |
| FL x1.10 on best (`submission_flx110_on_best.csv`) | 0.48369 |

Read this correctly:

- Global PA/FL/MT calibration on the `0.46041` lineage is already bracketed and spent.
- The threshold sweep is a different kind of lever: it changes **which fascicles exist** and where the
  lines sit, not just a column mean.
- The July 1 improvement is a fascicle-recall lever. The apo threshold is not the win.

## In-distribution test gate (2026-07-01)

First validation on the real test distribution: 23 hand-corrected test images
(`results/correction_labels/`) vs saved pipeline geometry, via a gate script kept in the private working repository.
Diagnosis (normalized MAE contribution): **aponeurosis fit is the #1 error source** (overall 0.134,
via MT 0.262 + FL 0.104); fascicle reject/add is #2 (0.132 combined); scale contributes 0.008. The
"scale is the master lever" idea is refuted.

The gate did produce one leaderboard probe, and it failed:

- `submission_bandfix_flx105_paDown1.5.csv` (PA -1.5 on the 0.46041 file, FL/MT unchanged) scored
  **0.46686**, worse than `0.46041`.

So the gate is **not** an LB predictor for broad PA/FL/MT calibration. The 23 hand-labels read
systematically low vs the hidden truth on all three terms. Use the gate to catch gross regressions and
to study mask failure modes, not to pick the next calibration submission.

## Family stratification (2026-07-01) - geometry on the 0.46041 lineage is closed

Stratified the 309 test images by self-evident mask failure mode
(stratification script and CSV kept in the private working repository). Two families dominate, both
aponeurosis-related:

- **Curved deep apo: 89/309 (29%)** - built as `UMUD_CURVED_APO=1`, but the routed family submission
  lost hard (`submission_fam_curved.csv` -> `0.51435`). Following the actual curve moves away from the
  straight-line scoring convention.
- **Multi-band: 92/309 (30%)** - audited inline. `USE_BAND_FIX` picks decisively and contains the
  fascicles. Not a lever.

Board-confirmed verdict on the old `0.46041` base:

- `submission_fam_pos_weight.csv` -> `0.46314`
- `submission_fam_top_robusttri.csv` -> `0.48730`
- `submission_fam_curved.csv` -> `0.51435`

So geometry itself is still closed on current evidence. The later move to `0.45615` did **not** come
from geometry; it came from fascicle thresholding. Practical rule:

- Do not spend slots on more geometry-family variants.
- Cheap live search = lower fascicle threshold at apo 0.50.
- Structural work = better OOD masks (retrain recipe kept in the private working repository), not more line-fitting tricks.

## Per-term truth (code + LB + benchmark grounded)

- **Benchmark with true scale, no recenter** (private benchmark scorer; `score_on_benchmark.py` scores the same benchmark with true scale): PA 0.1505 (below the
  0.2445 human floor), MT 0.0840 (at the 0.0810 floor), FL 0.5218 (floor 0.4026, over-reads +5.8 mm).
  This does **not** predict the leaderboard (min_extrap proved it again: benchmark 0.39, LB 0.49983).
- **MT is a clean scale probe**: it has no fascicle and no extrapolation and is at the human floor with
  true scale, so test MT error is mostly scale/aponeurosis foundation, not anatomy.
- **PA and FL are not tapped per-image.** Only their global means were nudged early. The current
  threshold win proves a per-image fascicle-existence lever was still live.
- **Scale**: 295/309 rows get a recovered px/mm; 14 fall back. Per-family detection is solid. Absolute
  per-image correctness is still unvalidated except where the author hand-read ticks.

## Validation discipline

1. The leaderboard is the only valid gate for global/calibration quantities, and it is
   distribution-specific.
2. The 35-image benchmark does **not** predict this leaderboard, even un-blinded. Use it to catch a
   measurement bug, not to decide a submission.
3. The only per-image test truth is the author's correction UI labels, and even that is not a safe
   oracle for global calibration.
4. For model/segmentation changes: GroupKFold by subject/device/muscle (recover sequence groups first).
   Never gate model changes on the benchmark or on visual plausibility alone.

## Plan

1. **Cheap board search:** keep the threshold ladder one-dimensional. Lower fascicle threshold below
   0.30 at apo 0.50, one isolated change at a time.
2. **Structural work, no leaderboard first:** run the train-mask error decomposition and keep the OOD
   augmentation path (retrain recipe kept in the private working repository) as the main mask-improvement branch.
3. **Decision discipline:** keep `results/submission_thr_a0.50_f0.30.csv` for final selection unless a
   later isolated submission beats `0.45615`.
