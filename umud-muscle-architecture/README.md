# UMUD Muscle Architecture

Kaggle competition "UMUD Challenge: Muscle Architecture in Ultrasound Data". For each of 309 B-mode ultrasound test images the task is to predict the pennation angle (PA, degrees), the fascicle length (FL, mm) and the muscle thickness (MT, mm). The metric is a tolerance-normalised mean absolute error, lower is better; `metric.py` is the local implementation. Competition facts, rules and data terms are in [competition_reference.md](competition_reference.md).

The approach is segmentation followed by measurement: two U-Nets predict aponeurosis and fascicle masks, straight lines are fitted to the masks, the pixel scale is read from the rulers and tick marks printed on each image, and a few global calibration constants (a pennation-angle shift, a fascicle-length factor) were set from public leaderboard results.

## Recorded results

| public score | file | how it was produced |
|---:|---|---|
| 0.45615 | `results/submission_thr_a0.50_f0.30.csv` (2026-07-01) | `benchmark_lab/generate_threshold_sweep.py`: one model pass with the saved weights, fascicle mask threshold 0.30 at aponeurosis threshold 0.50, on the `0.46041` post-processing lineage |
| 0.47473 | `results/submission_reproduced.csv` (2026-06-15) | one run of the pipeline's inference script (`local_infer.py`, kept in the private working repository) with default settings |

The provenance record for 0.45615 (generator, invocation, pipeline commit, weights, output hash, and what was not recorded) is in [docs/SUBMISSIONS.md](docs/SUBMISSIONS.md); the full leaderboard ledger and the validation discipline are in [docs/RESULTS.md](docs/RESULTS.md). Neither output file is tracked. The sweep regenerates submissions of the first kind from the saved weights and the data; whether a rerun reproduces the exact scores was not tested.

## Layout

| Location | Contents |
|---|---|
| `data/` (ignored by git) | the competition data, downloaded by a registered participant: `apo_images_new_model_v1/`, `apo_masks_new_model_v1/`, `fasc_images_new_model_v1/`, `fasc_masks_new_model_v1/` and `test_set_v2/` (309 images). The pipeline searches for these leaf folder names under `data/` (or `/kaggle/input`), so any nesting works |
| `results/` (ignored by git) | weights (`seg_apo.pt`, `seg_fasc.pt`), submission CSVs, per-image debug CSVs |
| `segment_then_measure.py` | the pipeline: trains both U-Nets, predicts masks with test-time augmentation, recovers the pixel scale, measures PA, FL and MT, and writes `results/submission_segmentation.csv`. Every setting is a `UMUD_*` environment variable listed at the top of the file |
| `benchmark_lab/generate_threshold_sweep.py` | inference once, binarised at a grid of (aponeurosis, fascicle) mask thresholds (`UMUD_APO_THRS`, `UMUD_FASC_THRS`); writes one `results/submission_thr_a{a}_f{f}.csv` per pair |
| `scale_ticks.py`, `tick_calibration.py`, `subpixel_spacing.py` | pixel-scale recovery from the on-image rulers, routed by device family (see `competition_reference.md`, section 3) |
| `scale_ocr.py` | optional cross-check that reads the ruler numbers and the printed depth with easyocr; not required by the pipeline |
| `mask_geometry.py` | geometry table derived from the training masks |
| `metric.py` | the competition metric, used for local scoring |
| `benchmark_validate.py`, `expert_consensus.py` | scoring of a submission CSV against the public 35-image expert benchmark, with the per-term human floor (external data, see the data terms in `competition_reference.md`) |
| `benchmark_lab/generate_synthetic_geometry.py`, `benchmark_lab/score_labels.py` | synthetic band-and-strand cases with exact measurements; a data-free check of the measurement rules |
| `docs/` | `RESULTS.md` (result ledger and validation discipline), `SUBMISSIONS.md` (submission log and provenance) |

## Run

The canonical path is segmentation, then measurement, in `segment_then_measure.py`; the threshold sweep is a post-processing step on the same model outputs. Commands are run from this folder.

1. Train and predict (GPU recommended; the recorded weights came from a Kaggle GPU notebook running this file):

   ```
   python segment_then_measure.py
   ```

   Trains the aponeurosis and fascicle U-Nets (12 epochs each by default; `UMUD_EPOCHS=2 UMUD_MAX_PAIRS=24` gives a short smoke run on a CPU), saves `results/seg_apo.pt` and `results/seg_fasc.pt`, and writes `results/submission_segmentation.csv` with the columns `image_id,pa_deg,fl_mm,mt_mm`.

2. Threshold sweep (one model pass; every threshold pair is written at once):

   ```
   UMUD_APO_THRS=0.50 UMUD_FASC_THRS=0.30 python benchmark_lab/generate_threshold_sweep.py
   ```

   writes `results/submission_thr_a0.50_f0.30.csv`, the setting of the recorded best. The default grid is 0.40, 0.50 and 0.60 on both axes.

On Windows PowerShell, set a variable with `$env:UMUD_APO_THRS='0.50'` before the command. The data-resolution step runs when `segment_then_measure.py` is imported: without the data folders the import stops with a message listing what was searched, so the sweep needs the data in place even for inference. Data-free checks: `python -c "import metric"` and `python benchmark_lab/generate_synthetic_geometry.py --n 2 --out-dir <folder>`.

## Environment

Python 3.13 with torch 2.12.0 (CPU build locally, CUDA on Kaggle), torchvision 0.27.0, segmentation-models-pytorch 0.5.0, albumentations 2.0.8, opencv-python-headless 4.13.0.92, numpy 2.4.6, pandas 3.0.3, scikit-image 0.26.0, Pillow 12.2.0 and openpyxl 3.1.5 (for the benchmark spreadsheet). `scale_ocr.py` additionally needs easyocr. These are the versions pinned in this folder's `requirements.txt` (install with `python -m pip install -r requirements.txt` from this folder) and installed locally; the weights were trained on Kaggle's GPU image, whose package versions were not recorded.

## Repository hygiene

`data/`, `results/`, trained weights, human labels, OCR caches and generated review artifacts are not tracked. Track a derived file only after checking it for private content and deciding to publish it deliberately.
