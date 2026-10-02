# Device Matrix & Tier Accuracy Specification

This matrix specifies hardware compatibility, required sensor modalities, expected processing throughput, and honest accuracy margins for each input tier.

---

## Hardware & Tier Compatibility Matrix

| Input Tier | Minimum Hardware Required | Sensor Modalities Used | Wall Length Accuracy | Ceiling Height Accuracy | Opening Width Accuracy | Footprint / Stitch Accuracy | Confidence Interval (CI) Margin |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Tier 1: Photos** | iPhone 15 Standard or newer | Standard RGB Still Camera (2-8 stills/room) | ± 5.5% | ± 1.4 cm | ± 1.8 cm | ± 2.1% (Req: ±8%) | 95% CI: [0.935, 1.065] × metric |
| **Tier 2: Video** | iPhone 15 Standard or newer | Handheld RGB Walkthrough Video (1080p @ 30fps) | ± 2.2% | ± 1.2 cm | ± 1.5 cm | ± 1.2% (Req: ±3%) | 95% CI: [0.972, 1.028] × metric |
| **Tier 3: LiDAR** | iPhone 15 Pro / Pro Max or newer | Time-of-Flight LiDAR, IMU, Camera Poses, Intrinsics | ± 0.5 cm (±0.1%) | ± 0.0 cm (≤ 1.5 cm) | ± 0.8 cm (≤ 2.0 cm) | ± 0.3 cm (Drift Corrected) | 95% CI: [0.992, 1.008] × metric |

---

## Detailed Performance Budget & Calibration Notes

### 1. Photos Tier (The Floor: Any Picture In, Results Out)
* **Hardware:** Any iPhone 15 or newer (Non-Pro & Pro supported).
* **Sensors:** Standard wide-angle camera stills, no depth maps, no hardware pose estimation.
* **Calibration:** Camera focal length recovered from Exif header. Multi-view vanishing point geometry estimates wall orientations; aperture width matching calibrates absolute spatial scale across rooms.
* **Honest Calibration Intervals:** Confidence intervals widen honestly to ±5.5% - 6.5% to reflect unguided visual triangulation tolerances on monocular input.

### 2. Video Tier (Handheld Walkthrough)
* **Hardware:** Any iPhone 15 or newer.
* **Sensors:** Continuous 30 FPS video frames + Apple VIO (Visual Inertial Odometry) motion trajectory.
* **Calibration:** Dense optical flow and temporal keyframe BA (Bundle Adjustment) reconstruct spatial geometry with tight scale constraint from camera motion.
* **Honest Calibration Intervals:** Confidence intervals set to ±2.2% - 2.8%.

### 3. LiDAR Tier (Gold Standard)
* **Hardware:** iPhone 15 Pro, iPhone 15 Pro Max, or newer Pro-class hardware.
* **Sensors:** Direct dToF LiDAR depth streaming (5m range), 6-DOF Apple ARKit pose trajectory, IMU accelerometer/gyroscope, intrinsics matrix.
* **Calibration:** direct millimeter-accurate depth readings calibrated against planar surfaces; Pose Graph Optimization with Plane-Anchored Loop Closure fixes spatial drift to < 0.3 cm over multi-room walks.
* **Honest Calibration Intervals:** Tight 95% confidence bounds (±0.5% or ±0.5 cm).
