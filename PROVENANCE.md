# Provenance

This repository is a journey edition, exported on 2026-09-17 from a private working repository that holds several Kaggle competition studies with their exploratory experiments and working notes. A journey edition presents what was asked, tried, shown and learned, with dated results; it is not a runnable reproduction of the recorded scores. The export started from a consolidated commit of the private repository and copied selected files; the history here is new.

## Included

- `predicting-stellar-class/`: the journey, the writeup, the experiments index with the experiment 06 note, the two run paths (`baseline.py`, `experiments6.py`) and the data inspection script (`eda.py`). These scripts run on a CPU once the competition data is downloaded.
- `umud-muscle-architecture/`: the journey; the author's modules that illustrate the techniques it names (the metric, scale recovery from the on-image rulers, mask geometry, the synthetic geometry check, the benchmark scorer with its consensus helper); the reference pipeline `segment_then_measure.py` and the threshold sweep that produced the recorded best, kept because the provenance record names them and marked as needing the competition data and the private weights; the results ledger, the submission log with its provenance record, the competition reference and the verified-facts ledger.
- Root: this file, the README, the MIT license and the documentation conventions.

## Not included, by design

| What | What it is | Where it lives | Why it is out |
|---|---|---|---|
| Submission files | the CSVs uploaded to Kaggle, including the files behind the recorded best scores | the private repository's ignored `results/` folders and the author's local copies | competition outputs, not a technique; where their identity (size, rows, hash, date) was kept it is recorded in `umud-muscle-architecture/docs/SUBMISSIONS.md` and `predicting-stellar-class/writeup.md` |
| Competition data and the external benchmark | the ultrasound training images and masks, the 309 test images, the 35-image expert benchmark spreadsheet and images; the stellar `train.csv` and `test.csv` | downloaded by a registered participant into ignored `data/` folders | redistribution is governed by the competition rules and the providers' terms, which are not recorded here (`umud-muscle-architecture/competition_reference.md`, section 11) |
| Trained weights | `seg_apo.pt` and `seg_fasc.pt`, 97.9 MB each, trained on 2026-06-09 | the private repository's ignored `results/` folder | binary artifacts of one training run whose configuration was never fully recorded; their sizes and hashes are in the submission log |
| Day-to-day experiment logs | for the ultrasound study, the append-only submission ledger, the findings registry with status tags, the handoff and strategy notes, the test-gate findings, 41 dated experiment notes and about 100 experiment scripts; for the stellar study, the notes and scripts of experiments 01 to 05; the project journal | the private repository | working records written for the author on the day. Each journey quotes every result it relies on with its date and the ledger's name, and the ledgers exported here (`VERIFIED_FACTS.md`, `docs/RESULTS.md`, `docs/SUBMISSIONS.md`) carry the decision-driving facts |
| Pipeline drivers and tooling | the inference driver, the standalone trainer and the benchmark runner for the U-Nets; labelling and review web interfaces; notebooks; hand-made labels; OCR caches; hygiene audits | the private repository | they exist to run the full competition pipeline on the data and illustrate nothing on their own |
| Other competition folders | a Pokemon TCG agent and a parked Spaceship Titanic study | the private repository | not selected for this edition |

## Recorded scores and their records

| Study | Score | Record |
|---|---|---|
| Stellar, baseline | public balanced accuracy 0.96523 | submission recorded on 2026-06-08 in the project journal; the submitted file's hash was not recorded |
| Stellar, stack | public balanced accuracy 0.96659 | ledger entry of 2026-06-08; no submission record was kept, and the same-day experiment note listed the output file as not submitted. The measured result of the experiment is the out-of-fold score 0.96596 |
| UMUD, best | public UMUD score 0.45615 | recorded on 2026-07-01 in the project ledgers; generator, pipeline commit, weights and output hash are reconstructed in `umud-muscle-architecture/docs/SUBMISSIONS.md`; the upload itself is not independently confirmed |
| UMUD, reproduction | public UMUD score 0.47473 | recorded on 2026-06-15 in the project ledgers for one run of the private inference script `local_infer.py`; the output file's hash was not recorded at the time |
| UMUD, trajectory | public scores from 0.61918 (2026-06-09) to 0.45615 (2026-07-01), listed in `umud-muscle-architecture/JOURNEY.md` | each carries the submission date recorded in the private experiment log; the intermediate submission files were not hashed at the time |

Developed with AI assistance; experiment choices, validation comparisons and the claims in these documents are the author's.
