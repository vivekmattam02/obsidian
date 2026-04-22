---
tags: [phase, implementation]
---

# Phase 3 - Stereo Calibration

**Goal**: Calibrate the two USB cameras (one per [[Jetson Nano B01]]) to find their intrinsics and relative extrinsics. This is the foundation for [[Triangulation]] in Phase 4.

## Duration: ~3-4 days

## What you need
- A printed ChArUco board (print on A4 paper, tape to cardboard for flatness)
- Both USB cameras plugged into the Jetsons (or your laptop for calibration — easier)
- A room with decent lighting

## Steps
1. **Generate a ChArUco board**:
```python
import cv2
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
board = cv2.aruco.CharucoBoard((7, 5), 0.04, 0.02, aruco_dict)
img = board.generateImage((800, 600))
cv2.imwrite('charuco_board.png', img)
# Print this
```

2. **Capture calibration images**: Hold the board in front of both cameras simultaneously. Take 20-30 image pairs from different angles and distances. Make sure the board is fully visible in both views.

3. **Detect corners**: Use OpenCV's ChArUco detector on each image pair.

4. **Individual intrinsic calibration**:
```python
ret, K1, dist1, rvecs, tvecs = cv2.calibrateCamera(...)
ret, K2, dist2, rvecs, tvecs = cv2.calibrateCamera(...)
```
This gives you the [[Camera Model]] intrinsics for each camera.

5. **Stereo calibration** (the key step):
```python
ret, K1, dist1, K2, dist2, R, T, E, F = cv2.stereoCalibrate(
    objPoints, imgPoints1, imgPoints2, K1, dist1, K2, dist2, imageSize,
    flags=cv2.CALIB_FIX_INTRINSIC
)
```
R and T are the rotation and translation from Camera 1 to Camera 2. This is the [[Stereo Geometry]] we need.

6. **Verify the calibration**: Undistort both images, rectify them, and check that horizontal features are aligned (epipolar lines are horizontal). If they're not → your calibration is bad, retake images.

## Save the calibration
```python
import numpy as np
np.savez('stereo_calibration.npz', K1=K1, dist1=dist1, K2=K2, dist2=dist2, R=R, T=T)
```
The [[Tracker Node]] on Pi A loads this at startup.

## Common failures
- Board not flat → corners are wrong → calibration is garbage
- Too few images or all from similar angles → poor coverage of the lens
- Cameras moved after calibration → extrinsics are invalid. Mount them and calibrate in final position.

Next: [[Phase 4 - 3D Tracking]]
