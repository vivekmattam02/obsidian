---
tags: [phase, implementation]
---

# Phase 2 - Hungarian and MOT

**Goal**: Extend the single [[Kalman Filter]] to multiple objects. Implement [[Data Association]] using [[Mahalanobis Distance]] gating + [[Hungarian Algorithm]]. Add [[Track Lifecycle]] management. Test on MOT17 detections (still no hardware).

## Duration: ~1.5 weeks

## Steps
1. **Download MOT17 detections**: The dataset provides pre-computed detection files (`det.txt`) so you don't need to run YOLO yet. Each line: `frame, -1, x, y, w, h, conf, -1, -1, -1`
2. **Write the Track class**: Wraps a [[Kalman Filter]] instance + state (TENTATIVE/CONFIRMED/LOST/DEAD) + hit count + age + ID counter
3. **Write `compute_cost_matrix()`**: For each track-detection pair, compute [[Mahalanobis Distance]]. Apply gating threshold.
4. **Implement Hungarian matching**: Use `scipy.optimize.linear_sum_assignment()` — you're allowed to use this since the algorithm itself is standard (the hard part is the cost matrix and gating, which you wrote from scratch)
5. **Handle unmatched detections**: Create new TENTATIVE tracks
6. **Handle unmatched tracks**: Move to LOST, eventually DEAD
7. **Run on MOT17 `det.txt`**: Frame by frame, feed detections, output track assignments
8. **Evaluate with `py-motmetrics`**: Compute MOTA, IDF1. See [[MOT17 Benchmark]].

## Tuning knobs
- `max_age = 30` (how long to keep LOST tracks)
- `n_init = 3` (how many hits before TENTATIVE → CONFIRMED)
- `gating_threshold = 9.49` (chi-squared 95% for 4 DOF measurement)
- `Q`, `R` in the [[Kalman Filter]]

## Expected results
Honest target: **MOTA ~65-75%** on MOT17. SORT gets ~74%. If you're in that ballpark with fully from-scratch code, that's excellent.

## Deliverable
A `MultiObjectTracker` class:
```python
class MultiObjectTracker:
    def __init__(self):
        self.tracks = []
        self.next_id = 0
    def step(self, detections: list) -> list:
        # predict, associate, update, manage lifecycle
        return active_tracks
```

Next: [[Phase 3 - Stereo Calibration]]
