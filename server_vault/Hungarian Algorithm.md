---
tags: [math, fundamental, core]
---

# Hungarian Algorithm

Also called the Munkres algorithm. Solves the **assignment problem**: given N detections and M tracks, find the optimal one-to-one matching that minimizes total cost.

## Why is this needed?
Every frame, YOLO gives you a bag of bounding boxes. You have existing tracks from previous frames. Which box belongs to which track?

You could greedily assign each detection to the nearest track, but greedy matching fails badly when objects are close together — it creates cascading errors. The Hungarian algorithm finds the **globally optimal** assignment.

## The cost matrix
Build an N×M matrix where `cost[i][j]` = "how unlikely is it that detection i belongs to track j?"

Options for computing cost:
- **IoU** (Intersection over Union) of the detection bbox with the track's predicted bbox
- **[[Mahalanobis Distance]]** between the detection and the track's predicted state (better — accounts for uncertainty)
- **Euclidean distance** in pixel space (works but ignores uncertainty)

## How it works (simplified)
1. Subtract the row minimum from each row
2. Subtract the column minimum from each column
3. Cover all zeros with minimum number of lines
4. If lines == min(N,M) → solved. Read off assignments from zeros.
5. Else → adjust matrix and repeat

Time complexity: O(n³). For tracking ~50 objects, this is instant.

## In practice
Use `scipy.optimize.linear_sum_assignment()` to compute it. But **understand the algorithm** — don't just call it blindly. The key insight is that assignment quality depends entirely on the quality of your cost matrix, which depends on the quality of your [[Kalman Filter]] predictions.

## Gating (critical)
Before building the cost matrix, **gate** impossible assignments using [[Mahalanobis Distance]]. If a detection is 10 standard deviations away from any track's prediction, don't even include it as a candidate. This prevents the Hungarian algorithm from making absurd long-distance assignments.

Used in [[Data Association]], implemented in [[Phase 2 - Hungarian and MOT]].
