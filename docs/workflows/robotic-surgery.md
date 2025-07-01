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

:material-download: **Pre-trained models**  
Ready-to-use policies for needle passing, tissue retraction, peg transfer, and basic suturing

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

-   ### :material-medical-bag: **Surgical Tasks**
    
    Pre-built surgical tasks ready to simulate and customize
    
    **Available tasks:**

    - :material-needle: Needle passing and handover
    - :material-hand-back-right: Tissue manipulation and retraction
    - :material-shape-circle-plus: Peg transfer and placement
    - :material-vector-polyline: Suturing demonstrations
    
    [Explore Tasks →](robotic-surgery-surgical-tasks.md)

-   ### :material-brain: **Train AI Policies**
    
    Use reinforcement learning to train surgical automation
    
    **Training options:**

    - :material-function: PPO and SAC algorithms
    - :material-gpu: Multi-GPU training support
    - :material-stairs: Curriculum learning
    - :material-sync: Sim-to-real transfer
    
    [Start Training →](../how-to/how-to-surgery-state-machines.md)

</div>

---

## :material-puzzle: Extend with Your Own Assets

The robotic surgery workflow integrates seamlessly with custom hardware and patient models:

- :material-human: [**Bring Your Own Patient**](../how-to/how-to-bring-your-own-patient.md) - Convert medical imaging to surgical planning models
- :material-robot: [**Bring Your Own Robot**](../how-to/how-to-bring-your-own-robot.md) - Add your surgical robot platform
- :material-virtual-reality: [**Bring Your Own XR**](../how-to/how-to-bring-your-own-xr.md) - Use mixed reality for surgical planning
