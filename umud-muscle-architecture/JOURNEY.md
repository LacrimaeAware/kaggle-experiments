# UMUD muscle architecture: the journey

Kaggle competition "UMUD Challenge: Muscle Architecture in Ultrasound Data". Work ran from 2026-06-09 to 2026-07-01; the recorded best public score is 0.45615 (2026-07-01). This document follows the approach as it changed, with the public-score trajectory, the probes that lost, and the lessons.

Every score is a Kaggle public leaderboard score (lower is better) carrying the submission date recorded in the private experiment log, the project's append-only submission ledger, unless another ledger is named. Local diagnostic numbers name their ledger too. Nothing was re-run for this document; the ledgers, the code and the recorded scores are the evidence. The submission files, the data, the weights and the day-to-day logs are not in this repository ([PROVENANCE.md](../PROVENANCE.md) says what they are and where they live).

## Question

For each of 309 B-mode ultrasound test images, predict three scalars: pennation angle (PA, degrees, the angle between the fascicle line and the deep aponeurosis), fascicle length (FL, mm, the distance between the two aponeuroses along the fascicle line with straight-line extrapolation past the frame) and muscle thickness (MT, mm, the perpendicular gap between the aponeuroses). The metric, implemented in [metric.py](metric.py), is

```
score = (1/3) * [ MAE(PA)/6 + MAE(FL)/12 + MAE(MT)/3 ]
```

with tolerances 6 deg, 12 mm and 3 mm and equal weight per term. One consequence shaped the whole project: a global mean shift on any one term is a first-order lever on the score.

The training set holds 1,048 aponeurosis and 2,761 fascicle (image, mask) pairs and no scalar PA, FL or MT labels; the test set holds 309 images with no labels of any kind; the only images with scalar truth are a public 35-image expert benchmark from a different distribution, scored with its true pixel scale (handoff document, 2026-06-15). The test set adds a device (Philips Lumify), a muscle (rectus femoris) and cerebral-palsy subjects that the training set lacks (findings registry, host-confirmed).

## Approach

Segment, then measure. Two U-Nets (ResNet-34 encoder, 384 px, dice plus BCE loss, 12 epochs, light augmentation, per the training notebook comment quoted in [docs/SUBMISSIONS.md](docs/SUBMISSIONS.md)) predict an aponeurosis mask and a fascicle mask with test-time augmentation. Straight lines are fitted to the aponeurosis bands and to each fascicle fragment; PA is the length-weighted median fragment angle to the deep aponeurosis, MT is the inner-edge gap between the two aponeurosis lines, FL is the per-fragment extrapolated span aggregated by the median. The pixel scale is not given, so it is read from the rulers and tick marks printed on each image by a per-device-family router. Global calibration constants (a flat PA shift, an FL factor) were set from public leaderboard results and applied as post-run transforms of the submission file.

The weights behind every recorded submission are the ones trained on a Kaggle GPU notebook on 2026-06-09. Later training runs (a controlled GPU matrix and a thin-structure attempt, both 2026-06-13) did not produce a submitted result; every later step changed scale recovery, mask geometry, calibration or the mask threshold.

## Trajectory of the public best

Each row is a submission that lowered the recorded best. The earliest submissions predicted near-constant FL and MT; the archived notes record their scores without dates, so they are not repeated here.

