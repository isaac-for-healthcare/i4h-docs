---
title: Holoscan Applications
source: i4h-workflows/workflows/robotic_ultrasound/scripts/holoscan_apps/README.md
generated: 2025-06-11
---

!!! info "Source"
    This content is synchronized from [`i4h-workflows/workflows/robotic_ultrasound/scripts/holoscan_apps/README.md`](https://github.com/isaac-for-healthcare/i4h-workflows/blob/main/workflows/robotic_ultrasound/scripts/holoscan_apps/README.md)
    
    To make changes, please edit the source file and run the synchronization script.

# Holoscan Apps
This folder contains Holoscan applications for robotic ultrasound.

## Building the applications

Run the following command to build the Holoscan SDK applications.

```
cmake -B build -S .
cmake --build build
```

## Running the applications

After building the applications, you can run them with the instructions below.

### RealSense Camera
```
python3 holoscan_apps/realsense/camera.py
```

### Clarius Cast
```
python3 holoscan_apps/clarius_cast/clarius_cast.py
```

### Clarius Solumn
```
python3 holoscan_apps/clarius_solumn/clarius_solumn.py
```

---

## Additional Resources

- [Holoscan SDK Documentation](https://docs.nvidia.com/holoscan/)
- [Edge Deployment Guide](../../how-to/ml/edge-deployment.md)
- [Hardware Integration](../../reference/workflows/hardware-integration.md)