# الموجّه السيادي AlMuwajjih AlSiyadi

الموجّه السيادي يقرر هل يذهب طلب AI إلى نموذج محلي أو سحابي حسب الحساسية والميزانية والكمون ونوع المهمة.

## آلية العمل

1. `route` يوجه طلباً واحداً.
2. `convert-dolly` يحول Dolly 15k إلى طلبات اختبار.
3. `batch/stress` يتأكدان من عدم إرسال طلب حساس للسحابة.

## تشغيل سريع

```powershell
python -m almuwajjih_alsiyadi.cli route --prompt "write python code"
python -m almuwajjih_alsiyadi.cli convert-dolly
python -m almuwajjih_alsiyadi.cli batch
```

## بيانات الاختبار

المصدر: Databricks Dolly 15k المحفوظ داخل `C:\Projects\almeezan`، ويُستخدم منه 12,000 طلب.

## آخر نتائج

- الاختبارات الذاتية: 3/3 ناجحة.
- بيانات الإنترنت: 12,000 طلب Dolly، منها 706 طلبات حساسة مصطنعة.
- Benchmark: 12,000 توجيه، errors=0، sensitive_cloud_leaks=0، p99=0.051ms.
- توزيع الأهداف: local=866، local_fast=11,086، cloud_coder=48.
- Stress: 36,000 توجيه، 0 تسريب حساس، p99=0.047ms، peak memory=1.19MB.

## تحسينات إنتاجية 2026-07-04

- أي PII/secret أو sensitivity صريحة يذهب إلى local فقط.
- cloud_coder لا يستخدم إلا لمهام برمجة غير حساسة ومع ميزانية/كمون مناسبين.
- batch/stress يقيسان `sensitive_cloud_leaks` كمعيار انهيار أساسي.

## التشغيل المؤسسي (Enterprise) — v1.0.0

- **خدمة توجيه HTTP**: `python -m almuwajjih_alsiyadi.cli serve` → `POST /api/route {"prompt",...}` يعيد `local/local_fast/cloud_coder` مع سبب عربي.
- **ثابت أمني**: أي prompt حساس لا يوجه للسحاب أبداً (اختبار إنفاذي).
- **نقاط فحص**: `/api/health` (مفتوح) · `/api/version` · `/api/metrics`.
- **تهيئة عبر البيئة**: متغيرات `ALMUWAJJIH_*` — انظر `docs/OPERATIONS.md`.
- **مصادقة**: `ALMUWAJJIH_API_KEY` → ترويسة `X-API-Key`. **سجلات JSON**: `logs\almuwajjih-alsiyadi.service.jsonl`.
