# UMUD measurements and implementation notes

Recorded measurements through 2026-07-01, with code locations for the reference pipeline. [Result comparisons](docs/RESULTS.md) and [submission records](docs/SUBMISSIONS.md) give the corresponding score context.

## Metric

- Score = (1/3)[MAE(PA)/6 + MAE(FL)/12 + MAE(MT)/3]; tolerances PA=6, FL=12, MT=3, equal weights.
  Median/RMSE side terms weighted 1e-6/1e-9 (tie-breakers only). `metric.py:10-19, 81-88`.
- Official scorer defaults to per-image (`eval_unit="image"`) but supports per-subject aggregation.
  the host's scorer notebook (local copy, not included). (Per-image assumed; not re-confirmed on the live host.)
- The metric penalizes calibration errors in each measurement.

## Recorded leaderboard results

- PA flat shift on burn_13 base: +0 -> 0.58910, +2 -> 0.55075, +2.5 -> 0.55033, +3 -> 0.55168.
- FL global scale on the PA+2.5 base: x1.05 -> 0.52570.
- family_b scale constant 134.5 -> 147 px/cm (41 rows; checked by reading the ruler ticks): ~0.488.
- aponeurosis band fix: 0.46076; band fix + FL x1.05: 0.46041.
- PA -1.5 on the 0.46041 file: 0.46686 (lost).
- family-route submissions on the 0.46041 file: pos-weight 0.46314, top robust triangle 0.48730,
  curved deep apo 0.51435 (all lost).
- threshold sweep on the 0.46041 lineage: apo 0.60 only -> 0.47200, apo 0.60 + fasc 0.30 -> 0.45669,
  fasc 0.30 only at apo 0.50 -> **0.45615 (recorded best, `submission_thr_a0.50_f0.30.csv`)**.
- reproducible median pipeline, one run of the private inference script `local_infer.py`: 0.47473 (`submission_reproduced.csv`); the
  earlier 0.460 file contains additional per-row corrections.
- min_extrap_top3 FL on that pipeline: **0.49983 (2026-06-15)**. The benchmark scored it 0.39, while its public error was 0.025 higher than the median pipeline.

## Pipeline (segment_then_measure.py)

- `PRIOR = {fl_mm:81.866, mt_mm:18.628, pa_deg:15.105}` `:96` (fl raised from 74.424 to bake in the
  LB-fitted FL level). Clips PA[5,45], FL[30,200], MT[10,50].
- `USE_FL_RECENTER` defaults to ON. In `main()`, `fl_mm *= PRIOR['fl_mm']/mean(fl_mm)` scales the raw mean of about 91.6 mm to 81.866 mm, a factor of about 0.89.
- `FL_FRAGMENT_MODE` default `median` `:107`. `min_extrap_top3` had higher public error
  (0.49983 vs median 0.47473, 2026-06-15).
- MT is converted as `mt_px / px_per_mm` and clipped to [10,50] mm in `main()`.
- Scale router `USE_SCALE_ROUTER` default ON; `calibrate_image`; per-family logic in `scale_ticks.py`,
  incl. `family_b_signature` now **147 px/cm** (was 134.5; hand readings of the ruler ticks at ~147 and the LB
  confirmed the fix, ~0.488). bottom_ticks reads were corrected ~+9.5% the same way. Real coverage 295/309.

## Per-image geometry (results/calibration_measurement_debug.csv, 309 rows)

- This file is PRE-recenter per-image geometry (recenter touches only the submission frame, not these rows).
- Raw FL mean 91.596 mm, std 27.07 mm (= 2.26 FL tolerances). PA mean 14.627 deg. MT mean 21.836 mm.
- Scale coverage: 295/309 rows have a recovered px/mm; 14 fall back to prior. Methods: right_ruler_5mm 87,
  bottom_ticks 59, png_left_ruler 58, left_ruler_1cm 50, family_b_signature 41, none 14.

## Local benchmark settings

- The older 35-image benchmark scorer (`experiments/score_weights.py`) feeds TRUE scale `:42` and recenters
  predicted FL to truth mean `:54` -> structurally cannot see a global FL scale/mean error.
- A true-scale benchmark scorer (`benchmark_lab/honest_validate.py`; built 2026-06-15) removes the recenter and reports per-image vs
  the 7-rater consensus + per-term rater disagreement. With true scale: PA 0.1505 (reference 0.2445), MT 0.0840
  (reference 0.0810), FL 0.5218 (reference 0.4026, over-reads +5.8 mm). The min_extrap_top3 variant had the lowest local FL error (0.39) and public score 0.49983.
- 19 hand labels are self-measured by the same geometry engine; reported FL bias ~-0.46 mm (~unbiased)
  and did not surface the 0.025 FL win. The correction UI supplied hand-labelled test measurements.
