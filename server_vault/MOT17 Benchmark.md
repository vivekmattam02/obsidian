---
tags: [evaluation]
---

# MOT17 Benchmark

The standard benchmark for evaluating multi-object trackers. If you're building a tracker from scratch, you need to measure it against something.

## The dataset
7 video sequences of pedestrians, filmed from static and moving cameras. Includes:
- Dense crowds (hard)
- Fast-moving people (hard)
- Occlusions (hard)
- Varying lighting

Ground truth bounding boxes with consistent IDs are provided for training sequences.

Download: https://motchallenge.net/data/MOT17/

## The metrics

**MOTA** (Multiple Object Tracking Accuracy): The headline number. Combines three error sources:
```
MOTA = 1 - (FN + FP + IDSW) / GT
```
- FN = false negatives (missed objects)
- FP = false positives (hallucinated objects)
- IDSW = identity switches (swapped two people's IDs)

Higher is better. ByteTrack gets ~80% on MOT17.

**MOTP** (Tracking Precision): Average IoU between matched tracks and ground truth. Measures localization quality.

**IDF1**: F1-score of identity preservation. "How often does the tracker maintain the correct ID?" This matters more than MOTA for applications like [[Re-Identification]].

**ID Switches**: Raw count of how many times the tracker swaps two IDs. Lower is better.

## How to evaluate
Use the official `py-motmetrics` library:
```bash
pip install motmetrics
```
```python
import motmetrics as mm
acc = mm.MOTAccumulator(auto_id=True)
# For each frame:
acc.update(gt_ids, pred_ids, distance_matrix)
# At the end:
mh = mm.metrics.create()
summary = mh.compute(acc, metrics=['mota', 'motp', 'idf1', 'num_switches'])
```

## For our project
In [[Phase 6 - Benchmark]], we run our from-scratch tracker on MOT17 and compare against:
- Raw SORT (the classic). Typical MOTA: ~74%
- ByteTrack (what you used before). Typical MOTA: ~80%

Even getting ~70% MOTA with a completely from-scratch implementation would be impressive and demonstrates you understand the fundamentals. The point isn't to beat SOTA — it's to prove you know what's inside the black box.
