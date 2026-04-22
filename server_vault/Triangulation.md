---
tags: [math, geometry, core]
---

# Triangulation

Given a 2D observation from Camera 1 and a 2D observation from Camera 2, recover the 3D position.

This is how stereo depth works, but here we're not matching pixels — we're matching *person detections*. If both Jetsons detect the same person, we triangulate their 3D position in the room.

## The setup
You need:
- Pixel coordinates from cam 1: `(u₁, v₁)` — bottom-center of the YOLO bounding box
- Pixel coordinates from cam 2: `(u₂, v₂)` — same person, bottom-center
- Camera intrinsics: `K₁, K₂` — from [[Phase 3 - Stereo Calibration|calibration]]
- Camera extrinsics: `R, t` — relative pose between cameras, also from calibration

## The math (DLT method)
Convert each pixel to a normalized ray:
```
ray₁ = K₁⁻¹ · [u₁, v₁, 1]ᵀ
ray₂ = K₂⁻¹ · [u₂, v₂, 1]ᵀ
```

Transform ray₂ into camera 1's frame using the extrinsics. Now both rays are in the same coordinate system. The 3D point is where they (approximately) intersect.

In practice the rays never perfectly intersect (noise). So we set up a least-squares problem:
```
A · X = 0
```
Where A is built from the projection matrices P₁ and P₂. Solve via SVD — the 3D point is the last column of V (the right singular vector with smallest singular value).

OpenCV: `cv2.triangulatePoints(P1, P2, pts1, pts2)` — but we'll code it by hand first.

## Ground plane shortcut
If you know the cameras are mounted at a known height and people are standing on a flat floor, you can skip full triangulation and just intersect the camera ray with the Z=0 plane. Simpler but less general. See [[Camera Model]] for the ray construction.

## Accuracy
Triangulation accuracy degrades with:
- **Small baseline**: cameras too close together → poor depth resolution
- **Bad calibration**: if R,t are off, the rays won't intersect correctly
- **Detection noise**: YOLO bboxes jitter by ±5px, which propagates into 3D error

The [[Kalman Filter]] smooths out this noise over time. That's why filtering and triangulation work so well together.

Used in [[Phase 4 - 3D Tracking]].
