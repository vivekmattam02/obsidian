---
tags: [philosophy, psychology]
---

# Active Inference

Passive perception is a flaw of amateur robotics. A passive robot processes every pixel of a 1080p frame at 30 FPS, exhausting its battery and compute, even if staring at a blank wall.

**Active Inference**, rooted in cognitive psychology and neuroscience (Friston's Free Energy Principle), states that the brain's ultimate goal is to *minimize surprise*. 

## The Core Loop
1. **Prediction**: The [[Extended Kalman Filter]] predicts where the object is and outputs a Covariance Matrix (our "Surprise" or "Uncertainty").
2. **Action**: The [[Behavior Trees|Behavior Tree]] looks at this uncertainty.
   - If Uncertainty is HIGH $\rightarrow$ Order the [[Jetson Edge Node]] to process a wide field of view. Search the room.
   - If Uncertainty is LOW $\rightarrow$ Order the Jetson to process a tiny 200x200 crop exactly where we predict the person to be.
3. **Embodiment**: If the predicted state moves beyond the camera's physical boundaries, the system invokes [[Pan-Tilt Actuation]] to physically move its neck.

## Why this makes you an expert
You are no longer building a "computer vision pipeline." You are building a system that exhibits **Visual Saccades**—the rapid eye movements humans use to scan a room. You are optimizing compute by treating CPU cycles as a finite resource allocated purely by mathematical uncertainty.
