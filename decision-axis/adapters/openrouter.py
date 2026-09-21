"""openrouter adapter — Jev 走 OpenRouter Decisions 端点 (alpha)。
本机无 OPENROUTER_API_KEY → 只允许 dry-run, 真调直接拒绝。
请求形状依据: openrouter.ai/docs "Submit a Decisions (questions and answers) request"
(2026-09-18 抓取): POST {base}/api/alpha/decisions, body {model, questions, state},
响应 {answers, id, model, provider, usage{cost, input_tokens, output_tokens}}。
"""
import json
import os
import urllib.request

from .base import Timer, make_response
from .typesafe_native import build_body

NAME = "openrouter"
ENDPOINT = f"{os.environ.get('OPENROUTER_BASE_URL', 'https://openrouter.ai')}/api/alpha/decisions"
ENV_KEY = "OPENROUTER_API_KEY"


def ask(record, model="typesafe/jev-1.13", dry_run=False, timeout_s=60, ctx=None):
    ctx = ctx or {}
    common = {"run_nonce": ctx.get("run_nonce"), "dataset_sha256": ctx.get("dataset_sha256")}
    q = record["question"]
    body = build_body(record["state"], q, model)  # 形状与 typesafe-native 一致(官方示例逐字段一致)
    if dry_run:
        print(f"[{NAME} DRY-RUN] POST {ENDPOINT}")
        print(f"[{NAME} DRY-RUN] headers: Authorization: Bearer ***  Content-Type: application/json")
        print(f"[{NAME} DRY-RUN] body: {json.dumps(body, ensure_ascii=False, indent=2)}")
        return make_response(NAME, model, record["id"], record["family"], False, None,
                             started=0, latency_s=0.0, error_class="dry_run",
                             error_detail="dry-run only: no request sent", **common)
    key = os.environ.get(ENV_KEY)
    if not key:
        raise RuntimeError(
            f"{NAME}: {ENV_KEY} not set and dry-run disabled; refusing to call OpenRouter without a key")
    req = urllib.request.Request(
        ENDPOINT, data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST")
    with Timer() as tm:
        try:
            with urllib.request.urlopen(req, timeout=timeout_s) as r:
                raw = json.loads(r.read().decode("utf-8"))
        except Exception as e:
            return _fail(record, model, tm, e, common)
    ans = raw.get("answers", {}).get(q["id"], {})
    a = _normalize(q["type"], ans)
    usage = raw.get("usage", {}) or {}
    return make_response(NAME, model, record["id"], record["family"], a is not None, a,
                         tm.started, tm.latency,
                         cost_usd=usage.get("cost"),
                         tokens={"input": usage.get("input_tokens"),
                                 "output": usage.get("output_tokens")},
                         raw_excerpt=json.dumps(raw, ensure_ascii=False)[:500], **common)


def _normalize(qtype, ans):
    from .typesafe_native import _normalize as _n
    return _n(qtype, ans)


def _fail(record, model, tm, e, common=None):
    common = common or {}
    err = str(e)
    cls = "invalid_infrastructure"  # 超时/quota/5xx/网络层/4xx 全是我们的问题, 见契约
    return make_response(NAME, model, record["id"], record["family"], False, None,
                         tm.started, tm.latency, error_class=cls, error_detail=err[:300], **common)
