# Stellar classification

Predicting stars, galaxies and quasars in [Kaggle Playground Series S6E6](https://www.kaggle.com/competitions/playground-series-s6e6).

[View the study](https://lacrimaeaware.github.io/kaggle-experiments/stellar.html) · [Experiments](JOURNEY.md) · [Method and results](writeup.md)

The experiments compare feature engineering and model combinations using five-fold balanced accuracy. A revised LightGBM reached 0.96518; combining five tree models with logistic regression reached 0.96596.

## Code

| File | Example |
|---|---|
| [baseline.py](baseline.py) | LightGBM, stratified folds and out-of-fold predictions |
| [experiments6.py](experiments6.py) | Five-model stack and per-class threshold calibration |
| [eda.py](eda.py) | Class proportions, feature types and missing values |

<details>
<summary>Running the code</summary>

Use Python 3.13 and the packages in [requirements.txt](requirements.txt). Place the competition's `train.csv` and `test.csv` in `data/`.

```sh
python -m pip install -r requirements.txt
python eda.py
python baseline.py
python experiments6.py
```

The modelling scripts write `id,class` predictions under `results/`. `python baseline.py --limit 20000` runs a smaller setup example; the comparison above uses all 577,347 training rows.

</details>
