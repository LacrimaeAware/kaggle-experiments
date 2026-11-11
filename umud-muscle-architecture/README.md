# UMUD Muscle Architecture

Kaggle competition "UMUD Challenge: Muscle Architecture in Ultrasound Data". For each of 309 B-mode ultrasound test images the task is to predict the pennation angle (PA, degrees), the fascicle length (FL, mm) and the muscle thickness (MT, mm). The metric is a tolerance-normalised mean absolute error, lower is better; `metric.py` is the local implementation. [Experiment history](JOURNEY.md) · [Competition and data terms](competition_reference.md).

The approach is segmentation followed by measurement: two U-Nets predict aponeurosis and fascicle masks, straight lines are fitted to the masks, the pixel scale is read from the rulers and tick marks printed on each image, and a few global calibration constants (a pennation-angle shift, a fascicle-length factor) were set from public leaderboard results.

## Recorded results

| public score | file | how it was produced |
|---:|---|---|
| 0.45615 | `results/submission_thr_a0.50_f0.30.csv` (2026-07-01) | `benchmark_lab/generate_threshold_sweep.py`: one model pass with the saved weights, fascicle mask threshold 0.30 at aponeurosis threshold 0.50, on the `0.46041` post-processing lineage |
| 0.47473 | `results/submission_reproduced.csv` (2026-06-15) | one run of the inference script `local_infer.py` with default settings |

[Submission records](docs/SUBMISSIONS.md) identify the pipeline, weights and outputs; [results](docs/RESULTS.md) list the dated scores. Competition data, trained weights and submission files are not included.

## What is here

| Location | Contents |
|---|---|
| `JOURNEY.md` | the narrative: dated trajectory, negative results, lessons, and which module illustrates which technique |
| `metric.py` | the competition metric, used for local scoring; imports without data |
| `scale_ticks.py`, `tick_calibration.py`, `subpixel_spacing.py` | pixel-scale recovery from the on-image rulers, routed by device family (see `competition_reference.md`, section 3); `python scale_ticks.py` validates the reader against the public benchmark's true scale when that data is present |
| `scale_ocr.py` | the independent second read of the printed depth and ruler numbers with easyocr (optional dependency); not required by the pipeline |
| `mask_geometry.py` | line fits to aponeurosis bands and fascicle fragments, and PA, FL and MT from masks; `python mask_geometry.py` writes a pseudo-label table over the training masks when they are present |
| `benchmark_lab/generate_synthetic_geometry.py`, `benchmark_lab/score_labels.py` | synthetic band-and-strand cases with exact measurements; a data-free check of the measurement rules |
| `benchmark_validate.py`, `expert_consensus.py` | scoring of a submission CSV against the public 35-image expert benchmark, with the per-term rater disagreement (external data, see the data terms in `competition_reference.md`) |
| `segment_then_measure.py` | reference code: the pipeline named by the provenance record. It trains both U-Nets, predicts masks with test-time augmentation, recovers the pixel scale, measures PA, FL and MT, and writes `results/submission_segmentation.csv`; every setting is a `UMUD_*` environment variable listed at the top of the file. It resolves the data folders when imported and needs the competition data; inference needs saved weights |
| `benchmark_lab/generate_threshold_sweep.py` | reference code: one inference pass binarised at a grid of (aponeurosis, fascicle) mask thresholds (`UMUD_APO_THRS`, `UMUD_FASC_THRS`), one `results/submission_thr_a{a}_f{f}.csv` per pair; the generator of the recorded best. It imports the pipeline, so it has the same needs |
| `docs/` | `RESULTS.md` (result ledger and validation discipline), `SUBMISSIONS.md` (submission log and provenance) |
| `data/`, `results/` (ignored by git) | where the competition data and the outputs would live: `apo_images_new_model_v1/`, `apo_masks_new_model_v1/`, `fasc_images_new_model_v1/`, `fasc_masks_new_model_v1/` and `test_set_v2/` (309 images) under `data/`, found by leaf folder name at any nesting (or under `/kaggle/input`); weights, submission CSVs and per-image debug CSVs under `results/` |

## Data-free checks

From this folder:

```
python -m pip install -r requirements.txt
python -c "import metric, scale_ticks, tick_calibration, subpixel_spacing, mask_geometry, scale_ocr, benchmark_validate, expert_consensus"
python -c "import pandas as pd, metric; s = pd.DataFrame({'image_id': ['a'], 'pa_deg': [15.0], 'fl_mm': [80.0], 'mt_mm': [20.0]}); p = s.assign(pa_deg=s.pa_deg + 6); print(metric.umud_score(s, p))"
python benchmark_lab/generate_synthetic_geometry.py --n 2 --out-dir results/synthetic-geometry
```

The metric call prints 0.333333667 for a one-tolerance PA offset (one term of three at exactly one tolerance, plus the tie-breaker terms in the last digits). The synthetic generator writes the cases, their exact truth and the light-measurement scores into the folder.

## Reference pipeline

`segment_then_measure.py` and the threshold sweep require competition images
and masks and additional training libraries. Inference uses saved weights.
Data folders are resolved on import; missing folders cause an error. Historical
settings and weight identities are in [docs/SUBMISSIONS.md](docs/SUBMISSIONS.md).

## Environment

The data-free examples use Python 3.13 with NumPy, pandas, OpenCV, scikit-image,
Pillow and openpyxl, pinned in `requirements.txt`. The [historical training
environment](../PROVENANCE.md#historical-ultrasound-training-environment) records
the additional packages used by the reference pipeline. OCR is optional and
requires easyocr plus images containing printed depth or ruler labels.
