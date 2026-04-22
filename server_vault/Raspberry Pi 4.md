---
tags: [hardware]
---

# Raspberry Pi 4 (8GB)

I have two of these. They're the "brain" — no GPU, but 8GB of RAM is enough for state estimation, databases, and serving a dashboard.

## Specs
- **CPU**: Quad-core Cortex-A72 (ARMv8-A, 1.8GHz)
- **RAM**: 8GB LPDDR4
- **Storage**: 32GB SD card (this is tight — see below)
- **Network**: Gigabit Ethernet + Wi-Fi 5
- **OS**: Ubuntu 22.04 Server (headless) or Raspberry Pi OS

## What it CAN do
- Run heavy matrix math (NumPy, Eigen) for [[Kalman Filter]] and [[Hungarian Algorithm]]
- Host a web dashboard or [[Visualization|Foxglove]] instance
- Act as a ROS 2 node with plenty of RAM headroom
- Run lightweight databases (SQLite) for trajectory logging

## What it CANNOT do
- Any GPU-accelerated inference (no CUDA, no TensorRT)
- Store large ROS bags or video files (32GB SD card)

## Storage warning
After Ubuntu + ROS 2 + Python packages, you'll have maybe 15-18GB free. That's fine for this project since we're only saving tiny trajectory CSVs. But don't install Docker on top — it eats 2-3GB minimum. Run things natively on the Pis.

## In this project
- **Pi A** → [[Tracker Node]] (the main brain, runs the from-scratch tracker)
- **Pi B** → [[Visualization]] (Foxglove dashboard + trajectory logging)
