# Robotic Ultrasound

Autonomous ultrasound scanning with force-controlled robots and AI-guided imaging for diagnostic and interventional applications.

## Overview

The robotic ultrasound workflow enables autonomous and semi-autonomous ultrasound scanning using robot manipulators. This framework combines:

- Real-time ultrasound simulation with GPU-accelerated raytracing
- Force-compliant robotic control for safe patient interaction
- AI policies trained on expert demonstrations
- Edge deployment with Holoscan for clinical use

Supports diagnostic imaging, interventional guidance, vascular access, and medical training applications.

### :material-hammer-wrench: Hardware & Models

- **Robots**: Franka Panda, UR5/UR10, custom URDF support
- **Ultrasound**: Linear, curvilinear, phased array probes
- **Sensors**: RealSense cameras, force/torque sensors, haptic devices
- **Pre-trained**: Liver scanning, vascular access, force control, safety monitoring

### :material-application-brackets: Development & Applications

- **Tools**: Multi-terminal orchestration, real-time visualization, performance profiling
- **Clinical**: Diagnostic automation, needle guidance, training simulation, telemedicine

---

## Get Started

<div class="grid cards" markdown>

-   ### :material-rocket-launch: **Quick Start Guide**
    
    Set up your environment and run your first ultrasound scan simulation
    
    **What you'll learn:**

    - Install DDS and dependencies
    - Configure ultrasound simulator
    - Run liver scan demo
    - Understand system architecture
    
    [View Setup Instructions →](robotic-ultrasound-quick-start.md)

-   ### :fontawesome-solid-wave-square: **Simulation & Scanning**
    
    Create realistic ultrasound environments and scanning scenarios
    
    **Available environments:**

    - Liver phantom scanning
    - Vascular access guidance
    - Cardiac echo acquisition
    - Custom anatomy support
    
    [Explore Simulation →](robotic-ultrasound-simulation.md)

-   ### :material-access-point-network: **Real-time Communication**
    
    Connect robots, sensors, and compute nodes with DDS
    
    **DDS capabilities:**

    - Low-latency robot control
    - Multi-sensor fusion
    - Distributed computing
    - Hardware abstraction
    
    [Learn DDS Setup →](robotic-ultrasound-dds-communication.md)

-   ### :material-memory: **Holoscan Applications**
    
    Deploy AI-powered ultrasound applications at the edge
    
    **Edge applications:**

    - Clarius probe integration
    - RealSense perception
    - Real-time inference
    - Clinical deployment
    
    [Build Apps →](robotic-ultrasound-holoscan-apps.md)

-   ### :material-brain: **AI Policy Runner**
    
    Execute trained policies for autonomous scanning
    
    **Supported policies:**

    - PI-0 vision-based control
    - GR00T-N1 multimodal
    - Custom trained models
    - Safety monitoring
    
    [Run Policies →](robotic-ultrasound-policy-runner.md)

-   ### :material-school: **Training & Customization**
    
    Train your own policies and customize the workflow
    
    **Training options:**

    - Collect demonstrations
    - Imitation learning
    - Sim-to-real transfer
    - Custom robot integration
    
    **Training guides:**
    
    - [PI-Zero Training](robotic-ultrasound-train-pi-zero.md)
    - [GR00T-N1 Training](robotic-ultrasound-train-gr00t.md)

-   ### :material-chart-line: **Visualization Tools**
    
    Monitor and debug your robotic ultrasound system in real-time
    
    **Visualization features:**

    - Multi-camera feeds (RGB/depth)
    - Live ultrasound imaging
    - Robot state monitoring
    - DDS data flow inspection
    
    [View Tools →](robotic-ultrasound-visualization-tools.md)

</div>

---

## :material-puzzle: Extend with Your Own Assets

The robotic ultrasound workflow integrates seamlessly with custom hardware and patient models:

- :material-human: [**Bring Your Own Patient**](tutorials/bring-your-own-patient.md) - Convert medical imaging to ultrasound phantoms
- :material-virtual-reality: [**Bring Your Own XR**](tutorials/bring-your-own-xr.md) - Teleoperate with mixed reality devices
- :material-robot: **Bring Your Own Robot** - Integrate custom platforms
    - [MIRA Robot Teleoperation](tutorials/mira-teleoperation.md) - Remote operation of MIRA surgical robot
    - [Replace Franka Hand with Ultrasound](tutorials/franka-ultrasound-probe.md) - Hardware modification guide

