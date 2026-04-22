---
tags: [cognition, architecture]
---

# Behavior Trees

Finite State Machines (FSMs) are brittle. If you use `if/else` logic to manage a robot's brain, your code will inevitably collapse into spaghetti. 

We use **Behavior Trees (BTs)**. This is how Halo programmed AI in 2004, and how modern ROS 2 (`Nav2`) programs autonomous navigation today.

## The Structure
A BT is a directed tree of nodes:
1. **Fallback Nodes (Selector - `?`)**: Tries children from left to right. Stops when one succeeds. (e.g., "Try to Track. If failed, try to Search").
2. **Sequence Nodes (`->`)**: Executes children left to right. Stops if any child fails. (e.g., "Pan camera TO target -> Read frame -> Detect").
3. **Condition Nodes**: Checks a truth (e.g., "Is Covariance $P$ low?").
4. **Action Nodes**: Does physical work (e.g., "Send ROI command to Jetson").

## Our Cognitive Tree
```text
Root
 └── Fallback (?)
      ├── Sequence (->) [Maintain Tracking]
      │    ├── Condition: Track CONFIRMED?
      │    ├── Condition: Uncertainty P < Threshold?
      │    └── Action: Send ROI Crop Command to Jetson
      │
      ├── Sequence (->) [Active Recovery]
      │    ├── Condition: Track LOST?
      │    ├── Action: Predict trajectory via EKF
      │    └── Action: Command Pan/Tilt Servo to intercept
      │
      └── Sequence (->) [Global Search]
           ├── Action: Send Full 1080p command to Jetson
           └── Action: Spin servos in sweeping pattern
```
This logic runs entirely on the [[KAMRUI AK1PLUS Mini PC]]. It brings [[Active Inference]] to life.
