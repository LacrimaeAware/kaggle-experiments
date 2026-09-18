# Kaggle experiments

Two Kaggle competition journeys: what was asked, what was tried, what it showed and what was learned, with every recorded result dated and tied to the ledger that holds it. This is a portfolio record, not a product. The code kept here is the author's own where it illustrates a technique the journeys name; the full pipelines, the submissions, the data and the trained weights stay out ([PROVENANCE.md](PROVENANCE.md) says what they are, where they live and why).

## Studies

| Study | Question and approach | Recorded result | Start here |
|---|---|---|---|
| Stellar classification (`predicting-stellar-class/`) | Three-class tabular classification (Playground Series S6E6), metric balanced accuracy. A LightGBM baseline, a noise floor measured before judging anything, four screening experiments, then a five-model GBDT stack with a balanced logistic meta-model. | Out-of-fold balanced accuracy 0.96596 for the stack (0.96591 after threshold calibration) and 0.9640 for the baseline. Public scores: baseline 0.96523 (submission recorded 2026-06-08); stack 0.96659 (ledger entry of 2026-06-08, submission record not kept). | [Journey](predicting-stellar-class/JOURNEY.md), then the [writeup](predicting-stellar-class/writeup.md) and the [README](predicting-stellar-class/README.md) |
| Muscle ultrasound (`umud-muscle-architecture/`) | Pennation angle, fascicle length and muscle thickness from B-mode ultrasound images (UMUD Challenge), metric a tolerance-normalised MAE, lower is better. Two U-Nets for aponeurosis and fascicle masks, line fitting on the masks, pixel scale read from the on-image rulers, calibration constants and mask thresholds set from leaderboard probes. | Public score from 0.61918 (2026-06-09) to 0.45615 (2026-07-01, the recorded best); 0.47473 for the documented single-run reproduction (2026-06-15). Provenance of the best in `umud-muscle-architecture/docs/SUBMISSIONS.md`. | [Journey](umud-muscle-architecture/JOURNEY.md), then the [README](umud-muscle-architecture/README.md) and the [results ledger](umud-muscle-architecture/docs/RESULTS.md) |

Other competition work (a Pokemon TCG agent and a parked Spaceship Titanic study) is kept outside this repository.

## Environment

Python 3.13. Each study has its own `requirements.txt` with the versions used for the recorded runs:

```
python -m venv .venv
.venv\Scripts\Activate.ps1          # Windows PowerShell; on macOS or Linux: source .venv/bin/activate
python -m pip install -r predicting-stellar-class/requirements.txt
python -m pip install -r umud-muscle-architecture/requirements.txt
```

The stellar scripts run on a CPU once the competition data is in place. The ultrasound code is reference code apart from its data-free checks (the metric, the synthetic geometry cases, the module imports); its recorded scores need the competition data, a GPU for training and the private weights, and are not reproducible from this repository.

## Data and terms

Competition data is downloaded by a registered participant under each competition's rules into the study's ignored `data/` folder. Nothing from the competitions, the external benchmark, the trained weights or the submission files is redistributed here. Each study README states the data layout; `umud-muscle-architecture/competition_reference.md` records that competition's rules and the declared external data. The MIT license covers the code only.

## Documents

[docs/conventions.md](docs/conventions.md) sets the writing rules: a journey follows question, approach, dated results, what did not help, lessons; a writeup follows Question, Method, Result, Caveat, Lesson. [PROVENANCE.md](PROVENANCE.md) records how this edition was exported, what stays private and why, and which recorded scores have a saved submission record.
