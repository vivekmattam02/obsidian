---
tags: [systems, networking]
---

# DDS Quality of Service

ROS 2 runs on DDS (Data Distribution Service). This is not typical TCP/IP. This is industrial-grade networking.

Because we are doing [[Active Inference]], the [[KAMRUI AK1PLUS Mini PC]] is constantly talking back and forth with the [[Jetson Edge Node]]. Latency is our absolute enemy. 

## The Profiles
You do not use default settings for high-speed robotic control.

1. **For Detections (Jetson $\rightarrow$ Brain)**
   - Reliability: `BEST_EFFORT`. We do not care if we drop a single bounding box frame. The [[Extended Kalman Filter]] is designed to survive missed detections. We care about speed. 
   - History: `KEEP_LAST(1)`. We only ever want the absolute newest frame. Never process a queued, stale detection.

2. **For Commands (Brain $\rightarrow$ Jetson)**
   - Reliability: `RELIABLE`. If the Brain tells the Jetson to change its ROI, we need to ensure that command is received, or the math will desynchronize.

We will tune FastDDS XML configurations to disable Multicast discovery and use Unicast UDP over the Gigabit switch to ensure sub-5ms latency across the cluster.
