---
tags: [systems, ros2]
---

# ROS 2 TF Trees

A robot must know the spatial relationship of every atom in its body relative to the universe. We track this using the **Transform (TF) Tree**.

If you do not define a rigorous TF tree, your 3D math will fail, and your [[Digital Twin]] will be a chaotic mess.

## The Hierarchy
Transforms are always defined as `parent` $\rightarrow$ `child`.

```text
world  (The absolute origin of your room)
 │
 ├── base_link  (The center of your Mini PC / Robot)
 │
 ├── cam1_base  (The physical mounting bracket of Camera 1)
 │    │
 │    └── cam1_pan_link  (Rotates around Z-axis via Servo)
 │         │
 │         └── cam1_tilt_link  (Rotates around Y-axis via Servo)
 │              │
 │              └── cam1_optical  (The actual camera lens)
 │
 └── tracked_person_1 (The X,Y,Z coordinate output by the EKF)
```

## Why this is beautiful
When the [[Pan-Tilt Actuation]] servo rotates 30 degrees, we update the `cam1_pan_link` TF. 
Because of the hierarchical tree, ROS 2 *automatically* calculates how the `cam1_optical` frame moved in the `world` space. 

When the [[Jetson Edge Node]] detects a person, it detects them in `cam1_optical` space. We use `tf2` to instantly transform that detection into `world` space before feeding it to the [[Extended Kalman Filter]].

Math becomes seamless. Visualized beautifully in Foxglove.
