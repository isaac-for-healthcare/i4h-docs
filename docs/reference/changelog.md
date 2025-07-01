# Changelog

## Latest Release: v0.2.0 (2024-01-15)

### New Features
- **GR00T Policy Support** - Deploy NVIDIA's foundation model for humanoid robots
- **Improved Ultrasound Physics** - 30% more accurate tissue modeling
- **Docker Support** - Pre-built containers for quick deployment
- **Unified Installer** - Single command installation for all components

### Improvements
- 2x faster ultrasound rendering on RTX 4090
- Reduced memory usage by 40%
- Better error messages and diagnostics
- Simplified API for common tasks

### Bug Fixes
- Fixed DDS communication timeouts
- Resolved OptiX compatibility issues
- Fixed memory leaks in long-running simulations

---

## Version History

### v0.2.0 (2024-01-15)

**Highlights**: GR00T support, 2x performance, Docker containers

<details>
<summary>Full Changelog</summary>

#### Added
- GR00T foundation model integration
- Docker containers for all components
- Unified installer script
- Advanced ultrasound tissue models
- Multi-GPU support for training
- Real-time visualization improvements

#### Changed
- Simplified API for common operations
- Improved error messages
- Better default parameters
- Faster asset loading

#### Fixed
- DDS timeout issues (#45)
- OptiX 8.1 compatibility (#38)
- Memory leaks in simulator (#52)
- Asset path resolution (#41)

</details>

### v0.1.0 (2023-10-01)

**Initial Release**: Core framework with ultrasound simulation, robotic workflows, and asset catalog

<details>
<summary>Full Changelog</summary>

#### Components Released
- **i4h-sensor-simulation**: GPU-accelerated ultrasound raytracing
- **i4h-asset-catalog**: Medical asset management system  
- **i4h-workflows**: Robotic surgery and ultrasound workflows

#### Key Features
- Physics-based ultrasound simulation with OptiX
- Support for linear, curvilinear, and phased array probes
- Integration with Isaac Sim and IsaacLab
- DDS communication for distributed systems
- PI0 policy support for ultrasound scanning
- dVRK and STAR robot support for surgery
- Reinforcement learning infrastructure

</details>