| date | public score | change that produced it | recorded in |
|---|---:|---|---|
| 2026-06-09 | 0.61918 | first fully wired pipeline: per-family scale router, inner-edge MT, fragment-extrapolation FL, on the two U-Nets with test-time augmentation | experiment log |
| 2026-06-12 | 0.60961 | temporal smoothing: median PA, FL and MT within 28 sequence-like clips detected among the test images (clip threshold 0.92) | experiment log |
| 2026-06-12 | 0.60936 | sub-pixel refinement of the ruler spacing, applied only where the sub-pixel comb agreed with the coarse read | experiment log |
| 2026-06-12 | 0.58910 | clean shape-neighbour fallback scale: 10 rows whose scale had fallen back to the prior received the scale of a shape-neighbour image. A one-row OCR scale fix for the one known tick-versus-ruler anomaly, submitted the same day, also scored 0.58910 (neutral) | experiment log |
| 2026-06-14 | 0.55075 | PA +2.0 deg flat shift, applied to the submission file (clip to 5 to 45) | experiment log |
| 2026-06-14 | 0.55033 | PA +2.5 deg flat | experiment log |
| 2026-06-14 | 0.52570 | FL x1.05 on the PA +2.5 file | experiment log |
| 2026-06-14 | about 0.488 (the log records it as approximate) | one scale constant corrected: the `family_b` instrument family's 134.5 px/cm became 147 px/cm on 41 rows, after the author hand-read the ticks; bottom-tick reads were corrected about +9.5% the same way | experiment log, findings registry |
| 2026-06-14 | 0.46076 | aponeurosis band fix: pick the pair of aponeurosis bands the fascicles sit between and drop out-of-band fragments (about 60 images changed) | experiment log |
| 2026-06-14 | 0.46041 | band fix plus FL x1.05 (`submission_bandfix_flx105.csv`, the anchor for every later probe) | experiment log |
| 2026-07-01 | 0.45669 | mask-threshold sweep on the 0.46041 lineage: aponeurosis threshold 0.60 and fascicle threshold 0.30 | experiment log |
| 2026-07-01 | 0.45615 | fascicle threshold 0.30 with the aponeurosis threshold left at 0.50: the recorded best | experiment log |

Three of the steps were mechanistic and per-image (the scale router, the `family_b` constant, the band fix). The PA and FL shifts moved a column mean and nothing else; the handoff document (2026-06-15) calls them aggregate band-aids, and the results ledger (2026-07-01) calls the July threshold step a fascicle-recall lever, not geometry.

## Techniques, in the order they mattered

**Scale recovery from the on-image rulers** ([scale_ticks.py](scale_ticks.py), [tick_calibration.py](tick_calibration.py), [subpixel_spacing.py](subpixel_spacing.py), [scale_ocr.py](scale_ocr.py)). The pixel scale differs per device family and is printed on the image as a ruler, tick marks or a depth label. The router recognises the family and reads the matching cue; on 2026-06-09 the competition reference recorded four device families rather than one, and the first detector had been reading a text panel instead of the ruler. Coverage on the final debug table is 295 of 309 images (right 5 mm ruler 87, bottom ticks 59, PNG left ruler 58, left 1 cm ruler 50, `family_b` signature 41, none 14; verified facts ledger). An OCR read of the printed depth and ruler numbers gave an independent second read: on 2026-06-10 the log recorded 48 images verified by both reads, 99 confirmed by text, 147 tick-only, 14 with no cue, and agreement on 147 of the 148 images with two reads; the one disagreement (a tick read of 201 px/cm against a printed 101 px/cm) was quarantined to the prior. On the mirrored, lower-resolution benchmark images the tick detectors failed (30 of 35 fell to the prior) while the OCR depth read worked on 30 of 35 (experiment log, 2026-06-10), which is why the OCR path was recorded as the device-agnostic one. Sub-pixel refinement of the tick spacing (2026-06-12) changed FL by a mean absolute 0.094 mm against a 12 mm tolerance; the findings registry records it as below the metric's resolution.

**Mask geometry** ([mask_geometry.py](mask_geometry.py), and the `measure()` stage of the reference pipeline). Straight-line fits to the aponeurosis bands and to fascicle fragments; PA from fragment orientation (total least squares), MT from the inner edges of the two bands, FL from extrapolation to both bands. Two checks anchored it: the author hand-drew fascicles on 8 test images and the fitted angle field was off by a mean of 1.8 deg (median 1.4, 90th percentile 3.8; experiment log, 2026-06-10 to 06-12), inside the 6 deg tolerance; and on the benchmark with true scale PA (0.1505) and MT (0.0840) sat at or below the inter-rater human floor (0.2445 and 0.0810) while FL (0.5218) did not (handoff document, 2026-06-15). The band fix of 2026-06-14, which chose the aponeurosis pair the fascicles actually sit between, was the last geometry change that moved the leaderboard.

