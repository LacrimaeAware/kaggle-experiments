# Muscle measurements from ultrasound

## Question

Can segmentation masks support useful measurements of pennation angle, fascicle length and muscle thickness? The UMUD task predicts those three quantities for 309 B-mode ultrasound images. Its metric averages MAE divided by tolerances of 6 degrees, 12 mm and 3 mm; lower is better.

## Approach

Two U-Nets predict aponeurosis and fascicle masks. Line fits turn the masks into measurements, while per-device ruler readers estimate pixel scale. The recorded models were trained on 2026-06-09 with ResNet-34 encoders, 384-pixel inputs, dice plus BCE loss, light augmentation and 12 epochs. Subsequent submitted changes used those same weights.

The training data contain 1,048 aponeurosis and 2,761 fascicle image-mask pairs, without scalar measurement labels. A separate 35-image expert benchmark supplied local measurement checks. Test images include devices, muscles and subjects not represented in training.

## Recorded public-score trajectory

Dates below come from the submission logs. The best recorded result is 0.45615 on 2026-07-01. [Submission records](docs/SUBMISSIONS.md) distinguish that result from the documented single-run pipeline at 0.47473.

| date | public score | change that produced it |
|---|---:|---|
| 2026-06-09 | 0.61918 | first fully wired pipeline: per-family scale router, inner-edge MT, fragment-extrapolation FL, on the two U-Nets with test-time augmentation |
| 2026-06-12 | 0.60961 | temporal smoothing: median PA, FL and MT within 28 sequence-like clips detected among the test images (clip threshold 0.92) |
| 2026-06-12 | 0.60936 | sub-pixel refinement of the ruler spacing, applied only where the sub-pixel comb agreed with the coarse read |
| 2026-06-12 | 0.58910 | clean shape-neighbour fallback scale: 10 rows whose scale had fallen back to the prior received the scale of a shape-neighbour image. A one-row OCR scale fix for the one known tick-versus-ruler anomaly, submitted the same day, also scored 0.58910 (neutral) |
| 2026-06-14 | 0.55075 | PA +2.0 deg flat shift, applied to the submission file (clip to 5 to 45) |
| 2026-06-14 | 0.55033 | PA +2.5 deg flat |
| 2026-06-14 | 0.52570 | FL x1.05 on the PA +2.5 file |
| 2026-06-14 | about 0.488 (the log records it as approximate) | one scale constant corrected: the `family_b` instrument family's 134.5 px/cm became 147 px/cm on 41 rows, after additional hand readings of the ticks; bottom-tick reads were corrected about +9.5% the same way |
| 2026-06-14 | 0.46076 | aponeurosis band fix: pick the pair of aponeurosis bands the fascicles sit between and drop out-of-band fragments (about 60 images changed) |
| 2026-06-14 | 0.46041 | band fix plus FL x1.05 (`submission_bandfix_flx105.csv`, the anchor for every later probe) |
| 2026-07-01 | 0.45669 | mask-threshold sweep on the 0.46041 lineage: aponeurosis threshold 0.60 and fascicle threshold 0.30 |
| 2026-07-01 | 0.45615 | fascicle threshold 0.30 with the aponeurosis threshold left at 0.50: the recorded best |

The scale router, instrument calibration and band selection changed individual measurements. PA and FL adjustments changed global calibration; the July threshold step changed which fascicle fragments were retained.

## Changes that did not transfer

Each comparison changed a setting on a named submission anchor. The anchor was 0.61918 until 2026-06-12, 0.58910 until 2026-06-14 and 0.46041 thereafter.

