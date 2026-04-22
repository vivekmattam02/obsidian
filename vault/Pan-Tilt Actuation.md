---
tags: [hardware, control]
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
