import unittest
from scan_pipeline.lidar import LidarProcessor
from scan_pipeline.models import CaptureOutputModel

class TestLidarProcessor(unittest.TestCase):
    def test_lidar_processing(self):
        sample_input = {
            "capture_id": "bench_lidar_01",
            "device_model": "iPhone 15 Pro",
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
                }
            },
            "adjacency": []
        }

        processor = LidarProcessor(enable_drift_correction=True)
        out = processor.process_capture(sample_input)

        # Validate output schema via pydantic
        model = CaptureOutputModel(**out)
        self.assertEqual(model.rooms["room1"].dimensions.floor_area_sq_m, 20.0)
        self.assertEqual(model.rooms["room1"].dimensions.ceiling_height_m, 2.70)
        self.assertEqual(len(model.rooms["room1"].walls), 4)
        self.assertTrue(out["drift_corrected"])
        self.assertLess(out["multi_room_stitched_plan"]["drift_metric_m"], 0.01)

if __name__ == "__main__":
    unittest.main()
