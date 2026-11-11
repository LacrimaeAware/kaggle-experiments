# Experiment 06: stacked ensemble with threshold calibration

## Question

Whether a five-model tree ensemble with a balanced logistic meta-model and threshold calibration improves on the single-LightGBM first attempt (out-of-fold balanced accuracy 0.9640, public leaderboard 0.96523).

## Setup

- Full training set (577,347 rows), 5-fold StratifiedKFold (seed 42), out-of-fold balanced accuracy.
- Base zoo: balanced LightGBM (500 trees), an unbalanced LightGBM (700 trees, different params, for diversity), XGBoost (balanced via sample weights), CatBoost (balanced), HistGradientBoosting (balanced). The two categoricals were ordinal-encoded into a single numeric matrix shared by all bases.
- Stack: features are the concatenated log-probabilities of each base's out-of-fold predictions; meta-model is LogisticRegression(class_weight=balanced).
- Threshold calibration: differential evolution over three per-class multipliers (bounds 0.1 to 5), maximizing balanced accuracy.
- Validation: base out-of-fold via the fold CV; the meta-model fit via CV over the stack features; the thresholds fit on disjoint out-of-fold rows. The final output file fits meta and thresholds on all out-of-fold rows and applies them to the test set.
- Code: experiments6.py.

## Results

| component | OOF bal_acc |
|---|---|
| base lgb_bal (500 trees) | 0.96518 |
| base lgb_unbal | 0.95469 |
| base xgb | 0.96396 |
| base cat | 0.95682 |
| base hgb | 0.96424 |
| meta (balanced logreg stack) | 0.96596 |
| meta + threshold calibration | 0.96591 |
| first attempt (single LightGBM, ~1700 trees, early-stopped) | 0.96400 |

Final threshold weights: approximately (3.6, 3.8, 3.4), near-uniform. Delta of the stack over the first attempt: +0.00196 out-of-fold. This out-of-fold comparison is the measured result of the experiment.

Public leaderboard: a score of 0.96659 for this stack was recorded in the project ledger on 2026-06-08; the submission record was not kept, and the Outputs section written the same day listed the file as not submitted. The two statements were committed together, so the repository history does not settle whether the file was uploaded. The baseline's 0.96523 comes from a submission recorded on 2026-06-08.

## Findings

1. The stack reached 0.96596 out-of-fold, +0.00196 over the first attempt.
2. The revised balanced LightGBM scored 0.96518, about +0.0012 over the first attempt. It used 500 fixed trees and ordinal-encoded categories. The five-model stack added a further +0.0008.
3. Threshold calibration changed the score from 0.96596 to 0.96591, with near-uniform weights.
4. CatBoost (0.95682) and the unbalanced LightGBM (0.95469) were the weak bases. The balanced LightGBM, HistGradientBoosting, and XGBoost cluster at 0.964 to 0.965.


## Caveats

- The categoricals were ordinal-encoded into a single numeric matrix for all bases, a minor simplification versus native categorical handling, applied consistently.
- Each base model used one configuration.

## Outputs

`results/submission_stack.csv` (ignored by git). The local copy has sha256 `d1004141ec933262bec2f39ba363b199488647fece673ff7c84a23f8526eb84e`, 247,435 rows, written 2026-06-08 18:00. Whether this file was uploaded is not recorded.

## Run

```
python experiments6.py
```
