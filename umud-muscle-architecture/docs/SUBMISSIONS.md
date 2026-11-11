# UMUD submission records

Recorded public results through 2026-07-01. Lower is better. The best recorded score is 0.45615 at fascicle threshold 0.30 and aponeurosis threshold 0.50. The documented single-run result is 0.47473.

| public score | submission | what it is |
|---:|---|---|
| **0.45615** | `submission_thr_a0.50_f0.30.csv` | fasc mask thr 0.30 (apo 0.50) |
| 0.45669 | `submission_thr_a0.60_f0.30.csv` | apo 0.60 + fasc 0.30 |
| 0.46041 | `submission_bandfix_flx105.csv` | family_b scale + band fix + PA+2.5 + FL x1.05 |
| 0.47200 | `submission_thr_a0.60_f0.50.csv` | apo 0.60 only (MT up) |
| 0.46076 | (aponeurosis band fix) | pick the apo pair fascicles sit between |
| 0.46314 | `submission_fam_pos_weight.csv` | downweight apo-hugging fascicles |
| 0.46686 | `submission_bandfix_flx105_paDown1.5.csv` | PA lowered 1.5 |
| 0.47473 | `submission_reproduced.csv` | median pipeline, one run |
| ~0.488 | (family_b scale 134.5->147 px/cm) | per-image scale constant fix |
| 0.48369 | `submission_flx110_on_best.csv` | FL x1.10 |
| 0.48730 | `submission_fam_top_robusttri.csv` | bent superficial aponeurosis |
| 0.49983 | `submission_minextrap.csv` | min-extrapolation FL mode |
| 0.51435 | `submission_fam_curved.csv` | curved deep aponeurosis |
| 0.53395 | `submission_mtx095_on_best.csv` | MT x0.95 |
| 0.55033 | (PA +2.5, 0.55-era) | global PA shift |
| 0.58910 | (shape-neighbor fallback scale) | |
| 0.60961 | (temporal smoothing of outputs) | median PA/FL/MT within clips |
| 0.61918 | (scale router + inner MT + fragment FL) | first wired pipeline |

## Best-result provenance

The file and pipeline record was reconstructed on 2026-09-17. Missing upload and training-run records are identified in the table.

| item | record |
|---|---|
| Public score | 0.45615, recorded on 2026-07-01 in the project's experiment log, `docs/RESULTS.md`, `VERIFIED_FACTS.md` and this log |
| Output file | `results/submission_thr_a0.50_f0.30.csv`: 11,114 bytes, 309 rows plus header, file date 2026-07-01 14:23, sha256 `fd81b41faa851f42157b198a6b1c1210c794eb40262ee7d88fe8caeb630c117c`. Local copy, ignored by git |
| Generator | `benchmark_lab/generate_threshold_sweep.py`, added in `07fc392` (2026-07-01); env-configurable grids in `acca15d`; CSV-first fix in `a3c4b6d` (last change to the file) |
| Invocation | `UMUD_APO_THRS=0.50 UMUD_FASC_THRS=0.30 python benchmark_lab/generate_threshold_sweep.py` from the study folder. Reconstructed from the sweep script and the file name, not from a saved shell log: the default grid (0.40, 0.50, 0.60) does not contain 0.30, so the fascicle grid was set by the variable. The 14:23 file dates cover `a0.50` and `a0.60` with `f0.20`, `f0.25`, `f0.30` and `f0.35`, so the batch most likely used both threshold lists; the single-pair form above writes the same file |
| Pipeline | `segment_then_measure.py` as of `007a9c4` (2026-07-01), the last commit touching it, imported by the generator. Effective settings: band fix on (`UMUD_BAND_FIX` default 1), `PA_SHIFT` 2.5 added by the generator, FL recentred to the prior mean and multiplied by 1.05 in the generator's `finalize()`, TTA on, scale router on. `PIPELINE_VERSION` string in the file: `2026-06-14.01` |
| Weights | `results/seg_apo.pt`: 97,918,867 bytes, sha256 `4010d1399c0cdcb34191bf76ce78624355d88cd797c7f30916b2da478d91c134`. `results/seg_fasc.pt`: 97,919,663 bytes, sha256 `8878419c498819451007f533c4f5dc259a5ac9c89dcde8c42885e41bf6c6e811`. Both dated 2026-06-09 02:52; untracked local files. Training run: not recorded (no notebook run id, seed or log was kept). The configuration described as the one that produced them, in a comment of the project's training notebook: 12 epochs, U-Net, ResNet-34 encoder, image size 384, dice+BCE loss, light augmentation |
| Base lineage | the sweep reproduces the post-processing of the `0.46041` file (band fix, FL recentre, FL x1.05). The documented one-run reproduction of the same pipeline scores 0.47473; `VERIFIED_FACTS.md` attributes the remaining ~0.014 to per-row residue of the older stack that no tracked script reproduces |
| Sibling files | `results/` also holds `a0.50` with `f0.05` to `f0.35` and `a0.65` to `a0.80` with `f0.30` (dated 2026-07-01 14:42 and 22:47) without ledger rows; whether they were uploaded is not recorded |
| Upload to Kaggle | not independently confirmed. No upload identity, timestamp or file hash was recorded at submission time; the score rests on the ledger entries above |
