---
tags: [systems]
---

# TensorRT Deployment

How we get YOLOv8-Nano running fast on the [[Jetson Nano B01]]. You've done this before on the Orin Nano for your Vortex project — the Nano is the same workflow but with weaker hardware.

## The pipeline
```
PyTorch model (.pt) → ONNX (.onnx) → TensorRT engine (.engine)
```

### Step 1: Export to ONNX
```python
from ultralytics import YOLO
model = YOLO('yolov8n.pt')
model.export(format='onnx', imgsz=640, simplify=True)
```

### Step 2: Build TensorRT engine ON the Jetson
The engine must be built on the target hardware (Maxwell FP16):
```bash
/usr/src/tensorrt/bin/trtexec \
    --onnx=yolov8n.onnx \
    --saveEngine=yolov8n.engine \
    --fp16
```
This takes 10-20 minutes on the Nano. Do it once, save the `.engine` file.

### Step 3: Run inference
Load the engine, allocate CUDA buffers, run:
```python
import tensorrt as trt
import pycuda.driver as cuda
# ... (boilerplate: create context, allocate input/output buffers)
# Copy image to GPU → execute → copy results back
```

## Gotchas on the Nano
- JetPack 4.6 ships with TensorRT 8.0. Some newer ONNX ops might not be supported. If export fails, try `opset=11`.
- Maxwell doesn't support INT8 well. Stick to FP16.
- The first inference after loading is slow (CUDA warmup). Run a dummy inference before entering the main loop.
- Monitor GPU temp: `tegrastats`. If it hits 100°C, it'll throttle and your FPS drops to 5.

## Memory budget
- CUDA context: ~300MB
- YOLOv8-Nano FP16 engine: ~15MB
- Input frame (640x640x3 FP32): ~5MB
- Output tensors: ~2MB
- **Total: ~400-500MB** out of 4GB. Leaves room for the camera pipeline and OS.

If we want to also run a ReID model ([[Re-Identification]]), it needs to fit in the remaining ~3.5GB. A MobileNetV2-based ReID model would add ~200MB. Feasible but tight.
