# System Requirements

This consolidated reference document outlines both hardware and software requirements for running the i4h framework and its components.

## Hardware Requirements

### System Requirements Overview

| Component | CPU | GPU | Memory | Storage | Operating System |
|-----------|-----|-----|--------|---------|------------------|
| Sensor Simulation | 8+ cores | NVIDIA RTX/Quadro/Tesla with RT Cores | 16GB+ | 20GB+ | Ubuntu 22.04 |
| Asset Catalog | 4+ cores | Any NVIDIA GPU | 8GB+ | 50GB+ | Ubuntu 22.04 |
| Robotic Ultrasound | 8+ cores | NVIDIA RTX/Quadro/Tesla (32GB+) | 32GB+ | 50GB+ | Ubuntu 22.04 |
| Robotic Surgery | 8+ cores | NVIDIA RTX/Quadro/Tesla | 32GB+ | 50GB+ | Ubuntu 22.04 |

### Recommended Hardware Configurations

#### Entry-Level Development System

- **CPU**: AMD Ryzen 7 5800X or Intel i7-12700K
- **GPU**: NVIDIA RTX 3070 Ti or RTX 4070 (12GB)
- **RAM**: 32GB DDR4-3600
- **Storage**: 1TB NVMe SSD + 2TB SATA SSD
- **Power Supply**: 750W Gold

Suitable for: Basic development, ultrasound simulation, single-component testing

#### Mid-Range Research System

- **CPU**: AMD Ryzen 9 7950X or Intel i9-13900K
- **GPU**: NVIDIA RTX 4090 (24GB)
- **RAM**: 64GB DDR5-6000
- **Storage**: 2TB NVMe SSD + 4TB SATA SSD
- **Power Supply**: 1000W Platinum

Suitable for: Robotic workflows, policy training, multi-component testing

#### High-Performance Research System

- **CPU**: AMD Threadripper Pro 7975WX
- **GPU**: NVIDIA RTX 6000 Ada (48GB) or dual RTX 4090
- **RAM**: 128GB DDR5-5600
- **Storage**: 4TB NVMe SSD + 8TB SATA SSD
- **Power Supply**: 1600W Platinum

Suitable for: Full multi-component workflows, large-scale policy training, complex simulations

### Component-Specific Hardware Requirements

#### Ultrasound Raytracing Simulator

The ultrasound raytracing simulator has the most stringent GPU requirements:


- **Architecture**: Ampere (RTX 30 series) or newer strongly recommended
- **Compute Capability**: 8.6 or higher
- **VRAM**: 16GB+ recommended for complex scenes
- **RT Cores**: Required for hardware-accelerated ray tracing
- **CUDA Cores**: More CUDA cores provide better performance

**Note**: GPUs without RT Cores (e.g., A100, H100) are not supported for the ultrasound raytracing simulator, as they lack hardware acceleration for ray tracing.

#### Robotic Ultrasound Workflow

For the complete robotic ultrasound workflow:


- **VRAM**: 32GB+ recommended for running all components simultaneously
- **Multiple GPUs**: Can split components across multiple GPUs if available
- **PCIe Bandwidth**: Higher bandwidth improves performance for multi-GPU setups

#### Robotic Surgery Workflow

For the robotic surgery workflow:


- **VRAM**: 16GB+ for single environment, 32GB+ for multi-environment training
- **CUDA Cores**: More CUDA cores improve performance for physics simulation
- **Tensor Cores**: Beneficial for reinforcement learning training

## Software Requirements

### Operating System

The i4h framework is primarily designed for and tested on:


- **Ubuntu 22.04 LTS (Jammy Jellyfish)**

### Core Software Components

| Component | Minimum Version | Purpose |
|-----------|----------------|---------|
| NVIDIA Driver | 555.0+ | GPU driver |
| CUDA Toolkit | 12.6+ | GPU programming |
| OptiX | 8.1.0 | Ray tracing |
| Python | 3.10 | Programming environment |
| CMake | 3.24.0+ | Building C++ components |
| GCC/G++ | 9.4.0+ | C++ compilation |

### Software Compatibility Matrix

| Component | Python | CUDA | NVIDIA Driver | OptiX | IsaacSim | IsaacLab |
|-----------|--------|------|---------------|-------|----------|----------|
| Ultrasound Simulator | 3.10 | 12.6+ | 555+ | 8.1 | N/A | N/A |
| Asset Catalog | 3.10 | N/A | 525+ | N/A | 4.5.0 | N/A |
| Robotic Ultrasound | 3.10 | 12.6+ | 555+ | 8.1* | 4.5.0 | 2.0.2 |
| Robotic Surgery | 3.10 | 12.1+ | 525+ | N/A | 4.5.0 | 2.0.2 |

*Required for ultrasound raytracing simulation

### NVIDIA Software Stack

#### NVIDIA Driver

- **Minimum Version**: 555.0 or newer
- **Recommended Installation Method**: 
  ```bash
  sudo apt-get install nvidia-driver-555
  ```
- **Verification**: 
  ```bash
  nvidia-smi
  ```

#### CUDA Toolkit

- **Minimum Version**: CUDA 12.6 or newer
- **Installation**: Follow the [NVIDIA CUDA Installation Guide](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html)
- **Verification**:
  ```bash
  nvcc --version
  ```

#### NVIDIA OptiX

- **Version**: OptiX 8.1.0
- **Download**: Available from [NVIDIA OptiX Downloads](https://developer.nvidia.com/designworks/optix/downloads/legacy)
- **Installation**: Follow instructions in the ultrasound-raytracing README

### Python Environment

- **Required Version**: Python 3.10
- **Not Supported**: Python 3.11 or newer (due to compatibility with IsaacSim)
- **Recommended Installation**: via Conda or system package manager

#### Conda Environment

```bash
conda create -n i4h python=3.10
conda activate i4h
```

#### Required Python Packages

| Package | Minimum Version | Purpose |
|---------|----------------|---------|
| numpy | 1.23.0 | Numerical computing |
| pytorch | 2.5.1 | Deep learning (for IsaacLab) |
| torch | 2.6.0 | Deep learning (for OpenPI) |
| matplotlib | 3.7.0 | Visualization |
| pynvml | 11.0.0 | NVIDIA GPU monitoring |
| pytest | 7.0.0 | Testing |
| cmake | 3.24.0 | Building C++ components |

### Component-Specific Software Requirements

#### Ultrasound Raytracing Simulator

- **CUDA 12.6+**
- **OptiX 8.1**
- **CMake 3.24+**
- **GCC/G++ 9.4+**

#### Asset Catalog

- **Python 3.10**
- **IsaacSim 4.5.0** (for asset downloading)

#### Robotic Ultrasound Workflow

- **Python 3.10**
- **IsaacSim 4.5.0**
- **IsaacLab 2.0.2**
- **RTI DDS** (with license)
- **Lerobot (from Hugging Face)**
- **Holoscan 2.9.0**

For PI0 policy (default):

- **OpenPI**

For GR00T N1 policy:

- **Isaac-GR00T**

#### Robotic Surgery Workflow

- **Python 3.10**
- **IsaacSim 4.5.0**
- **IsaacLab 2.0.2**
- **Robotic Surgery Extensions**
