---
tags: [hardware, setup]
---

# Physical Setup

## What to buy (~$25-45 total)
| Item | Why | Cost |
|------|-----|------|
| 5-port Gigabit Ethernet switch | ROS 2 FastDDS over Wi-Fi is a nightmare. Ethernet is mandatory. | ~$15 |
| 4x Ethernet cables (Cat5e/Cat6) | One per board | ~$10 |
| 2x USB webcams | One per [[Jetson Nano B01]]. Even cheap Logitech C270s work. | $0-20 (might already own) |
| ChArUco calibration board | Print on A4 paper for [[Phase 3 - Stereo Calibration]] | Free |

## What you already have
- 2x [[Jetson Nano B01]]
- 2x [[Raspberry Pi 4]]
- 4x 32GB SD cards
- Power supplies for all boards
- Your laptop (runs Gazebo sim if we go that route)

## Network topology
```
Laptop ──────┐
             │
Jetson A ────┤
             ├──── Gigabit Switch
Jetson B ────┤
             │
Pi A ────────┤
             │
Pi B ────────┘
```

All on the same subnet (e.g., 192.168.1.x). Set static IPs so you don't lose machines on reboot. See [[ROS 2 Networking]] for DDS config.

## Camera placement
For the multi-camera tracker to be interesting, the two USB cameras need **overlapping fields of view** — ideally placed 1-2 meters apart, angled toward the same area (a doorway, a desk, a hallway). This gives you overlapping detections for [[Triangulation]] and also non-overlapping zones for [[Re-Identification]].

## Power
Just a power strip. All 4 boards + switch can run off USB/barrel jacks. Total draw is maybe 30-40W.
