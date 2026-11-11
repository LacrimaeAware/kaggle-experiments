# Muscle measurements from ultrasound

## From images to measurements

The UMUD task predicts pennation angle, fascicle length and muscle thickness. Segmentation models mark the muscle boundaries (aponeuroses) and fibre bundles (fascicles); geometric fits turn those masks into measurements. Ruler ticks supply the pixel-to-millimetre scale.

The metric averages absolute measurement errors divided by tolerances of 6 degrees, 12 mm and 3 mm. Lower is better.

## Early measurement experiments

The first pipeline used two ResNet-34 U-Nets trained on the competition masks. Ruler readers handled several image layouts, straight-line fits estimated the boundaries and fascicles, and global calibration adjusted angle and length.

Correcting an instrument scale and choosing the pair of muscle boundaries containing the fascicle fragments improved the early results. Lowering the fascicle-mask threshold retained fainter fragments and brought the July score to 0.45615.

| Date | Change | Public score |
|---|---|---:|
| June 9, 2026 | Initial segmentation and measurement pipeline | 0.61918 |
| June 12, 2026 | Ruler and fallback-scale changes | 0.58910 |
| June 14, 2026 | Calibration and muscle-boundary selection | 0.46041 |
| July 1, 2026 | Lower fascicle-mask threshold | 0.45615 |

## Pretrained models and robust fitting

The November experiments followed a [public geometry and texture method](https://www.kaggle.com/code/prvsiyan/trying-some-stuff-with-ultrasound-geometry). It measures predictions from a base model pair and five fold-trained pairs, then combines their measurements. It also estimates fibre angle from image texture and fits fascicle angle against depth within the muscle.

Robust fitting (Huber reweighting) reduced the influence of isolated angle outliers. The ensemble weights stayed the same.

| November 9 comparison | Public score |
|---|---:|
| Public pretrained-model ensemble | 0.30108 |
| Ensemble with robust angle-depth fit | **0.30038** |
| Excluding failed model measurements | 0.30545 |

Most of the change from July came from the public ensemble and its measurement recipe. Robust fitting gave a smaller improvement. Excluding failed model measurements worsened the score.

## Local checks and competition results

A 35-image expert benchmark helped expose measurement bugs, but it often preferred changes that worsened competition results. One fascicle-length rule improved the local comparison while moving the public score from 0.47473 to 0.49983.

The original local scorer supplied the correct ruler scale and adjusted mean fascicle length to the labels. That concealed calibration errors. Removing the adjustment still left a mismatch between the small benchmark and the competition images.

The test images also include new devices, muscles and related frames. Those differences make image grouping and the choice of validation examples important when comparing models.

[Measurement definitions](competition_reference.md) · [Model and method sources](../PROVENANCE.md) · [Code examples](README.md#code)
