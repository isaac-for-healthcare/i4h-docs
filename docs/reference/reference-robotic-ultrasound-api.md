# Robotic Ultrasound API Reference

This page provides comprehensive API reference for the robotic ultrasound workflow components.

## Core Components

### DDS Communication

#### Publisher Classes

```python
from workflows.robotic_ultrasound.scripts.dds.publisher import (
    FrankaControlPublisher,
    CameraControlPublisher,
    TargetControlPublisher,
    USPDataPublisher
)

# Initialize publishers
franka_pub = FrankaControlPublisher(domain_id=0)
camera_pub = CameraControlPublisher(domain_id=0)
target_pub = TargetControlPublisher(domain_id=0)
usp_pub = USPDataPublisher(domain_id=0)

# Publish control commands
franka_pub.publish_joint_positions([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7])
camera_pub.publish_capture_command()
target_pub.publish_target_pose([0.5, 0.3, 0.2], [0, 0, 0, 1])
```

#### Subscriber Classes

```python
from workflows.robotic_ultrasound.scripts.dds.subscriber import (
    FrankaInfoSubscriber,
    CameraInfoSubscriber,
    TargetInfoSubscriber,
    USPInfoSubscriber
)

# Initialize subscribers
franka_sub = FrankaInfoSubscriber(domain_id=0)
camera_sub = CameraInfoSubscriber(domain_id=0)
target_sub = TargetInfoSubscriber(domain_id=0)
usp_sub = USPInfoSubscriber(domain_id=0)

# Set up callbacks
def on_franka_state(data):
    print(f"Robot joint positions: {data.joint_positions}")

franka_sub.set_callback(on_franka_state)
franka_sub.start_listening()
```

### State Machine Components

#### Liver Scan State Machine

```python
from workflows.robotic_ultrasound.scripts.simulation.environments.state_machine.liver_scan_sm import (
    LiverScanStateMachine
)

# Initialize state machine
sm = LiverScanStateMachine(
    robot_prim_path="/World/Franka",
    ultrasound_prim_path="/World/UltrasoundProbe",
    target_prim_path="/World/LiverPhantom"
)

# Configure scan parameters
sm.set_scan_pattern("raster")
sm.set_scan_bounds(width=0.1, height=0.08, depth=0.05)
sm.set_probe_pressure(5.0)  # Newtons

# Start scan
sm.start_scan()
```

#### Base State Module

```python
from workflows.robotic_ultrasound.scripts.simulation.environments.state_machine.modules.base_module import (
    BaseModule
)

class CustomModule(BaseModule):
    def __init__(self, name: str):
        super().__init__(name)
        self.target_reached = False
    
    def update(self, dt: float) -> str:
        """Update module and return next state"""
        if self.target_reached:
            return "complete"
        else:
            return "in_progress"
    
    def reset(self):
        """Reset module state"""
        self.target_reached = False
```

### Policy Runners

#### Pi0 Policy Runner

```python
from workflows.robotic_ultrasound.scripts.policy_runner.pi0.runners import Pi0PolicyRunner

# Initialize policy runner
runner = Pi0PolicyRunner(
    policy_path="path/to/policy.pt",
    device="cuda"
)

# Configure environment
runner.setup_environment(
    robot_prim_path="/World/Franka",
    camera_prim_paths=["/World/Camera1", "/World/Camera2"]
)

# Run policy
action = runner.get_action(observation)
runner.apply_action(action)
```

#### GR00TN1 Policy Runner

```python
from workflows.robotic_ultrasound.scripts.policy_runner.gr00tn1.runners import GR00TN1PolicyRunner

# Initialize policy runner
runner = GR00TN1PolicyRunner(
    model_path="path/to/model.pth",
    config_path="path/to/config.yaml"
)

# Load policy
runner.load_policy()

# Run inference
with runner.inference_context():
    action = runner.predict(observation)
```

### Holoscan Applications

#### Clarius Cast Integration

```python
from workflows.robotic_ultrasound.scripts.holoscan_apps.clarius_cast.clarius_cast import (
    ClariusCastApp
)

# Initialize Clarius Cast application
app = ClariusCastApp()

# Configure connection
app.set_device_ip("192.168.1.100")
app.set_streaming_params(
    gain=50,
    depth=80,
    frequency=5.0
)

# Start streaming
app.start_streaming()

# Get ultrasound frame
frame = app.get_latest_frame()
if frame is not None:
    print(f"Frame shape: {frame.shape}")
```

#### RealSense Camera

