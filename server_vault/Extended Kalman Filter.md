---
tags: [math, fundamental]
---

# Extended Kalman Filter

The [[Kalman Filter]] assumes linear models (F and H are matrices). Real systems aren't linear. The EKF handles this by linearizing around the current estimate using Jacobians.

## When do you need this?
- Tracking in pixel coordinates → converting to world coordinates is nonlinear (involves division by depth)
- Tracking with a non-constant-velocity model (e.g., constant turn-rate)
- Any time F or H becomes a function instead of a matrix

## The change from KF
Instead of `x̂⁻ = F · x̂`, you use `x̂⁻ = f(x̂)` (a nonlinear function).
Instead of `y = z - H · x̂⁻`, you use `y = z - h(x̂⁻)` (a nonlinear function).

But you still need matrices for the covariance propagation. So you compute the **Jacobian**:
```
F_jacobian = ∂f/∂x  evaluated at x̂
H_jacobian = ∂h/∂x  evaluated at x̂⁻
```

Then plug these Jacobian matrices into the exact same KF equations. That's it. The EKF is just "KF but you re-linearize at every step."

## For our tracker
In [[Phase 4 - 3D Tracking]], when we move from 2D pixel tracking to 3D world tracking via [[Triangulation]], the measurement model h() becomes nonlinear (projecting a 3D point through the [[Camera Model]] to get pixel coordinates involves division). That's where EKF kicks in.

## The catch
Linearization only works well when the nonlinearity is mild near the current estimate. If your state estimate is way off (bad initialization), the Jacobian approximation is garbage and the filter diverges. For badly nonlinear systems, you'd use an Unscented Kalman Filter (UKF) or a particle filter instead.

For our use case with relatively smooth motion and decent YOLO detections, EKF is more than sufficient.
