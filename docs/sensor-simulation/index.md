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
    
    RGB-D simulation with photorealistic rendering
    
    **Includes:**

    - :material-microscope: Surgical microscope views
    - :material-video-vintage: Endoscopic cameras
    - :material-cube-scan: Depth and stereo vision
    - :material-palette-advanced: Multi-spectral imaging
    
    [Learn More →](cameras.md)

-   ### :material-cog: **Custom Sensors**
    
    Framework for implementing your own sensor models
    
    **Support for:**

    - :material-function-variant: Custom physics models
    - :material-creation: Novel imaging modalities
    - :material-lock: Proprietary sensors
    - :material-flask-outline: Research prototypes
    
    [Learn More →](../how-to/how-to-custom-sensors.md)

</div>
