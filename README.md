<h1 align='center'>The Active Perception Engine</h1>

> *A First-Principles Distributed Architecture for Embodied Cognition*

---

# 00 Active Perception Bible

This vault is the sacred text for the **Active Perception Engine**. It contains the fundamental truths of Mathematics, Cognitive Architecture, and Distributed Systems. 

A standard robot passively records the world. An intelligent robot *actively interrogates* the world. This is the difference between a sensor and a mind.

## I. The Philosophy of the Mind
Read these to understand *why* the system behaves the way it does.
- [[Active Inference]]: The psychological core. Why we only look at what matters.
- [[Behavior Trees]]: The architecture of cognition and decision-making.

## II. The Mathematics of Reality
Read these to understand how we separate truth from noise.
- [[Extended Kalman Filter]]: The beating heart of the system. Modeling uncertainty.
- [[Mahalanobis Distance]]: The geometry of probability.
- [[Data Association]]: How we stitch fragments of time into a continuous identity.
- [[Triangulation]]: Lifting 2D pixels into 3D reality.

## III. The Nervous System (ROS 2)
Read these to understand how the body communicates with the brain.
- [[ROS 2 TF Trees]]: The spatial relationship of the universe.
- [[DDS Quality of Service]]: The physics of low-latency networking.

## IV. The Embodied Hardware
Read these to understand the physical manifestation of the system.
- [[KAMRUI AK1PLUS Mini PC]]: The Brain. Where the math lives.
- [[Jetson Edge Node]]: The Eyes. Where raw photons become semantic meaning.
- [[Pan-Tilt Actuation]]: The Muscles. Control theory and PID tracking.
- [[Digital Twin]]: The inner simulation. How the robot visualizes its own existence.

---

# Active Inference

Passive perception is a flaw of amateur robotics. A passive robot processes every pixel of a 1080p frame at 30 FPS, exhausting its battery and compute, even if staring at a blank wall.

