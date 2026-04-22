---
tags: [architecture, node]
---

# Detection Node

This runs on each [[Jetson Nano B01]]. It's deliberately simple — grab frame, run YOLO, publish boxes. No tracking, no filtering, no saving to disk.

## What it does
1. Opens the USB camera via GStreamer (not OpenCV's VideoCapture — GStreamer gives you zero-copy GPU frames on Jetson)
2. Resizes to 640x640 (YOLO input)
3. Runs YOLOv8-Nano via [[TensorRT Deployment|TensorRT]] FP16
4. Publishes `vision_msgs/Detection2DArray` over [[ROS 2 Networking|ROS 2]]
5. That's it. No disk writes. Everything stays in RAM.

## Why not track on the Jetson?
Because the whole point of this project is to build the tracker from scratch on the Pi. The Jetsons are just fancy sensor nodes. If I wanted to run ByteTrack on the Jetson, I'd learn nothing.

## Expected performance
On the Nano's Maxwell GPU with TensorRT FP16:
- YOLOv8-Nano: ~15-20 FPS
- Latency per frame: ~50-70ms
- Memory: ~800MB (model + CUDA context + frame buffer)
- That leaves ~3GB headroom on the 4GB Jetson. Comfortable.

## Implementation
Language: Python with `tensorrt` bindings (or C++ if doing [[Phase 5 - Distributed Pipeline]] properly)
ROS 2: Standard `rclpy` node publishing `Detection2DArray`

The detection message includes per-box:
- `bbox.center.position.x/y` (pixel coords)
- `bbox.size_x/y` (width/height in pixels)
- `results[0].hypothesis.class_id` (e.g., "person")
- `results[0].hypothesis.score` (confidence)

The [[Tracker Node]] on the Pi consumes these.
