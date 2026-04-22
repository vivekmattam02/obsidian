---
tags: [architecture, node]
---

# Visualization

Runs on [[Raspberry Pi 4|Pi B]]. The "control tower" — shows what the tracker sees in real-time.

## Options
1. **Foxglove Studio** (recommended) — web-based, subscribes to ROS 2 topics natively, supports custom panels. Open `http://pi-b:8765` from your laptop.
2. **Custom Flask/FastAPI dashboard** — more work, but you can design exactly the view you want.

## What to display
- **Bird's Eye View (BEV)**: Top-down 2D plot showing tracked object positions in world coordinates. Each track gets a color and an ID number. Show the [[Kalman Filter]] predicted position as a faded dot ahead of the current position.
- **Track history**: Draw the last N positions as a fading trail behind each object.
- **Camera feeds**: Side-by-side raw camera views with bounding boxes overlaid (streamed from the Jetsons as compressed images).
- **Stats panel**: Number of active tracks, FPS, network latency from each Jetson.

## Logging
Save tracked trajectories to a simple CSV:
```
timestamp, track_id, x, y, z, vx, vy, vz
```
These files are tiny (a few KB per minute). Safe for the 32GB SD card.

## Why a separate Pi for this?
Honestly, the tracker Pi could run the viz too. But separating them:
- Keeps the tracker's CPU fully dedicated to math
- Proves you can distribute ROS 2 nodes across machines
- Lets you access the dashboard from your laptop's browser without SSH tunneling
