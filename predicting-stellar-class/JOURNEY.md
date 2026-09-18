# Predicting Stellar Class: the journey

Kaggle Playground Series, Season 6 Episode 6 (`playground-series-s6e6`). The baseline, the six experiments and the writeup were committed together on 2026-06-08; the project journal for that day records the environment setup, the pivot to this competition, the baseline run and its submission. Nothing was rerun for this document.

Unless stated otherwise, a score is out-of-fold balanced accuracy on a 5-fold StratifiedKFold split with seed 42. Experiments 01 to 04 ran on stratified subsamples with a fast fixed model; the baseline and experiment 06 ran on the full 577,347 training rows. The two public leaderboard figures are stated exactly as [writeup.md](writeup.md) records them, with the state of their records.

## Question

Predict whether an astronomical object is a GALAXY, a QSO or a STAR from sky coordinates, five photometric magnitudes, redshift and two categorical fields; the metric is balanced accuracy, the mean per-class recall. The working question of the study became: is there a lever that beats a plain gradient-boosted baseline by more than the metric's noise, and if so, of which kind?

## Approach

Baseline first ([baseline.py](baseline.py)): LightGBM multiclass, balanced class weights, early stopping per fold, out-of-fold balanced accuracy as the truth meter. Then a screening loop: one fixed fold split reused for every comparison, so each experiment is paired against the same held-out rows; a fast fixed model (350 trees, learning rate 0.05, 63 leaves) on a subsample, so a run takes minutes; a noise floor measured before any change is judged; every per-fold transformer fitted on the training fold only. Each experiment has a note with Question, Setup, Results, Findings, Caveats, Outputs and Run; the index is [experiments/README.md](experiments/README.md).

## The experiments in order

**Baseline ([baseline.py](baseline.py)).** Out-of-fold balanced accuracy 0.9640, per-fold 0.9632 to 0.9645. Public leaderboard 0.96523 from a submission recorded on 2026-06-08; the hash of the submitted file was not recorded at the time. The leaderboard sat 0.0012 above the out-of-fold score, which was read as the local score tracking the leaderboard with no sign of leakage.

**01 Feature screen** (250,000 rows). Thirteen engineered feature sets added to the ten raw features: adjacent and all-pair colour indices, SED moments (skew, kurtosis), second-difference spectral curvature, centred bands, redshift transforms and redshift-colour interactions, per-fold PCA, a per-fold Gaussian-mixture density, and a Gaussian-noise null. None beat the baseline above noise; the best (per-fold PCA) was +0.00018 against a fold standard deviation of about 0.0020, the null was worst at -0.00119, and the 27-feature combination trended toward the null (-0.00082). Reading: a tree model already splits on deterministic functions of its inputs; adding them adds dimensions, not information.

**02 Levers beyond features** (200,000 rows). The noise floor: the baseline under fold seeds 42, 1 and 7 scored 0.9625, 0.9620 and 0.9625, standard deviation 0.0002. Model capacity (1,500 trees, 255 leaves, learning rate 0.03) scored -0.00595, a real loss. Leak-free kNN neighbour features (k = 50, fitted per training fold) scored -0.00053, a small real loss. Per-class probability thresholds fitted on 60% of the out-of-fold rows and evaluated on the other 40% returned the identity weights and no change, with the caveat that the Nelder-Mead search may have stalled on a piecewise-constant objective.

**03 Physics-motivated features and diagnostics** (200,000 rows). The stellar-locus distance scored -0.00050, a UV-excess indicator -0.00015, both together -0.00035. The diagnostics reversed the prior: QSO recall was the highest of the three classes (0.9727, against GALAXY 0.9568 and STAR 0.9579), the errors concentrated on the galaxy/star boundary (3,861 galaxies labelled star, 1,033 stars labelled galaxy), and redshift carried 0.554 of the feature-importance gain, more than the five magnitudes together. A grid recheck of the thresholds gave -0.00008 on the evaluation split, confirming experiment 02. Sky position carried 0.056 of the importance although it cannot causally determine class; the note flags it as a possible generation artifact and leaves it.

**04 Model diversity** (200,000 rows). An untuned CatBoost scored -0.00738; an even blend with LightGBM -0.00142; the grid search over blend weights put the optimum at weight 1.0 on LightGBM. One configuration each, so a verdict on the untuned drop-in, not on CatBoost.

