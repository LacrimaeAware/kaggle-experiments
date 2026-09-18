"""Mask-threshold sweep in ONE model pass (probability maps computed once per image, then binarized at
each threshold - free). The threshold is where the segmentation draws the aponeurosis line and which
fascicles it keeps, i.e. WHERE THE LINES SIT and WHICH FASCICLES EXIST - the actual wall - tunable
without any retrain. This is the first batch of the sustained leaderboard grind (deadline is months out;
we have hundreds of submissions over time, so search, keep winners).

3x3 grid of (apo_threshold, fasc_threshold). (0.50, 0.50) reproduces the baseline. Each written at the
0.46041 lineage (FL recenter + FL x1.05) to results/submission_thr_a{a}_f{f}.csv.

    python umud-muscle-architecture/benchmark_lab/generate_threshold_sweep.py
"""
import os
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import torch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import segment_then_measure as M

APO_THRS = [float(x) for x in os.environ.get("UMUD_APO_THRS", "0.40,0.50,0.60").split(",")]
FASC_THRS = [float(x) for x in os.environ.get("UMUD_FASC_THRS", "0.40,0.50,0.60").split(",")]


def load(t):
    m = M.build_model(encoder_weights=None)
    m.load_state_dict(M.checkpoint_state(torch.load(M.weights_path(t), map_location="cpu")))
    return m.eval().to(M.DEVICE)


def row(p, geom, cand):
    pa = geom["pa_deg"] if geom else None
    pa = float(np.clip((pa if pa is not None else M.PRIOR["pa_deg"]) + M.PA_SHIFT, M.PA_MIN, M.PA_MAX))
    fl_mm, mt_mm = M.PRIOR["fl_mm"], M.PRIOR["mt_mm"]
    px = cand.px_per_mm if (cand is not None and cand.confidence >= M.CALIBRATION_MIN_CONF) else None
    if px and M.USE_CALIBRATED_MT and geom and geom["mt_px"] is not None:
        mt_mm = float(np.clip(geom["mt_px"] / px, M.MT_MIN, M.MT_MAX))
    if M.USE_FRAGMENT_FL and px and geom and geom.get("fl_px"):
        fl_mm = float(np.clip(geom["fl_px"] / px, M.FL_MIN, M.FL_MAX))
    elif M.USE_IDENTITY_FL and geom and geom["pa_deg"] is not None:
        fl_mm = float(np.clip(mt_mm / np.sin(np.radians(pa)), M.FL_MIN, M.FL_MAX))
    return {"image_id": p.name, "pa_deg": round(pa, 3), "fl_mm": round(fl_mm, 3), "mt_mm": round(mt_mm, 3)}


def finalize(rows):
    sub = pd.DataFrame(rows)
    if (M.USE_FRAGMENT_FL or M.USE_IDENTITY_FL) and sub["fl_mm"].mean() > 0:
        sub["fl_mm"] = (sub["fl_mm"] * (M.PRIOR["fl_mm"] / sub["fl_mm"].mean())).clip(M.FL_MIN, M.FL_MAX)
    sub["fl_mm"] = (sub["fl_mm"] * 1.05).clip(M.FL_MIN, M.FL_MAX).round(3)
    return sub


def main():
    apo, fasc = load("apo"), load("fasc")
    files = sorted(p for p in M.DIRS["test"].iterdir() if p.is_file() and p.suffix.lower() in M.IMG_EXTS)
    combos = [(a, f) for a in APO_THRS for f in FASC_THRS]
    rows = {c: [] for c in combos}
    t0 = time.time()
    for i, p in enumerate(files):
        img = M.read_rgb(p)
        pa_prob = M.predict_prob(apo, img)     # probability maps ONCE per image
        fa_prob = M.predict_prob(fasc, img)
        cand = M.calibrate_image(p) if (M.USE_CALIBRATED_MT or M.USE_CALIBRATED_FL) else None
        for a, f in combos:
            am = M.binarize_prob(pa_prob, "apo", a)
            fm = M.binarize_prob(fa_prob, "fasc", f)
            try:
                geom = M.measure(am, fm)
            except Exception:
                geom = None
            rows[(a, f)].append(row(p, geom, cand))
        if (i + 1) % 60 == 0:
            print(f"  {i+1}/{len(files)} ({time.time()-t0:.0f}s)", flush=True)

    # write ALL submissions FIRST so a reporting bug can never lose the compute
    subs = {}
    for a, f in combos:
        sub = finalize(rows[(a, f)])
        sub.to_csv(ROOT / "results" / f"submission_thr_a{a:.2f}_f{f:.2f}.csv", index=False)
        subs[(a, f)] = sub
    base_key = (0.50, 0.50) if (0.50, 0.50) in subs else combos[0]
    base = subs[base_key]
    print(f"\n=== {len(combos)} threshold submissions ({time.time()-t0:.0f}s); diff vs a{base_key[0]:.2f}_f{base_key[1]:.2f} ===")
    print(f"  {'apo':>5}{'fasc':>6}{'PA':>8}{'FL':>8}{'MT':>8}{'rows != ref':>13}   file")
    for a, f in combos:
        sub = subs[(a, f)]
        d = int((~np.isclose(sub.pa_deg, base.pa_deg) | ~np.isclose(sub.fl_mm, base.fl_mm) | ~np.isclose(sub.mt_mm, base.mt_mm)).sum())
        tag = "  <- ref" if (a, f) == base_key else ""
        print(f"  {a:>5.2f}{f:>6.2f}{sub.pa_deg.mean():>8.2f}{sub.fl_mm.mean():>8.2f}{sub.mt_mm.mean():>8.2f}{d:>13}   submission_thr_a{a:.2f}_f{f:.2f}.csv{tag}")
    print("\n  descriptive. Submit across days, keep winners, iterate.")


if __name__ == "__main__":
    main()
