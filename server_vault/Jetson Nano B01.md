---
tags: [hardware]
---

# Jetson Nano B01

I have two of these. They're the "eyes" of the system — dedicated to running [[TensorRT Deployment|TensorRT]] inference and nothing else.

## Specs
- **GPU**: 128-core Maxwell (FP16, no Tensor Cores)
- **CPU**: Quad-core ARM Cortex-A57
- **RAM**: 4GB LPDDR4
- **Storage**: 16GB eMMC
- **OS**: JetPack 4.6 (Ubuntu 18.04 based)

## What it CAN do
- Run YOLOv8-Nano at ~15-20 FPS via TensorRT FP16
- Handle a single USB camera stream in RAM
- Publish lightweight JSON/ROS 2 messages over Ethernet

## What it CANNOT do
- Run modern LLMs or VLMs (4GB RAM is not enough, Maxwell has no Tensor Cores)
- Store large datasets (eMMC is tiny, SD card is only 32GB)
- Run SLAM, heavy databases, or anything memory-intensive

## Gotchas
- Maxwell doesn't support INT8 quantization well — stick to FP16
- Will thermal throttle if you don't have a heatsink/fan. The B01 usually comes with one but double check
- JetPack 4.6 ships with CUDA 10.2 and Python 3.6 — some modern libraries won't install cleanly
- The eMMC variant means the OS is on the module, not the SD card. SD card is extra storage

## In this project
Each Jetson is a [[Detection Node]] — receives a camera stream, runs YOLO, publishes detections to the [[Tracker Node]] on the Pi via [[ROS 2 Networking]].
