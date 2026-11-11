# Stellar classification: method and results

## Task

Predict GALAXY, QSO (quasar) or STAR from sky coordinates, five photometric magnitudes, redshift and two categorical fields. Balanced accuracy is the mean recall across the three classes.

## Comparison

The experiments used five stratified folds over 577,347 training rows, with seed 42. Comparisons reused these folds. Learned transforms were fitted on the training part of each fold.

The baseline used LightGBM with balanced class weights and native categorical features. Early screens tested colour indices, spectral features, PCA, nearest-neighbour features and probability thresholds. The final stack retained the ten raw features, with ordinal-encoded categoricals.

Five base models supplied out-of-fold log-probabilities: balanced and unbalanced LightGBM, XGBoost, CatBoost and HistGradientBoosting. A balanced logistic regression model combined these predictions. Per-class threshold calibration used disjoint out-of-fold rows.

## Results

All scores below are out-of-fold balanced accuracies from the June 8 experiments. Higher is better.

| Model | Score |
|---|---:|
| Original LightGBM | 0.9640 |
| Revised LightGBM | 0.96518 |
| Five-model stack | 0.96596 |
| Stack with threshold calibration | 0.96591 |

The revised single model supplied most of the gain. Combining models added a smaller improvement, and threshold calibration slightly reduced the score.

The baseline used its validation folds for early stopping. Each base model in the stack used one configuration.

## Data

The [competition](https://www.kaggle.com/competitions/playground-series-s6e6) supplied 577,347 training rows and 247,435 test rows. The training class proportions were about 65% galaxy, 20% quasar and 14% star. Balanced accuracy prevents the largest class from dominating the metric.

[Experiment sequence](JOURNEY.md) · [Component scores and stacking setup](experiments/06_stacked_ensemble/stacked_ensemble.md) · [Code](README.md#code)
