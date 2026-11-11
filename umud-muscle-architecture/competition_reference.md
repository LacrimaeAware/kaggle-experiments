# UMUD data and measurement reference

Competition description and host clarifications recorded on 2026-06-09, with scale observations updated during June. These notes describe the study's data and measurement conventions; they are not a current competition-status page.

## 1. Task and targets

- One case = one single B-mode ultrasound image. Predict three values per image.
- **PA** (deg) = angle between the fascicle line and the **deep** aponeurosis.
- **FL** (mm) = distance between superficial and deep aponeuroses **along the fascicle line**; linear
  extrapolation is used when the fascicle runs past the image frame.
- **MT** (mm) = perpendicular distance between the two aponeuroses, measured at **3 locations** across
  the muscle width and averaged.
- Test-set physiological ranges (use as clip bounds): **PA 5-45 deg, FL 30-200 mm, MT 10-50 mm**.
- Submission columns: `image_id, pa_deg, fl_mm, mt_mm`.

## 2. Competition conditions

The recorded rules required algorithm or model development and reproducible code. External data and pretrained models had to be declared and accessible to participants. Host clarifications treated hand-created test labels as external data requiring disclosure, rather than automatically excluding that approach.

This study used the public expert benchmark and pretrained encoder weights. It did not fine-tune on hand-labelled test images. Rulers were read by eye to check device scales, and a 23-image hand-corrected set was used for diagnostics. Those uses of target-image information belong in any external-data declaration.

## 3. Scale and calibration

Pixels are square. Numbered depth rulers and bottom-edge ticks provide scale; bottom ticks on the cropped examples were recorded as 1 cm apart. The dashed gain-compensation curve is not a ruler. Full-frame images contain several device families, so image dimensions alone do not identify the appropriate scale reader.

### 3b. Recorded ruler checks

| family | n | scale | how validated |
| --- | ---: | ---: | --- |
| PNG left ruler | 58 | 150 px/cm | ruler reads 0->4 cm over ~595 px; 5 mm minor ticks (tick_mm=5 is correct - the feared 2x bug does NOT exist) |
| 644x1088 left ruler | 50 | 126 px/cm | left depth ruler 0->50 mm, 1 cm ticks ~126 px; all 50 identical |
| Telemed 800x1200 (English "De 50 mm", right text panel) | 49 | 134 px/cm | bottom ticks AND left 0->50 mm ruler independently agree (~134-140) |
| clean cropped/other | ~10 | bottom ticks | e.g. IMG_00040 -> 78 px/cm conf 0.99, green ticks land on real marks |
| German Siemens 800x1200 ("12L3 Quadriceps", left text panel) | 87 | ~136 px/cm | faint RIGHT-edge 5 mm depth ruler (not the bottom bracket). Interval pinned 3 ways: MT physiology (1cm->49mm absurd, 0.5cm->24.7mm), the "4.5 cm" depth label (ruler span ~141 vs detected 136), 4.5cm/9ticks=5mm. |
| Family-B signature 800x1200 | 41 | 134.5 px/cm | fixed left-margin UI marks identify a family whose bottom-tick scale was validated at 134.5 px/cm; this is an assigned instrument scale, not per-image ruler reading. |

The family-B value above records the initial check. It was changed from 134.5 to 147 px/cm on 2026-06-14 after further tick readings. The recorded router recovered scale for 295 of 309 rows; 14 fell back to the prior. Its method counts were right-ruler 87, bottom-ticks 59, PNG-left-ruler 58, left-ruler-1cm 50 and family-B signature 41. Coverage does not establish the correctness of every inferred scale.

## 4. Training data

- 2761 fascicle images + masks; 1048 aponeurosis images + masks; 309 test images.
- Aponeurosis images are 800 by 1200 pixels and masks 864 by 1152. The recorded pipeline resizes both to a common 384-pixel square before training.
- Masks are binarized above zero; aponeurosis masks form bands and fascicle masks contain fragments.

## 5. Annotation convention

- **Two researchers** annotated manually; their results were **averaged** per image.
- Per image they marked: superficial apo, deep apo, **3 visible fascicles, 3 pennation angles, 3
  muscle-thickness estimates** (MT at 3 width locations).
- Re-evaluated when raters disagreed by **> 10 mm FL, > 4 deg PA, > 1 mm MT** (the inter-rater bands).
- PA and FL use approximately three fascicles per image; MT uses three positions.

Only clearly visible fascicle fragments and aponeurosis portions were labelled. A bright lower structure can be bone rather than another aponeurosis. The task concerns superficial muscle measurements.

## 7. Devices and domain shift

- Train devices: Siemens Acuson Juniper, Telemed ArtUS EXT-1H, Telemed Echo Blaster 128, Hitachi Aloka
  Alpha-10, Philips HD11.
- Test devices: Siemens Acuson Juniper, Telemed ArtUS EXT-1H, **Philips Lumify** (Lumify is test-only).
- Muscles: train = Vastus lateralis, Gastrocnemius medialis/lateralis, Tibialis anterior; test = VL,
  GM, **Rectus femoris** (RF is test-only).
- Test includes **diseased (cerebral palsy)** subjects, ages 18-28, none overlapping with train.


## 11. Data and terms

What the code needs:

- The competition data from Kaggle: the aponeurosis and fascicle training images with their masks,
  and the 309 test images. A registered participant downloads them under the competition rules into
  `data/`; `segment_then_measure.py` searches for the leaf folder names (`apo_images_new_model_v1`,
  `apo_masks_new_model_v1`, `fasc_images_new_model_v1`, `fasc_masks_new_model_v1`, `test_set_v2`)
  under `data/` or `/kaggle/input`, so the nesting does not matter.
- Trained weights `results/seg_apo.pt` and `results/seg_fasc.pt` for inference
  (used by `benchmark_lab/generate_threshold_sweep.py`). `segment_then_measure.py` produces them (a Kaggle GPU notebook in the recorded runs). They are not tracked; their identity is
  recorded in `docs/SUBMISSIONS.md`.
- ImageNet-pretrained ResNet-34 encoder weights, downloaded by segmentation_models_pytorch at training
  time (`UMUD_MODEL_ENCODER_WEIGHTS=imagenet`). Inference loads the saved checkpoints with
  `encoder_weights=None`.
- Optional, for local benchmark scoring only: the public 35-image expert benchmark (OSF), read by
  `benchmark_validate.py` from `Results_benchmark_architecture*.xlsx` and
  the benchmark images under `data/`.

Files downloaded or generated separately: competition images and masks, the benchmark spreadsheet and images,
trained weights, submission CSVs, hand-made labels, OCR caches and per-image debug output. `data/`,
`results/` and `*.csv` are ignored by git.

Declared external data: the 35-image expert benchmark, used for local validation and
counted as external data; public pretrained encoder weights. The recorded submissions used no
fine-tuning on test images. The per-device-family pixel scales in `scale_ticks.py` were validated by
reading rulers on test images by eye, and a 23-image set of hand-corrected test images was used as a
diagnostic gate, not as training data; both count as human-derived information about the test set in
the host's interpretation and belong in any declaration.

Licence terms of the competition data and of the OSF benchmark are those published by their
providers. They are not recorded in this repository and should be checked before any reuse of the
data, the weights or the outputs.
