# UMUD Muscle Architecture

Kaggle competition "UMUD Challenge: Muscle Architecture in Ultrasound Data". For each of 309 B-mode ultrasound test images the task is to predict the pennation angle (PA, degrees), the fascicle length (FL, mm) and the muscle thickness (MT, mm). The metric is a tolerance-normalised mean absolute error, lower is better; `metric.py` is the local implementation. [JOURNEY.md](JOURNEY.md) is the narrative: the approach, the dated public-score trajectory from 0.61918 (2026-06-09) to 0.45615 (2026-07-01), the probes that lost, and the lessons. Competition facts, rules and data terms are in [competition_reference.md](competition_reference.md).

The approach is segmentation followed by measurement: two U-Nets predict aponeurosis and fascicle masks, straight lines are fitted to the masks, the pixel scale is read from the rulers and tick marks printed on each image, and a few global calibration constants (a pennation-angle shift, a fascicle-length factor) were set from public leaderboard results.

## Recorded results

| public score | file | how it was produced |
|---:|---|---|
| 0.45615 | `results/submission_thr_a0.50_f0.30.csv` (2026-07-01) | `benchmark_lab/generate_threshold_sweep.py`: one model pass with the saved weights, fascicle mask threshold 0.30 at aponeurosis threshold 0.50, on the `0.46041` post-processing lineage |
| 0.47473 | `results/submission_reproduced.csv` (2026-06-15) | one run of the pipeline's inference script (`local_infer.py`, kept in the private working repository) with default settings |

The provenance record for 0.45615 (generator, invocation, pipeline commit, weights, output hash, and what was not recorded) is in [docs/SUBMISSIONS.md](docs/SUBMISSIONS.md); the full leaderboard ledger and the validation discipline are in [docs/RESULTS.md](docs/RESULTS.md). Neither output file is tracked, and neither score is reproducible from this repository: both need the competition data and the private weights, and whether a rerun would reproduce them exactly was not tested.

## What is here

The code is the author's own, kept where it illustrates a technique the journey names. The pipeline drivers (inference, standalone training, the benchmark runner), the labelling and review tooling and the notebooks stay in the private working repository.

| Location | Contents |
|---|---|
| `JOURNEY.md` | the narrative: dated trajectory, negative results, lessons, and which module illustrates which technique |
| `metric.py` | the competition metric, used for local scoring; imports without data |
| `scale_ticks.py`, `tick_calibration.py`, `subpixel_spacing.py` | pixel-scale recovery from the on-image rulers, routed by device family (see `competition_reference.md`, section 3); `python scale_ticks.py` validates the reader against the public benchmark's true scale when that data is present |
| `scale_ocr.py` | the independent second read of the printed depth and ruler numbers with easyocr (optional dependency); not required by the pipeline |
| `mask_geometry.py` | line fits to aponeurosis bands and fascicle fragments, and PA, FL and MT from masks; `python mask_geometry.py` writes a pseudo-label table over the training masks when they are present |
| `benchmark_lab/generate_synthetic_geometry.py`, `benchmark_lab/score_labels.py` | synthetic band-and-strand cases with exact measurements; a data-free check of the measurement rules |
| `benchmark_validate.py`, `expert_consensus.py` | scoring of a submission CSV against the public 35-image expert benchmark, with the per-term human floor (external data, see the data terms in `competition_reference.md`) |
| `segment_then_measure.py` | reference code: the pipeline named by the provenance record. It trains both U-Nets, predicts masks with test-time augmentation, recovers the pixel scale, measures PA, FL and MT, and writes `results/submission_segmentation.csv`; every setting is a `UMUD_*` environment variable listed at the top of the file. It resolves the data folders when imported and needs the competition data; inference needs the private weights |
| `benchmark_lab/generate_threshold_sweep.py` | reference code: one inference pass binarised at a grid of (aponeurosis, fascicle) mask thresholds (`UMUD_APO_THRS`, `UMUD_FASC_THRS`), one `results/submission_thr_a{a}_f{f}.csv` per pair; the generator of the recorded best. It imports the pipeline, so it has the same needs |
| `docs/` | `RESULTS.md` (result ledger and validation discipline), `SUBMISSIONS.md` (submission log and provenance) |
| `data/`, `results/` (ignored by git) | where the competition data and the outputs would live: `apo_images_new_model_v1/`, `apo_masks_new_model_v1/`, `fasc_images_new_model_v1/`, `fasc_masks_new_model_v1/` and `test_set_v2/` (309 images) under `data/`, found by leaf folder name at any nesting (or under `/kaggle/input`); weights, submission CSVs and per-image debug CSVs under `results/` |

## Data-free checks

From this folder, in the project environment:

```
python -c "import metric, scale_ticks, tick_calibration, subpixel_spacing, mask_geometry, scale_ocr, benchmark_validate, expert_consensus"
python -c "import pandas as pd, metric; s = pd.DataFrame({'image_id': ['a'], 'pa_deg': [15.0], 'fl_mm': [80.0], 'mt_mm': [20.0]}); p = s.assign(pa_deg=s.pa_deg + 6); print(metric.umud_score(s, p))"
python benchmark_lab/generate_synthetic_geometry.py --n 2 --out-dir <folder>
```

The metric call prints 0.333333667 for a one-tolerance PA offset (one term of three at exactly one tolerance, plus the tie-breaker terms in the last digits). The synthetic generator writes the cases, their exact truth and the light-measurement scores into the folder.

## Reference pipeline

`segment_then_measure.py` is kept as the code behind the recorded scores, not as a run path for this repository. With the competition data under `data/` and a GPU, `python segment_then_measure.py` trains the two U-Nets (12 epochs each by default; `UMUD_EPOCHS=2 UMUD_MAX_PAIRS=24` gives a short CPU smoke run), saves `results/seg_apo.pt` and `results/seg_fasc.pt` and writes `results/submission_segmentation.csv` with the columns `image_id,pa_deg,fl_mm,mt_mm`. The recorded weights came from a Kaggle GPU notebook running this file and are not included, so a new training run produces new weights and a different score. Without the data folders, importing the file stops with a message listing what was searched. The sweep's invocation for the recorded best is in [docs/SUBMISSIONS.md](docs/SUBMISSIONS.md); on Windows PowerShell, set a variable with `$env:UMUD_APO_THRS='0.50'` before the command.

## Environment

Python 3.13 with torch 2.12.0 (CPU build locally, CUDA on Kaggle), torchvision 0.27.0, segmentation-models-pytorch 0.5.0, albumentations 2.0.8, opencv-python-headless 4.13.0.92, numpy 2.4.6, pandas 3.0.3, scikit-image 0.26.0, Pillow 12.2.0 and openpyxl 3.1.5 (for the benchmark spreadsheet). `scale_ocr.py` additionally needs easyocr. These are the versions pinned in this folder's `requirements.txt` (install with `python -m pip install -r requirements.txt` from this folder), each annotated with the module that needs it; the weights were trained on Kaggle's GPU image, whose package versions were not recorded. The data-free checks need only numpy, pandas, OpenCV, scikit-image and Pillow.

## Repository hygiene

`data/`, `results/`, trained weights, human labels, OCR caches and generated review artifacts are not tracked. Track a derived file only after checking it for private content and deciding to publish it deliberately.
