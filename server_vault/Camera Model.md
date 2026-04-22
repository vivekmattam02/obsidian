---
tags: [math, geometry]
---

# Camera Model

The pinhole model. Every single thing in visual perception starts here — projection, calibration, triangulation, SLAM. If you don't internalize this, nothing else makes sense.

## The projection equation
A 3D point in the camera frame `[X, Y, Z]ᵀ` projects to pixel `[u, v]ᵀ`:
```
[u]       [fx  0  cx] [X/Z]
[v]   =   [0  fy  cy] [Y/Z]
[1]       [0   0   1] [ 1 ]
```
Or more compactly: `p = K · [X/Z, Y/Z, 1]ᵀ`

**K** is the intrinsic matrix:
- `fx, fy` = focal length in pixels (how "zoomed in" the camera is)
- `cx, cy` = principal point (usually near image center)

## Distortion
Real lenses bend light. The pinhole model assumes straight rays. Distortion coefficients correct for this:
- **Radial**: `k1, k2, k3` — barrel or pincushion warping
- **Tangential**: `p1, p2` — lens not perfectly parallel to sensor

You estimate these during [[Phase 3 - Stereo Calibration|calibration]] with a checkerboard. OpenCV's `calibrateCamera()` gives you both K and distortion.

## Extrinsics
The camera doesn't sit at the world origin. The **extrinsic matrix** `[R|t]` transforms a point from world coordinates to camera coordinates:
```
P_cam = R · P_world + t
```
Where R ∈ SO(3) (rotation) and t ∈ ℝ³ (translation).

## The full pipeline
```
World point → [R|t] → Camera frame → K → Pixel
```
Going backward (pixel → world) requires depth information. That's what [[Triangulation]] gives you when you have two cameras.

## For our project
Each [[Jetson Nano B01]] has a camera with its own K and distortion. During [[Phase 3 - Stereo Calibration]], we find K₁, K₂, and the relative [R|t] between them. The [[Tracker Node]] uses these to lift 2D detections into 3D.
