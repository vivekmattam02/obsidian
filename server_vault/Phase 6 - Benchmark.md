---
tags: [phase, implementation]
---

# Phase 6 - Benchmark

**Goal**: Prove your tracker works with numbers, not just demos.

## Duration: ~3-4 days

## Two benchmarks

### 1. MOT17 (offline, standardized)
Run your tracker on MOT17's provided detections (`det.txt`). Compute metrics using `py-motmetrics`. See [[MOT17 Benchmark]] for details.

**Target numbers** (from-scratch, no deep features):
| Metric | Your target | SORT reference | ByteTrack reference |
|--------|------------|----------------|-------------------|
| MOTA | 65-75% | 74% | 80% |
| IDF1 | 55-65% | 60% | 77% |
| ID Switches | < 800 | ~600 | ~350 |

Getting within 10% of SORT is a win. You wrote everything from scratch.

### 2. Live system (your own cameras)
Record a 2-minute video of 2-3 people walking through the cameras' overlapping FOV. Manually annotate a few hundred frames (tedious but necessary). Run your live pipeline and compute:
- Track consistency: does each person keep the same ID the whole time?
- 3D position accuracy: measure real distances with a tape measure, compare to triangulated estimates
- Latency: timestamp from camera capture to track publication. Target < 100ms.

## What to put on the portfolio
- MOTA/IDF1 numbers on MOT17
- A side-by-side video: raw camera feed with bboxes | BEV with 3D tracks
- A latency histogram showing end-to-end processing time
- Architecture diagram from [[System Architecture]]

## Comparison table for GitHub README
```
| Component | ByteTrack (library) | Ours (from scratch) |
|-----------|-------------------|-------------------|
| Kalman Filter | ✅ (filterpy) | ✅ (hand-written) |
| Hungarian | ✅ (scipy) | ✅ (scipy + custom cost matrix) |
| Mahalanobis Gating | ❌ (uses IoU) | ✅ |
| Multi-camera | ❌ | ✅ (stereo calibration + triangulation) |
| 3D tracking | ❌ | ✅ |
| MOTA | 80% | ~70% |
```

The story isn't "we beat ByteTrack." The story is "we understand everything inside ByteTrack and extended it to 3D multi-camera."
