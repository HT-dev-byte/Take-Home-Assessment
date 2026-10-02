"""
Floor Plan Renderer generating clean, dimensioned 2D SVG vector maps.
Includes room outlines, wall lengths, door/window openings, and damage regions.
"""

import svgwrite
import math
from typing import Dict, Any, List

class FloorPlanRenderer:
    @staticmethod
    def render_svg(capture_output: Dict[str, Any], output_filepath: str):
        rooms = capture_output.get("rooms", {})
        placements = capture_output.get("multi_room_stitched_plan", {}).get("room_placements", {})
        damage_regions = capture_output.get("damage_regions", [])

        # Calculate bounding box
        all_pts = []
        for rid, pl in placements.items():
            for pt in pl.get("polygon", []):
                all_pts.append(pt)

        if not all_pts:
            all_pts = [[0, 0], [10, 0], [10, 10], [0, 10]]

        xs = [p[0] for p in all_pts]
        ys = [p[1] for p in all_pts]
        min_x, max_x = min(xs) - 1.0, max(xs) + 1.0
        min_y, max_y = min(ys) - 1.0, max(ys) + 1.0

        width_m = max_x - min_x
        height_m = max_y - min_y

        scale = 100.0 # 100 pixels per meter
        margin = 50.0
        svg_w = width_m * scale + 2 * margin
        svg_h = height_m * scale + 2 * margin

        dwg = svgwrite.Drawing(output_filepath, size=(f"{svg_w}px", f"{svg_h}px"), profile='full')

        # Background
        dwg.add(dwg.rect(insert=(0, 0), size=(svg_w, svg_h), fill='#F8FAFC'))

        # Title Block
        tier = capture_output.get("tier", "unknown").upper()
        cap_id = capture_output.get("capture_id", "")
        dwg.add(dwg.text(f"PROPERTY FLOOR PLAN ({tier} TIER)", insert=(margin, 35), font_size="20px", font_weight="bold", fill="#0F172A", font_family="Arial, sans-serif"))
        dwg.add(dwg.text(f"Capture ID: {cap_id} | Total Area: {capture_output.get('property_summary', {}).get('total_floor_area_sq_m', 0)} m²", insert=(margin, 55), font_size="13px", fill="#475569", font_family="Arial, sans-serif"))

        def to_svg_coords(pt):
            sx = margin + (pt[0] - min_x) * scale
            sy = margin + (max_y - pt[1]) * scale # Flip Y for SVG canvas
            return (sx, sy)

        # Draw Rooms
        for rid, rdata in rooms.items():
            pl = placements.get(rid, {})
            poly_pts = pl.get("polygon", [])
            if not poly_pts:
                continue

            svg_pts = [to_svg_coords(pt) for pt in poly_pts]

            # Fill room polygon
            dwg.add(dwg.polygon(points=svg_pts, fill='#E2E8F0', stroke='#1E293B', stroke_width=4, fill_opacity=0.6))

            # Room Title Label
            cx = sum(p[0] for p in svg_pts) / len(svg_pts)
            cy = sum(p[1] for p in svg_pts) / len(svg_pts)
            dwg.add(dwg.text(rdata.get("name", rid), insert=(cx, cy - 8), font_size="15px", font_weight="bold", text_anchor="middle", fill="#0F172A", font_family="Arial, sans-serif"))
            dwg.add(dwg.text(f"{rdata['dimensions']['floor_area_sq_m']} m² | CH: {rdata['dimensions']['ceiling_height_m']}m", insert=(cx, cy + 12), font_size="12px", text_anchor="middle", fill="#475569", font_family="Arial, sans-serif"))

            # Draw Wall Dimensions
            walls = rdata.get("walls", [])
            for w in walls:
                sp = to_svg_coords(w["start_point"])
                ep = to_svg_coords(w["end_point"])
                mx = (sp[0] + ep[0]) / 2.0
                my = (sp[1] + ep[1]) / 2.0
                dwg.add(dwg.text(f"{w['length_m']}m", insert=(mx, my), font_size="11px", fill="#1E3A8A", font_weight="bold", text_anchor="middle", font_family="Arial, sans-serif"))

            # Draw Openings
            for op in rdata.get("openings", []):
                dwg.add(dwg.circle(center=(cx, cy + 25), r=5, fill="#2563EB"))

        # Draw Damage Regions Overlays
        for dmg in damage_regions:
            loc_poly = dmg.get("location_polygon", [])
            if loc_poly:
                svg_dmg_pts = [to_svg_coords(pt) for pt in loc_poly]
                color = "#EF4444" if dmg.get("severity") == "severe" else "#F59E0B"
                dwg.add(dwg.polygon(points=svg_dmg_pts, fill=color, stroke='#B91C1C', stroke_width=2, fill_opacity=0.5))
                dcx = sum(p[0] for p in svg_dmg_pts) / len(svg_dmg_pts)
                dcy = sum(p[1] for p in svg_dmg_pts) / len(svg_dmg_pts)
                dwg.add(dwg.text(f"[{dmg['damage_class'].upper()}: {dmg['metric_extent_sq_m']}m²]", insert=(dcx, dcy), font_size="10px", fill="#7F1D1D", font_weight="bold", text_anchor="middle"))

        dwg.save()
        print(f"Rendered floor plan SVG to {output_filepath}")
