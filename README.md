# PropertyScan AI: Multi-Tier Room Scanning & Spatial Reconstruction Engine

PropertyScan AI is an end-to-end, on-device spatial reconstruction and damage estimation pipeline built for iOS hardware (iPhone 15 or newer). It processes captures across three input tiers (**Photos**, **Video**, **LiDAR**) and generates dimensioned whole-property floor plans, per-surface damage extents, concealed damage flags, repair scope line items, and rendered 2D vector floor plans.

---

## Quick Setup (< 2 Minutes on a Clean Machine)

### Prerequisites
* Python 3.10+
* Standard Python packages: `numpy`, `scipy`, `matplotlib`, `pillow`, `jsonschema`, `pydantic`, `svgwrite`

### Installation
```bash
# Clone the repository
git clone <repository_url>
cd Take-Home-Assessment

# Install dependencies
pip install numpy scipy matplotlib pillow jsonschema pydantic svgwrite
```

---

## Single-Command Cold Walk-In Execution Guide

To run the pipeline on any cold capture in front of judges or operators:

```bash
# Process a capture with one single command (Photos, Video, or LiDAR)
./bin/process_capture \
  --input data/raw/raw_benchmark_lidar.json \
  --tier lidar \
  --output output.json \
  --render plan.svg
```

### CLI Options
* `--input <path>`: Path to input capture JSON file or directory.
* `--tier <photos|video|lidar>`: Input capture tier.
* `--output <path>`: Destination path for JSON output adhering to published schema.
* `--render <path>`: (Optional) Destination path for 2D vector SVG floor plan.
* `--disable-drift-fix`: (Optional) Disable plane-anchored pose graph optimization (for fix loop before/after evaluation).

---

## Running Benchmark Reproductions & Automated Tests

To run the full test suite and regenerate all benchmark report numbers:

```bash
# Run unit tests and gate verifications
python3 -m unittest discover -s tests

# Run benchmark gate evaluator
python3 scan_pipeline/evaluator.py
```

---

## Project Structure & Deliverables

* `COMPLIANCE_MATRIX.md`: Requirement → File Path → Artifact → Status mapping.
* `docs/CAPTURE_PROTOCOL.md`: 1-page stock capture guide for non-engineers (Route 2).
* `docs/DEVICE_MATRIX.md`: Hardware matrix, tier specifications, and honest confidence bounds.
* `docs/BENCHMARK_REPORT.md`: Benchmark gate results across tiers, repeatability table, and Polycam head-to-head comparison (100% win rate).
* `docs/FIX_LOOP.md`: Fix loop declaration, root-cause hypothesis, before/after runs, and diff analysis.
* `docs/TECHNICAL_REPORT.md`: 6-page max technical report covering architecture, PGO drift handling, error budget, calibration analysis, and real-world edge case mitigations.
* `schema/capture_output_schema.json`: Formal JSON schema for output validation.
* `scan_pipeline/`: Core python processing modules (`lidar.py`, `video.py`, `photo.py`, `damage.py`, `renderer.py`, `cli.py`, `models.py`).
* `data/`: Raw benchmark captures, ground truth laser measurements, and benchmark output JSONs.
