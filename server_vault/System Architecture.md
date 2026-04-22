---
tags: [architecture]
---

# System Architecture

The pipeline is simple on purpose. Data flows in one direction: cameras → detections → tracks → visualization.

```
┌─────────────┐         ┌─────────────┐
│ USB Camera 1│         │ USB Camera 2│
└──────┬──────┘         └──────┬──────┘
       │                       │
       ▼                       ▼
┌──────────────┐       ┌──────────────┐
│ Jetson Nano A│       │ Jetson Nano B│
│  YOLOv8-Nano│       │  YOLOv8-Nano│
│  (TensorRT)  │       │  (TensorRT)  │
└──────┬───────┘       └──────┬───────┘
       │ Detection2DArray     │ Detection2DArray
       │     (ROS 2)          │     (ROS 2)
       └──────────┬───────────┘
                  │
                  ▼
          ┌───────────────┐
          │ Raspberry Pi A│
          │               │
          │ • Kalman Filter│
          │ • Hungarian    │
          │ • Triangulation│
          │ • Track Mgmt   │
          └───────┬───────┘
                  │ TrackedObjects (ROS 2)
                  ▼
          ┌───────────────┐
          │ Raspberry Pi B│
          │               │
          │ • Foxglove/Web│
          │ • BEV Display  │
          │ • CSV Logger   │
          └───────────────┘
```

## Why this split?
- Jetsons have GPUs → they do the matrix multiply (YOLO inference)
- Pis have RAM → they do the state estimation math (KF, Hungarian)
- Separating detection from tracking is how every real AV perception stack works
- We keep the SD cards safe: no images saved to disk, everything streams through RAM

## ROS 2 Topics
| Topic | Publisher | Subscriber | Message Type |
|-------|-----------|------------|-------------|
| `/cam1/detections` | Jetson A | Pi A | `vision_msgs/Detection2DArray` |
| `/cam2/detections` | Jetson B | Pi A | `vision_msgs/Detection2DArray` |
| `/tracked_objects` | Pi A | Pi B | Custom `TrackedObject3DArray` |
| `/costmap` | Pi A | Laptop (Gazebo) | `nav_msgs/OccupancyGrid` |

See [[Detection Node]], [[Tracker Node]], [[Visualization]], [[ROS 2 Networking]].
