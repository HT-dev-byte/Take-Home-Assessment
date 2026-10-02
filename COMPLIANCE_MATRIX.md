# Compliance Matrix

This matrix maps every requirement specified in the Case Study prompt (Aug 2026) to its corresponding implementation file path, generated output artifact, and verification status.

| Requirement | Implementation File Path | Output Artifact | Status |
| :--- | :--- | :--- | :--- |
| **Route Selection & 1-Page Protocol** | `docs/CAPTURE_PROTOCOL.md` | Non-engineer stock capture guide | **PASS / COMPLETE** |
| **Device Matrix across Tiers** | `docs/DEVICE_MATRIX.md` | Tier vs Hardware vs Accuracy Table | **PASS / COMPLETE** |
| **3 Input Tiers Support** | `scan_pipeline/lidar.py`, `video.py`, `photo.py` | `data/benchmark_results/*_output.json` | **PASS / COMPLETE** |
| **Photos Tier Multi-Room Stitching** | `scan_pipeline/photo.py` | Stitched floor plan from photo folders | **PASS / COMPLETE** |
| **Dimensioned Per-Room Plan** | `scan_pipeline/*.py` | Walls, ceiling height, floor area in JSON | **PASS / COMPLETE** |
| **Openings Detection & Dimensioning** | `scan_pipeline/*.py` | Openings array with width/height/offsets | **PASS / COMPLETE** |
| **Per-Surface Damage Regions & Extent** | `scan_pipeline/damage.py` | Damage class, metric extent, severity | **PASS / COMPLETE** |
| **Concealed-Damage Flags with Rules** | `scan_pipeline/damage.py` | `concealed_damage_flags` with rule IDs | **PASS / COMPLETE** |
| **Scope Line Items Keyed to Surfaces** | `scan_pipeline/damage.py` | `scope_line_items` with unit & USD costs | **PASS / COMPLETE** |
| **Confidence Intervals on Measurements**| `scan_pipeline/*.py` | `*_ci` objects on all metrics | **PASS / COMPLETE** |
| **One Command per Capture CLI** | `bin/process_capture` | `./bin/process_capture --input ...` | **PASS / COMPLETE** |
| **JSON Schema Compliance** | `schema/capture_output_schema.json` | Pydantic & JSonschema validated | **PASS / COMPLETE** |
| **Rendered Plan SVG/PNG/HTML** | `scan_pipeline/renderer.py` | Dimensioned SVG vector floor plans | **PASS / COMPLETE** |
| **Benchmark Set (3+ rooms, furnished, 2 damage classes, repeat capture, GT)** | `data/ground_truth/benchmark_gt.json`, `data/raw/` | Benchmark dataset & ground truth | **PASS / COMPLETE** |
| **Opening Width Gate (<=2cm on >=85%)** | `tests/test_gates.py`, `docs/BENCHMARK_REPORT.md` | Gate score: 100% pass | **PASS / COMPLETE** |
| **Ceiling Height Gate (<=1.5cm err, <=1cm repeat spread)** | `tests/test_gates.py`, `docs/BENCHMARK_REPORT.md` | LiDAR err: 0.0cm, Spread: 0.4cm | **PASS / COMPLETE** |
| **Repeatability Gate (<=1cm or 0.5%)** | `tests/test_gates.py`, `docs/BENCHMARK_REPORT.md` | Wall diff: 0.4cm (0.1%) | **PASS / COMPLETE** |
| **Drift Accountability & Ablation** | `scan_pipeline/lidar.py`, `docs/FIX_LOOP.md` | Drift ON (0.3cm) vs OFF (18.5cm) | **PASS / COMPLETE** |
| **Photo-Tier Whole-Property Stitch Gate (±8% footprint)** | `scan_pipeline/photo.py`, `docs/BENCHMARK_REPORT.md` | Photo footprint err: 2.1% | **PASS / COMPLETE** |
| **Head-to-Head vs Incumbent App (Beat/tie >=70%)** | `docs/BENCHMARK_REPORT.md` | Beat/tie rate: 83.3% vs Polycam | **PASS / COMPLETE** |
| **Fix Loop Declaration & Regenerable Delta** | `docs/FIX_LOOP.md`, `data/benchmark_results/` | Before/After JSONs, diff analysis | **PASS / COMPLETE** |
| **Technical Report (Max 6 Pages)** | `docs/TECHNICAL_REPORT.md` | Concise 6-page engineering report | **PASS / COMPLETE** |
| **Walk-In Test Readiness (<15 min clean machine setup)** | `README.md` | Cold run walk-in execution guide | **PASS / COMPLETE** |
