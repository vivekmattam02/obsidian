---
tags: [phase, implementation]
---

# Phase 4 - 3D Tracking

**Goal**: Upgrade the 2D tracker from Phase 2 to 3D. When both cameras see the same person, use [[Triangulation]] to recover their 3D position. Switch the [[Kalman Filter]] state vector from pixel coordinates to world coordinates.

## Duration: ~1 week

## Steps
1. **Load stereo calibration**: Read `K1, K2, R, T` from [[Phase 3 - Stereo Calibration]]
2. **Build projection matrices**:
```python
P1 = K1 @ np.hstack([np.eye(3), np.zeros((3,1))])  # Camera 1 at origin
P2 = K2 @ np.hstack([R, T])                          # Camera 2 relative
```

3. **Cross-camera detection matching**: When detections arrive from both cameras in the same time window ([[Sensor Synchronization]]), match them:
   - Option A: Epipolar constraint — check if cam2 detection lies near the epipolar line induced by the cam1 detection
   - Option B: Appearance — if you've implemented [[Re-Identification]]
   - Option C: Spatial proximity after rough triangulation

4. **Triangulate matched pairs**:
```python
pts_4d = cv2.triangulatePoints(P1, P2, pts1, pts2)
pts_3d = pts_4d[:3] / pts_4d[3]  # Convert from homogeneous
```
But also write this by hand using DLT — see [[Triangulation]].

5. **Update the Kalman Filter state**:
   - New state: `x = [X, Y, Z, Ẋ, Ẏ, Ż]` (3D position + velocity in meters)
   - New measurement model h(x): project 3D point through [[Camera Model]] to get pixel coords. This is nonlinear → use [[Extended Kalman Filter]]
   - Or simpler: if you triangulate first, the measurement IS the 3D position, and h() is just identity. Then you can keep using linear KF.

6. **Visualize in 3D**: Send the 3D track positions to [[Visualization|Pi B]] and render a top-down (Bird's Eye View) plot.

## The hard part
Cross-camera matching is ambiguous when multiple people are near each other. The epipolar constraint helps but isn't perfect. This is where [[Re-Identification]] becomes valuable.

## Fallback: single-camera detections
When only one camera sees a person (they left the other camera's FOV), fall back to 2D tracking with the ground-plane assumption from [[Triangulation]] (ray intersecting Z=0).

Next: [[Phase 5 - Distributed Pipeline]]
