# Kaggle experiments

Experiments with stellar classification, muscle-ultrasound measurement and a Pokémon TCG agent.

[Project pages](https://lacrimaeaware.github.io/kaggle-experiments/).

| Study | Techniques explored | Question | Read |
|---|---|---|---|
| Stellar classification | LightGBM baseline, feature screens and a five-model tree ensemble | How do feature engineering and model stacking change a LightGBM classifier’s validation score? | [Case study](https://lacrimaeaware.github.io/kaggle-experiments/stellar.html) |
| Muscle ultrasound | U-Net segmentation, ruler-scale recovery, line fitting and calibration | Can segmentation masks support measurements of pennation angle, fascicle length and muscle thickness? | [Case study](https://lacrimaeaware.github.io/kaggle-experiments/ultrasound.html) |

[Pokémon TCG agent](https://lacrimaeaware.github.io/pokemon-tcg-agent/): rules, hidden-card search, learned models and action-effect experiments.

[Stellar code and setup](predicting-stellar-class/README.md) · [Ultrasound code and setup](umud-muscle-architecture/README.md)

Stellar scripts require the competition CSV files. Ultrasound metric and synthetic-geometry examples run without competition data; training and score reproduction require additional data and weights.

The code uses the [MIT license](LICENSE). [Data and result records](PROVENANCE.md) describe dataset terms and the limits of the recorded scores.

Generated with AI.
