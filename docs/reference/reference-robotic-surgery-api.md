# Robotic Surgery API Reference

This page provides comprehensive API reference for the robotic surgery workflow components.

## Core Components

### Surgical Robot Assets

#### da Vinci Research Kit (dVRK)

```python
from workflows.robotic_surgery.scripts.simulation.exts.robotic_surgery_assets.robotic.surgery.assets.psm import (
    PatientSideManipulator
)

# Initialize PSM
psm = PatientSideManipulator(
    prim_path="/World/PSM1",
    name="psm1"
)

# Configure PSM
psm.set_joint_positions([0.1, 0.2, 0.15, 0.0, 0.0, 0.0])
psm.set_end_effector("large_needle_driver")

# Get current state
joint_positions = psm.get_joint_positions()
ee_pose = psm.get_end_effector_pose()
```

#### Endoscopic Camera Manipulator (ECM)

```python
from workflows.robotic_surgery.scripts.simulation.exts.robotic_surgery_assets.robotic.surgery.assets.ecm import (
    EndoscopicCameraManipulator
)

# Initialize ECM
ecm = EndoscopicCameraManipulator(
    prim_path="/World/ECM",
    name="ecm"
)

# Configure camera
ecm.set_camera_parameters(
    focal_length=8.0,  # mm
    aperture_size=2.8,
    resolution=(1920, 1080)
)

# Control camera position
ecm.move_to_pose([0.3, 0.2, 0.5], [0, 0, 0, 1])
```

### Surgical Tasks

#### Reach Task

```python
from workflows.robotic_surgery.scripts.simulation.exts.robotic_surgery_tasks.robotic.surgery.tasks.surgical.reach.reach_env_cfg import (
    ReachEnvCfg
)

# Configure reach environment
reach_cfg = ReachEnvCfg()
reach_cfg.scene.num_envs = 4096
reach_cfg.scene.env_spacing = 2.0

# Set target configuration
reach_cfg.target_cfg.spawn_range = {
    "x": [-0.2, 0.2],
    "y": [-0.2, 0.2],
    "z": [0.1, 0.3]
}

# Initialize environment
from omni.isaac.lab.envs import DirectRLEnv
env = DirectRLEnv(cfg=reach_cfg)
```

#### Lift Task

```python
from workflows.robotic_surgery.scripts.simulation.exts.robotic_surgery_tasks.robotic.surgery.tasks.surgical.lift.lift_env_cfg import (
    LiftEnvCfg
)

# Configure lift environment
lift_cfg = LiftEnvCfg()
lift_cfg.object_cfg.spawn_range = {
    "x": [-0.1, 0.1],
    "y": [-0.1, 0.1],
    "z": [0.02, 0.02]
}

# Set object properties
lift_cfg.object_cfg.rigid_props.mass = 0.01  # kg
lift_cfg.object_cfg.rigid_props.friction = 0.7
```

#### Handover Task

```python
from workflows.robotic_surgery.scripts.simulation.exts.robotic_surgery_tasks.robotic.surgery.tasks.surgical.handover.handover_env_cfg import (
    HandoverEnvCfg
)

# Configure handover environment
handover_cfg = HandoverEnvCfg()
handover_cfg.num_robots = 2
handover_cfg.handover_distance = 0.05  # meters

# Set coordination parameters
handover_cfg.coordination.timing_tolerance = 0.1  # seconds
handover_cfg.coordination.force_threshold = 2.0  # Newtons
```

### Reinforcement Learning Integration

#### Training Configuration

```python
from workflows.robotic_surgery.scripts.reinforcement_learning.rsl_rl.train import (
    train_policy
)

# Configure training
training_config = {
    "algorithm": "PPO",
    "num_envs": 4096,
    "num_steps": 24,
    "learning_rate": 3e-4,
    "num_epochs": 5,
    "clip_range": 0.2,
    "value_loss_coef": 0.5,
    "entropy_coef": 0.01
}

# Start training
train_policy(
    task="SurgicalReach-v0",
    num_envs=4096,
    config=training_config
)
```

#### Policy Evaluation

```python
from workflows.robotic_surgery.scripts.reinforcement_learning.rsl_rl.play import (
    evaluate_policy
)

# Load trained policy
policy_path = "logs/rsl_rl/reach_policy/model.pt"

# Evaluate policy
results = evaluate_policy(
    task="SurgicalReach-v0",
    checkpoint=policy_path,
    num_envs=16,
    num_episodes=100
)

print(f"Success rate: {results.success_rate:.2%}")
print(f"Average reward: {results.mean_reward:.3f}")
```

## MDP Components

### Observations

```python
from workflows.robotic_surgery.scripts.simulation.exts.robotic_surgery_tasks.robotic.surgery.tasks.surgical.lift.mdp.observations import (
    robot_joint_pos_rel,
    object_position_in_robot_root_frame
)

# Get robot observations
joint_positions = robot_joint_pos_rel(env, "robot")

# Get object observations
object_pos = object_position_in_robot_root_frame(env, "robot", "object")
```

### Rewards

