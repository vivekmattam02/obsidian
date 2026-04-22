---
tags: [phase, implementation]
---

# Phase 1 - KF From Scratch

**Goal**: Write a single-object [[Kalman Filter]] in Python from scratch. No libraries except NumPy. Test it on fake data before touching any hardware.

## Duration: ~1 week

## Steps
1. **Define the state vector**: `x = [u, v, s, r, u̇, v̇, ṡ]` (bbox center, area, aspect ratio, velocities)
2. **Build F** (state transition): constant velocity model
3. **Build H** (measurement model): maps state to `[u, v, s, r]` (direct observation)
4. **Initialize Q and R**: process noise and measurement noise. Start with identity × small scalar, tune later.
5. **Write `predict()`**: propagate state and covariance
6. **Write `update(z)`**: compute innovation, Kalman gain, correct state
7. **Test with synthetic data**: generate a fake trajectory (sine wave + noise), run the filter, plot true vs. estimated state

## Test it works
Plot three lines:
- Blue: true position (ground truth)
- Red dots: noisy measurements (simulated YOLO bbox jitter)
- Green: Kalman filter output

The green line should be smoother than the red dots and closely follow the blue line. If it does, your filter works.

## What to watch for
- If the filter diverges (green line flies off to infinity): Q or P₀ initialization is wrong
- If the filter is too sluggish (green line lags behind): Q is too small, increase it
- If the filter is too jittery (green line follows the noise): R is too small, increase it

## Deliverable
A clean Python class:
```python
class KalmanFilter:
    def __init__(self, initial_state):
        ...
    def predict(self):
        ...
    def update(self, measurement):
        ...
```

No scipy. No filterpy. Just NumPy matrix operations. This is the point.

Next: [[Phase 2 - Hungarian and MOT]]
