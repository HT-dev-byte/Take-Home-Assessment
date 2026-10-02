"""
Unified CLI Entrypoint for PropertyScan AI Pipeline.
Accepts raw capture file, tier flag, drift correction flag, output JSON destination, and SVG render path.
"""

import sys
import os
import json
import argparse
from scan_pipeline.lidar import LidarProcessor
from scan_pipeline.video import VideoProcessor
from scan_pipeline.photo import PhotoProcessor
from scan_pipeline.damage import DamageEngine
from scan_pipeline.renderer import FloorPlanRenderer


def main():
    parser = argparse.ArgumentParser(description="PropertyScan AI Capture Processing Engine")
    parser.add_argument("--input", required=True, help="Path to input raw capture JSON file")
    parser.add_argument("--tier", required=True, choices=["lidar", "video", "photos"], help="Input capture tier")
    parser.add_argument("--output", required=True, help="Destination path for output JSON schema")
    parser.add_argument("--render", required=False, help="Destination path for rendered SVG floor plan")
    parser.add_argument("--disable-drift-fix", action="store_true", help="Disable pose graph optimization & loop closure (for fix loop before/after evaluation)")

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)

    with open(args.input, "r") as f:
        raw_data = json.load(f)

    drift_fix_enabled = not args.disable_drift_fix

    # Dispatch processor based on tier
    if args.tier == "lidar":
        processor = LidarProcessor(enable_drift_correction=drift_fix_enabled)
    elif args.tier == "video":
        processor = VideoProcessor()
    elif args.tier == "photos":
        processor = PhotoProcessor()
    else:
        print(f"Unsupported tier: {args.tier}")
        sys.exit(1)

    # Core processing
    capture_output = processor.process_capture(raw_data)

    # Process damage regions, concealed damage rules, and scope line items
    raw_damage = raw_data.get("damage_regions", [])
    dmg_out, concealed_flags, scope_items = DamageEngine.process_damage_and_scope(raw_damage)

    capture_output["damage_regions"] = dmg_out
    capture_output["concealed_damage_flags"] = concealed_flags
    capture_output["scope_line_items"] = scope_items

    # Ensure output directory exists
    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)

    # Write Output JSON
    with open(args.output, "w") as f:
        json.dump(capture_output, f, indent=2)
    print(f"Successfully processed capture [{args.tier.upper()}]. Output saved to {args.output}")

    # Render SVG Floor Plan if requested
    if args.render:
        os.makedirs(os.path.dirname(os.path.abspath(args.render)), exist_ok=True)
        FloorPlanRenderer.render_svg(capture_output, args.render)


if __name__ == "__main__":
    main()
