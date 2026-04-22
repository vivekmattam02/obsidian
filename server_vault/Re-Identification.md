---
tags: [concept]
---

# Re-Identification

ReID answers the question: "I saw a person leave Camera 1's view. A person just appeared in Camera 2. Are they the same person?"

This is different from [[Data Association]] within a single camera (which uses motion prediction). ReID uses **appearance** — what the person looks like.

## Simple approach: color histogram
1. Crop the bounding box from the image
2. Convert to HSV (more robust to lighting than RGB)
3. Compute a histogram of the H and S channels
4. Compare with stored histograms using Bhattacharyya distance or correlation

Pros: Runs on any hardware, no GPU needed, fast.
Cons: Fails if people wear similar clothes. Sensitive to lighting changes.

## Better approach: deep ReID embeddings
1. Run a small CNN (like OSNet or a MobileNetV2-based ReID model) on the cropped bbox
2. Get a 128-d or 256-d embedding vector
3. Compare embeddings using cosine similarity
4. If similarity > threshold → same person

This is what DeepSORT does. On our [[Jetson Nano B01]], we could run a tiny ReID model alongside YOLO, but memory is tight (YOLO already uses ~800MB of the 4GB). Color histograms might be more practical.

## Gallery management
For each CONFIRMED track ([[Track Lifecycle]]), store the last N appearance descriptors. When a new detection is unmatched, compare it against the galleries of recently LOST tracks. If there's a strong appearance match, resurrect the track with the same ID.

## For our project
This is a [[Phase 5 - Distributed Pipeline]] extension. Start with color histograms (free, no model needed). If that works, explore a tiny ReID model on the Jetsons if memory allows.
