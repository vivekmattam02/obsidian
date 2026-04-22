---
tags: [hub, project]
---

# Distributed Multi-Camera 3D Tracker

The whole point: build a **from-scratch multi-object tracker** that runs across 4 edge devices and feeds a robot's navigation stack. No black boxes. No ByteTrack library calls. Every line of math written by hand.

## Why this project?
My portfolio has a hole — I use perception frameworks but I've never built the core algorithms myself. This fixes that. See [[My Skill Gaps]].

## The Hardware
- 2x [[Jetson Nano B01]] → run detection (YOLOv8-Nano via [[TensorRT Deployment]])
- 2x [[Raspberry Pi 4]] → run the [[Tracker Node]] and [[Visualization]]
- See [[Physical Setup]] for cables, switch, cameras

## Architecture
![[System Architecture]]

## The Math (the actual hard part)
Start here → [[Bayes Filter]] (everything else is a special case)
Then → [[Kalman Filter]] → [[Extended Kalman Filter]]
Then → [[Hungarian Algorithm]] + [[Mahalanobis Distance]]
Then → [[Camera Model]] → [[Stereo Geometry]] → [[Triangulation]]

## Build Phases
1. [[Phase 1 - KF From Scratch]]
2. [[Phase 2 - Hungarian and MOT]]
3. [[Phase 3 - Stereo Calibration]]
4. [[Phase 4 - 3D Tracking]]
5. [[Phase 5 - Distributed Pipeline]]
6. [[Phase 6 - Benchmark]]

## Key Concepts
- [[Multi-Object Tracking]]
- [[Track Lifecycle]]
- [[Data Association]]
- [[Re-Identification]]
- [[Sensor Synchronization]]
- [[ROS 2 Networking]]

## References
[[Papers and Resources]] · [[MOT17 Benchmark]]
