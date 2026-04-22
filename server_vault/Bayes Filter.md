---
tags: [math, fundamental]
---

# Bayes Filter

This is the root of everything in state estimation. [[Kalman Filter]], [[Extended Kalman Filter]], particle filters (AMCL) — they're all special cases of this one idea.

## The idea in one sentence
You have a belief about where something is. You get a noisy measurement. You combine your prior belief with the measurement to get a better belief, weighted by how confident you are in each.

## The two steps
**Predict** (motion model):
```
p(x_t | z_{1:t-1}) = ∫ p(x_t | x_{t-1}, u_t) · p(x_{t-1} | z_{1:t-1}) dx_{t-1}
```
"Where do I *think* the object is now, given where it was and how I expect it to move?"

**Update** (measurement model):
```
p(x_t | z_{1:t}) = η · p(z_t | x_t) · p(x_t | z_{1:t-1})
```
"Now that I've *seen* a measurement, how should I correct my prediction?"

η is just a normalizing constant so the probabilities sum to 1.

## Why it matters
- If you assume everything is Gaussian → you get the [[Kalman Filter]]
- If the models are nonlinear → you linearize and get the [[Extended Kalman Filter]]
- If nothing is Gaussian and everything is ugly → you use a particle filter (that's how AMCL works in Nav2)

## The key insight
The predict step *increases* uncertainty (you're less sure after the object moves).
The update step *decreases* uncertainty (you gain information from the sensor).
The balance between these two is what makes the filter work.

See [[Kalman Filter]] for the concrete implementation.
