from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from almuwajjih_alsiyadi.batch import evaluate
from almuwajjih_alsiyadi.datasets import convert_dolly
from almuwajjih_alsiyadi.router import route_request


class AlMuwajjihTests(unittest.TestCase):
    def test_sensitive_routes_local(self):
        result = route_request({"prompt": "email user@example.com token=sk-12345678901234567890"})
        self.assertTrue(result["target"].startswith("local"))

    def test_coding_can_route_cloud(self):
        result = route_request({"prompt": "write python code", "budget_usd": 0.02, "max_latency_ms": 2000})
        self.assertEqual(result["target"], "cloud_coder")

    def test_convert_and_batch_fixture(self):
        with tempfile.TemporaryDirectory(dir="C:/Projects") as tmp:
            src = Path(tmp) / "dolly.jsonl"
            out = Path(tmp) / "requests.jsonl"
            src.write_text('{"instruction":"write python code"}\n{"instruction":"hello"}\n', encoding="utf-8")
            convert_dolly(src, out, limit=2)
            summary = evaluate(out)
            self.assertEqual(summary["errors"], 0)
            self.assertEqual(summary["sensitive_cloud_leaks"], 0)


if __name__ == "__main__":
    unittest.main()

