---
tags: [math, algorithms]
---

# Data Association

Once you have [[Mahalanobis Distance]] determining the mathematical distance between predicted states and raw detections, you must solve the assignment problem.

If you have 3 detections from the [[Jetson Edge Node]] and 3 predicted tracks from the [[Extended Kalman Filter]], which detection belongs to which track?

## The Hungarian Algorithm
A naive approach assigns the closest detection to the first track. This is "Greedy" and fails when people cross paths.

The **Hungarian Algorithm** (Kuhn-Munkres) solves for the *global minimum cost*. It evaluates every possible permutation of Track-to-Detection assignments and finds the one arrangement that minimizes the total sum of Mahalanobis Distances.

If a Track is assigned a detection that exceeds the $7.81$ Chi-Squared threshold, the assignment is rejected (Gating), and the track enters a `[LOST]` state managed by the [[Behavior Trees]].
