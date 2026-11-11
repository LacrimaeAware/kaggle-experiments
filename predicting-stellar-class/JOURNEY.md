# Stellar classification experiments

## Question

How do feature engineering and model stacking change a LightGBM classifier's validation score? The task predicts GALAXY, QSO or STAR from sky coordinates, five photometric magnitudes, redshift and two categorical fields. Balanced accuracy gives each class equal weight.

## Starting with a baseline

A LightGBM model reached 0.9640 out-of-fold balanced accuracy. Five stratified folds kept similar class proportions, and each row was predicted by a model trained on the other folds. Later comparisons reused the same splits.

## Trying additional features

Colour differences, spectral curvature, redshift interactions, PCA and density features were tested on stratified subsamples. The best change, PCA features, added 0.00018. Repeating the baseline with different fold seeds produced a standard deviation of about 0.0002, so that change was small relative to the variation between splits.

Larger trees and nearest-neighbour features reduced the score. The confusion matrix concentrated errors at the galaxy/star boundary, while redshift supplied more feature-importance gain than the five magnitudes combined.

## Combining models

An initial CatBoost blend favoured LightGBM alone. The next comparison used five tree models and trained a logistic regression model on their out-of-fold log-probabilities.

The revised LightGBM reached 0.96518; the stack reached 0.96596. Part of the improvement came from the single-model configuration, with a smaller gain from combining models. Per-class threshold calibration reduced the score slightly to 0.96591.

[Method and results](writeup.md) · [Stacking details](experiments/06_stacked_ensemble/stacked_ensemble.md) · [Code](README.md#code)
