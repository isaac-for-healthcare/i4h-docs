# Available Assets

The Isaac for Healthcare Asset Catalog provides validated 3D models for medical simulation and training.

For detailed file listings of each catalog version, including all textures, materials, and configuration files, see the [Asset Catalog Documentation](https://github.com/isaac-for-healthcare/i4h-asset-catalog/tree/main/docs) on GitHub.

## Complete Asset List

### Policies

Pre-trained AI models ready for deployment in medical robotics applications.

| Asset | Path | Description |
|-------|------|-------------|
| GR00T-N1 | `Policies/LiverScan/GR00TN1/` | GR00T-N1 policy for liver scanning |
| GR00T-N1 Cosmos | `Policies/LiverScan/GR00TN1_Cosmos/` | GR00T-N1 policy trained with Cosmos textures |
| PI-Zero | `Policies/LiverScan/Pi0/` | PI-Zero policy for liver scanning |
| PI-Zero Cosmos | `Policies/LiverScan/Pi0_Cosmos/` | PI-Zero policy trained with Cosmos textures |

### Props

Medical and surgical equipment for simulation and training.

#### Medical Equipment

| Asset | Path | Description |
|-------|------|-------------|
| Clarius Probe | `Props/ClariusUltrasoundProbe/fixture.usda` | Clarius ultrasound probe model |
| Ultrasound Fixture | `Props/UltrasoundCameraFixture/fixture.usda` | Mounting fixture for ultrasound and camera |
| RealSense D405 | `Props/D405/D405_blend.usd` | Intel RealSense D405 depth camera |

#### Anatomical Models

| Asset | Path | Description |
|-------|------|-------------|
| ABD Phantom | `Props/ABDPhantom/phantom.usda` | Complete abdominal phantom with organs |
| Organs Bundle | `Props/Organs/organs.usd` | Standalone organ models with materials |

**Individual Organs Available in ABDPhantom:**

- Back muscles, Bones (ribs, spine, hips)
- Colon, Gallbladder, Heart
- Kidneys (left and right), Liver, Lungs
- Pancreas, Skin, Small bowel
- Spleen, Stomach
- Tumors (2 variants), Vessels

#### Surgical Training Props

| Asset | Path | Description |
|-------|------|-------------|
| Peg Board | `Props/Board/board.usd` | Peg transfer training board |
| Peg Block | `Props/PegBlock/block.usd` | Individual peg block for training |
| Suture Needle | `Props/SutureNeedle/needle.usd` | Surgical suture needle |
| Suture Pad | `Props/SuturePad/suture_pad.usd` | Suturing practice pad |

#### Tables and Fixtures

| Asset | Path | Description |
|-------|------|-------------|
| Operating Table | `Props/Table/table.usd` | Standard operating table |
| Vention Table | `Props/VentionTable/table.usda` | Vention modular table |
| Vention with Cover | `Props/VentionTableWithBlackCover/table_with_cover.usd` | Vention table with black cover |

### Robots

Pre-configured medical robot models with accurate kinematics and dynamics.

#### da Vinci Surgical System

| Asset | Path | Description |
|-------|------|-------------|
| ECM | `Robots/dVRK/ECM/ecm.usd` | Endoscopic Camera Manipulator |
| PSM | `Robots/dVRK/PSM/psm.usd` | Patient Side Manipulator |

#### Franka Robotics

| Asset | Path | Description |
|-------|------|-------------|
| Panda Assembly | `Robots/Franka/Collected_panda_assembly/panda_assembly.usda` | Franka Emika Panda robot |
| FR3 Assembly | `Robots/Franka/Collected_fr3_assembly/fr3_assembly.usda` | Franka FR3 robot |

#### Other Surgical Robots

| Asset | Path | Description |
|-------|------|-------------|
| MIRA | `Robots/MIRA/mira-bipo-size-experiment-smoothing.usd` | Virtual Incision MIRA robot |
| MIRA Suture Needle | `Robots/MIRA/suture-needle.usd` | Suture needle for MIRA robot |
| STAR | `Robots/STAR/star.usd` | Smart Tissue Autonomous Robot |

### Test Assets

| Asset | Path | Description |
|-------|------|-------------|
| Basic Test | `Test/basic.usda` | Simple test asset for development |

