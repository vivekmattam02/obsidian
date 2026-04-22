---
tags: [systems]
---

# ROS 2 Networking

Getting ROS 2 to work across multiple machines is where most people waste days. Here's what actually matters.

## DDS choice
ROS 2 Humble defaults to FastDDS. CycloneDDS is often easier for multi-machine setups. Pick one and use it on ALL machines:
```bash
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
```
Add to `.bashrc` on every board.

## ROS_DOMAIN_ID
All boards must share the same domain ID:
```bash
export ROS_DOMAIN_ID=42
```
Pick any number 0-232. Just make sure it's the same everywhere and nobody else on your network is using it.

## Multicast issues
DDS uses UDP multicast for discovery. Some switches/routers block multicast. If nodes can't find each other:
1. Check: `ros2 multicast receive` on one machine, `ros2 multicast send` on another
2. If it fails, configure unicast discovery (explicitly tell each node where the others are)

For CycloneDDS, create a `cyclonedds.xml`:
```xml
<CycloneDDS>
  <Domain>
    <General>
      <AllowMulticast>false</AllowMulticast>
    </General>
    <Discovery>
      <Peers>
        <Peer address="192.168.1.10"/>  <!-- Pi A -->
        <Peer address="192.168.1.11"/>  <!-- Pi B -->
        <Peer address="192.168.1.20"/>  <!-- Jetson A -->
        <Peer address="192.168.1.21"/>  <!-- Jetson B -->
      </Peers>
    </Discovery>
  </Domain>
</CycloneDDS>
```
```bash
export CYCLONEDDS_URI=file:///path/to/cyclonedds.xml
```

## QoS profiles
For detections (small, frequent messages): use `BEST_EFFORT` reliability with `KEEP_LAST(1)` history. We want lowest latency, and dropping an occasional detection is fine — the [[Kalman Filter]] handles it.

For calibration data or config (rare, must arrive): use `RELIABLE` with `TRANSIENT_LOCAL` durability.

## Bandwidth
Each `Detection2DArray` message is roughly 200-500 bytes (just numbers, no images). At 15 FPS from each Jetson, that's ~15 KB/s. Gigabit Ethernet handles this without breaking a sweat. The bottleneck is never bandwidth — it's latency and discovery.