```python
from workflows.robotic_surgery.scripts.simulation.exts.robotic_surgery_tasks.robotic.surgery.tasks.surgical.lift.mdp.rewards import (
    object_ee_distance,
    object_is_lifted
)

# Distance-based reward
dist_reward = object_ee_distance(env, std=0.1)

# Binary lift reward
lift_reward = object_is_lifted(env, minimal_height=0.05)

# Combined reward
total_reward = dist_reward + 10.0 * lift_reward
```

### Terminations

```python
from workflows.robotic_surgery.scripts.simulation.exts.robotic_surgery_tasks.robotic.surgery.tasks.surgical.lift.mdp.terminations import (
    object_dropped,
    time_out
)

# Check termination conditions
is_dropped = object_dropped(env)
is_timeout = time_out(env)

# Combined termination
is_terminated = is_dropped | is_timeout
```

## State Machine Integration

### Surgical State Machine

```python
from workflows.robotic_surgery.scripts.environments.state_machine.lift_block_sm import (
    LiftBlockStateMachine
)

# Initialize state machine
sm = LiftBlockStateMachine(
    robot_prim_path="/World/PSM1",
    block_prim_path="/World/Block"
)

# Configure states
sm.add_state("approach", approach_block)
sm.add_state("grasp", grasp_block)
sm.add_state("lift", lift_block)
sm.add_state("release", release_block)

# Set transitions
sm.add_transition("approach", "grasp", condition=near_block)
sm.add_transition("grasp", "lift", condition=grasped_successfully)
sm.add_transition("lift", "release", condition=lifted_sufficiently)
```

## Asset Configuration

### Robot Configuration

```python
from workflows.robotic_surgery.scripts.simulation.utils.assets import (
    configure_surgical_robot
)

# Configure PSM
psm_config = {
    "joint_limits": {
        "lower": [-1.57, -0.5, 0.0, -2.27, -1.57, -1.57],
        "upper": [1.57, 0.5, 0.24, 2.27, 1.57, 1.57]
    },
    "joint_stiffness": [400] * 6,
    "joint_damping": [40] * 6,
    "end_effector": "large_needle_driver"
}

psm = configure_surgical_robot("PSM", psm_config)
```

### Surgical Tools

```python
from workflows.robotic_surgery.scripts.simulation.exts.robotic_surgery_assets.robotic.surgery.assets.star import (
    SurgicalTool
)

# Configure needle driver
needle_driver = SurgicalTool(
    name="large_needle_driver",
    tool_type="grasper",
    jaw_angle_range=[0, 0.8],  # radians
    force_limit=10.0  # Newtons
)

# Attach to robot
psm.attach_tool(needle_driver)
```

## Simulation Parameters

### Physics Configuration

```python
# Configure physics parameters
physics_config = {
    "gravity": [0.0, 0.0, -9.81],
    "dt": 1.0/60.0,  # 60 FPS
    "substeps": 4,
    "solver_iterations": 10,
    "contact_offset": 0.001,
    "friction_offset_threshold": 0.001,
    "friction_correlation_distance": 0.025
}
```

### Rendering Configuration

```python
# Configure rendering
render_config = {
    "resolution": (1920, 1080),
    "anti_aliasing": True,
    "ambient_occlusion": True,
    "shadows": True,
    "reflections": True
}
```

## Error Handling

```python
from workflows.robotic_surgery.exceptions import (
    RobotControlError,
    TaskExecutionError,
    SimulationError,
    SafetyLimitError
)

try:
    # Execute surgical task
    sm.execute_task("needle_passing")
except SafetyLimitError as e:
    print(f"Safety limit exceeded: {e}")
    sm.emergency_stop()
except TaskExecutionError as e:
    print(f"Task execution failed: {e}")
    sm.reset_task()
```

## Performance Optimization

### Parallel Environment Configuration

```python
# Optimize for parallel training
parallel_config = {
    "num_envs": 4096,
    "env_spacing": 2.0,
    "use_gpu_pipeline": True,
    "physics_gpu": True,
    "sim_device": "cuda:0",
    "rl_device": "cuda:0"
}
```

### Memory Management

```python
# Configure memory usage
memory_config = {
    "max_gpu_memory": 0.8,  # Use 80% of GPU memory
    "enable_memory_pooling": True,
    "garbage_collection_interval": 100  # steps
}
```

## Testing and Validation

### Unit Tests

```python
import unittest
from workflows.robotic_surgery.tests.test_environments.test_surgery_sm import (
    TestSurgicalStateMachine
)

# Run specific test
test_suite = unittest.TestLoader().loadTestsFromTestCase(TestSurgicalStateMachine)
unittest.TextTestRunner(verbosity=2).run(test_suite)
```

### Integration Tests

```python
from workflows.robotic_surgery.tests.test_reinforcement_learning.test_rsl_rl_train import (
    test_training_pipeline
)

# Test complete training pipeline
result = test_training_pipeline(
    task="SurgicalReach-v0",
    num_envs=16,
    max_iterations=10
)

assert result.success, f"Training test failed: {result.error}"
```

## See Also

- [Robotic Surgery Overview](./robotic-surgery.md)
- [Configuration Guide](./configuration.md)
- [Hardware Integration](./hardware-integration.md)