**05 Full-scale tuning and seed bagging** (full data). The first experiment to drop the subsample shortcut: more trees with early stopping, three-seed bagging and one alternative hyperparameter set, compared on the baseline's own folds. It was stopped before completion and no result was recorded; effort moved to experiment 06, whose balanced LightGBM base with a fixed 500 trees answered the tree-count question on the way (0.96518 against the first attempt's 0.9640 with about 1,700 early-stopped trees). The script stays in the private working repository and is not part of the run path.

**06 Stacked ensemble with threshold calibration** (full data, [experiments6.py](experiments6.py), [note](experiments/06_stacked_ensemble/stacked_ensemble.md)). Five base models (balanced LightGBM, an unbalanced LightGBM for diversity, XGBoost, CatBoost, HistGradientBoosting) on ordinal-encoded categoricals; a balanced logistic-regression meta-model on the concatenated out-of-fold log-probabilities; differential-evolution threshold calibration on disjoint out-of-fold rows. Components: balanced LightGBM 0.96518, unbalanced LightGBM 0.95469, XGBoost 0.96396, CatBoost 0.95682, HistGradientBoosting 0.96424; meta 0.96596; meta plus thresholds 0.96591. The stack gained +0.00196 over the first attempt, of which about +0.0012 was the tighter single configuration and about +0.0008 the ensemble; calibration added nothing (near-uniform weights) because the bases were already balanced. Neural-tabular base models used by top public entries were omitted (they need a GPU). Public leaderboard: a score of 0.96659 for this stack was recorded in the project ledger on 2026-06-08; the submission record was not kept, and the experiment note written the same day lists the output file as not submitted.

## The noise-floor lesson

The screen's within-run fold standard deviation was about 0.0020, but the right bar for comparing two out-of-fold scores is the seed-to-seed standard deviation of the same pipeline, 0.0002 (experiment 02). Against that bar the feature screen's best result (+0.00018) is indistinguishable from nothing, the pure-noise feature (-0.00119) bounds what an uninformative change does, and the real effects of experiments 01 to 04 are all losses (capacity -0.00595, kNN -0.00053, locus distance -0.00050, untuned CatBoost -0.00738). Only experiment 06 cleared the floor by an order of magnitude (+0.00196). Measuring the floor first turned a table of small deltas into one conclusion: within the tested transforms of these ten features the signal was already extracted, and the gain had to come from the model side.

## Out-of-fold score versus public score

The out-of-fold score averages over all 577,347 training rows and is the measured result of each experiment; the public leaderboard score is a single number on a subset of the test set. The two were compared once, early: baseline 0.9640 out-of-fold against 0.96523 public (submission recorded 2026-06-08). For the stack, the out-of-fold comparison (0.96596 against 0.9640) is the evidence; its public 0.96659 is a ledger entry of 2026-06-08 without a kept submission record, so the writeup presents it as such and no claim rests on it. No private score or final rank is recorded. Agreement between the two surfaces is a necessary check against leakage, not a proof of its absence, and selecting a submission by the public number would have been selecting on one noisy slice.

## Lessons

1. Estimate the noise floor before judging any change; a change below it is not evidence (0.0002 here, against a fold-level spread ten times larger).
2. Confirm the discriminative information is present before engineering features. Colour indices, SED moments, curvature, densities, neighbour features and the physically motivated locus distance all stayed within or below the floor; the discriminators that separate galaxies from stars in real surveys (morphology, infrared colour) are absent from the columns, so no transform of the optical columns could supply them.
3. Diagnose the error structure before optimising. Redshift (0.554 of the importance) made the quasar class the easiest, the opposite of the photometry-only expectation, and left the galaxy/star boundary as the residual.
4. Added capacity is not neutral: -0.00595 for a larger LightGBM, and the first attempt's roughly 1,700 early-stopped trees were themselves past the optimum (500 fixed trees scored about +0.0012 higher).
5. Ensembling reduces variance; it does not add signal. The five-model stack added about +0.0008 over its best base.
6. Metric-aligned post-processing helps only when the model is not already aligned. Per-class thresholds were null three times (experiments 02, 03 and 06) because every base used balanced class weights.
7. Select and report on the out-of-fold surface; treat the public score as one more measurement; and keep the submission record (filename and hash) at upload time, since a score without its record cannot later be upgraded to evidence.

## Sources

In this repository: [writeup.md](writeup.md), [experiments/README.md](experiments/README.md), the [experiment 06 note](experiments/06_stacked_ensemble/stacked_ensemble.md), `baseline.py`, `experiments6.py` and `eda.py`. Kept in the private working repository: the notes and scripts for experiments 01 to 05, the project journal entry of 2026-06-08 and the cross-competition lessons file.
