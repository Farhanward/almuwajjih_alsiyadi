from __future__ import annotations


def markdown(summary: dict, title: str = "تقرير الموجّه السيادي") -> str:
    return "\n".join([f"# {title}", "", f"- المعالجة: `{summary.get('processed', 0)}`", f"- تسريب حساس للسحاب: `{summary.get('sensitive_cloud_leaks', 0)}`", f"- الأهداف: `{summary.get('targets', {})}`", f"- أخطاء: `{summary.get('errors', 0)}`", f"- p99: `{summary.get('latency_ms', {}).get('p99', 0):.4f}ms`", ""])

