# Predicting Stellar Class

Kaggle Playground Series, Season 6 Episode 6 (`playground-series-s6e6`), closed 2026-06-30. The task is to predict whether an astronomical object is a GALAXY, a QSO or a STAR from its sky coordinates, five photometric magnitudes, redshift and two categorical fields. The metric is balanced accuracy. [JOURNEY.md](JOURNEY.md) tells the study in order: the baseline, experiments 01 to 06, the noise-floor lesson and the out-of-fold versus public-score distinction. The recorded results are in [writeup.md](writeup.md); the experiment records are indexed in [experiments/README.md](experiments/README.md).

## Layout

| Location | Contents |
|---|---|
| `JOURNEY.md` | the study in order: experiments 01 to 06, what each tried and showed, the lessons |
| `data/` (ignored by git) | `train.csv` (577,347 rows) and `test.csv` (247,435 rows) downloaded from Kaggle |
| `baseline.py` | canonical run A: LightGBM multiclass, 5-fold StratifiedKFold, balanced class weights |
| `experiments6.py` | canonical run B: five-model GBDT stack with a balanced logistic meta-model and threshold calibration |
| `eda.py` | prints shapes, dtypes, the target distribution and missingness |
| `experiments/` | the experiments index and the note for experiment 06; the exploratory scripts and notes for experiments 01 to 05 are kept in the private working repository |
| `results/` (ignored by git) | output files written by the scripts |

## Data

Download with the Kaggle CLI from this folder (a Kaggle account that has joined the competition is required), then extract into `data/`:

```
kaggle competitions download -c playground-series-s6e6 -p data
python -c "import zipfile,glob; [zipfile.ZipFile(z).extractall('data') for z in glob.glob('data/*.zip')]"
```

The data is used under the competition rules and is not redistributed in this repository.

## Run

From this folder, in the project environment:

```
python eda.py            # inspect the data
python baseline.py       # writes results/submission_lgbm_baseline.csv
python experiments6.py   # writes results/submission_stack.csv
```

Both modelling scripts exit with a message when `data/train.csv` is missing. They run on the CPU. Runtimes were not recorded; the full baseline takes on the order of tens of minutes and the stack takes longer. Expected outputs: `results/submission_lgbm_baseline.csv` and `results/submission_stack.csv`, each with 247,435 rows and the columns `id,class`.

## Smoke run versus recorded score

`python baseline.py --limit 20000` trains on a random 20,000-row sample of the training set (seed 42) and writes `results/submission_lgbm_baseline_smoke.csv`. It checks that the environment and the pipeline work in a minute or two; its score is not comparable with the recorded results. Reproducing the recorded out-of-fold scores (0.9640 for the baseline, 0.96596 for the stack) needs the full data and the full runs; small differences across library versions are possible. The public leaderboard figures and the state of their records are described in [writeup.md](writeup.md).

## Environment

Python 3.13.1 with numpy 2.4.6, pandas 3.0.3, scipy 1.17.1, scikit-learn 1.9.0, lightgbm 4.6.0, xgboost 3.2.0 and catboost 1.2.10, the versions pinned in this folder's `requirements.txt` and installed in the environment used for these runs. Install them with `python -m pip install -r requirements.txt` from this folder. `baseline.py` needs only numpy, pandas, scikit-learn and lightgbm; `experiments6.py` needs all seven packages.
