---
tags: [concept]
---

# Track Lifecycle

A track isn't just a [[Kalman Filter]] — it's a state machine. Getting this right is the difference between a tracker that works in a demo and one that works in production.

## States
```
Detection ──▶ TENTATIVE ──▶ CONFIRMED ──▶ LOST ──▶ DEAD
                │                           │
                └── (delete if not          └── (delete after
                    confirmed in N frames)      max_age frames)
```

**TENTATIVE**: Just born. Created from an unmatched detection. Don't display it yet — it might be a false positive. Only promote to CONFIRMED if it gets matched in `n_init` consecutive frames (typically 3).

**CONFIRMED**: Real track. Display it, give it a visible ID, track it.

**LOST**: Wasn't matched in the last frame. The object might be occluded. Keep predicting its position using the [[Kalman Filter]] predict step (no update), but don't display it. If it gets matched again within `max_age` frames, bring it back to CONFIRMED.

**DEAD**: Been lost for too long (`max_age` exceeded). Delete the filter, free the ID.

## Why tentative tracks matter
YOLO produces false positives — a shadow, a reflection, a weird texture. Without the tentative stage, every false positive gets an ID and shows up on screen for one frame, making the output look terrible. Requiring 3 consecutive matches eliminates most of these.

## Why lost tracks matter
When two people cross paths in the camera view, one might occlude the other for 5-10 frames. If we immediately killed the track, we'd lose the person's identity forever. The lost state with KF prediction lets us "coast" through the occlusion and recover gracefully.

## Tuning
- `n_init = 3` usually works. Lower = more false tracks. Higher = slow to start tracking.
- `max_age = 30` (at 15fps, that's 2 seconds of occlusion). Depends on your application.

Implemented in [[Phase 2 - Hungarian and MOT]].