```python
from workflows.robotic_ultrasound.scripts.holoscan_apps.realsense.camera import (
    RealSenseCamera
)

# Initialize camera
camera = RealSenseCamera()

# Configure streams
camera.configure_color_stream(width=1920, height=1080, fps=30)
camera.configure_depth_stream(width=1280, height=720, fps=30)

# Start capture
camera.start_capture()

# Get frames
color_frame, depth_frame = camera.get_frames()
if color_frame is not None:
    print(f"Color frame shape: {color_frame.shape}")
```

## Data Schemas

### DDS Message Types

#### Franka Control Message

```python
from workflows.robotic_ultrasound.scripts.dds.schemas.franka_ctrl import FrankaCtrl

# Create control message
ctrl_msg = FrankaCtrl()
ctrl_msg.joint_positions = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
ctrl_msg.joint_velocities = [0.0] * 7
ctrl_msg.control_mode = "position"
ctrl_msg.timestamp = time.time_ns()
```

#### Camera Control Message

```python
from workflows.robotic_ultrasound.scripts.dds.schemas.camera_ctrl import CameraCtrl

# Create camera control message
cam_msg = CameraCtrl()
cam_msg.command = "capture"
cam_msg.exposure = 15.0
cam_msg.gain = 1.0
cam_msg.white_balance = 4000
```

#### Ultrasound Data Message

```python
from workflows.robotic_ultrasound.scripts.dds.schemas.usp_data import USPData

# Create ultrasound data message
us_msg = USPData()
us_msg.image_data = ultrasound_image.tobytes()
us_msg.width = 256
us_msg.height = 256
us_msg.depth = 0.08  # meters
us_msg.gain = 50
us_msg.timestamp = time.time_ns()
```

## Simulation Integration

### Isaac Sim Environment

```python
from workflows.robotic_ultrasound.scripts.simulation.environments.sim_with_dds import (
    UltrasoundSimulationEnvironment
)

# Initialize simulation environment
env = UltrasoundSimulationEnvironment(
    headless=False,
    dds_domain_id=0
)

# Load scene
env.load_scene("ultrasound_scanning_scene.usd")

# Add DDS communication
env.enable_dds_communication()

# Start simulation
env.start_simulation()
```

### Data Collection

```python
from workflows.robotic_ultrasound.scripts.simulation.environments.state_machine.data_collection.data_collector import (
    DataCollector
)

# Initialize data collector
collector = DataCollector(
    output_dir="/path/to/data",
    collection_rate=30.0  # Hz
)

# Configure data streams
collector.add_stream("ultrasound_images", dtype="uint8")
collector.add_stream("robot_states", dtype="float32")
collector.add_stream("camera_images", dtype="uint8")

# Start collection
collector.start_collection()

# Record data
collector.record("ultrasound_images", ultrasound_frame)
collector.record("robot_states", joint_positions)
```

## Configuration

### Environment Variables

- `I4H_ULTRASOUND_DOMAIN_ID`: DDS domain ID (default: 0)
- `I4H_ULTRASOUND_DATA_DIR`: Data storage directory
- `I4H_ULTRASOUND_LOG_LEVEL`: Logging level
- `I4H_ULTRASOUND_DEVICE`: CUDA device ID

### Configuration Files

#### Basic Configuration

```yaml
# ultrasound_config.yaml
dds:
  domain_id: 0
  qos_profile: "reliable"

robot:
  type: "franka_panda"
  control_frequency: 100.0
  safety_limits:
    max_velocity: 2.0
    max_acceleration: 5.0

ultrasound:
  probe_type: "linear"
  frequency: 5e6
  depth: 0.08
  gain: 50

camera:
  resolution: [1920, 1080]
  fps: 30
  exposure: 15.0
```

## Error Handling

```python
from workflows.robotic_ultrasound.exceptions import (
    DDSCommunicationError,
    RobotControlError,
    UltrasoundAcquisitionError,
    SimulationError
)

try:
    # Run ultrasound acquisition
    ultrasound_frame = acquire_ultrasound_frame()
except UltrasoundAcquisitionError as e:
    print(f"Ultrasound acquisition failed: {e}")
except DDSCommunicationError as e:
    print(f"DDS communication error: {e}")
```

## Performance Optimization

- Use DDS QoS profiles for reliable communication
- Configure appropriate buffer sizes for real-time performance
- Monitor system resources during data collection
- Use CUDA acceleration for image processing
- Optimize state machine transitions for smooth operation

## See Also

- [Robotic Ultrasound Workflow](../workflows/robotic-ultrasound.md)
- [DDS Communication](../workflows/robotic-ultrasound-dds-communication.md)
- [Hardware Integration Guide](./reference-hardware-integration.md)
