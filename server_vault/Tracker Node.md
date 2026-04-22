---
tags: [architecture, node, core]
---

# Tracker Node

This is the heart of the entire project. Runs on [[Raspberry Pi 4|Pi A]]. Everything here is written from scratch — no library calls for tracking.

## What it does
1. Subscribes to `/cam1/detections` and `/cam2/detections` from the [[Detection Node|Jetsons]]
2. Handles [[Sensor Synchronization]] (time-aligns the two streams)
3. Runs the [[Kalman Filter]] predict step (propagate all existing tracks forward)
4. Computes [[Mahalanobis Distance]] between predicted track states and new detections
5. Solves [[Data Association]] using the [[Hungarian Algorithm]]
6. Runs the [[Kalman Filter]] update step for matched tracks
7. Manages [[Track Lifecycle]] (create new tracks, kill lost ones)
8. If both cameras see the same object → [[Triangulation]] to get 3D position
9. Publishes `TrackedObject3DArray` for [[Visualization]]

## The state vector
For 2D tracking (Phase 1-2):
```
x = [u, v, s, r, u̇, v̇, ṡ]
```
Where u,v = bbox center, s = area, r = aspect ratio, dots = velocities.

For 3D tracking (Phase 4+):
```
x = [X, Y, Z, Ẋ, Ẏ, Ż]
```
Where X,Y,Z = world coordinates from [[Triangulation]].

## Why on the Pi and not the Jetson?
- The tracker is pure linear algebra (matrix multiplies, inversions). No GPU needed.
- The Pi has 8GB RAM — can hold thousands of track states without sweating.
- Keeping detection and tracking on separate hardware forces me to deal with [[ROS 2 Networking|network latency]], which is a real-world constraint.

## Implementation
Language: Python + NumPy first (for prototyping in [[Phase 1 - KF From Scratch|Phase 1]]), then optionally C++ with Eigen for speed.
