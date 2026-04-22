---
tags: [math, fundamental, core]
---

# Kalman Filter

The single most important algorithm in robotics. If you understand this deeply, you understand `robot_localization`, GPS fusion, IMU integration, and tracking. It's the Gaussian special case of the [[Bayes Filter]].

## Setup
You're tracking a state vector **x** (e.g., position + velocity of a person) and a covariance matrix **P** (how uncertain you are about each component).

## The equations
### Predict
```
x̂⁻ = F · x̂ + B · u          (propagate state)
P⁻  = F · P · Fᵀ + Q         (propagate uncertainty)
```
- **F** = state transition matrix ("constant velocity" model: next position = current position + velocity × dt)
- **Q** = process noise ("I don't trust my motion model perfectly" — accounts for acceleration, jitter)
- **B · u** = control input (usually 0 for tracking — we don't control the person)

### Update
```
y   = z - H · x̂⁻             (innovation: how far off was my prediction?)
S   = H · P⁻ · Hᵀ + R        (innovation covariance)
K   = P⁻ · Hᵀ · S⁻¹          (Kalman gain: how much to trust the measurement)
x̂   = x̂⁻ + K · y             (corrected state)
P   = (I - K · H) · P⁻       (corrected uncertainty)
```
- **H** = measurement matrix (maps state space to measurement space — e.g., "I can only observe position, not velocity")
- **R** = measurement noise (how noisy is YOLO? bounding box jitters by ±5 pixels? That goes here)
- **K** = Kalman gain. THIS is the magic. When R is small (good sensor), K is large → trust the measurement. When R is large (bad sensor), K is small → trust the prediction.

## Intuition for Kalman Gain
Think of it as a slider between 0 and 1:
- K ≈ 0 → "I don't trust the measurement, stick with my prediction"
- K ≈ 1 → "My prediction was garbage, just use the raw measurement"
- K ≈ 0.5 → "Split the difference"

The filter automatically computes the optimal K at every timestep based on the noise characteristics.

## For our tracker
State: `x = [u, v, s, r, u̇, v̇, ṡ]` (bbox center, area, aspect ratio, and their velocities)
Measurement: `z = [u, v, s, r]` (what YOLO gives us each frame)
F: constant velocity model
H: picks out [u, v, s, r] from the full state
Q: tuning parameter — start small, increase if tracks are too sluggish
R: measure YOLO's bbox jitter empirically and put those numbers in

This is implemented in [[Phase 1 - KF From Scratch]]. Then generalized to nonlinear models in [[Extended Kalman Filter]].
