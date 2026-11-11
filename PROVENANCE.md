# Data and result records

The studies contain code, dated experiment summaries and result records. The code is licensed under MIT; competition datasets, benchmark data and pretrained models have separate terms.

## Recorded scores

| Study | Score | Record |
|---|---|---|
| Stellar, baseline | public balanced accuracy 0.96523 | submission recorded on 2026-06-08 in the project journal; the submitted file's hash was not recorded |
| Stellar, stack | public balanced accuracy 0.96659 | ledger entry of 2026-06-08; no submission record was kept, and the same-day experiment note listed the output file as not submitted. The measured result of the experiment is the out-of-fold score 0.96596 |
| UMUD, best | public UMUD score 0.45615 | recorded on 2026-07-01 in the project ledgers; generator, pipeline commit, weights and output hash are reconstructed in `umud-muscle-architecture/docs/SUBMISSIONS.md`; the upload itself is not independently confirmed |
| UMUD, reproduction | public UMUD score 0.47473 | recorded on 2026-06-15 in the project ledgers for one run of the private inference script `local_infer.py`; the output file's hash was not recorded at the time |
| UMUD, trajectory | public scores from 0.61918 (2026-06-09) to 0.45615 (2026-07-01), listed in `umud-muscle-architecture/JOURNEY.md` | each carries the submission date recorded in the private experiment log; the intermediate submission files were not hashed at the time |


## Data and weights

Stellar classification uses the Kaggle competition's `train.csv` and `test.csv`, downloaded separately. Its scripts run on a CPU.

The ultrasound study uses competition images and masks, a public 35-image expert benchmark and ImageNet-pretrained encoder weights. The competition images, benchmark files, trained checkpoints and submission CSV files are not included. Data layouts and external-data declarations are in the [competition reference](umud-muscle-architecture/competition_reference.md).

The ultrasound checkpoints were trained on 2026-06-09. Their hashes and the reconstructed invocation for the best result are in the [submission record](umud-muscle-architecture/docs/SUBMISSIONS.md). The training seed and complete run configuration were not recorded, and the best submission includes processing that no retained script fully reproduces.

## Code examples

The stellar baseline and ensemble are executable with the competition CSV files. Ultrasound examples cover the metric, synthetic geometry, ruler detection and measurements from masks. `segment_then_measure.py` and the threshold sweep document the recorded pipeline; using them requires the competition data and trained weights.

## Historical ultrasound training environment

The recorded reference pipeline used PyTorch 2.12.0, torchvision 0.27.0,
segmentation-models-pytorch 0.5.0 and albumentations 2.0.8, with Pillow 12.2.0.
These identify the earlier local environment; the Kaggle GPU image's complete
package versions were not recorded. They are not the installation requirements
for the metric and geometry examples. Those use the study's current
`requirements.txt`, including Pillow 13.0.0. OCR additionally uses easyocr.
