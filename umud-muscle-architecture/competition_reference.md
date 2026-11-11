# Ultrasound measurements

The [UMUD competition](https://www.kaggle.com/competitions/umud-challenge-muscle-architecture-in-ultrasound-data) asks for three measurements from each B-mode ultrasound image.

| Quantity | Definition | Error tolerance |
|---|---|---|
| Pennation angle (PA) | Angle between a fascicle and the deep muscle boundary | 6 degrees |
| Fascicle length (FL) | Length along the fascicle between the superficial and deep muscle boundaries | 12 mm |
| Muscle thickness (MT) | Perpendicular distance between the boundaries | 3 mm |

The metric averages the three tolerance-normalised absolute errors. Small median-error and RMSE terms break ties. [metric.py](metric.py) implements this calculation.

## Image scale

Numbered depth rulers and edge ticks convert pixel distances to millimetres. The images have several scanner layouts, so a ruler reader must identify the actual tick marks rather than infer scale from image dimensions. The gain-compensation curve is a different display element.

The early experiments used readers for left, right and bottom rulers, plus instrument-specific fallback scales. A family-B scale correction from 134.5 to 147 pixels per centimetre improved the measurements.

## Labels and validation

The training data contain 1,048 aponeurosis and 2,761 fascicle image-mask pairs. Scalar measurements were evaluated separately, using a 35-image expert benchmark and competition submissions.

The reference annotations use visible fascicles and muscle boundaries. Fascicle length may require extending a visible segment to the boundaries. A bright lower structure can also be bone, so selecting the correct pair of boundaries matters.

The 309 test images include devices, muscles and subjects beyond the training set. Related images should stay together when forming validation groups.

[Experiment sequence](JOURNEY.md) · [Method and model sources](../PROVENANCE.md)