**Active Inference**, rooted in cognitive psychology and neuroscience (Friston's Free Energy Principle), states that the brain's ultimate goal is to *minimize surprise*. 

## The Core Loop
1. **Prediction**: The [[Extended Kalman Filter]] predicts where the object is and outputs a Covariance Matrix (our "Surprise" or "Uncertainty").
2. **Action**: The [[Behavior Trees|Behavior Tree]] looks at this uncertainty.
   - If Uncertainty is HIGH $\rightarrow$ Order the [[Jetson Edge Node]] to process a wide field of view. Search the room.
   - If Uncertainty is LOW $\rightarrow$ Order the Jetson to process a tiny 200x200 crop exactly where we predict the person to be.
3. **Embodiment**: If the predicted state moves beyond the camera's physical boundaries, the system invokes [[Pan-Tilt Actuation]] to physically move its neck.

## Why this makes you an expert
You are no longer building a "computer vision pipeline." You are building a system that exhibits **Visual Saccades**—the rapid eye movements humans use to scan a room. You are optimizing compute by treating CPU cycles as a finite resource allocated purely by mathematical uncertainty.

---

# Extended Kalman Filter

The EKF is not just an algorithm; it is a worldview. It assumes that sensors lie, models are imperfect, and truth is merely a Gaussian probability distribution.

## The Matrices of Truth
- $x$: The State Vector. $[X, Y, Z, V_x, V_y, V_z]$. This is what we *think* reality is.
- $P$: The Covariance Matrix. This is our **Doubt**. It represents how confused we are.
- $Q$: Process Noise. The physics of the world are chaotic. People change directions. $Q$ prevents the filter from becoming too stubborn.
- $R$: Measurement Noise. The [[Jetson Edge Node]] YOLO bounding boxes jitter. $R$ models this hardware imperfection.

## The Two-Step Heartbeat
1. **Predict (Time Update)**
   We push $x$ through the laws of physics. We push $P$ through the Jacobian $F$. Our uncertainty $P$ always *grows* during prediction because the future is unknown.
2. **Update (Measurement Update)**
   We receive a measurement $z$. We compute the **Kalman Gain ($K$)**.
   - If $R$ (sensor noise) is high, $K$ is low. We trust our physics model.
   - If $P$ (our doubt) is high, $K$ is high. We trust the new sensor data.

## In Our System
The EKF runs on the [[KAMRUI AK1PLUS Mini PC]]. It is the sole source of truth. The doubt $P$ is directly fed into the [[Behavior Trees]] to drive [[Active Inference]].

---

# Mahalanobis Distance

How do you know if a bounding box seen in Frame 2 is the same person from Frame 1?

Amateurs use Euclidean Distance (a straight line between two points). 
Experts use **Mahalanobis Distance**.

## The Geometry of Uncertainty
Euclidean distance treats space equally in all directions. But the [[Extended Kalman Filter]] produces an ellipsoid of uncertainty (the Covariance matrix $S$). 

If a person is walking fast along the X-axis, our uncertainty along the X-axis is stretched. A detection 1 meter away on the X-axis might be highly probable, while a detection 1 meter away on the Y-axis might be impossible.

## The Equation
$$ D^2 = (z - \hat{z})^T S^{-1} (z - \hat{z}) $$

Where:
- $z$ is the new measurement.
- $\hat{z}$ is where the EKF *predicted* the measurement would be.
- $S$ is the Innovation Covariance (our uncertainty about the prediction).

## The Gating Threshold
Because $D^2$ follows a Chi-Squared ($\chi^2$) distribution, we can draw a mathematical line in the sand. For a 3-DOF measurement (X, Y, Z), a 95% confidence interval is $7.81$. 
If $D^2 > 7.81$, it is mathematically impossible for that detection to be our tracked person. We reject it entirely.

This feeds directly into [[Data Association]].

---

# Data Association

Once you have [[Mahalanobis Distance]] determining the mathematical distance between predicted states and raw detections, you must solve the assignment problem.

If you have 3 detections from the [[Jetson Edge Node]] and 3 predicted tracks from the [[Extended Kalman Filter]], which detection belongs to which track?

## The Hungarian Algorithm
A naive approach assigns the closest detection to the first track. This is "Greedy" and fails when people cross paths.

The **Hungarian Algorithm** (Kuhn-Munkres) solves for the *global minimum cost*. It evaluates every possible permutation of Track-to-Detection assignments and finds the one arrangement that minimizes the total sum of Mahalanobis Distances.

If a Track is assigned a detection that exceeds the $7.81$ Chi-Squared threshold, the assignment is rejected (Gating), and the track enters a `[LOST]` state managed by the [[Behavior Trees]].

---

# Triangulation

A single 2D camera image has no depth. A bounding box $[u, v, w, h]$ tells you where a person is on the screen, but not where they are in the physical room.

To track in 3D space with our [[Extended Kalman Filter]], we must perform Stereo Triangulation using both of the [[Jetson Edge Node|Jetson Nodes]].

## The Epipolar Geometry
We calibrate the two cameras using a checkerboard to obtain:
1. Intrinsic Matrices ($K_1, K_2$)
2. Extrinsic Translation/Rotation ($R, t$)

When Camera 1 sees a person, that person must lie somewhere along a 3D ray extending from Camera 1's lens into the room. 
When Camera 2 sees the *same* person (verified via [[Data Association]]), they must lie on a 3D ray extending from Camera 2.

**Triangulation is simply finding the 3D point where those two mathematical rays intersect.**

This 3D $[X, Y, Z]$ coordinate is then fed into the EKF as a measurement $z$.

---

# Behavior Trees

Finite State Machines (FSMs) are brittle. If you use `if/else` logic to manage a robot's brain, your code will inevitably collapse into spaghetti. 

We use **Behavior Trees (BTs)**. This is how Halo programmed AI in 2004, and how modern ROS 2 (`Nav2`) programs autonomous navigation today.

## The Structure
A BT is a directed tree of nodes:
1. **Fallback Nodes (Selector - `?`)**: Tries children from left to right. Stops when one succeeds. (e.g., "Try to Track. If failed, try to Search").
2. **Sequence Nodes (`->`)**: Executes children left to right. Stops if any child fails. (e.g., "Pan camera TO target -> Read frame -> Detect").
3. **Condition Nodes**: Checks a truth (e.g., "Is Covariance $P$ low?").
4. **Action Nodes**: Does physical work (e.g., "Send ROI command to Jetson").

## Our Cognitive Tree
```text
Root
 └── Fallback (?)
      ├── Sequence (->) [Maintain Tracking]
      │    ├── Condition: Track CONFIRMED?
      │    ├── Condition: Uncertainty P < Threshold?
      │    └── Action: Send ROI Crop Command to Jetson
      │
      ├── Sequence (->) [Active Recovery]
      │    ├── Condition: Track LOST?
      │    ├── Action: Predict trajectory via EKF
      │    └── Action: Command Pan/Tilt Servo to intercept
      │
      └── Sequence (->) [Global Search]
           ├── Action: Send Full 1080p command to Jetson
           └── Action: Spin servos in sweeping pattern
```
This logic runs entirely on the [[KAMRUI AK1PLUS Mini PC]]. It brings [[Active Inference]] to life.

---

# ROS 2 TF Trees

A robot must know the spatial relationship of every atom in its body relative to the universe. We track this using the **Transform (TF) Tree**.

If you do not define a rigorous TF tree, your 3D math will fail, and your [[Digital Twin]] will be a chaotic mess.

## The Hierarchy
Transforms are always defined as `parent` $\rightarrow$ `child`.

```text
world  (The absolute origin of your room)
 │
 ├── base_link  (The center of your Mini PC / Robot)
 │
 ├── cam1_base  (The physical mounting bracket of Camera 1)
 │    │
 │    └── cam1_pan_link  (Rotates around Z-axis via Servo)
 │         │
 │         └── cam1_tilt_link  (Rotates around Y-axis via Servo)
 │              │
 │              └── cam1_optical  (The actual camera lens)
 │
 └── tracked_person_1 (The X,Y,Z coordinate output by the EKF)
```

## Why this is beautiful
When the [[Pan-Tilt Actuation]] servo rotates 30 degrees, we update the `cam1_pan_link` TF. 
Because of the hierarchical tree, ROS 2 *automatically* calculates how the `cam1_optical` frame moved in the `world` space. 

When the [[Jetson Edge Node]] detects a person, it detects them in `cam1_optical` space. We use `tf2` to instantly transform that detection into `world` space before feeding it to the [[Extended Kalman Filter]].

Math becomes seamless. Visualized beautifully in Foxglove.

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

---

# Jetson Edge Node

The [[Jetson Nano B01]] serves as the optical cortex of the system. 
It does **not** think. It merely processes what the [[KAMRUI AK1PLUS Mini PC|Brain]] tells it to process.

## The Zero-Copy C++ Pipeline
Python is too slow for edge vision. We write this node in modern C++.

1. **Wait for Command**: The node listens to a ROS 2 topic for an `ROI_Command`.
2. **Memory Map**: We pull a frame from the USB camera directly into GPU memory using V4L2. Zero CPU copying.
3. **Crop**: We crop the image to the exact 200x200 pixel Region of Interest requested by the Brain. 
4. **TensorRT**: We run YOLOv8-Nano (FP16 quantized) *only* on that cropped square. Inference drops from 20ms to 4ms.
5. **Publish**: We publish the resulting bounding box back to the Brain via ROS 2 FastDDS.

## The Beauty of Constraint
By refusing to process the full 1080p frame when we don't have to, the Jetson runs cooler, consumes less power, and leaves GPU cycles open. 
This is the physical manifestation of [[Active Inference]].

---

# Pan-Tilt Actuation

To truly embody intelligence, a robot must physically manipulate its environment or its own sensors. 

## The Hardware
- Standard micro servos (e.g., SG90 or MG996R).
- Controlled via GPIO PWM pins on a Raspberry Pi, Jetson, or a connected Arduino.

## The Control Theory (PID)
When the [[Extended Kalman Filter]] predicts a person's 3D coordinate, we want to keep that person dead-center in the camera's Field of View.

We don't just "snap" the camera. We use a **Proportional-Integral-Derivative (PID) Controller**.

- **Error ($e$)**: The difference between the center of the camera lens and the projected position of the person.
- **Proportional ($P$)**: Pushes the servo toward the target. "The further away, the harder I push."
- **Integral ($I$)**: Fixes steady-state error. "If I'm consistently slightly off-center, push a little harder over time."
- **Derivative ($D$)**: Dampens the movement. "Slow down as I get closer so I don't overshoot and violently shake the camera."

## The ROS 2 Bridge
The Mini PC runs the PID math and publishes a `std_msgs/Float64` to the `cam1_pan_cmd` topic. A simple node connected to the physical servos translates that Float64 (in radians) into a PWM pulse width.

This dynamically alters the [[ROS 2 TF Trees]].

---

# Digital Twin

The final layer of the architecture is how we visualize the AI's understanding of reality. We will use Foxglove Studio running on the [[KAMRUI AK1PLUS Mini PC]].

## The 3D Render
We do not just overlay bounding boxes on a flat video feed. 

We construct a 3D environment tied directly to the [[ROS 2 TF Trees]]. 
- The physical cameras are rendered as 3D models.
- If the [[Pan-Tilt Actuation]] rotates a physical camera, the virtual camera inside Foxglove rotates exactly in sync.
- The [[Extended Kalman Filter]] tracks are drawn as moving 3D spheres or cylinders on the virtual floor, leaving a decaying trail behind them to show velocity vectors.

This proves that the system is not doing "image processing." It is doing **Embodied Spatial Intelligence**.

---

