---
tags: [hardware, systems]
---

# Jetson Edge Node

The [[Jetson Nano B01]] serves as the optical cortex of the system. 
It does **not** think. It merely processes what the [[KAMRUI AK1PLUS Mini PC|Brain]] tells it to process.

## The Zero-Copy C++ Pipeline
Python is too slow for edge vision. We write this node in modern C++.

1. **Wait for Command**: The node listens to a ROS 2 topic for an `ROI_Command`.
2. **Memory Map**: We pull a frame from the USB camera directly into GPU memory using V4L2. Zero CPU copying.
3. **Crop**: We crop the image to the exact 200x200 pixel Region of Interest requested by the Brain. 
4. **TensorRT**: We run YOLOv8-Nano (FP16 quantized) *only* on that cropped square. Inference drops from 20ms to 4ms.
5. **Publish**: We publish the resulting bounding box back to the Brain via ROS 2 FastDDS.

## The Beauty of Constraint
By refusing to process the full 1080p frame when we don't have to, the Jetson runs cooler, consumes less power, and leaves GPU cycles open. 
This is the physical manifestation of [[Active Inference]].
