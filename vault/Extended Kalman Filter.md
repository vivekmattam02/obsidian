---
tags: [math, state_estimation]
---

# Extended Kalman Filter

The EKF is not just an algorithm; it is a worldview. It assumes that sensors lie, models are imperfect, and truth is merely a Gaussian probability distribution.

## The Matrices of Truth
- $x$: The State Vector. $[X, Y, Z, V_x, V_y, V_z]$. This is what we *think* reality is.
- $P$: The Covariance Matrix. This is our **Doubt**. It represents how confused we are.
- $Q$: Process Noise. The physics of the world are chaotic. People change directions. $Q$ prevents the filter from becoming too stubborn.
- $R$: Measurement Noise. The [[Jetson Edge Node]] YOLO bounding boxes jitter. $R$ models this hardware imperfection.

## The Two-Step Heartbeat
1. **Predict (Time Update)**
   We push $x$ through the laws of physics. We push $P$ through the Jacobian $F$. Our uncertainty $P$ always *grows* during prediction because the future is unknown.
2. **Update (Measurement Update)**
   We receive a measurement $z$. We compute the **Kalman Gain ($K$)**.
   - If $R$ (sensor noise) is high, $K$ is low. We trust our physics model.
   - If $P$ (our doubt) is high, $K$ is high. We trust the new sensor data.

## In Our System
The EKF runs on the [[KAMRUI AK1PLUS Mini PC]]. It is the sole source of truth. The doubt $P$ is directly fed into the [[Behavior Trees]] to drive [[Active Inference]].
