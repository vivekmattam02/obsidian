---
tags: [meta]
---

# My Skill Gaps

Honest assessment of what my portfolio shows vs. what it doesn't. This project exists to close these gaps.

## ✅ I'm solid at
- Object detection (YOLOv8/v11) — multiple projects
- Model distillation (Depth Anything → EfficientViT) — Vortex project
- TensorRT/ONNX deployment on Jetson — Vortex (21.9 FPS on Orin Nano)
- Full ROS 2 navigation stacks (Nav2, SLAM Toolbox) — Vortex, VIP Self-Drive
- ORB-SLAM3 (visual SLAM) — Lunar Autonomy, VIP Self-Drive
- Reinforcement learning (PPO, Isaac Lab) — Quadruped project
- Building physical robot platforms — Vortex RC car from scratch

## ❌ Gaps this project fills
| Gap | How this project fixes it |
|-----|--------------------------|
| Never built a [[Kalman Filter]] from scratch | Core of [[Phase 1 - KF From Scratch]] |
| Never implemented [[Hungarian Algorithm]] | Core of [[Phase 2 - Hungarian and MOT]] |
| Never done multi-camera [[Stereo Geometry\|stereo calibration]] | [[Phase 3 - Stereo Calibration]] |
| [[Triangulation]] never demonstrated | [[Phase 4 - 3D Tracking]] |
| Use ByteTrack as a library, never built a tracker | The entire project |
| [[Mahalanobis Distance]] / statistical gating | Part of [[Data Association]] |
| [[Re-Identification]] across cameras | Extension in Phase 5 |
| Distributed ROS 2 across physical machines | [[ROS 2 Networking]] setup |

## What this still won't cover
- Factor graph optimization (GTSAM/g2o) — would need a separate SLAM project
- 3D object detection (PointPillars/CenterPoint) — would need LiDAR
- Hand-eye calibration — would need a robot arm
