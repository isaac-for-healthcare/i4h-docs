---
title: Ultrasound Raytracing Simulator
source: i4h-sensor-simulation/ultrasound-raytracing/README.md
---

!!! info "Source"
    This content is synchronized from [`i4h-sensor-simulation/ultrasound-raytracing/README.md`](https://github.com/isaac-for-healthcare/i4h-sensor-simulation/blob/main/ultrasound-raytracing/README.md)
    
    To make changes, please edit the source file and run the synchronization script.

# Ultrasound Raytracing Simulator

## Overview

A high-performance GPU-accelerated ultrasound simulator using NVIDIA OptiX raytracing technology. This library provides physically accurate ultrasound simulation with real-time performance, enabling applications in robotic guidance, AI training, and medical education.

## Getting Started

### Prerequisites

- **GPU**: NVIDIA GPU with Compute Capability 7.0+ (RTX 2000 series or newer)
- **CUDA**: Version 12.6 or higher
- **Driver**: NVIDIA Driver 555 or higher
- **OS**: Ubuntu 20.04 or 22.04
- **Build Tools**: CMake 3.24+, GCC 9+
- **Python**: 3.10+

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/isaac-for-healthcare/i4h-sensor-simulation.git
   cd i4h-sensor-simulation/ultrasound-raytracing
   ```

2. **Set up OptiX SDK**
   
   Download OptiX SDK 8.1 from [NVIDIA Developer](https://developer.nvidia.com/designworks/optix/downloads/legacy):
   
   ```bash
   # Make the downloaded script executable
   chmod +x NVIDIA-OptiX-SDK-8.1.0-linux64-x86_64-*.sh
   
   # Extract the SDK
   ./NVIDIA-OptiX-SDK-8.1.0-linux64-x86_64-*.sh
   
   # Move to the correct location
   mv NVIDIA-OptiX-SDK-8.1.0-linux64-x86_64 third_party/optix/
   ```

3. **Download anatomical models**
   
   ```bash
   # Install asset helper
   pip install git+ssh://git@github.com/isaac-for-healthcare/i4h-asset-catalog.git
   
   # Download and extract assets
   i4h-asset-retrieve
   
   # Copy organ meshes to project
   cp -r ~/.cache/i4h-assets/*/Props/ABDPhantom/Organs mesh/
   ```

4. **Install with uv (recommended)**
   
   ```bash
   # Create environment and install dependencies
   uv sync
   source .venv/bin/activate
   ```
   
   Alternative: Install with conda
   ```bash
   conda create -n ultrasound python=3.10 libstdcxx-ng -c conda-forge -y
   conda activate ultrasound
   pip install -e .
   ```

5. **Build the C++ components**
   
   ```bash
   # Configure with CMake
   cmake -DPYTHON_EXECUTABLE=$(which python) -DCMAKE_BUILD_TYPE=Release -B build-release
   
   # Build (use all CPU cores)
   cmake --build build-release -j $(nproc)
   ```

   Note: If you have multiple GPUs with different compute capabilities, specify one:
   ```bash
   export CUDA_VISIBLE_DEVICES=0  # Use first GPU only
   ```

6. **Verify installation**
   
   ```bash
   # Run basic example
   uv run examples/sphere_sweep.py
   
   # Launch interactive web demo
   uv run examples/server.py
   # Open http://localhost:8000 in your browser
   ```

## Quick Start Tutorial

Create your first ultrasound simulation:

```python
import raysim.cuda as rs
import numpy as np
import matplotlib.pyplot as plt

# 1. Set up the scene
materials = rs.Materials()
world = rs.World("water")  # Background medium

# 2. Add a target object
sphere = rs.Sphere(
    center=[0, 0, -145],      # 145mm below probe
    radius=40,                # 40mm radius
    material=materials.get_index("fat")
)
world.add(sphere)

# 3. Configure ultrasound probe
probe = rs.UltrasoundProbe(
    rs.Pose(position=[0, 0, 0], rotation=[0, np.pi, 0])
)

# 4. Set simulation parameters
sim_params = rs.SimParams()
sim_params.t_far = 180.0      # Maximum depth in mm

# 5. Run simulation
simulator = rs.RaytracingUltrasoundSimulator(world, materials)
b_mode_image = simulator.simulate(probe, sim_params)

# 6. Display result
plt.imshow(b_mode_image, cmap='gray', aspect='auto')
plt.title('Simulated B-mode Ultrasound')
plt.xlabel('Lateral Position')
plt.ylabel('Depth')
plt.show()
```

## Understanding the Simulator

### Architecture

The simulator combines several technologies for optimal performance:

1. **OptiX Ray Tracing**: Hardware-accelerated ray-scene intersection
2. **CUDA Kernels**: Parallel computation of acoustic propagation
3. **Python Bindings**: High-level interface for ease of use
4. **C++ Core**: Performance-critical algorithms

### Physics Model

The simulation implements realistic ultrasound physics:

- **Acoustic Impedance**: Material-dependent wave reflection
- **Attenuation**: Frequency-dependent signal loss
- **Scattering**: Sub-resolution tissue structure effects
- **Beamforming**: Delay-and-sum image reconstruction

### Probe Types

Three transducer geometries are supported:

```python
# Linear array - rectangular field of view
linear = rs.LinearArrayProbe(
    num_elements=128,
    pitch=0.3,  # mm between elements
    frequency=5e6  # 5 MHz
)

# Curvilinear - fan-shaped field of view
curved = rs.CurvilinearProbe(
    num_elements=128,
    radius=60,  # mm radius of curvature
    angular_width=np.pi/3  # 60 degree FOV
)

# Phased array - sector scan from small aperture
phased = rs.PhasedArrayProbe(
    num_elements=64,
    pitch=0.15,
    frequency=2.5e6
)
```

## How-to Guides

### Load Anatomical Models

```python
# Load liver mesh from file
liver = rs.TriangleMesh.from_file(
    "mesh/Organs/liver.ply",
    material=materials.get_index("liver")
)
world.add(liver)

# Transform mesh position
liver.set_transform(
    translation=[10, 0, -100],
    rotation=[0, np.pi/4, 0],
    scale=[1.2, 1.2, 1.2]
)
```

### Simulate Tissue Layers

```python
# Create layered phantom
world = rs.World("water")

# Add skin layer
skin_box = rs.Box(
    min_corner=[-50, -50, -5],
    max_corner=[50, 50, -3],
    material=materials.get_index("skin")
)
world.add(skin_box)

# Add fat layer
fat_box = rs.Box(
    min_corner=[-50, -50, -15],
    max_corner=[50, 50, -5],
    material=materials.get_index("fat")
)
world.add(fat_box)

# Add muscle layer
muscle_box = rs.Box(
    min_corner=[-50, -50, -50],
    max_corner=[50, 50, -15],
    material=materials.get_index("muscle")
)
world.add(muscle_box)
```

### Enable Advanced Features

```python
# High-quality simulation settings
sim_params = rs.SimParams()
sim_params.samples_per_element = 512  # More rays for better quality
sim_params.enable_multiple_scattering = True
sim_params.max_bounces = 5

# Performance settings
sim_params.use_fp16 = True  # Use half precision for speed
sim_params.tile_size = 16    # GPU optimization parameter
```

### Real-time Streaming

```python
# Set up continuous simulation
simulator = rs.RealtimeSimulator(world, materials)
simulator.set_probe(probe)

# Simulation loop
for frame in range(1000):
    # Update probe position
    angle = frame * 0.01
    probe.set_position([10 * np.sin(angle), 0, 0])
    
    # Get image (non-blocking)
    image = simulator.get_frame()
    
    # Process or display image
    process_image(image)
```

## Performance Optimization

### Benchmark Results

On NVIDIA RTX 6000 Ada (48GB):
- **Resolution**: 512x512 pixels
- **Frame Rate**: 136 FPS average
- **Latency**: 7.3ms per frame

Run benchmarks on your system:
```bash
uv run examples/benchmark.py
```

### Memory Management

```python
# Pre-allocate GPU memory
simulator = rs.RaytracingUltrasoundSimulator(
    world, 
    materials,
    preallocate_mb=4096  # Reserve 4GB
)

# Reuse simulator for multiple frames
for i in range(100):
    world.update_object_positions()  # Only update positions
    image = simulator.simulate(probe, sim_params)
```

### Multi-GPU Support

```python
# Use specific GPU
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'  # First GPU

# Or distribute across GPUs
from multiprocessing import Pool

def simulate_on_gpu(gpu_id):
    os.environ['CUDA_VISIBLE_DEVICES'] = str(gpu_id)
    # Run simulation...
    
with Pool(4) as p:
    results = p.map(simulate_on_gpu, range(4))
```

## API Reference

### Core Classes

#### `World`
Container for scene objects
- `add(object)`: Add geometric primitive or mesh
- `remove(object)`: Remove object from scene
- `clear()`: Remove all objects
- `set_background_material(name)`: Set ambient medium

#### `Materials`
Material property database
- `get_index(name)`: Get material ID by name
- `add_custom(properties)`: Define new material
- `list_available()`: Show all materials

#### `UltrasoundProbe`
Base class for transducers
- `set_pose(pose)`: Update position/orientation
- `get_element_positions()`: Get transducer geometry
- Subclasses: `LinearArrayProbe`, `CurvilinearProbe`, `PhasedArrayProbe`

#### `SimParams`
Simulation configuration
- `t_near`, `t_far`: Depth range (mm)
- `samples_per_element`: Ray density
- `frequency`: Ultrasound frequency (Hz)
- `enable_multiple_scattering`: Physics fidelity

#### `RaytracingUltrasoundSimulator`
Main simulation engine
- `simulate(probe, params)`: Generate B-mode image
- `simulate_rf(probe, params)`: Get raw RF data
- `get_statistics()`: Performance metrics

### Geometric Primitives

- `Sphere(center, radius, material)`
- `Box(min_corner, max_corner, material)`
- `Cylinder(center, axis, radius, height, material)`
- `TriangleMesh.from_file(path, material)`

## Examples

- [Basic Shapes](examples/sphere_sweep.py) - Simple geometric primitives
- [Liver Scan](examples/liver_sweep.py) - Anatomical model simulation
- [Web Interface](examples/server.py) - Interactive browser demo
- [Benchmark](examples/benchmark.py) - Performance testing
- [C++ Example](examples/cpp/main.cpp) - Direct C++ API usage

## Development

### Setting Up Development Environment

For VSCode users:
```bash
# Install development dependencies
uv pip install -e ".[dev]"

# Set up pre-commit hooks
pre-commit install

# Run tests
pytest tests/
```

### Building from Source

Debug build with symbols:
```bash
cmake -DCMAKE_BUILD_TYPE=Debug -B build-debug
cmake --build build-debug
```

### Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for:
- Code style guidelines
- Testing requirements
- Pull request process

## Troubleshooting

### Common Issues

**CUDA Architecture Mismatch**
```bash
# If you see "no kernel image available"
export CUDA_VISIBLE_DEVICES=0  # Use single GPU
# Rebuild with specific architecture
cmake -DCMAKE_CUDA_ARCHITECTURES=86 -B build  # For RTX 3090
```

**OptiX Not Found**
```bash
# Verify OptiX location
ls third_party/optix/NVIDIA-OptiX-SDK-*/include/optix.h
# Should show the header file
```

**Python Import Error**
```bash
# Ensure build directory is in Python path
export PYTHONPATH=$PWD/build-release:$PYTHONPATH
```

## License

Apache License 2.0 - see [LICENSE](../../LICENSE) for details.