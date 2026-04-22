---
tags: [math]
---

# Mahalanobis Distance

Regular Euclidean distance treats all directions equally. Mahalanobis distance accounts for the **shape and spread of uncertainty**. It asks: "How many standard deviations away is this point from the distribution?"

## Formula
```
d² = (z - ẑ)ᵀ · S⁻¹ · (z - ẑ)
```
Where:
- `z` = new measurement (detection)
- `ẑ` = predicted measurement from the [[Kalman Filter]] (`H · x̂⁻`)
- `S` = innovation covariance (`H · P⁻ · Hᵀ + R`)

## Why not just Euclidean?
Imagine tracking a car on a highway. The car's position uncertainty is large *along* the road (it could be anywhere on that 100m stretch) but tiny *perpendicular* to the road (it's definitely in its lane).

A detection 50m ahead on the road should have a small Mahalanobis distance (within the uncertainty ellipse). A detection 5m to the side should have a huge Mahalanobis distance (way outside the ellipse). Euclidean distance would say the opposite.

## For gating
Before running the [[Hungarian Algorithm]], reject any detection-track pair where d² exceeds a threshold (typically chi-squared with degrees of freedom = measurement dimension). For a 4D measurement, the 95% gate is roughly d² < 9.49.

This prevents absurd assignments and massively speeds up the Hungarian algorithm (smaller cost matrix).

## For the cost matrix
You can use Mahalanobis distance directly as the cost in the [[Hungarian Algorithm]] instead of IoU. It's better because it incorporates the [[Kalman Filter]]'s uncertainty — a detection that's 20 pixels away from a high-uncertainty track is "closer" (in Mahalanobis terms) than a detection that's 10 pixels away from a very-confident track.
