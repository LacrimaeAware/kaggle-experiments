# Provenance

This repository is a public edition exported on 2026-09-17 from a private working repository that holds several Kaggle competition studies with their exploratory experiments and working notes. The export started from a consolidated commit of that repository and copied selected files; the history here is new.

## Included

- `predicting-stellar-class/`: the two run paths (`baseline.py`, `experiments6.py`), the data inspection script, the writeup, the experiments index and the note for the stacked ensemble.
- `umud-muscle-architecture/`: the segment-then-measure pipeline and the modules it imports, the inference and threshold-sweep scripts, the metric, the benchmark scorers, a data-free synthetic-geometry check, the results ledger, the submission log with its provenance record, the competition reference and the verified-facts ledger.
- Root: this file, the README, the MIT license and the documentation conventions.

## Left out

Exploratory experiment scripts and their notes, dated working logs, hand-off and strategy notes, hygiene audits, labeling and review tooling with its web interfaces, notebooks, data, trained weights, submission files, and two other competition folders (a Pokemon TCG agent and a parked Spaceship Titanic study). The stellar experiments 01 to 05 and the UMUD experiment series appear only as outcomes in the included indexes and ledgers.

## Recorded scores and their records

| Study | Score | Record |
|---|---|---|
| Stellar, baseline | public balanced accuracy 0.96523 | submission recorded on 2026-06-08 in the project journal; the submitted file's hash was not recorded |
| Stellar, stack | public balanced accuracy 0.96659 | ledger entry of 2026-06-08; no submission record was kept, and the same-day experiment note listed the output file as not submitted. The measured result of the experiment is the out-of-fold score 0.96596 |
| UMUD, best | public UMUD score 0.45615 | recorded on 2026-07-01 in the project ledgers; generator, pipeline commit, weights and output hash are reconstructed in `umud-muscle-architecture/docs/SUBMISSIONS.md`; the upload itself is not independently confirmed |
| UMUD, reproduction | public UMUD score 0.47473 | recorded on 2026-06-15 in the project ledgers for one `local_infer.py` run; the output file's hash was not recorded at the time |

Developed with AI assistance; experiment choices, validation comparisons and the claims in these documents are the author's.
