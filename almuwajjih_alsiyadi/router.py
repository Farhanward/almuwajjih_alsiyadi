from __future__ import annotations

import re


SENSITIVE_RE = re.compile(r"(?i)(password|secret|token|api[_-]?key|email|phone|medical|legal|financial|private|سري|كلمة مرور|بريد)")


def route_request(request: dict) -> dict:
    prompt = str(request.get("prompt") or "")
    sensitivity = str(request.get("sensitivity") or "auto").lower()
    max_latency = float(request.get("max_latency_ms") or 2000)
    budget = float(request.get("budget_usd") or 0.02)
    needs_coding = bool(request.get("coding", False)) or any(word in prompt.lower() for word in ("code", "python", "debug", "function"))
    sensitive = sensitivity in {"secret", "restricted", "pii"} or bool(SENSITIVE_RE.search(prompt))
    if sensitive:
        target = "local"
        reason = "حساسية أو PII؛ يمنع السحاب."
    elif budget < 0.005:
        target = "local"
        reason = "ميزانية منخفضة."
    elif needs_coding and max_latency >= 1500:
        target = "cloud_coder"
        reason = "مهمة برمجة غير حساسة وتستفيد من نموذج أقوى."
    else:
        target = "local_fast"
        reason = "طلب عام سريع."
    return {"target": target, "reason_ar": reason, "sensitive": sensitive, "estimated_cost_usd": 0.0 if target.startswith("local") else min(0.02, budget)}

