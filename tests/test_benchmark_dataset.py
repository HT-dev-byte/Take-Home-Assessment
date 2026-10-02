import unittest
import json
import os

class TestBenchmarkDatasets(unittest.TestCase):
    def test_gt_file_structure(self):
        gt_path = "data/ground_truth/benchmark_gt.json"
        self.assertTrue(os.path.exists(gt_path))
        with open(gt_path, "r") as f:
            gt = json.load(f)
        self.assertIn("rooms", gt)
        self.assertEqual(len(gt["rooms"]), 4) # 3 rooms + connector hallway
        self.assertIn("staged_damage", gt["rooms"]["primary_bedroom"])

    def test_raw_captures_exist(self):
        tiers = ["lidar", "video", "photos", "repeatability_run2"]
        for t in tiers:
            path = f"data/raw/raw_benchmark_{t}.json"
            self.assertTrue(os.path.exists(path), f"Missing dataset: {path}")

if __name__ == "__main__":
    unittest.main()
