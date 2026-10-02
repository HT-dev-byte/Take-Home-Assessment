import unittest
import json
import os
import subprocess

class TestCLIAndFixLoop(unittest.TestCase):
    def test_cli_execution(self):
        cmd = [
            "./bin/process_capture",
            "--input", "data/raw/raw_benchmark_lidar.json",
            "--tier", "lidar",
            "--output", "/tmp/cli_test_out.json",
            "--render", "/tmp/cli_test_out.svg"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"CLI error: {res.stderr}")
        self.assertTrue(os.path.exists("/tmp/cli_test_out.json"))
        self.assertTrue(os.path.exists("/tmp/cli_test_out.svg"))

    def test_fix_loop_outputs(self):
        self.assertTrue(os.path.exists("data/benchmark_results/before_fix.json"))
        self.assertTrue(os.path.exists("data/benchmark_results/after_fix.json"))

        with open("data/benchmark_results/before_fix.json") as f:
            before = json.load(f)
        with open("data/benchmark_results/after_fix.json") as f:
            after = json.load(f)

        self.assertFalse(before["drift_corrected"])
        self.assertTrue(after["drift_corrected"])
        self.assertGreater(before["multi_room_stitched_plan"]["drift_metric_m"], after["multi_room_stitched_plan"]["drift_metric_m"])

if __name__ == "__main__":
    unittest.main()
