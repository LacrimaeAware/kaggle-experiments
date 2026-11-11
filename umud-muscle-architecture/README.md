# Muscle measurements from ultrasound

Experiments in segmentation, ruler recovery and geometric measurement for the [UMUD competition](https://www.kaggle.com/competitions/umud-challenge-muscle-architecture-in-ultrasound-data).

[View the study](https://lacrimaeaware.github.io/kaggle-experiments/ultrasound.html) · [Experiment sequence](JOURNEY.md) · [Measurement definitions](competition_reference.md)

The task predicts pennation angle, fascicle length and muscle thickness from ultrasound images. Early experiments fitted lines to segmentation masks and read the image rulers. November experiments used a public pretrained-model ensemble, image texture and a robust angle-versus-depth fit.

The public score reached **0.30038 on November 9, 2026**, compared with 0.30108 for the public ensemble and 0.45615 for the July pipeline. Lower is better.

## Code

| Example | Technique |
|---|---|
| [metric.py](metric.py) | Tolerance-normalised error for the three measurements |
| [scale_ticks.py](scale_ticks.py), [subpixel_spacing.py](subpixel_spacing.py) | Ruler detection and pixel-to-millimetre conversion |
| [mask_geometry.py](mask_geometry.py) | Boundary and fascicle fits |
| [Synthetic geometry](benchmark_lab/generate_synthetic_geometry.py) | Generated bands and fibre fragments with known measurements |
| [segment_then_measure.py](segment_then_measure.py) | The earlier U-Net training and measurement pipeline |

<details>
<summary>Running the measurement examples</summary>

Use Python 3.13 and the packages in [requirements.txt](requirements.txt).

```sh
python -m pip install -r requirements.txt
python benchmark_lab/generate_synthetic_geometry.py --n 2 --out-dir results/synthetic-geometry
```

The synthetic examples generate image masks, their target measurements and scores. The segmentation pipeline uses the competition images and trained weights; its settings are the `UMUD_*` variables at the top of the file. OCR is optional and uses easyocr.

</details>

[Method and model sources](../PROVENANCE.md#ultrasound-methods-and-models)
