"""typesafe-native adapter — Jev 原生 API (POST /v1/systemone)。
本机无 TYPESAFE_API_KEY → 只允许 dry-run(打印将发送的请求体), 真调直接拒绝。
请求形状依据: docs.typesafe.ai/introduction/quickstart.md (2026-09-18 抓取)。
错误分类(r1): 任何 HTTP 错误(含 4xx: 模型名/路径/参数写错 = 我们的配置错误)一律
invalid_infrastructure; 见契约「错误分类」表。
"""
import json
import os
import urllib.error
import urllib.request

from .base import Timer, make_response

NAME = "typesafe-native"
ENDPOINT = f"{os.environ.get('TYPESAFE_BASE_URL', 'https://api.typesafe.ai')}/v1/systemone"
ENV_KEY = "TYPESAFE_API_KEY"


def build_body(state, question, model):
    q = {"type": question["type"], "instructions": question["instructions"]}
    if question["type"] == "choice":
        q["criteria"] = question["options"]
    elif question["type"] == "score":
        q["criteria"] = question["criteria"]
    return {"state": state, "model": model, "questions": {question["id"]: q}}


def ask(record, model="jev-latest", dry_run=False, timeout_s=60, ctx=None):
    ctx = ctx or {}
    common = {"run_nonce": ctx.get("run_nonce"), "dataset_sha256": ctx.get("dataset_sha256")}
    q = record["question"]
    body = build_body(record["state"], q, model)
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
            f"{NAME}: {ENV_KEY} not set and dry-run disabled; refusing to call Jev without a key")
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
                         tokens={"input": usage.get("input_tokens"),
                                 "output": usage.get("output_tokens")},
                         raw_excerpt=json.dumps(raw, ensure_ascii=False)[:500], **common)


def _normalize(qtype, ans):
    if not ans:
        return None
    if qtype == "choice":
        if "choice" not in ans or "probabilities" not in ans:
            return None
        return {"choice": ans["choice"], "probabilities": ans["probabilities"],
                "confidence": ans.get("confidence")}
    if qtype == "score":
        if "score" not in ans or "probabilities" not in ans:
            return None
        return {"score": ans["score"], "probabilities": ans["probabilities"],
                "confidence": ans.get("confidence")}
    if "noul" not in ans:
        return None
    return {"noul": ans["noul"]}


def _fail(record, model, tm, e, common=None):
    common = common or {}
    err = str(e)
    cls = "invalid_infrastructure"  # HTTP 4xx/5xx/超时/网络层一律 infra, 见契约错误分类表
    return make_response(NAME, model, record["id"], record["family"], False, None,
                         tm.started, tm.latency, error_class=cls, error_detail=err[:300], **common)
