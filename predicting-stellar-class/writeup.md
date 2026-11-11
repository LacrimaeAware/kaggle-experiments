# Predicting Stellar Class (playground-series-s6e6)

Kaggle Playground Series, Season 6 Episode 6. https://www.kaggle.com/competitions/playground-series-s6e6
Deadline 2026-06-30.

## Question

Predict `class`, the type of an astronomical object, one of GALAXY, QSO (quasar), or STAR. One row is one object, described by sky coordinates (alpha, delta), five-band photometric magnitudes (u, g, r, i, z), redshift, and two categorical fields (spectral_type, galaxy_population). The metric is balanced accuracy, the mean of per-class recall, which weights each of the three classes equally regardless of how common the class is.

## Method

Baseline: LightGBM multiclass (objective multiclass, three classes) with 5-fold StratifiedKFold cross-validation on the class label and balanced class weights (LightGBM class_weight balanced). The two categorical fields (spectral_type, 4 values; galaxy_population, 2 values) are passed as pandas category dtype; the eight numeric fields are used as is. The score is out-of-fold balanced accuracy, which mirrors the competition metric. The submission file uses the mean test-set class probabilities across the five folds, with the predicted label as the argmax. Code in baseline.py.

Experiments 01 to 04 tested engineered features and per-class thresholds. Experiment 06 retained the ten raw features. The latest recorded model is the experiment 06 stack: LightGBM, XGBoost, CatBoost, and HistGradientBoosting base models with a balanced logistic-regression meta-model on out-of-fold log-probabilities. It uses the 10 raw features with ordinal-encoded categoricals. Threshold calibration was tested and added no out-of-fold gain. See [experiment 06](experiments/06_stacked_ensemble/stacked_ensemble.md) for the setup and component scores. Code in experiments6.py.

## Result

The measured results are out-of-fold balanced accuracies on the 577,347 training rows (5-fold StratifiedKFold, seed 42). The stack reached 0.96596 before threshold calibration and 0.96591 after it. The baseline reached 0.9640, with per-fold scores from 0.9632 to 0.9645.

Public leaderboard scores are recorded as follows. The baseline's 0.96523 comes from a submission recorded on 2026-06-08; the hash of the submitted file was not recorded at the time. The stack's 0.96659 was recorded in the project ledger on 2026-06-08; the submission record was not kept, and the experiment note written the same day lists the output file as not submitted. The local output files are `results/submission_lgbm_baseline.csv` (sha256 `544ff1e7ca87dcdfaebf06c4967dc1c885b8b2d37809d1a5fce0a5cd9c3d7278`, written 2026-06-08 16:19) and `results/submission_stack.csv` (sha256 `d1004141ec933262bec2f39ba363b199488647fece673ff7c84a23f8526eb84e`, written 2026-06-08 18:00), each 247,435 rows. Which file, if any, was uploaded for the stack is not established by the records in this repository.

| Model | Features | Local OOF | Public LB |
| --- | --- | --- | --- |
| LightGBM multiclass, 5-fold, balanced weights (baseline.py) | 10 raw (8 numeric, 2 categorical) | 0.9640 | 0.96523 (submission recorded 2026-06-08; file hash not recorded) |
| Stacked GBDT zoo + balanced-logreg + thresholds (experiment 06, experiments6.py) | 10 raw | 0.96596 before thresholds; 0.96591 after | 0.96659 (ledger entry 2026-06-08; submission record not kept) |

## Caveat

The baseline out-of-fold balanced accuracy uses early stopping on each validation fold, which makes it mildly optimistic as an estimate of generalization. The public leaderboard score is computed on a subset of the test set. The stack's public score rests on a ledger entry without a kept submission record, so the comparison that stands on measured evidence is the out-of-fold one: 0.96596 against 0.9640. The stack results come from the single configuration per base model documented in experiment 06.

## Lesson

The strongest recorded gain came from revising the model ensemble, rather than adding the tested engineered features. Experiment 06 combined diverse tree models through a logistic-regression stack and reached 0.96596 OOF balanced accuracy before threshold calibration; threshold calibration reduced that score slightly to 0.96591.

The saved results support that comparison for these runs. A useful follow-up would fix a held-out evaluation split before further feature or model selection, then compare the revised LightGBM configuration with the full stack. The experiments in order, with the seed-variation check and the out-of-fold versus public-score distinction, are in [JOURNEY.md](JOURNEY.md).

## Data

- Metric: balanced accuracy, as stated on the competition's Evaluation page.
- train.csv: 577,347 rows, 12 columns. test.csv: 247,435 rows, 11 columns.
- Target `class` distribution in train: GALAXY 0.654, QSO 0.203, STAR 0.143. Imbalanced across three classes.
- No missing values in train.
- Columns: id, alpha, delta, u, g, r, i, z, redshift, spectral_type (categorical), galaxy_population (categorical), class (target).
