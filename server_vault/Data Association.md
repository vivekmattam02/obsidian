---
tags: [concept]
---

# Data Association

The problem: you have N detections this frame and M existing tracks. Which detection belongs to which track? Some detections might be new objects. Some tracks might have no detection (occlusion). Some detections might be false positives.

## The approach stack (simplest to best)
1. **Nearest neighbor**: Assign each detection to the closest track. Greedy, fast, terrible when objects are near each other.
2. **Global nearest neighbor (GNN)**: Use the [[Hungarian Algorithm]] to find the globally optimal assignment. This is what SORT does. Much better.
3. **Joint probabilistic data association (JPDA)**: Don't commit to a single assignment — maintain a weighted mixture over possible associations. Theoretically beautiful, computationally heavy.
4. **Multiple hypothesis tracking (MHT)**: Maintain a tree of possible association hypotheses over time. Best accuracy, exponential complexity.

We're doing GNN (option 2). It's the industry standard for real-time systems.

## The cost matrix
The quality of your association is only as good as your cost metric. Options:
- **IoU** (Intersection over Union): Simple, works well when objects move slowly. Fails with fast motion.
- **Centroid distance**: Euclidean distance between bbox centers. Ignores size.
- **[[Mahalanobis Distance]]**: Best for us. Uses the [[Kalman Filter]]'s uncertainty to weight the distance. A detection far from a high-uncertainty track is "closer" than one near a low-uncertainty track.

## Two-stage matching (ByteTrack's trick)
First match high-confidence detections to tracks. Then match remaining low-confidence detections to unmatched tracks. This recovers partially occluded objects that YOLO gives low confidence to. We can add this as an extension in [[Phase 2 - Hungarian and MOT]].

## Cross-camera association
When a person is seen by BOTH cameras, we need to associate the *same person* across cameras before [[Triangulation]]. Options:
- **Spatial gating**: If the cameras overlap and we know the [[Stereo Geometry|epipolar geometry]], the matching person's detection should lie near the epipolar line.
- **Appearance matching**: [[Re-Identification]] via color histograms or deep features.
- **Temporal coincidence**: If a person disappears from cam 1 and appears in cam 2 at the right time, likely the same person.