**Global calibration from leaderboard probes.** With the metric's per-term MAE, a constant shift of a whole column is the cheapest lever, and the leaderboard is the only place to set it because no test labels exist. The PA shift was bracketed on 2026-06-14 (+0 -> 0.58910, +2.0 -> 0.55075, +2.5 -> 0.55033, +3.0 -> 0.55168; optimum about +2.4), FL on 2026-06-14 and 2026-06-15 (x1.00 -> 0.46076, x1.05 -> 0.46041, x1.10 -> 0.48369) and MT on 2026-06-15 (x0.95 -> 0.53395; x1.0 stays). After that the global levers were spent: they can only move a mean, and the mean is one number per term.

**Mask thresholds without retraining** ([benchmark_lab/generate_threshold_sweep.py](benchmark_lab/generate_threshold_sweep.py)). The probability maps are computed once per image and binarised at a grid of (aponeurosis, fascicle) thresholds, so one model pass writes every candidate. Lowering the fascicle threshold from 0.50 to 0.30 recovered faint fascicles and produced the best score; the same-day isolation reads fascicle-only 0.45615, combined 0.45669, aponeurosis-only 0.47200 (worse than the 0.46041 anchor), so the whole gain was the fascicle term (experiment log, 2026-07-01).

**Exact synthetic geometry** ([benchmark_lab/generate_synthetic_geometry.py](benchmark_lab/generate_synthetic_geometry.py), [benchmark_lab/score_labels.py](benchmark_lab/score_labels.py)). Abstract band-and-strand images with a known pixel scale and exact PA, FL and MT, built on 2026-06-12 as unit tests for the measurement rules (straight, steep, curved and fan-like cases). They test the rules, not the ultrasound; the log records that they are not leaderboard evidence.

**Segmentation.** The submitted U-Nets were trained once. A thin-structure retraining attempt on 2026-06-13 (soft and dilated fascicle targets, skeleton decoding, heavy augmentation, about nine axes changed at once) underperformed the control by epoch 20 (fascicle Dice 0.2594 against 0.2925, aponeurosis 0.7873 against 0.7945; experiment log) and was stopped; the method audit the same day recorded that it changed too many things to test any of them. Later retraining notebooks were specified and never run (findings registry).

## What did not help

Every probe below changed one thing on a named anchor file and was scored on the leaderboard. Anchor 0.61918 until 2026-06-12, 0.58910 until 2026-06-14, 0.46041 from then on.

| date | probe | public score | recorded in | reading |
|---|---|---:|---|---|
| 2026-06-10 | facing-geometry FL (keep a fascicle bend only when it bows toward the muscle) | 0.66459 | experiment log | the bend is real (a parabola fits independent aponeurosis edges 44% better than a line) but the gate was wrong on 41% of edges, and the FL change (median 3.6%) sat under the tolerance with harmful outliers (archived state note, 2026-06-10) |
| June 2026, day not recorded | FL identity blend; three-position vertical MT; bar-only scale tail (4 rows) | 0.63905; 0.62561; 0.66711 | experiment log | each looked better on the local benchmark and lost publicly |
| 2026-06-12 | top-3 minimal-extrapolation FL on 307 rows | 0.62994 | experiment log | broad FL reshaping did not transfer |
| 2026-06-13 | robust-triangle upper boundary (piecewise aponeurosis) | 0.60102 | experiment log | the strongest benchmark geometry win (0.251 -> 0.170, findings registry) and a public loss |
| 2026-06-13 | robust triangle plus visibility-weighted FL; plus vertical-MT proxy | 0.64511; 0.60720 | experiment log | benchmark-derived proxies regressed |
| 2026-06-13 | broad field-depth scale override on 114 rows; local-benchmark proxy stack plus a 4-row missing-scale patch | 0.66197; 0.65917 | experiment log | never override an existing per-image scale broadly; the field-rectangle heuristic overcounts the UI height |
| 2026-06-14 | PA +3.0 flat; PA hinge (extra lift above 16 deg) | 0.55168; 0.56681 | experiment log | +3 overshoots; per-image PA reshaping fitted the 19 hand labels, not the hidden truth |
| 2026-06-15 | min-extrapolation top-3 FL on the clean pipeline | 0.49983 (against 0.47473 for the median) | experiment log | the benchmark had ranked it best (FL 0.39, below the human floor); the benchmark does not predict the leaderboard |
| 2026-06-15 | MT x0.95; FL x1.10 | 0.53395; 0.48369 | experiment log | MT and FL brackets closed |
| 2026-07-01 | aponeurosis threshold 0.60 alone | 0.47200 | experiment log | a thinner aponeurosis mask raises MT, and MT was already right |
| 2026-07-01 | PA -1.5 on the anchor, recommended by the 23-image hand-labelled test gate | 0.46686 | experiment log, test-gate findings | the gate is not a leaderboard predictor for calibration; the 23 labels read low on all three terms |
| 2026-07-01 | three geometry family routes: down-weight aponeurosis-hugging fascicles; bent superficial aponeurosis; curved deep aponeurosis | 0.46314; 0.48730; 0.51435 | experiment log | geometry on the 0.46041 lineage is closed; the ground truth follows the raters' straight-line convention, not the anatomy |

