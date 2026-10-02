import unittest
from scan_pipeline.video import VideoProcessor
from scan_pipeline.models import CaptureOutputModel

class TestVideoProcessor(unittest.TestCase):
    def test_video_processing(self):
        sample_input = {
            "capture_id": "bench_video_01",
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
                }
            },
            "adjacency": []
        }

        processor = VideoProcessor()
        out = processor.process_capture(sample_input)

        model = CaptureOutputModel(**out)
        self.assertEqual(model.tier, "video")
        self.assertEqual(model.rooms["room1"].dimensions.floor_area_sq_m, 20.0)
        self.assertEqual(len(model.rooms["room1"].walls), 4)

if __name__ == "__main__":
    unittest.main()
