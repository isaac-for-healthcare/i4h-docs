# Workflows

Complete end-to-end healthcare robotics applications that combine simulation, training, and deployment. Workflows provide production-ready implementations that integrate all aspects of the Isaac for Healthcare platform.

## What are Workflows?

Workflows are pre-built, modular robotics applications that demonstrate the full development journey from simulation to deployment. Each workflow includes:

- **Complete Implementation**: Full source code with simulation environments
- **Pre-trained Policies**: AI models ready for deployment or fine-tuning
- **Evaluation Metrics**: Benchmarks and validation tools
- **Hardware Integration**: Recipes for connecting to real robots and sensors
- **Deployment Guides**: Instructions for edge deployment with Holoscan

![Workflow Overview](../assets/images/workflow.png)

---

## Available Workflows

<div class="grid cards" markdown>

-   ### :material-heart-pulse: **Robotic Ultrasound**
    
    Autonomous diagnostic imaging with force-controlled scanning
    
    **Key Features:**

    - Real-time force feedback
    - AI-guided probe positioning  
    - Automated organ scanning
    
    [Learn More →](robotic-ultrasound.md)

-   ### :material-robot: **Robotic Surgery**
    
    Surgical automation with dVRK and custom surgical robots
    
    **Key Features:**

    - Dual-arm coordination
    - Reinforcement learning
    - Tissue manipulation
    
    [Learn More →](robotic-surgery.md)

-   ### :material-remote-desktop: **Telesurgery**
    
    Remote surgical operation with haptic feedback
    
    **Key Features:**

    - Ultra-low latency streaming
    - Multi-camera views
    - Haptic device integration
    
    [Learn More →](telesurgery.md)

</div>

---

## Extend the Platform

Isaac for Healthcare is designed to be extensible. Learn how to customize and extend the platform:

**Tutorials:**

- [Bring Your Own Patient](tutorials/bring-your-own-patient.md) - Convert medical imaging to simulation
- [Bring Your Own XR](tutorials/bring-your-own-xr.md) - Mixed reality devices
- **Bring Your Own Robot** - Integrate custom platforms
    - [MIRA Robot Teleoperation](tutorials/mira-teleoperation.md) - Remote operation of MIRA surgical robot
    - [Replace Franka Hand with Ultrasound](tutorials/franka-ultrasound-probe.md) - Hardware modification guide

These tutorials show how to extend any workflow with your own hardware, patients, robots, and interaction devices.