Two families of negative results carried the most information. Every per-image FL reshaping lost (identity blend, top-3 extrapolation, visibility weighting, facing FL, robust triangle, min-extrapolation twice), while the one FL change that won was a global factor. And every broad scale override lost, while the two scale wins were narrow (10 fallback rows; one instrument constant read by hand).

## Local diagnostics and the leaderboard are different surfaces

The project had three local instruments, and the central lesson is what each could and could not see.

The 35-image expert benchmark comes with its true scale and a different distribution. The first scorer fed it that true scale and recentred predicted FL to the truth mean, so it was blind by construction to scale error and to a global FL bias, the two things that dominated the leaderboard (findings registry). A scorer without the recentre, built 2026-06-15, still ranked min-extrapolation FL best (FL 0.39 against a 0.40 human floor) and that submission regressed the leaderboard by 0.025 (0.49983 against 0.47473). Between 2026-06-12 and 2026-06-13 more than 2,000 geometry and aggregation configurations were scored on those 35 images, grinding the local score from 0.170 to 0.131, about 1.1 standard errors of the label noise; the three pieces of that stack that reached the leaderboard (0.60102, 0.64511, 0.60720) all lost (findings registry, experiment log). The benchmark remained useful for one thing: catching a measurement bug, and showing that PA and MT were at the human floor given true scale.

The hand-labelled test gate (23 test images corrected by the author on 2026-07-01, 16 with all three terms and 7 with a blind PA line) is the only per-image truth on the test distribution. It decomposed the error by source (aponeurosis fit 0.134, fascicle reject-and-add 0.132, scale 0.008, in metric units; test-gate findings) and refuted the idea that scale was still the master lever. Its one calibration recommendation, lowering PA, lost on the leaderboard (0.46686), and the author recorded that the labels were drawn by a non-expert and read low. The gate's decomposition stands; its direction calls do not.

The leaderboard itself: about five submissions per day (submission log), one hidden statistic per submission, and the only signal that ever predicted the leaderboard. The findings registry's rule after 2026-06-15: gate global and calibration quantities on isolated single-variable leaderboard probes only, and treat the local surfaces as diagnostics.

## Rollback anchors and the submission discipline

The experiment log has a "how to reproduce / roll back" column on every submission row. Each public best became a named anchor file: a copy of the 0.61918 submission was kept outside the repository as the protected baseline, and from 2026-06-14 every probe row ends with "revert to `submission_bandfix_flx105.csv`". Probes were built as post-run transforms of the anchor (a PA column shift, an FL factor, a routed family variant), so each one changed a single variable, could be diffed against the anchor row by row before upload, and cost one submission slot rather than a code change when it lost. Before a batch of slots was spent, a burn pack listed the candidates in order with the expected effect of each (2026-06-12), and the scores were written back to the log the same day.

