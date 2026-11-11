# Stellar classification experiments

## Question

How do feature engineering and model stacking change a LightGBM classifier’s validation score? The Kaggle Playground Series S6E6 task predicts GALAXY, QSO or STAR from sky coordinates, five photometric magnitudes, redshift and two categorical fields. Balanced accuracy is the mean recall across the three classes.

## Approach

The experiments below were recorded on 2026-06-08. They use five-fold stratified out-of-fold validation with seed 42. Experiments 01 to 04 use stratified subsamples; the baseline and experiment 06 use all 577,347 training rows. Comparisons reuse fold splits, and learned feature transforms are fitted on each training fold.

## Experiments

**Baseline ([baseline.py](baseline.py)).** Out-of-fold balanced accuracy 0.9640, per-fold 0.9632 to 0.9645. Public leaderboard 0.96523 from a submission recorded on 2026-06-08; the hash of the submitted file was not recorded at the time. The public score was 0.0012 above the out-of-fold score.

**01 Feature screen** (250,000 rows). Thirteen engineered feature sets added to the ten raw features: adjacent and all-pair colour indices, SED moments (skew, kurtosis), second-difference spectral curvature, centred bands, redshift transforms and redshift-colour interactions, per-fold PCA, a per-fold Gaussian-mixture density, and a Gaussian-noise null. The best change (per-fold PCA) was +0.00018, with fold standard deviation about 0.0020. The Gaussian-noise null scored -0.00119 and the 27-feature combination -0.00082.

**02 Capacity, neighbours and thresholds** (200,000 rows). Seed variation: the baseline under fold seeds 42, 1 and 7 scored 0.9625, 0.9620 and 0.9625, standard deviation 0.0002. Model capacity (1,500 trees, 255 leaves, learning rate 0.03) scored -0.00595, a lower score. kNN neighbour features (k = 50, fitted per training fold) scored -0.00053, a lower score. Per-class probability thresholds fitted on 60% of the out-of-fold rows and evaluated on the other 40% returned the identity weights and no change, with the caveat that the Nelder-Mead search may have stalled on a piecewise-constant objective.

**03 Physics-motivated features and diagnostics** (200,000 rows). The stellar-locus distance scored -0.00050, a UV-excess indicator -0.00015, both together -0.00035. QSO recall was the highest of the three classes (0.9727, against GALAXY 0.9568 and STAR 0.9579), the errors concentrated on the galaxy/star boundary (3,861 galaxies labelled star, 1,033 stars labelled galaxy), and redshift carried 0.554 of the feature-importance gain, more than the five magnitudes together. A grid recheck of the thresholds gave -0.00008 on the evaluation split. Sky position carried 0.056 of the importance, possibly reflecting a generation artifact.

**04 Model diversity** (200,000 rows). An untuned CatBoost scored -0.00738; an even blend with LightGBM -0.00142; the grid search over blend weights put the optimum at weight 1.0 on LightGBM. Only one configuration per model was tested.

**05 Full-scale tuning and seed bagging** (full data). More trees with early stopping, three-seed bagging and one alternative hyperparameter set were compared on the baseline's folds. The run was stopped before completion; no result was recorded. In experiment 06, balanced LightGBM used a fixed 500 trees and scored 0.96518, against the original 0.9640 with about 1,700 early-stopped trees.

**06 Stacked ensemble with threshold calibration** (full data, [experiments6.py](experiments6.py), [note](experiments/06_stacked_ensemble/stacked_ensemble.md)). Five base models (balanced LightGBM, an unbalanced LightGBM for diversity, XGBoost, CatBoost, HistGradientBoosting) on ordinal-encoded categoricals; a balanced logistic-regression meta-model on the concatenated out-of-fold log-probabilities; differential-evolution threshold calibration on disjoint out-of-fold rows. Components: balanced LightGBM 0.96518, unbalanced LightGBM 0.95469, XGBoost 0.96396, CatBoost 0.95682, HistGradientBoosting 0.96424; meta 0.96596; meta plus thresholds 0.96591. The stack gained +0.00196 over the first attempt, of which about +0.0012 was the tighter single configuration and about +0.0008 the ensemble; calibration used near-uniform weights and slightly reduced the score. Public leaderboard: a score of 0.96659 for this stack was recorded in the project ledger on 2026-06-08; the submission record was not kept, and the experiment note written the same day lists the output file as not submitted.

## Validation and score records

[Detailed results](writeup.md) include the public-score records and local output hashes.

Early stopping uses each baseline validation fold, so its validation estimate is mildly optimistic. Experiment 06 tested one configuration per base model. A further comparison would reserve an evaluation split before selecting more models or features.

[Baseline code](baseline.py) · [Ensemble code](experiments6.py) · [Experiment 06](experiments/06_stacked_ensemble/stacked_ensemble.md) · [Setup](README.md)
