---
tags: [math, geometry]
---

# Stereo Geometry

When you have two cameras looking at the same scene, the geometry between them constrains where a point can be. This is epipolar geometry — the foundation of stereo vision, visual SLAM, and multi-view reconstruction.

## Epipolar constraint
If a point is at pixel `p₁` in camera 1, it *must* lie on a specific line in camera 2's image — the **epipolar line**. You don't need to search the entire image for a match, just along that line.

## The matrices
**Essential Matrix (E)**: Encodes the rotation and translation between two *calibrated* cameras.
```
p₂ᵀ · E · p₁ = 0   (in normalized coordinates)
```
E has 5 degrees of freedom (3 rotation + 2 translation direction, scale is ambiguous).

**Fundamental Matrix (F)**: Same idea but for *uncalibrated* cameras (works directly in pixel coordinates).
```
p₂ᵀ · F · p₁ = 0   (in pixel coordinates)
```
Relationship: `F = K₂⁻ᵀ · E · K₁⁻¹`

## How to estimate them
1. Find point correspondences between the two camera views (feature matching, or in our case, matching the same person's detection)
2. Use the **8-point algorithm** (or 5-point for E) with RANSAC for outlier rejection
3. Decompose E into R and t using SVD

## For our project
During [[Phase 3 - Stereo Calibration]], we use a ChArUco board (known geometry) so we don't need to estimate F/E from correspondences — OpenCV's `stereoCalibrate()` directly gives us R and t. But understanding epipolar geometry is critical for knowing *why* the calibration works and for debugging when it doesn't.

The calibrated extrinsics feed directly into [[Triangulation]].
