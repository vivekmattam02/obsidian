# Project Context

## User Profile: Vivekananda Swamy Mattam
- **Degree**: M.S. Mechatronics & Robotics, NYU Tandon (Expected May 2026)
- **Lab**: AI4CE Lab (Prof. Chen Feng), ASAS Lab (Prof. Aliasghar Arab)
- **Prior**: B.Tech Mechanical Engineering, VNR VJIET; Intern at Xmachines (Agricultural Robotics)
- **Career Goal**: Internship/full-time in robotics, autonomous systems, or applied AI

## Key Technical Strengths (from resume + portfolio)
- **Autonomous Nav**: ROS 2, Nav2, SLAM Toolbox, ORB-SLAM3, MPC, MPPI, A*, Pure Pursuit, EKF
- **Perception & ML**: PyTorch, TensorRT, OpenCV, Depth Anything, SAM2, CosPlace, SuperGlue, YOLOv8/v11, ByteTrack, RANSAC, ICP, FoundationStereo
- **Hardware**: Jetson Orin Nano, Teensy 4.1, VESC, RPLiDAR, Orbbec Femto Bolt, TurtleBot3, Spot, EarthRover
- **Languages**: Python, C++, C, MATLAB

## Hardware Available

### KAMRUI AK1PLUS Mini PC (NEW — the Central Server)
- **CPU**: Intel N95 (4-core, 4-thread, Alder Lake-N, up to 3.4GHz)
- **RAM**: 16GB DDR4
- **Storage**: 512GB internal SSD + **1TB external SSD**
- **GPU**: Intel UHD Graphics (integrated, no CUDA)
- **Role**: Master node. Has the most RAM and storage by far. Runs the tracker, databases, visualization, Gazebo sim, logging — everything that needs memory or disk.

### 2x NVIDIA Jetson Nano B01
- **GPU**: 128-core Maxwell (FP16, no Tensor Cores)
- **CPU**: Quad-core ARM Cortex-A57
- **RAM**: 4GB LPDDR4
- **Storage**: 16GB eMMC + 32GB SD card
- **Role**: Dedicated YOLO inference nodes. Run TensorRT, publish detections, nothing else.

### 2x Raspberry Pi 4 Model B (8GB RAM)
- **CPU**: Quad-core Cortex-A72 (1.8GHz)
- **RAM**: 8GB LPDDR4
- **Storage**: 32GB SD card
- **Role**: Now freed up. Could be additional worker nodes, or act as robot simulation proxies.

## How the 1TB SSD + Mini PC Changes Things
1. **Storage constraint is gone**: MOT17 datasets, ROS bags, model checkpoints, Docker images — all fit on the 1TB SSD.
2. **16GB RAM**: Can run Ollama with quantized LLMs (Phi-3, Llama 3 8B) alongside the tracker. Could even serve as a local coding assistant.
3. **Mini PC becomes the brain**: It's faster than both Pis (N95 >> Cortex-A72). The tracker, Foxglove, and any databases should run here.
4. **Pis are freed up**: They can act as edge nodes, robot proxies, or additional camera nodes.

## Updated Cluster Architecture
```
┌─────────────┐  ┌─────────────┐
│ Jetson A    │  │ Jetson B    │   ← GPU inference (YOLO)
│ (Camera 1)  │  │ (Camera 2)  │
└──────┬──────┘  └──────┬──────┘
       │                │
       └────────┬───────┘
                │  Gigabit Ethernet Switch
                │
       ┌────────┴────────┐
       │  KAMRUI Mini PC │   ← Central brain (tracker + viz + storage)
       │  16GB / 1TB SSD │
       └────────┬────────┘
                │
       ┌────────┴────────┐
       │                 │
  ┌────┴─────┐    ┌──────┴────┐
  │  Pi 4 A  │    │  Pi 4 B   │   ← Available for extensions
  │  (8GB)   │    │  (8GB)    │
  └──────────┘    └───────────┘
```

## Identified Skill Gaps (what portfolio does NOT show)
- No C++ perception node (all inference is Python wrappers around TensorRT)
- No explicit multi-camera calibration or stereo calibration project
- No standalone state estimation / tracking project (EKF listed as skill but not demonstrated)
- No explicit edge deployment pipeline project
- Heavy reliance on existing frameworks (Nav2, SLAM Toolbox) — no from-scratch algorithm

## The Project: Distributed Multi-Camera 3D Multi-Object Tracker
See Obsidian vault at `/home/vivek/Desktop/Projects/server/vault/` for full breakdown.
