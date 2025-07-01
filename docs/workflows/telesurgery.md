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

<div class="grid cards" markdown>

-   ### :material-rocket-launch: **Quick Start Guide**
    
    Set up your telesurgery environment for remote operation
    
    **What you'll learn:**

    - Configure patient and surgeon stations
    - Set up network communication
    - Run your first remote session
    - Understand latency requirements
    
    [View Setup Instructions →](telesurgery-quick-start.md)

-   ### :material-hospital-box: **Patient-Side Setup**
    
    Configure the patient-side robot and camera systems
    
    **Components:**

    - Physical or simulated MIRA robot
    - Multi-camera capture (room + robot views)
    - Video encoding and streaming
    - Safety monitoring systems
    
    [Configure Patient Side →](telesurgery-patient-setup.md)

-   ### :fontawesome-solid-user-doctor: **Surgeon-Side Setup**
    
    Set up the surgeon's control station
    
    **Control options:**

    - Gamepad controller interface
    - Haply haptic device integration
    - Multi-display visualization
    - Low-latency video decoding
    
    [Configure Surgeon Side →](telesurgery-surgeon-setup.md)

-   ### :material-lan: **Network & Communication**
    
    Configure DDS for reliable real-time communication
    
    **Network features:**

    - RTI DDS configuration
    - QoS optimization for video
    - Latency monitoring
    - Secure peer-to-peer setup
    
    [Setup Communication →](telesurgery-network-setup.md)

-   ### :material-video-wireless: **Video Streaming**
    
    Optimize video codecs for surgical visualization
    
    **Streaming options:**

    - H.264/HEVC encoding
    - NVIDIA Video Codec SDK
    - Multi-stream synchronization
    - Adaptive bitrate control
    
    [Configure Streaming →](telesurgery-video-streaming.md)

-   ### :material-memory: **Edge Deployment**
    
    Deploy on NVIDIA IGX for clinical use
    
    **Deployment features:**

    - Holoscan operator integration
    - Real-time performance monitoring
    - Docker containerization
    - Hardware acceleration
    
    [Deploy to Edge →](telesurgery-edge-deployment.md)

</div>

---

## :material-puzzle: Extend with Your Own Assets

The telesurgery workflow integrates seamlessly with custom hardware and surgical scenarios:

- :material-human: [**Bring Your Own Patient**](../how-to/how-to-bring-your-own-patient.md) - Create patient-specific surgical scenarios
- :material-robot: [**Bring Your Own Robot**](../how-to/how-to-bring-your-own-robot.md) - Integrate your teleoperated surgical platform
- :material-virtual-reality: [**Bring Your Own XR**](../how-to/how-to-bring-your-own-xr.md) - Add mixed reality to enhance remote visualization