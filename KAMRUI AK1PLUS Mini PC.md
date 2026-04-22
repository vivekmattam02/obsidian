---
tags: [hardware]
---

# KAMRUI AK1PLUS Mini PC

This is the newest and most powerful machine in the cluster. It replaces the Raspberry Pis as the central brain.

## Specs
- **CPU**: Intel N95 (4-core, 4-thread, Alder Lake-N, base 1.7GHz / boost 3.4GHz)
- **RAM**: 16GB DDR4
- **Storage**: 512GB internal SSD + 1TB external SSD
- **GPU**: Intel UHD Graphics (no CUDA — can't run TensorRT)
- **Network**: Gigabit Ethernet + Wi-Fi
- **OS**: Can run Ubuntu 22.04 natively

## Why this changes everything

### Storage is no longer a problem
With 1.5TB total (512GB + 1TB), we can:
- Store the entire MOT17 dataset (~6GB)
- Record hours of ROS bag data for offline testing
- Keep Docker images without worrying about space
- Store model checkpoints, calibration files, logs, everything
- The 32GB SD card constraint on the Pis was killing us. Now it doesn't matter.

### 16GB RAM is serious
- The [[Extended Kalman Filter]] tracking math uses maybe 200MB of RAM. Leaves 15.8GB free.
- We can run [[Digital Twin]] rendering, a web dashboard, and the [[Behavior Trees]] simultaneously without sweat.
- Could even run Ollama with a 4-bit quantized Llama 3 8B (~5GB) or Phi-3 (~2GB) on the side — basically a free local ChatGPT for coding help while we work.

### N95 is faster than the Pi's A72
Single-threaded performance matters for the [[Extended Kalman Filter]] and [[Data Association]] (both are sequential). The N95 at 3.4GHz boost is roughly 50-70% faster than the Pi 4's Cortex-A72 at 1.8GHz. The tracker will run noticeably faster here.

## Role in the cluster
This is the **master node**. It runs:
- The Math: [[Extended Kalman Filter]] and [[Data Association]]
- The Cognition: [[Behavior Trees]] determining ROI and framerate.
- The Visualization: [[Digital Twin]] rendering via Foxglove Studio.
- The Coordination: Master for [[ROS 2 TF Trees]] and logging to the 1TB SSD.

The [[Jetson Edge Node|Jetsons]] remain the GPU inference workers.
The [[Raspberry Pi 4|Pis]] are now free to drive the [[Pan-Tilt Actuation]] servos or other edge extensions.

## What it CANNOT do
- No CUDA → no TensorRT inference. The Jetsons still handle all neural network work.
- Intel UHD Graphics is weak — don't count on it for anything compute-heavy.
- No GPIO pins — can't directly interface with sensors or motors like the Pi can.
