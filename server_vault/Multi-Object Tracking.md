---
tags: [concept, core]
---

# Multi-Object Tracking

MOT is the problem of detecting multiple objects in video and maintaining a consistent identity for each one across frames. It's not just "where are the objects?" — it's "which box in frame 10 is the same person as which box in frame 9?"

## Online vs. offline
- **Online** (what we're building): Process one frame at a time, no future information. This is what runs on a robot.
- **Offline/batch**: Look at the entire video, globally optimize assignments. Better accuracy, useless for robotics.

## The tracking-by-detection paradigm
We don't track pixels. We run a detector (YOLO) every frame and then **associate** detections to existing tracks. This decouples detection quality from tracking quality.

The pipeline per frame:
1. Get detections from [[Detection Node]]
2. [[Kalman Filter]] predict (where should each track be now?)
3. Build cost matrix → [[Mahalanobis Distance]] or IoU
4. [[Hungarian Algorithm]] → optimal assignment
5. [[Kalman Filter]] update (correct matched tracks)
6. [[Track Lifecycle]] management

## Key papers
- **SORT** (2016): KF + Hungarian + IoU. Dead simple. Our baseline.
- **DeepSORT** (2017): SORT + appearance features (deep ReID). Adds [[Re-Identification]].
- **ByteTrack** (2022): Uses low-confidence detections in a second matching round. You used this in VIP Self-Drive as a black box.
- **OC-SORT** (2023): Handles occlusion better with virtual trajectories.

We're essentially building SORT from scratch, then optionally adding DeepSORT's ReID.

## Evaluation metrics
See [[MOT17 Benchmark]].
