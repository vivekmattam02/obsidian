---
tags: [concept, systems]
---

# Sensor Synchronization

When two Jetsons publish detections at slightly different times, and the [[Tracker Node]] receives them over a network with variable latency, you need to be very careful about *when* each detection actually happened.

## The problem
Jetson A publishes a detection at t=1.003s.
Jetson B publishes a detection at t=1.017s.
The Pi receives them at t=1.025s and t=1.030s.

If you treat both detections as "happening now," your [[Triangulation]] will be wrong — the person moved 14ms between the two observations. At walking speed (1.5 m/s), that's 2cm of error. At running speed, it's worse.

## Solutions

### Hardware sync (ideal)
Use cameras with an external trigger pin. Fire both cameras simultaneously. We probably can't do this with cheap USB webcams.

### Software sync via timestamps
ROS 2 `message_filters` has an `ApproximateTimeSynchronizer` that buffers messages from multiple topics and matches them by timestamp:
```python
from message_filters import ApproximateTimeSynchronizer, Subscriber

sub1 = Subscriber(node, Detection2DArray, '/cam1/detections')
sub2 = Subscriber(node, Detection2DArray, '/cam2/detections')
ats = ApproximateTimeSynchronizer([sub1, sub2], queue_size=10, slew=0.03)
ats.registerCallback(callback)
```
The `slew` parameter is the max allowed time difference (30ms here).

### NTP / chrony
All boards need their clocks synchronized. Without this, timestamps are meaningless. Install `chrony` on all boards, point them at the same NTP server (or make one Pi the NTP server for the cluster).

```bash
sudo apt install chrony
```

## For our project
Use `ApproximateTimeSynchronizer` with a 30-50ms slew. Good enough for tracking people at walking speed. Tighter sync would need hardware triggers.