Two costs of the discipline are also on record. The 0.46041 anchor was a stack of spliced post-run transforms; a clean regeneration of the same pipeline in one inference run scored 0.47473 on 2026-06-15, and the 0.014 residue (shape-neighbour scale rows, sub-pixel reads, the spliced band fix) is not reproduced by any tracked script (verified facts ledger). The competition judges the whole pipeline, so the reproducible score, not the best CSV, is the one that would count. And the 0.45615 threshold sweep was generated on the spliced lineage, so it inherits the residue.

## Where the project stands

- Recorded best 0.45615 (2026-07-01); reproducible single-run pipeline 0.47473 (2026-06-15). The provenance of the best, including what was not recorded at the time, is in [docs/SUBMISSIONS.md](docs/SUBMISSIONS.md).
- Measurement geometry is closed on the current masks, every global calibration constant is bracketed, and the results ledger (2026-07-01) rules out further geometry-family variants without a new per-image mechanism.
- The remaining error is in the masks: on the 23-image gate the human-rejected fragments carried the same model confidence as the kept ones (mean probability 0.723 against 0.731, rank AUC 0.511), and the fascicles the author had to add scored a median probability of 0.054, with 59% below 0.15 (test-gate findings, 2026-07-01).
- The test set is out of distribution: nearest-neighbour appearance matching gives a median best match of 0.970 within the training set and 0.739 from test to training, and about 20% of the test images come from a sensor size nearly absent from training (test-gate findings, 2026-07-01). The test set also contains short clips (197 groups over 309 images, 169 of them single frames, at most 5 frames each), so any training-set cross-validation must group by subject or sequence.
- The next structural step recorded in the ledgers is a segmentation model that generalises to the test-only domains, validated on grouped folds and on the test gate, never on same-domain Dice; the classical ridge-and-orientation fascicle extractor is the ranked GPU-free alternative (findings registry, strategy direction of 2026-06-15).

## Lessons

1. Decide which surface a number lives on before believing it. Benchmark scores, hand-label gates and the public leaderboard measured different distributions with different inputs; only leaderboard-to-leaderboard comparisons were ever predictive here. The two clearest cases are the min-extrapolation FL (benchmark best, leaderboard 0.49983 against 0.47473, 2026-06-15) and the PA de-shift (gate-optimal, leaderboard 0.46686 against 0.46041, 2026-07-01).
2. Small public-score moves can be noise. PA +2.0, +2.5 and +3.0 scored 0.55075, 0.55033 and 0.55168 on 2026-06-14, a spread of 0.0014 that the test-gate findings later describe as an aggregate nearly insensitive to a half-degree shift; a one-row scale fix scored exactly the anchor's 0.58910 (2026-06-12). The methodology note of 2026-06-15 in the findings registry treats moves smaller than twice the leaderboard's standard error as noise and admits one isolated change per submission.
3. Keep every public-best file and name it as the anchor for the next probes. Losing probes then cost one slot and nothing else, and the rollback path is a filename in the log, not code archaeology.
4. A global calibration win reveals the sign of the average residual and nothing about which images are wrong. The handoff document (2026-06-15) names this the global-probe aggregation fallacy; the PA, FL and MT brackets were each spent within two days of being opened.
5. Scoring thousands of configurations on 35 images finds the minimum of the label noise. The 0.170 to 0.131 chase (2026-06-12 to 06-13) produced three public losses and no gain.
6. The ground truth is the raters' convention, not the anatomy. The fascicle bend is real on independent data (2026-06-10) and every curved or bent variant lost (0.66459, 0.48730, 0.51435), because the scored FL is a straight-line extrapolation.
7. Measure on the right input. The FL recentre was recorded as a no-op (0 of 309 rows changed) until 2026-06-14, when the check turned out to have re-applied the pin to an already pinned file; on the raw per-image table it shrank FL by about 19% on 308 of 309 rows (experiment log).
8. Fix the foundation first, narrowly. The scale router moved the first submissions to 0.61918 (2026-06-09); one hand-read instrument constant moved the score by about 0.04 (2026-06-14); every broad scale override lost (0.66711, 0.66197, 0.65917). MT, which has no fascicle and no extrapolation, was the clean probe of scale.
9. Recover the grouping before any random split. The test set is made of short clips; a shuffled split would leak frames of the same clip across folds (findings registry).
10. Retraining is not "more epochs". The one retraining attempt changed nine axes and underperformed its control (2026-06-13); the later probes showed a model that is confidently wrong on speckle and blind to faint fascicles on out-of-distribution images (2026-07-01). Dice and the metric are decoupled: one missed thin fascicle is a few pixels of Dice and one vote in a median of about fifteen.
11. Name the cheap decisive test and run it before the expensive virtuous-looking one. The findings registry records the pattern of deferring exactly those tests (the Dice-versus-angle check, the orientation audit, the human-row gate) for four commits at a time.
12. Ledgers with status tags beat narrative notes. After the 2026-06-14 documentation reset the project kept one append-only submission log with a rollback column, one registry where every idea carries LIVE, FACT, UNTESTED, REJECTED, FALSE or PAST judged against code and the leaderboard rather than against what the source note claimed, and one verified-facts file where every line needs a `file:line` or an exact leaderboard number. The corrected beliefs in this document (the recentre no-op, "scale is banked", "FL is mask-limited") were caught by that discipline.

