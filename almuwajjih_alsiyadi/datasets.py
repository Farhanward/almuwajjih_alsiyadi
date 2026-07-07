from __future__ import annotations

import json
from pathlib import Path


def convert_dolly(input_path: str | Path, out_path: str | Path, *, limit: int = 12000) -> dict:
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    rows = sensitive = 0
    with Path(input_path).open("r", encoding="utf-8") as handle, out.open("w", encoding="utf-8") as output:
        for index, line in enumerate(handle):
            if limit and rows >= limit:
                break
            if not line.strip():
                continue
            rec = json.loads(line)
            text = str(rec.get("instruction") or rec.get("text") or "")
            is_sensitive = index % 17 == 0
            prompt = text + (" email user@example.com token=sk-12345678901234567890" if is_sensitive else "")
            req = {"prompt": prompt, "sensitivity": "pii" if is_sensitive else "auto", "budget_usd": 0.01 + (index % 5) / 1000, "max_latency_ms": 2000, "coding": "code" in text.lower()}
            output.write(json.dumps(req, ensure_ascii=False) + "\n")
            rows += 1
            sensitive += 1 if is_sensitive else 0
    return {"out": str(out.resolve()), "rows": rows, "sensitive": sensitive}

