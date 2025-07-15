# Telesurgery

Remote surgical operation with ultra-low latency streaming, haptic feedback, and real-time robot control.

## Overview

The telesurgery workflow enables surgeons to perform procedures remotely through high-fidelity video streaming and precise robotic control. This framework provides:

- Ultra-low latency video streaming with H.264/HEVC encoding
- Real-time bilateral control with haptic feedback
- Multi-camera surgical views with depth perception
- Secure DDS-based communication for patient safety

Supports both physical and simulated environments, enabling training, collaboration, and remote surgical care.

### Key Features

:material-speedometer: **Ultra-Low Latency**

- End-to-end latency < 150ms
- Hardware-accelerated video encoding
- Optimized network protocols
- Predictive control algorithms

:material-shield-check: **Safety & Reliability**

- Redundant communication channels
- Automatic failover mechanisms
- Force limiting and workspace constraints
- Emergency stop capabilities

:material-hospital: **Clinical Integration**

- HIPAA-compliant communication
- Audit logging and recording
- Integration with hospital systems
- Multi-user collaboration support

---

## Get Started


### :material-rocket-launch: **Quick Start Guide**

Set up your telesurgery environment for remote operation

**What you'll learn:**

- Configure patient and surgeon stations
- Set up network communication
- Run your first remote session
- Understand latency requirements

[View Setup Instructions →](telesurgery-quick-start.md)


---

## :material-puzzle: Extend with Your Own Assets

The telesurgery workflow integrates seamlessly with custom hardware and surgical scenarios:

- :material-human: [**Bring Your Own Patient**](tutorials/bring-your-own-patient.md) - Create patient-specific surgical scenarios
- :material-robot: **Bring Your Own Robot** - Integrate custom platforms
  - [MIRA Robot Teleoperation](tutorials/mira-teleoperation.md) - Remote operation of MIRA surgical robot
  - [Replace Franka Hand with Ultrasound](tutorials/franka-ultrasound-probe.md) - Hardware modification guide
- :material-virtual-reality: [**Bring Your Own XR**](tutorials/bring-your-own-xr.md) - Add mixed reality to enhance remote visualization