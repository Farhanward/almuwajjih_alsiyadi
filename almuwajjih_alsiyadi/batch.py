from __future__ import annotations

import json
import statistics
import time
import tracemalloc
from pathlib import Path

from .router import route_request


def _p(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, int(round((pct / 100) * (len(ordered) - 1))))]


def evaluate(path: str | Path, *, repeat: int = 1) -> dict:
    rows = [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]
    errors = leaks = 0
    targets: dict[str, int] = {}
    latencies = []
    started = time.perf_counter()
    tracemalloc.start()
    for _ in range(repeat):
        for row in rows:
            t0 = time.perf_counter()
            try:
                result = route_request(row)
                targets[result["target"]] = targets.get(result["target"], 0) + 1
                if result["sensitive"] and not result["target"].startswith("local"):
                    leaks += 1
            except Exception:
                errors += 1
            latencies.append((time.perf_counter() - t0) * 1000)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {"processed": len(rows) * repeat, "errors": errors, "sensitive_cloud_leaks": leaks, "targets": targets, "latency_ms": {"mean": statistics.fmean(latencies) if latencies else 0.0, "p99": _p(latencies, 99)}, "memory_mb": {"current": current / 1_000_000, "peak": peak / 1_000_000}, "elapsed_seconds": time.perf_counter() - started, "collapse_check": {"passed": errors == 0 and leaks == 0, "criteria": "errors == 0 and sensitive_cloud_leaks == 0"}}

