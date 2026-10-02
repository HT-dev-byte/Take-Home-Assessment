import unittest
import json
import os
from scan_pipeline.models import CaptureOutputModel, CaptureTier

class TestModelsAndSchema(unittest.TestCase):
    def test_sample_capture_output(self):
        sample = {
            "capture_id": "cap_001",
            "tier": "lidar",
            "device_model": "iPhone 15 Pro",
            "timestamp": "2026-08-15T10:00:00Z",
            "processing_time_sec": 3.5,
            "drift_corrected": True,
            "property_summary": {
                "total_floor_area_sq_m": 45.0,
                "total_rooms": 3,
                "confidence_interval": {
                    "lower": 44.5,
                    "upper": 45.5,
                    "margin_pct": 1.1
                }
            },
            "rooms": {
                "living_room": {
                    "room_id": "living_room",
                    "name": "Living Room",
                    "dimensions": {
                        "ceiling_height_m": 2.70,
                        "ceiling_height_ci": {"lower": 2.69, "upper": 2.71},
                        "floor_area_sq_m": 20.0,
                        "floor_area_ci": {"lower": 19.8, "upper": 20.2},
                        "perimeter_m": 18.0
                    },
                    "walls": [
                        {"wall_id": "w1", "length_m": 5.0, "start_point": [0.0, 0.0], "end_point": [5.0, 0.0], "orientation_deg": 0.0},
                        {"wall_id": "w2", "length_m": 4.0, "start_point": [5.0, 0.0], "end_point": [5.0, 4.0], "orientation_deg": 90.0},
                        {"wall_id": "w3", "length_m": 5.0, "start_point": [5.0, 4.0], "end_point": [0.0, 4.0], "orientation_deg": 180.0},
                        {"wall_id": "w4", "length_m": 4.0, "start_point": [0.0, 4.0], "end_point": [0.0, 0.0], "orientation_deg": 270.0}
                    ],
                    "openings": [
                        {"opening_id": "op_1", "wall_id": "w1", "type": "door", "width_m": 0.90, "height_m": 2.10, "offset_from_wall_start_m": 2.0}
                    ]
                }
            },
            "multi_room_stitched_plan": {
                "adjacency_graph": [
                    {"room_a": "living_room", "room_b": "hallway", "connector_type": "door", "shared_opening_id": "op_1"}
                ],
                "room_placements": {
                    "living_room": {
                        "translation": [0.0, 0.0],
                        "rotation_deg": 0.0,
                        "polygon": [[0.0, 0.0], [5.0, 0.0], [5.0, 4.0], [0.0, 4.0]]
                    }
                },
                "drift_metric_m": 0.005
            },
            "damage_regions": [
                {
                    "damage_id": "dmg_1",
                    "room_id": "living_room",
                    "surface_id": "w1",
                    "surface_type": "wall",
                    "damage_class": "water_stain",
                    "metric_extent_sq_m": 1.2,
                    "severity": "moderate",
                    "location_polygon": [[1.0, 0.5], [2.0, 0.5], [2.0, 1.7], [1.0, 1.7]]
                }
            ],
            "concealed_damage_flags": [
                {
                    "flag_id": "flag_1",
                    "rule_id": "RULE_PLUMBING_MOISTURE",
                    "rule_name": "Adjacent Wet-Wall Moisture Risk",
                    "surface_id": "w1",
                    "room_id": "living_room",
                    "risk_level": "high",
                    "description": "Water stain on wall adjacent to wet plumbing stack indicates potential sub-surface mold.",
                    "action_required": "Infrared thermal scan & targeted drywall probe."
                }
            ],
            "scope_line_items": [
                {
                    "line_item_id": "item_1",
                    "item_code": "DRY-REPAIR-MOD",
                    "category": "Drywall",
                    "description": "Cut, patch, and paint damaged wall section",
                    "surface_id": "w1",
                    "quantity": 1.2,
                    "unit": "sq_m",
                    "unit_cost_usd": 85.0,
                    "estimated_cost_usd": 102.0
                }
            ]
        }

        # Test Pydantic model validation
        model = CaptureOutputModel(**sample)
        self.assertEqual(model.tier, CaptureTier.LIDAR)
        self.assertEqual(model.rooms["living_room"].dimensions.ceiling_height_m, 2.70)

        # Test JSON Schema validation
        schema_path = os.path.join(os.path.dirname(__file__), "../schema/capture_output_schema.json")
        with open(schema_path, "r") as f:
            schema = json.load(f)

        import jsonschema
        jsonschema.validate(instance=sample, schema=schema)

if __name__ == "__main__":
    unittest.main()