## What the code here illustrates

| module | technique | runs without the competition data |
|---|---|---|
| [metric.py](metric.py) | the tolerance-normalised MAE and why a column mean is a first-order lever | yes |
| [scale_ticks.py](scale_ticks.py), [tick_calibration.py](tick_calibration.py), [subpixel_spacing.py](subpixel_spacing.py) | per-family scale router, tick detection, sub-pixel comb refinement | import yes; the self-test in `scale_ticks.py` needs the public benchmark images and spreadsheet |
| [scale_ocr.py](scale_ocr.py) | reading the printed depth and ruler numbers as an independent second read, trusted only on agreement (needs easyocr) | import yes |
| [mask_geometry.py](mask_geometry.py) | line fits to aponeurosis bands and fascicle fragments; PA, FL and MT from masks, as a pseudo-label table over the training masks | import yes; the table needs the training masks |
| [benchmark_lab/generate_synthetic_geometry.py](benchmark_lab/generate_synthetic_geometry.py), [benchmark_lab/score_labels.py](benchmark_lab/score_labels.py) | exact synthetic geometry cases as unit tests of the measurement rules | yes |
| [benchmark_validate.py](benchmark_validate.py), [expert_consensus.py](expert_consensus.py) | scoring a submission against a 7-rater consensus with the leave-one-rater-out human floor and single-rater tail handling | import yes; scoring needs the public benchmark spreadsheet |
| [segment_then_measure.py](segment_then_measure.py) | the reference pipeline named by the provenance record: training, test-time augmentation, band fix, fragment FL, scale router, recentre | no: it resolves the data folders at import and needs the private weights for inference |
| [benchmark_lab/generate_threshold_sweep.py](benchmark_lab/generate_threshold_sweep.py) | the one-pass mask-threshold sweep that produced the recorded best | no: imports the reference pipeline |

## Sources

Kept in the private working repository and cited above by name: the experiment log (append-only submission ledger with the rollback column), the findings registry (every idea with a status tag), the handoff document and strategy direction of 2026-06-15, the test-gate findings of 2026-07-01, the results ledger (exported here as [docs/RESULTS.md](docs/RESULTS.md)), 41 dated experiment notes and about 100 experiment scripts. In this repository: [VERIFIED_FACTS.md](VERIFIED_FACTS.md), [docs/SUBMISSIONS.md](docs/SUBMISSIONS.md), [docs/RESULTS.md](docs/RESULTS.md) and [competition_reference.md](competition_reference.md).
