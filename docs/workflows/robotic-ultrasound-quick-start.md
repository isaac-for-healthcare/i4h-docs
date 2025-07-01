---
title: Quick Start Guide
source: i4h-workflows/workflows/robotic_ultrasound/README.md
---

# Quick Start Guide

!!! info "Source"
    This content is synchronized from [`i4h-workflows/workflows/robotic_ultrasound/README.md`](https://github.com/isaac-for-healthcare/i4h-workflows/blob/main/workflows/robotic_ultrasound/README.md)
    
    To make changes, please edit the source file and run the synchronization script.

# Robotic Ultrasound Workflow

![Robotic Ultrasound Workflow](../../assets/images/robotic_us_workflow.jpg)

## Overview

The Robotic Ultrasound workflow enables autonomous and semi-autonomous ultrasound scanning using robot manipulators with force control and AI-guided positioning. This workflow combines real-time ultrasound simulation, robotic control, and machine learning for applications in diagnostic imaging, interventional guidance, and medical training.

## Getting Started

### Prerequisites

**Hardware Requirements:**
- Ubuntu 22.04
- NVIDIA GPU with RT Cores and 32GB+ memory (RTX 3090 or better)
- 50GB available disk space

**Software Requirements:**
- NVIDIA Driver 555+
- CUDA 12.6+
- Python 3.10
- RTI DDS License (free academic/trial available)

### Quick Start

Get up and running in 5 minutes:

```bash
# 1. Create conda environment
conda create -n robotic_ultrasound python=3.10 -y
conda activate robotic_ultrasound

# 2. Clone and enter repository
git clone https://github.com/isaac-for-healthcare/i4h-workflows.git
cd i4h-workflows

# 3. Run automated setup (choose your AI policy)
bash tools/env_setup_robot_us.sh --policy pi0  # or gr00tn1

# 4. Download required assets
i4h-asset-retrieve

# 5. Set environment variables
export PYTHONPATH=$PWD/workflows/robotic_ultrasound/scripts
export RTI_LICENSE_FILE=/path/to/your/rti_license.dat

# 6. Run example simulation
cd workflows/robotic_ultrasound
python scripts/simulation/liver_scan_demo.py
```

## Understanding the System

### Architecture Overview

The robotic ultrasound system consists of four main components:

1. **Simulation Environment**: Isaac Sim-based physics simulation with realistic patient models
2. **Ultrasound Simulation**: GPU-accelerated raytracing for real-time B-mode imaging
3. **Robot Control**: Force-compliant control with safety monitoring
4. **AI Policies**: Pre-trained models for autonomous scanning tasks

### Supported Configurations

**Robots:**
- Franka Emika Panda (7-DOF collaborative robot)
- Universal Robots UR5/UR10
- Custom robots via URDF import

**Ultrasound Probes:**
- Linear array (vascular, musculoskeletal)
- Curvilinear (abdominal, obstetric)
- Phased array (cardiac)

**AI Policies:**
- **PI0**: Vision-based policy from Physical Intelligence
- **GR00T-N1**: Multi-modal policy with force feedback

## Installation Guide

### Step 1: System Setup

**Install NVIDIA Driver (555+):**
```bash
# Check current version
nvidia-smi

# If upgrade needed, download from:
# https://www.nvidia.com/drivers
```

**Install CUDA (12.6+):**
```bash
# Follow official guide:
# https://docs.nvidia.com/cuda/cuda-quick-start-guide/
```

### Step 2: RTI DDS License

RTI DDS enables real-time communication between components:

1. Register at [RTI website](https://www.rti.com/free-trial) for free trial
2. Download license file (rti_license.dat)
3. Set environment variable:
   ```bash
   export RTI_LICENSE_FILE=/path/to/rti_license.dat
   ```

### Step 3: Dependency Installation

The setup script installs all dependencies automatically:

```bash
# From repository root
bash tools/env_setup_robot_us.sh --policy <choice>
```

**Policy Options:**
- `pi0` (default): Install PI0 policy dependencies
- `gr00tn1`: Install GR00T-N1 policy dependencies  
- `none`: Base dependencies only

**What Gets Installed:**
- Isaac Sim 4.5.0 (GPU simulation platform)
- Isaac Lab 2.1.0 (robotics framework)
- Ultrasound raytracing simulator
- Holoscan 2.9.0 (edge deployment)
- Policy-specific ML frameworks

**Note**: PyTorch version warnings during installation are expected and can be ignored.

### Step 4: Asset Download

Download simulation assets (patient models, robot meshes, etc.):

```bash
i4h-asset-retrieve
```

Assets are cached in `~/.cache/i4h-assets/`. First download is ~5GB.

### Step 5: Ultrasound Simulator Setup

**Option A: Pre-built Binary (Experimental)**
```bash
# Download from releases
wget https://github.com/isaac-for-healthcare/i4h-sensor-simulation/releases/download/v0.2.0rc1/raysim-linux-x86_64.tar.gz
tar -xzf raysim-linux-x86_64.tar.gz -C workflows/robotic_ultrasound/scripts/
```

**Option B: Build from Source (Recommended)**
Follow instructions at [Ultrasound Raytracing Simulator](https://github.com/isaac-for-healthcare/i4h-sensor-simulation/tree/main/ultrasound-raytracing#installation)

## How-to Guides

### Run a Basic Liver Scan

```python
# scripts/simulation/liver_scan_demo.py
from simulation.environments import LiverScanEnv
from simulation.configs import BasicConfig

# Create environment
env = LiverScanEnv(BasicConfig())

# Run automated scan
trajectory = env.generate_scan_trajectory()
for i, target in enumerate(trajectory):
    obs = env.step(target)
    ultrasound_image = obs['ultrasound_image']
    print(f"Scan point {i}: Force = {obs['force']:.1f}N")
```

### Teleoperate with Haptic Device

```bash
# Terminal 1: Start simulation
python scripts/simulation/teleoperation/teleop_se3_agent.py

# Terminal 2: Connect haptic device (optional)
python scripts/holoscan_apps/haply_controller.py
```

### Train Custom Policy

```bash
# Collect demonstrations
python scripts/simulation/state_machine/data_collection_manager.py \
    --task liver_scan \
    --num_episodes 100

# Train policy
python scripts/training/pi_zero/train.py \
    --dataset data/liver_scan_demos \
    --epochs 50
```

### Deploy to Real Robot

```python
# scripts/deploy_to_robot.py
from policy_runner import PolicyRunner
from dds import FrankaController

# Load trained policy
runner = PolicyRunner(
    policy_path="models/liver_scan_pi0.pth",
    robot_ip="192.168.1.100"
)

# Run with safety monitoring
runner.execute_with_safety(
    force_limit=10.0,  # Newtons
    velocity_limit=0.1  # m/s
)
```

## Available Components

### Simulation Environments
- **Liver Scan**: Autonomous scanning of liver phantom
- **Vascular Access**: Needle guidance for IV insertion  
- **Cardiac Echo**: Four-chamber heart view acquisition
- **Training Phantom**: Basic skills development

### State Machines
- **Data Collection**: Record expert demonstrations
- **Evaluation**: Benchmark policy performance
- **Replay**: Visualize recorded trajectories

### Holoscan Applications  
- **Clarius Integration**: Real ultrasound probe support
- **RealSense Cameras**: RGB-D perception
- **Haptic Controllers**: Force feedback devices

### Training Scripts
- **PI0 Training**: Vision-based imitation learning
- **GR00T-N1 Training**: Multi-modal policy learning

## Multi-Terminal Workflow

A complete system typically requires 4 terminal windows:

**Terminal 1 - Visualization:**
```bash
python scripts/utils/visualization.py
```

**Terminal 2 - Policy Runner:**
```bash
python scripts/policy_runner/run_policy.py --policy pi0
```

**Terminal 3 - Simulation with DDS:**
```bash
python scripts/simulation/environments/sim_with_dds.py
```

**Terminal 4 - Ultrasound Simulation:**
```bash
python scripts/simulation/ultrasound_raytracing.py
```

## Troubleshooting

### Common Issues

**"No RTI license found"**
- Ensure `RTI_LICENSE_FILE` environment variable is set
- Verify license file exists and is valid

**"CUDA out of memory"**
- Reduce simulation resolution in config
- Use smaller batch size for training
- Close other GPU applications

**"Module not found" errors**
- Verify `PYTHONPATH` includes scripts directory
- Ensure all dependencies installed successfully

**Poor ultrasound image quality**
- Increase ray samples in ultrasound config
- Check probe-phantom contact
- Verify material properties are set correctly

### Performance Optimization

- Use `--headless` flag for training without GUI
- Enable GPU memory pooling in configs
- Reduce physics substeps for faster simulation

## API Reference

### Core Classes

- `LiverScanEnv`: Main simulation environment
- `PolicyRunner`: Executes trained policies
- `DDSInterface`: Real-time communication
- `UltrasoundSimulator`: B-mode image generation

### Configuration

See `scripts/simulation/configs/` for detailed configuration options:
- `basic.py`: Default settings
- `advanced.py`: High-fidelity simulation
- `performance.py`: Optimized for speed

## Contributing

We welcome contributions! See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

## License

Apache License 2.0 - see [LICENSE](../../LICENSE) for details.