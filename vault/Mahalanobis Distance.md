---
tags: [math, probability]
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
