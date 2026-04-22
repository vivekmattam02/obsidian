---
tags: [visualization]
---

# Digital Twin

The final layer of the architecture is how we visualize the AI's understanding of reality. We will use Foxglove Studio running on the [[KAMRUI AK1PLUS Mini PC]].

## The 3D Render
We do not just overlay bounding boxes on a flat video feed. 

We construct a 3D environment tied directly to the [[ROS 2 TF Trees]]. 
- The physical cameras are rendered as 3D models.
- If the [[Pan-Tilt Actuation]] rotates a physical camera, the virtual camera inside Foxglove rotates exactly in sync.
- The [[Extended Kalman Filter]] tracks are drawn as moving 3D spheres or cylinders on the virtual floor, leaving a decaying trail behind them to show velocity vectors.

This proves that the system is not doing "image processing." It is doing **Embodied Spatial Intelligence**.
