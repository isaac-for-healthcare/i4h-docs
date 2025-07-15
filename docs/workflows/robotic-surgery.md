# Robotic Surgery

Complete surgical automation framework combining simulation, AI training, and deployment for robotic surgical systems.

## Overview

The robotic surgery workflow provides a comprehensive framework for developing and deploying autonomous surgical capabilities. Built on Isaac Sim and Isaac Lab, it enables researchers and developers to:

- :material-brain: Train AI policies for surgical manipulation tasks
- :material-animation: Simulate complex tissue interactions with realistic physics
- :material-robot-industrial: Deploy trained models to real surgical robots
- :material-chart-line: Evaluate performance with clinical metrics

### :material-package-variant: What's Included

:material-eye: **High-fidelity surgical scene rendering**  
Deformable tissue simulation powered by NVIDIA PhysX with realistic material properties

:material-download: **Pre-built environments**  
State machine implementations and RL environments for fundamental surgical tasks

:material-tools: **Development tools**  
Performance profiling, trajectory visualization, and debugging utilities

:material-robot: **Hardware support**  
Compatible with dVRK (da Vinci Research Kit), Virtual Incision MIRA, Universal Robots arms, and custom robot integration

---

## Get Started

<div class="grid cards" markdown>

-   ### :material-rocket-launch: **Quick Start Guide**
    
    Set up your development environment and run your first surgical simulation
    
    **What you'll learn:**

    - Install dependencies and drivers
    - Download required assets
    - Run example demonstrations
    - Understand the basic framework
    
    [View Setup Instructions →](robotic-surgery-quick-start.md)

-   ### :material-medical-bag: **State Machine Environments**
    
    Hand-crafted state machines for fundamental surgical subtasks
    
    **Available tasks:**

    - :material-robot-industrial: dVRK-PSM and STAR robot reaching
    - :material-gesture-two-double-tap: Dual-arm bimanual coordination
    - :material-needle: Suture needle lifting and manipulation
    - :material-shape-circle-plus: Peg block transfer tasks
    
    [Explore State Machines →](robotic-surgery-state-machine.md)

-   ### :material-brain: **Reinforcement Learning**
    
    Train adaptive AI policies for surgical automation
    
    **Training capabilities:**

    - :material-function: RSL-RL framework with PPO
    - :material-memory: Multi-GPU training support
    - :material-target: dVRK-PSM reaching tasks
    - :material-needle: Suture needle manipulation
    
    [Start Training →](robotic-surgery-reinforcement-learning.md)

</div>

---

## :material-puzzle: Extend with Your Own Assets

The robotic surgery workflow integrates seamlessly with custom hardware and patient models:

- :material-human: [**Bring Your Own Patient**](tutorials/bring-your-own-patient.md) - Convert medical imaging to surgical planning models
- :material-virtual-reality: [**Bring Your Own XR**](tutorials/bring-your-own-xr.md) - Use mixed reality for surgical planning
- :material-robot: **Bring Your Own Robot** - Integrate custom platforms
    - [MIRA Robot Teleoperation](tutorials/mira-teleoperation.md) - Remote operation of MIRA surgical robot
    - [Replace Franka Hand with Ultrasound](tutorials/franka-ultrasound-probe.md) - Hardware modification guide
