# Experiments

Experiments 01–04 compare feature and method changes with LightGBM on five-fold splits of stratified subsamples. Experiment 02 repeated the 200,000-row baseline with three fold seeds; its score standard deviation was about 0.0002.

Experiments 01 to 05 are summarized below. [Experiment 06](06_stacked_ensemble/stacked_ensemble.md) includes its setup, component scores and the ensemble code.

| Experiment | Tests | Result |
|---|---|---|
| 01 feature_screen | color indices, SED moments (skew, kurtosis), spectral curvature, centered bands, redshift transforms and interactions, per-fold PCA, per-fold Gaussian-mixture density; a Gaussian-noise null | Best (PCA) +0.00018. Gaussian-noise null -0.00119; 27-feature combination -0.00082. |
| 02 levers | multi-seed noise floor, model capacity, per-fold kNN neighbor features, per-class thresholds | Seed standard deviation 0.0002. Capacity -0.00595. kNN -0.00053. Thresholds no change. |
| 03 locus_and_diagnostics | stellar-locus distance, UV-excess indicator, grid thresholds; confusion matrix, per-class recall, feature importance | Locus features -0.0005 to -0.0001. QSO recall highest (0.973); errors on the galaxy/star boundary. Redshift 0.554 of feature importance. |
| 04 model_diversity | CatBoost, LightGBM and CatBoost blend | CatBoost -0.00738 (untuned). Best blend weight 1.0 on LightGBM (no gain). |
| 05 full_scale_seedbag (experiments5.py) | full-data tuning and seed bagging of a single LightGBM | Stopped before completion; no result recorded. Effort moved to multi-model stacking (experiment 06).  |
| [06 stacked_ensemble](06_stacked_ensemble/stacked_ensemble.md) | 5-model GBDT zoo, balanced-logreg stack, DE threshold calibration | OOF 0.96596, +0.00196 over the first attempt. The revised LightGBM supplied +0.0012 and the stack added +0.0008; calibration reduced the score slightly. |