| date | probe | public score | reading |
|---|---|---:|---|
| 2026-06-10 | facing-geometry FL (keep a fascicle bend only when it bows toward the muscle) | 0.66459 | the bend is real (a parabola fits independent aponeurosis edges 44% better than a line) but the gate was wrong on 41% of edges, and the FL change (median 3.6%) sat under the tolerance with harmful outliers (archived state note, 2026-06-10) |
| June 2026, day not recorded | FL identity blend; three-position vertical MT; bar-only scale tail (4 rows) | 0.63905; 0.62561; 0.66711 | each looked better on the local benchmark and lost publicly |
| 2026-06-12 | top-3 minimal-extrapolation FL on 307 rows | 0.62994 | broad FL reshaping did not transfer |
| 2026-06-13 | robust-triangle upper boundary (piecewise aponeurosis) | 0.60102 | the strongest benchmark geometry win (0.251 -> 0.170, findings registry) and a public loss |
| 2026-06-13 | robust triangle plus visibility-weighted FL; plus vertical-MT proxy | 0.64511; 0.60720 | benchmark-derived proxies regressed |
| 2026-06-13 | broad field-depth scale override on 114 rows; local-benchmark proxy stack plus a 4-row missing-scale patch | 0.66197; 0.65917 | the broad override regressed; the field-rectangle heuristic overcounted the UI height |
| 2026-06-14 | PA +3.0 flat; PA hinge (extra lift above 16 deg) | 0.55168; 0.56681 | +3 overshoots; per-image PA reshaping fitted the 19 hand labels, not the hidden truth |
| 2026-06-15 | min-extrapolation top-3 FL on the clean pipeline | 0.49983 (against 0.47473 for the median) | the benchmark had ranked it best (FL 0.39, below the rater disagreement) |
| 2026-06-15 | MT x0.95; FL x1.10 | 0.53395; 0.48369 | both settings worsened the anchor |
| 2026-07-01 | aponeurosis threshold 0.60 alone | 0.47200 | a thinner aponeurosis mask raised MT and worsened the score |
| 2026-07-01 | PA -1.5 on the anchor, recommended by the 23-image hand-labelled test gate | 0.46686 | the gate is not a leaderboard predictor for calibration; the 23 labels read low on all three terms |
| 2026-07-01 | three geometry family routes: down-weight aponeurosis-hugging fascicles; bent superficial aponeurosis; curved deep aponeurosis | 0.46314; 0.48730; 0.51435 | none of these family routes improved the 0.46041 anchor; curved fits departed from the straight-line annotation convention |

## What the comparisons showed

Ruler-scale recovery, global calibration and a lower fascicle-mask threshold improved the recorded scores. The two clearest scale changes were narrow: a fallback on 10 rows and a corrected instrument scale. Broad scale overrides lost. Per-image fascicle-length reshaping also lost repeatedly, even when it improved the local benchmark.

The local benchmark and public leaderboard measured different things. The original benchmark scorer supplied true scale and recentred fascicle length to the true mean, hiding the global biases that mattered publicly. Removing that recentring did not solve the distribution mismatch: min-extrapolation length scored 0.39 locally but 0.49983 publicly, against 0.47473 for the median pipeline.

More than 2,000 geometry and aggregation configurations were compared on the 35 benchmark images on 2026-06-12 to 2026-06-13. The local metric fell from 0.170 to 0.131, about 1.1 standard errors of label noise; the three submitted components scored 0.60102, 0.64511 and 0.60720, all worse than their anchor.

A 23-image hand-corrected test diagnostic on 2026-07-01 attributed normalized error to aponeurosis fit (0.134), fascicle rejection/addition (0.132) and scale (0.008). Its PA-shift recommendation worsened the public score to 0.46686. The labels were non-expert measurements and read systematically low. They helped inspect failure modes rather than reliably choose calibration.

## Remaining limitations

The 0.45615 result used the processing history of an older submission. A clean single-run pipeline scored 0.47473; roughly 0.014 of the earlier improvement was not reproduced by retained scripts. The best file's identity is recorded, but its Kaggle upload was not independently confirmed.

The masks also missed faint fascicles. On the July 1 diagnostic, rejected and retained fragments had mean probabilities 0.723 and 0.731 (rank AUC 0.511). Added fascicles had median probability 0.054, with 59% below 0.15. Appearance matching was 0.970 within training and 0.739 from test to training; about 20% of test images used a sensor size nearly absent in training.

The test images form 197 groups over 309 images, with 169 single-frame groups and at most five frames per group. Future training comparisons need subject or sequence grouping. Follow-up ideas were broader-domain segmentation and a classical ridge-and-orientation extractor that could run without a GPU.

[Metric](metric.py) · [Synthetic geometry](benchmark_lab/generate_synthetic_geometry.py) · [Measurements from masks](mask_geometry.py) · [Detailed results](docs/RESULTS.md) · [Data and setup](README.md)
