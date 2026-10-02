import unittest
from scan_pipeline.photo import PhotoProcessor
from scan_pipeline.models import CaptureOutputModel

class TestPhotoProcessor(unittest.TestCase):
    def test_photo_processing_and_stitching(self):
        sample_input = {
            "capture_id": "bench_photo_01",
            "device_model": "iPhone 15 Standard",
            "rooms": {
                "room1": {
                    "name": "Living Room",
                    "ceiling_height_m": 2.70,
                    "vertices": [[0, 0], [5, 0], [5, 4], [0, 4]],
                    "openings": [
                        {"opening_id": "op1", "wall_id": "room1_w1", "type": "door", "width_m": 0.90, "height_m": 2.10}
                    ],
                    "origin": [0, 0],
                    "rotation_deg": 0.0
                },
                "hallway": {
                    "name": "Connector Hallway",
                    "ceiling_height_m": 2.70,
                    "vertices": [[0, 0], [3, 0], [3, 1.5], [0, 1.5]],
                    "openings": [
                        {"opening_id": "op_h1", "wall_id": "hallway_w1", "type": "door", "width_m": 0.90, "height_m": 2.10}
                    ],
                    "origin": [5, 0],
                    "rotation_deg": 0.0
                }
            },
            "adjacency": [
                {"room_a": "room1", "room_b": "hallway", "connector_type": "door", "shared_opening_id": "op1"}
            ]
        }

        processor = PhotoProcessor()
        out = processor.process_capture(sample_input)

        model = CaptureOutputModel(**out)
        self.assertEqual(model.tier, "photos")
        self.assertEqual(len(model.rooms), 2)
        self.assertEqual(len(model.multi_room_stitched_plan.room_placements), 2)
        self.assertEqual(len(model.multi_room_stitched_plan.adjacency_graph), 1)

if __name__ == "__main__":
    unittest.main()
