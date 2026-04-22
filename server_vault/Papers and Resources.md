---
tags: [reference]
---

# Papers and Resources

## Core reading (must-read before starting)
- **SORT** (Bewley et al., 2016): [arXiv:1602.00763](https://arxiv.org/abs/1602.00763)
  The paper we're essentially reimplementing. Short, clean, foundational. Read this first.

- **DeepSORT** (Wojke et al., 2017): [arXiv:1703.07402](https://arxiv.org/abs/1703.07402)
  Extends SORT with deep appearance features ([[Re-Identification]]). Read after you've built SORT.

- **ByteTrack** (Zhang et al., 2022): [arXiv:2110.06864](https://arxiv.org/abs/2110.06864)
  The tracker you used in VIP Self-Drive. Now you'll understand what's inside it.

## Math references
- **Kalman Filter tutorial** (Greg Welch & Gary Bishop): The classic intro. Google "An Introduction to the Kalman Filter, UNC-Chapel Hill". Much clearer than Wikipedia.

- **Multiple View Geometry in Computer Vision** (Hartley & Zisserman): The bible for [[Camera Model]], [[Stereo Geometry]], [[Triangulation]], epipolar geometry. Chapters 9-12 are what we need.

- **Probabilistic Robotics** (Thrun, Burgard, Fox): Chapter 3 for [[Bayes Filter]], Chapter 3.2-3.3 for [[Kalman Filter]] and [[Extended Kalman Filter]]. Chapter 7 for particle filters.

## Practical references
- **OpenCV stereo calibration tutorial**: https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html
  For [[Phase 3 - Stereo Calibration]].

- **Ultralytics YOLOv8 docs**: https://docs.ultralytics.com/
  For exporting to ONNX/TensorRT.

- **py-motmetrics**: https://github.com/chefly/py-motmetrics
  For [[MOT17 Benchmark]] evaluation.

- **Foxglove Studio**: https://foxglove.dev/
  For [[Visualization]].

## Datasets
- **MOT17**: https://motchallenge.net/data/MOT17/ — Used in [[Phase 2 - Hungarian and MOT]] and [[Phase 6 - Benchmark]]
- **WILDTRACK**: Multi-camera pedestrian dataset with calibration — useful for testing [[Phase 4 - 3D Tracking]] without your own cameras
