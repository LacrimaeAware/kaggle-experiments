# UMUD results ledger

Recorded comparisons through 2026-07-01. Lower public scores are better; local diagnostic metrics are identified separately.

## Best score

**Recorded public best: `0.45615`** = fascicle mask threshold 0.30 with apo at the default 0.50
(`results/submission_thr_a0.50_f0.30.csv`, 2026-07-01). The threshold submissions were generated on the
old `0.46041` lineage by `benchmark_lab/generate_threshold_sweep.py`.

The threshold comparison was `0.45615` (fasc-only) < `0.45669` (apo 0.60 + fasc 0.30) < `0.47200` (apo-only
0.60/0.50). The lower fascicle threshold retained fainter mask fragments. The
apo/MT changes both worsened the anchor: MT x0.95 worsened the score (`0.53395`), and raising MT via a thinner apo mask
also lost (`0.47200`).

The documented one-run pipeline (`local_infer.py`, median FL) scored `0.47473`
(`submission_reproduced.csv`).

## Recorded leaderboard comparisons

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
| min_extrap_top3 FL (`submission_minextrap.csv`) | 0.49983 (higher error than median) |
| MT x0.95 on best (`submission_mtx095_on_best.csv`) | 0.53395 |
| FL x1.10 on best (`submission_flx110_on_best.csv`) | 0.48369 |

## In-distribution test gate (2026-07-01)

The diagnostic compared 23 hand-corrected test images (`results/correction_labels/`) with saved pipeline geometry. Normalized MAE contributions were 0.134 for aponeurosis fit (MT 0.262 and FL 0.104), 0.132 for fascicle rejection/addition and 0.008 for scale.

Its PA-shift recommendation produced this comparison:

- `submission_bandfix_flx105_paDown1.5.csv` (PA -1.5 on the 0.46041 file, FL/MT unchanged) scored
  **0.46686**, worse than `0.46041`.

The gate did not reliably predict leaderboard changes for broad PA/FL/MT calibration. The 23 hand-labels read systematically low in the recorded comparison. They remained useful for inspecting gross regressions and mask failures.

## Family stratification (2026-07-01)

The 309 test images were grouped by visible mask failure mode. The two largest groups involved aponeuroses:

- **Curved deep apo: 89/309 (29%)** - built as `UMUD_CURVED_APO=1`, but the routed family submission
  worsened the score (`submission_fam_curved.csv` -> `0.51435`). Following the actual curve moves away from the
  straight-line scoring convention.
- **Multi-band: 92/309 (30%)** - `USE_BAND_FIX` selects the adjacent aponeurosis bands containing the most fascicle centroids.

Recorded submissions on the `0.46041` base:

- `submission_fam_pos_weight.csv` -> `0.46314`
- `submission_fam_top_robusttri.csv` -> `0.48730`
- `submission_fam_curved.csv` -> `0.51435`

The tested geometry-family changes did not improve the 0.46041 anchor. The later 0.45615 result came from fascicle thresholding.

## Per-term diagnostics

- **Benchmark with true scale, no recenter** (`benchmark_validate.py` here scores any submission CSV against the same 7-rater consensus and human floor): PA 0.1505 (below the
  0.2445 rater disagreement), MT 0.0840 (at the 0.0810 reference), FL 0.5218 (reference 0.4026, over-reads +5.8 mm).
  The min_extrap variant scored 0.39 on the benchmark and 0.49983 publicly.
- **MT** is calculated from aponeurosis positions and pixel scale.
- **Scale**: 295/309 rows receive a ruler or device-family scale; 14 use the prior.

## Validation limits

The 35-image benchmark exposed measurement bugs but did not reliably rank submissions on the test distribution. The hand-corrected test diagnostic also failed to select the best global calibration. Model comparisons need subject or sequence grouping; random frame-level splits can mix related images across folds.
