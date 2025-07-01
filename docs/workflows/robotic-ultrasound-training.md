---
title: Training & Customization
source: i4h-workflows/workflows/robotic_ultrasound/scripts/training
generated: 2025-06-11
---

!!! info "Source"
    This content is synchronized from [`i4h-workflows/workflows/robotic_ultrasound/scripts/training`](https://github.com/isaac-for-healthcare/i4h-workflows/tree/main/workflows/robotic_ultrasound/scripts/training)
    
    To make changes, please edit the source file and run the synchronization script.

# Training & Customization

Train custom policies for robotic ultrasound and extend the workflow with your own robots, sensors, and applications.

## Training Guides

### PI-Zero Training

Train vision-based policies using the PI-Zero framework from Physical Intelligence.

[**View PI-Zero Training Guide →**](training/pi-zero.md)

Key features:

- Vision-language-action model
- LoRA fine-tuning support
- LeRobot data format
- ~22GB GPU memory for LoRA

### GR00T-N1 Training

Train multi-modal policies with NVIDIA's GR00T foundation model.

[**View GR00T-N1 Training Guide →**](training/gr00t-n1.md)

Key features:

- Cross-embodiment foundation model
- Multi-modal inputs (vision, language, force)
- LeRobot data conversion
- Optimized for edge deployment