import unittest
import os
from scan_pipeline.damage import DamageEngine
from scan_pipeline.renderer import FloorPlanRenderer

class TestDamageAndRenderer(unittest.TestCase):
    def test_damage_engine(self):
        raw_damage = [
            {
                "damage_id": "dmg_1",
                "room_id": "living_room",
                "surface_id": "living_room_w1",
                "surface_type": "wall",
                "damage_class": "water_stain",
                "metric_extent_sq_m": 1.5,
                "severity": "moderate"
            }
        ]

        dmg_out, flags, scope = DamageEngine.process_damage_and_scope(raw_damage)
        self.assertEqual(len(dmg_out), 1)
        self.assertEqual(len(flags), 1)
        self.assertEqual(len(scope), 1)
        self.assertEqual(scope[0]["item_code"], "DRY-WTR-REPAIR")
        self.assertEqual(flags[0]["rule_id"], "RULE_WATER_STAIN_PLUMBING")

    def test_renderer(self):
        sample_output = {
            "capture_id": "test_render",
            "tier": "lidar",
            "property_summary": {"total_floor_area_sq_m": 20.0},
            "rooms": {
                "r1": {
                    "name": "Room 1",
                    "dimensions": {"floor_area_sq_m": 20.0, "ceiling_height_m": 2.70},
                    "walls": [{"length_m": 5.0, "start_point": [0,0], "end_point": [5,0]}],
                    "openings": []
                }
            },
            "multi_room_stitched_plan": {
                "room_placements": {
                    "r1": {"polygon": [[0,0], [5,0], [5,4], [0,4]]}
                }
            },
            "damage_regions": [
                {
                    "damage_class": "water_stain",
                    "metric_extent_sq_m": 1.2,
                    "severity": "moderate",
                    "location_polygon": [[1,1], [2,1], [2,2], [1,2]]
                }
            ]
        }

        output_path = "/tmp/test_plan.svg"
        FloorPlanRenderer.render_svg(sample_output, output_path)
        self.assertTrue(os.path.exists(output_path))

if __name__ == "__main__":
    unittest.main()
