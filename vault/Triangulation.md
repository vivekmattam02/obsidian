---
tags: [math, geometry]
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
