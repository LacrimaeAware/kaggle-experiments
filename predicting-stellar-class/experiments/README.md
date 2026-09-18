# Experiments

Index of the feature and method experiments for predicting-stellar-class. Each experiment compares against the LightGBM baseline on fixed 5-fold StratifiedKFold out-of-fold balanced accuracy, on a stratified subsample. The seed-to-seed noise floor is 0.0002 (experiment 02), so a change below about 0.0002 to 0.0004 is within noise.

The exploratory scripts and notes for experiments 01 to 05 are kept in the private working repository; this index records their outcomes. Experiment 06 is included in full (`experiments6.py` and its [note](06_stacked_ensemble/stacked_ensemble.md)).

| Experiment | Tests | Result |
|---|---|---|
| 01 feature_screen | color indices, SED moments (skew, kurtosis), spectral curvature, centered bands, redshift transforms and interactions, per-fold PCA, per-fold Gaussian-mixture density; a Gaussian-noise null | No feature set beat the baseline above noise. Best (PCA) +0.00018. Adding more columns trended toward the null. |
| 02 levers | multi-seed noise floor, model capacity, leak-free kNN neighbor features, per-class thresholds | Noise floor 0.0002. Capacity -0.00595. kNN -0.00053. Thresholds no change. |
| 03 locus_and_diagnostics | stellar-locus distance, UV-excess indicator, grid thresholds; confusion matrix, per-class recall, feature importance | Locus features -0.0005 to -0.0001. QSO recall highest (0.973); errors on the galaxy/star boundary. Redshift 0.554 of feature importance. |
| 04 model_diversity | CatBoost, LightGBM and CatBoost blend | CatBoost -0.00738 (untuned). Best blend weight 1.0 on LightGBM (no gain). |
| 05 full_scale_seedbag (experiments5.py) | full-data tuning and seed bagging of a single LightGBM | Stopped before completion; no result recorded. Effort moved to multi-model stacking (experiment 06). The script is kept in the private working repository and is not part of the run path. |
| [06 stacked_ensemble](06_stacked_ensemble/stacked_ensemble.md) | 5-model GBDT zoo, balanced-logreg stack, DE threshold calibration | OOF 0.96596, +0.00196 over the first attempt. Mostly a tighter single config (+0.0012) plus a small ensemble lift (+0.0008); calibration null (bases pre-balanced). Neural-tabular base models used by top public entries were omitted (they need a GPU). |

## Conclusion

No tested feature transform or single-model lever beat the baseline above the 0.0002 noise floor (experiments 01 to 04): within the tested set of transforms, the optical-plus-redshift features gave no further gain. The diagnostics (experiment 03) explain why: redshift carries most of the signal and makes the quasar class the easiest of the three, the residual errors fall on the galaxy/star boundary where the real discriminator is morphology (absent here), and the strongest photometry-only discriminator, infrared color, is also absent.

A model-level gain exists. The stacked GBDT ensemble (experiment 06) reached out-of-fold 0.96596, +0.00196 over the single-LightGBM first attempt (0.9640). About +0.0012 of that corrects the first attempt's tree count (it slightly overfit), and about +0.0008 is the ensemble. Threshold calibration added nothing because the base models were already balanced. Top public entries add neural-tabular base models that need a GPU; they were omitted here. Forum figures about the leaderboard's noise and ceiling were read during the competition but not recorded as sources, so they are not cited in these notes; see the Leaderboard interpretation section of the writeup.
