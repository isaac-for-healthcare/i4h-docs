# Installation Guide

Complete installation instructions for Isaac for Healthcare core infrastructure components.

## Overview

Isaac for Healthcare requires several NVIDIA platform components to be installed before you can use the workflows. This guide covers the installation of:

- **Isaac Sim**: Physics simulation and digital twin environment
- **Holoscan SDK**: Edge deployment and real-time processing
- **Isaac Lab**: Robot learning and control framework
- **CUDA & OptiX**: GPU acceleration and raytracing

---

## System Requirements

### Hardware Requirements
- **GPU**: NVIDIA RTX 3090 or better (24GB+ VRAM recommended)
- **CPU**: 16+ cores recommended
- **RAM**: 32GB minimum, 64GB recommended
- **Storage**: 100GB+ available space

### Software Requirements
- **OS**: Ubuntu 20.04 or 22.04 LTS
- **NVIDIA Driver**: 535+ (555+ recommended)
- **CUDA**: 12.6+
- **Python**: 3.10

---

## Core Infrastructure Installation

### 1. NVIDIA Driver and CUDA

```bash
# Check current driver version
nvidia-smi

# If driver < 535, update:
sudo apt update
sudo apt install nvidia-driver-555

# Install CUDA Toolkit
wget https://developer.download.nvidia.com/compute/cuda/12.6.0/local_installers/cuda_12.6.0_560.28.03_linux.run
sudo sh cuda_12.6.0_560.28.03_linux.run
```

### 2. Isaac Sim

Isaac Sim provides the core simulation environment for all workflows.

```bash
# Download Isaac Sim (requires NVIDIA Developer account)
# Visit: https://developer.nvidia.com/isaac-sim

# Install via Omniverse Launcher or pip
pip install isaacsim==4.2.0 isaacsim-extscache-physics==4.2.0

# Verify installation
python -c "import isaacsim; print(isaacsim.__version__)"
```

### 3. Holoscan SDK

Holoscan enables edge deployment and real-time processing.

```bash
# Add Holoscan repository
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:holoscan-sdk/release

# Install Holoscan
sudo apt update
sudo apt install holoscan

# Verify installation
holoscan --version
```

### 4. Isaac Lab

Isaac Lab provides robot learning and control capabilities.

```bash
# Clone Isaac Lab
git clone https://github.com/isaac-sim/IsaacLab.git
cd IsaacLab

# Create conda environment
conda create -n isaaclab python=3.10
conda activate isaaclab

# Install Isaac Lab
./isaaclab.sh --install

# Verify installation
python -c "import isaaclab; print(isaaclab.__version__)"
```

### 5. OptiX (for Sensor Simulation)

OptiX is required for GPU-accelerated sensor simulation.

```bash
# Download OptiX SDK 8.0
# Visit: https://developer.nvidia.com/optix

# Extract and set environment variable
export OPTIX_ROOT_DIR=/path/to/optix
echo 'export OPTIX_ROOT_DIR=/path/to/optix' >> ~/.bashrc
```

---

## Workflow-Specific Installation

After installing the core infrastructure, proceed to install your specific workflow.

