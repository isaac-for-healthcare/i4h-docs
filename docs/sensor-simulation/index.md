# Sensor Simulation

Physics-based medical sensor emulation for AI training and validation. Generate photorealistic synthetic data with GPU-accelerated performance for healthcare robotics applications.

## What is Sensor Simulation?

Sensor Simulation provides high-fidelity emulation of medical imaging devices used in healthcare robotics. Each simulator implements physically accurate models to ensure synthetic data transfers seamlessly to real hardware.

**Key Benefits:**

- :material-infinity: **Unlimited Training Data**: Generate diverse datasets without patient involvement
- :material-target: **Ground Truth Labels**: Perfect annotations for every frame
- :material-shield-alert: **Edge Case Testing**: Safely simulate rare or dangerous scenarios
- :material-link-variant: **Hardware-in-the-Loop**: Connect simulated sensors to real control systems
- :material-flash: **Real-time Performance**: 30+ FPS on modern GPUs

---

## Available Sensors

<div class="grid cards" markdown>

-   ### :fontawesome-solid-wave-square: **Ultrasound Simulation**
    
    GPU-accelerated ultrasound imaging with realistic tissue interactions
    
    **Features:**

    - :material-format-list-bulleted-type: Linear, curvilinear, and phased array probes
    - :material-timer: Real-time B-mode and Doppler imaging
    - :material-texture: Tissue-specific acoustic properties
    - :material-grain: Speckle and artifact modeling
    
    [Learn More →](ultrasound-raytracing.md)

-   ### :material-camera: **Camera & Depth Sensors**
    
    Photorealistic RGB and depth sensing powered by Isaac Sim
    
    **Capabilities:**

    - :material-microscope: Surgical vision systems (endoscopes, microscopes)
    - :material-cube-scan: Depth sensing for navigation and collision avoidance
    - :material-camera-control: Multiple camera models and calibration support
    - :material-layers-triple: Multi-sensor rigs and sensor fusion
    
    [Learn More →](cameras.md)


</div>
