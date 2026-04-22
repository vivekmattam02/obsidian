---
tags: [phase, implementation]
---

# Phase 5 - Distributed Pipeline

**Goal**: Deploy the full tracker across all 4 physical boards. Until now, everything ran on your laptop against saved data. Now it's real cameras, real network, real latency.

## Duration: ~1.5 weeks

## Steps
1. **Flash the boards**:
   - Jetsons: JetPack 4.6 (Ubuntu 18.04, CUDA 10.2, TensorRT 8.0)
   - Pis: Ubuntu 22.04 Server (headless, no desktop — save SD space)

2. **Install ROS 2**:
   - Jetsons: ROS 2 Foxy (matches Ubuntu 18.04). Or build Humble from source if you're brave.
   - Pis: ROS 2 Humble (matches Ubuntu 22.04)
   - Cross-version communication works fine over DDS as long as message types match.

3. **Set up networking**: See [[ROS 2 Networking]]. Static IPs, same `ROS_DOMAIN_ID`, install chrony for [[Sensor Synchronization|clock sync]].

4. **Deploy the [[Detection Node]] on each Jetson**:
   - Export YOLOv8-Nano to TensorRT FP16 engine ON the Jetson (see [[TensorRT Deployment]])
   - Write the ROS 2 node that reads USB camera → runs inference → publishes `Detection2DArray`

5. **Deploy the [[Tracker Node]] on Pi A**:
   - Port your Phase 1-4 Python code into a ROS 2 node
   - Subscribe to both Jetsons' detection topics
   - Publish `TrackedObject3DArray`

6. **Deploy [[Visualization]] on Pi B**:
   - Install Foxglove bridge: `ros2 launch foxglove_bridge foxglove_bridge_launch.xml`
   - Open Foxglove Studio on your laptop's browser, connect to Pi B
   - Or: write a simple Flask app with a canvas-based BEV renderer

7. **Test end-to-end**: Walk around in front of both cameras. Watch the BEV display. Tracks should follow you smoothly with consistent IDs.

## Optional: connect to a simulated robot
On your laptop, run Gazebo with a TurtleBot3. Pi A publishes the tracked objects as a `nav_msgs/OccupancyGrid` costmap layer. The simulated robot navigates using Nav2 while avoiding the tracked people. This closes the perception-to-action loop — see [[System Architecture]].

## Debugging tips
- Start with just ONE Jetson + ONE Pi. Get that working first.
- Use `ros2 topic hz /cam1/detections` to check detection rates from each Jetson
- Use `ros2 topic echo` to spot-check detection contents
- If Foxglove can't connect, check firewall rules on Pi B

Next: [[Phase 6 - Benchmark]]
