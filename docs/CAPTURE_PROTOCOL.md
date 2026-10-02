# Stock Capture Protocol (Route 2)

**Target Audience:** Non-engineer field operator / homeowner
**Time Required:** 3 to 5 minutes per property
**Supported Devices:** iPhone 15 or newer (Photos/Video), iPhone 15 Pro or newer (LiDAR)

---

## 1. What to Install
1. Open the **App Store** on your iPhone.
2. For **LiDAR Tier** & **Stock Data Export**: Install **Polycam - 3D Scanner & LiDAR** (Free tier is sufficient) OR the native **Files & Camera App**.
3. For **Video Tier**: Standard iOS **Camera** app (1080p or 4K at 30 fps).
4. For **Photo Tier**: Standard iOS **Camera** app.

---

## 2. Capture Protocol & Walking Procedure

### Tier 1: Photos (Floor: 2 to 8 Stills per Room)
* **Goal:** Capture every wall, corner, and door/window transition.
* **How to Walk & Capture:**
  1. Create a folder on your phone named by room (e.g., `Living_Room`, `Hallway`, `Bedroom`).
  2. Stand near the center or entry of the room.
  3. Take **1 photo per wall corner** ensuring ceiling-wall and floor-wall edges are visible.
  4. Take **1 photo straight-on at each door or window** showing the frame boundaries.
  5. Crucial for Multi-Room Stitching: Take **1 photo through the open doorway** looking into the adjacent hallway/room so the connector aperture is visible.
* **What to Avoid:** Blurry photos, fast movement, covering the lens, pitch-black lighting, or closing connecting doors.

---

### Tier 2: Video (Handheld Walkthrough Clip)
* **Goal:** A continuous, smooth walkthrough recording connecting all rooms.
* **How to Walk:**
  1. Open the native **Camera** app -> **Video** mode.
  2. Start at the main entry doorway. Hold the phone at chest height, tilted slightly upward (~15°) to capture both ceiling corners and wall baseboards.
  3. Walk slowly (normal walking speed, ~0.5 m/s) around the perimeter of Room 1 in a smooth loop.
  4. Walk through the connecting doorway into the connector hallway, panning smoothly.
  5. Continue through into adjacent rooms.
  6. Return to the starting point or end at the final room doorway.
* **Clip Duration:** 45 seconds to 2.5 minutes depending on property size.

---

### Tier 3: LiDAR (Pro Devices)
* **Goal:** High-precision point cloud, camera pose trajectory, and depth map recording.
* **How to Walk:**
  1. Open **Polycam** (or iOS LiDAR Logging App) -> Select **FloorPlan / LiDAR** mode.
  2. Tap **Record**. Walk smoothly around each room, aiming the camera at wall-floor intersections and ceiling corners.
  3. Pass slowly through connecting doorways to allow IMU and visual feature tracking to anchor the pose graph across rooms.
  4. Tap **Done** once all rooms are covered. Export as **JSON / Raw Mesh / Polycam Session**.

---

## 3. How to Hand Files to Pipeline

1. AirDrop or transfer the recorded capture directory to the processing machine (`/data/raw/`):
   - **Photo Tier:** Directory containing per-room subfolders with `.jpg` / `.png` images.
   - **Video Tier:** Continuous `.mov` or `.mp4` video file.
   - **LiDAR Tier:** `.json` / session folder containing sensor depth logs, pose trajectory, and intrinsics.
2. Execute the single pipeline command:
   ```bash
   ./bin/process_capture --input data/raw/your_capture.json --tier [photos|video|lidar] --output output.json --render plan.svg
   ```
