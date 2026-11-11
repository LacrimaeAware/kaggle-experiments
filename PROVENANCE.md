# Sources

## Competitions

- [Stellar classification: Playground Series S6E6](https://www.kaggle.com/competitions/playground-series-s6e6).
- [UMUD: muscle architecture in ultrasound](https://www.kaggle.com/competitions/umud-challenge-muscle-architecture-in-ultrasound-data).

## Ultrasound methods and models

The November experiments follow [prvsiyan's geometry and texture notebook](https://www.kaggle.com/code/prvsiyan/trying-some-stuff-with-ultrasound-geometry), which combines geometric measurements with an image-texture angle estimate. Its code uses the Apache 2.0 license.

The notebook builds on [mawramusawwar's geometry and texture method](https://www.kaggle.com/code/mawramusawwar/umud-two-u-nets-texture-angle-lb-0-30652) and [watehell's training recipe](https://www.kaggle.com/code/watehell/ans-is-simple-physical-scale-u-net-geometry).

Pretrained model sources:

- [Base U-Net pair](https://www.kaggle.com/datasets/watehell/umud-r34-unet-weights), CC BY-NC-SA 4.0.
- [Five-fold U-Net pairs](https://www.kaggle.com/datasets/prvsiyan/umud-r34-5fold-unet-weights), CC BY-NC 4.0.

The earlier experiments used ResNet-34 U-Nets trained on the competition's aponeurosis and fascicle masks, with a 35-image expert benchmark for measurement comparisons.

The selected code uses the [MIT license](LICENSE). Competition data and third-party models retain their providers' terms.
