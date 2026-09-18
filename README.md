# Kaggle experiments

Two Kaggle competition studies, each with its own input, code and output locations, a writeup or ledger of the recorded results, and a statement of which scores have a kept submission record.

## Studies

| Study | Task and method | Recorded result | Start here |
|---|---|---|---|
| Stellar classification (`predicting-stellar-class/`) | Three-class tabular classification (Playground Series S6E6). LightGBM baseline; five-fold stratified out-of-fold stack of LightGBM, XGBoost, CatBoost and HistGradientBoosting with a balanced logistic meta-model. | Out-of-fold balanced accuracy 0.96596 for the stack (0.96591 after threshold calibration) and 0.9640 for the baseline. Public scores: baseline 0.96523 (submission recorded 2026-06-08); stack 0.96659 (ledger entry of 2026-06-08, submission record not kept). | [README](predicting-stellar-class/README.md), [writeup](predicting-stellar-class/writeup.md) |
| Muscle ultrasound (`umud-muscle-architecture/`) | Pennation angle, fascicle length and muscle thickness from B-mode ultrasound images (UMUD Challenge). Two U-Nets for aponeurosis and fascicle masks, line fitting on the masks, pixel-scale recovery from the on-image rulers. | Public UMUD score 0.45615 (recorded best, lower is better; provenance in `docs/SUBMISSIONS.md`) and 0.47473 for the documented one-run reproduction. | [README](umud-muscle-architecture/README.md), [results ledger](umud-muscle-architecture/docs/RESULTS.md) |

Other competition work (a Pokemon TCG agent and a parked Spaceship Titanic study) is kept outside this repository.

## Environment

Python 3.13. Each study has its own `requirements.txt` with the versions used for the recorded runs:

```
python -m venv .venv
.venv\Scripts\Activate.ps1          # Windows PowerShell; on macOS or Linux: source .venv/bin/activate
python -m pip install -r predicting-stellar-class/requirements.txt
python -m pip install -r umud-muscle-architecture/requirements.txt
```

The stellar study runs on a CPU. The ultrasound pipeline trains on a GPU (the recorded weights came from a Kaggle GPU notebook) and runs inference on a CPU.

## Data and terms

Competition data is downloaded by a registered participant under each competition's rules into the study's ignored `data/` folder. Nothing from the competitions, the external benchmark, the trained weights or the submission files is redistributed here. Each study README states the download step and the data layout; `umud-muscle-architecture/competition_reference.md` records that competition's rules and the declared external data. The MIT license covers the code only.

## Documents

[docs/conventions.md](docs/conventions.md) sets the writing rules; each writeup follows Question, Method, Result, Caveat, Lesson. [PROVENANCE.md](PROVENANCE.md) records how this edition was exported and which recorded scores have a saved submission record.
