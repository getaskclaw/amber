"""openai-compatible-baseline adapter — 真跑。
走 ollama-cloud OpenAI 兼容 chat API (POST {OLLAMA_BASE_URL:-https://ollama.com/v1}/chat/completions)。
把封闭判断题翻译成"只输出 JSON"的 chat 请求, 解析并严格校验回包;
解析失败重试一次, 再失败记 valid_task_failure。超时/quota/空响应 → invalid_infrastructure。
密钥只从环境变量 OLLAMA_API_KEY 读, 永不落盘。

HTTP 错误归类(r1, WO-DEC-001-r1 Blocker 3/4):
  - 401/402/403/429/5xx  → invalid_infrastructure(凭据失效/账单/限流/服务端)
  - 其余 4xx(400/404/405/409/422 等) → invalid_infrastructure: 请求本身写错(模型名拼错、
    路径或参数不对)是**我们的**配置错误, 不是模型失败, 按 AMBER 规矩归基础设施。
  唯一例外: 400/422 且响应体 error.code/type 命中语义类枚举 → valid_task_failure。
  判定见 `_is_semantic_body_error`; 响应体缺失/解析失败/未知 code 一律按 infra 处理
  (宁可把基础设施噪声算进 infra, 也不把运维错误算成模型分)。
"""
import json
import os
import re
import urllib.error
import urllib.request

from .base import Timer, make_response

NAME = "openai-compatible-baseline"
ENDPOINT = f"{os.environ.get('OLLAMA_BASE_URL', 'https://ollama.com/v1')}/chat/completions"
ENV_KEY = "OLLAMA_API_KEY"

# 唯一可能属于「模型输出问题」的状态码; 且必须有语义类 error code 佐证
SEMANTIC_CAPABLE_CODES = {400, 422}
SEMANTIC_CODES = {
    "content_filter", "context_length_exceeded", "invalid_prompt",
    "string_above_max_length", "token_limit_exceeded", "max_tokens_exceeded",
}


def _error_body(raw):
    try:
        return json.loads(raw.decode("utf-8", "replace"))
    except Exception:
        return None


def _is_semantic_body_error(code, body):
    """400/422 是否确为「模型输出/请求语义」错误(→ valid_task_failure)。"""
    if code not in SEMANTIC_CAPABLE_CODES or not isinstance(body, dict):
        return False
    err = body.get("error")
    if isinstance(err, dict):
        code_field = str(err.get("code") or err.get("type") or "").lower()
    elif isinstance(err, str):
        code_field = err.lower()
    else:
        code_field = ""
    return code_field in SEMANTIC_CODES


def classify_http_error(code, body, detail=None):
    """返回 error_class。见模块 docstring 的归类表。"""
    if _is_semantic_body_error(code, body):
        return "valid_task_failure"
    return "invalid_infrastructure"


def build_messages(record):
    q = record["type_obj"]
    t = q["type"]
    if t == "choice":
        spec = ("a choice: output JSON {\"answer\": \"<one of the option keys>\", "
                "\"probabilities\": {\"<key>\": <p>, ...}, \"confidence\": <0..1>} "
                "where probabilities cover every option key and sum to 1.")
        crit = "Options (key: description):\n" + "\n".join(
            f"- {k}: {v}" for k, v in q["options"].items())
    elif t == "score":
        spec = ("a score: output JSON {\"answer\": <integer level index>, "
                "\"probabilities\": {\"<index>\": <p>, ...}, \"confidence\": <0..1>} "
                "where indices are the level positions below and probabilities cover every index and sum to 1.")
        crit = "Levels (index: description):\n" + "\n".join(
            f"- {i}: {c}" for i, c in enumerate(q["criteria"]))
    else:
        spec = ("a probability: output JSON {\"answer\": <number 0..1>} = your probability "
                "that the answer to the yes/no question is YES.")
        crit = ""
    system = (
        "You are a deterministic decision engine. You never write prose. "
        "Given a STATE and a QUESTION, you reply with exactly one JSON object and nothing else. "
        "The JSON object must validate against this shape: " + spec +
        " No markdown fences, no explanation, no trailing text.")
    user = (f"STATE:\n{json.dumps(record['state'], ensure_ascii=False, indent=1) if not isinstance(record['state'], str) else record['state']}\n\n"
            f"QUESTION: {q['instructions']}\n" + (f"\n{crit}\n" if crit else "") +
            "\nReply with the single JSON object only.")
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def _validate_and_normalize(record, obj):
    t = record["type_obj"]["type"]
    if not isinstance(obj, dict) or "answer" not in obj:
        return None, "missing 'answer'"
    if t == "noul":
        v = obj["answer"]
        if isinstance(v, bool) or not isinstance(v, (int, float)) or not (0.0 <= v <= 1.0):
            return None, f"noul answer must be number 0..1, got {v!r}"
        return {"noul": float(v)}, None
    probs = obj.get("probabilities")
    conf = obj.get("confidence")
    if not isinstance(probs, dict) or not probs:
        return None, "missing/empty probabilities"
    try:
        pvals = {str(k): float(v) for k, v in probs.items()}
    except (TypeError, ValueError):
        return None, "probabilities must be numeric"
    if any(v < 0 or v > 1 for v in pvals.values()):
        return None, "probabilities out of [0,1]"
    if abs(sum(pvals.values()) - 1.0) > 0.05:
        return None, f"probabilities sum {sum(pvals.values()):.3f} != 1"
    if conf is not None:
        try:
            conf = float(conf)
        except (TypeError, ValueError):
            return None, "confidence not numeric"
        if not (0 <= conf <= 1):
            return None, "confidence out of [0,1]"
    if t == "choice":
        keys = set(record["type_obj"]["options"].keys())
        if set(pvals.keys()) != keys:
            return None, f"probability keys {sorted(pvals)} != option keys {sorted(keys)}"
        ans = obj["answer"]
        if ans not in keys:
            return None, f"answer {ans!r} not an option key"
        return {"choice": ans, "probabilities": pvals, "confidence": conf}, None
    # score
    n = len(record["type_obj"]["criteria"])
    keys = {str(i) for i in range(n)}
    if set(pvals.keys()) != keys:
        return None, f"probability keys {sorted(pvals)} != level indices 0..{n-1}"
    ans = obj["answer"]
    if isinstance(ans, bool) or not isinstance(ans, (int, float)):
        return None, f"score answer must be numeric, got {ans!r}"
    return {"score": float(ans), "probabilities": pvals, "confidence": conf}, None


def _extract_json(text):
    text = text.strip()
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None


def ask(record, model, dry_run=False, timeout_s=60, max_tokens=4096, effort="low",
        max_attempts=2, seed=None, ctx=None):
    ctx = ctx or {}
    common = {"run_nonce": ctx.get("run_nonce"), "dataset_sha256": ctx.get("dataset_sha256")}
    rec = {"state": record["state"], "type_obj": record["question"]}
    key = os.environ.get(ENV_KEY)
    if not key:
        raise RuntimeError(f"{NAME}: {ENV_KEY} not set; refusing to call baseline without a key")
    body_base = {
        "model": model,
        "messages": build_messages(rec),
        "max_tokens": max_tokens,
        "temperature": 0,
    }
    if seed is not None:
        body_base["seed"] = seed
    if effort:
        body_base["reasoning_effort"] = effort
    last_detail = "no attempts made"
    with Timer() as tm:
        for attempt in range(1, max_attempts + 1):
            if attempt > 1:
                body_base["messages"] = body_base["messages"] + [
                    {"role": "assistant", "content": last_raw},
                    {"role": "user", "content":
                     "Your previous reply was not valid (it could not be parsed as the required JSON). "
                     "Reply again with exactly one JSON object and nothing else."},
                ]
            payload = json.dumps(body_base).encode("utf-8")
            if dry_run:
                print(f"[{NAME} DRY-RUN] POST {ENDPOINT}")
                print(f"[{NAME} DRY-RUN] headers: Authorization: Bearer ${ENV_KEY}  Content-Type: application/json")
                print(f"[{NAME} DRY-RUN] body: {json.dumps(body_base, ensure_ascii=False, indent=2)}")
                return make_response(NAME, model, record["id"], record["family"], False, None,
                                     started=tm.started, latency_s=0.0, error_class="dry_run",
                                     error_detail="dry-run only: no request sent", **common)
            req = urllib.request.Request(
                ENDPOINT, data=payload,
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                method="POST")
            try:
                with urllib.request.urlopen(req, timeout=timeout_s) as r:
                    raw_resp = json.loads(r.read().decode("utf-8"))
            except urllib.error.HTTPError as e:
                code = e.code
                raw_body = e.read()
                body = _error_body(raw_body)
                detail = f"HTTP {code}: {raw_body.decode('utf-8', 'replace')[:200]}"
                cls = classify_http_error(code, body, detail)
                return make_response(NAME, model, record["id"], record["family"], False,
                                     None, tm.started, tm.latency,
                                     error_class=cls, error_detail=detail, **common)
            except Exception as e:
                # 网络层/超时一律 infra(契约: invalid_infrastructure)
                err = str(e)
                return make_response(NAME, model, record["id"], record["family"], False,
                                     None, tm.started, tm.latency,
                                     error_class="invalid_infrastructure",
                                     error_detail=err[:300], **common)
            try:
                content = raw_resp["choices"][0]["message"]["content"]
            except (KeyError, IndexError):
                content = ""
            if not content or not content.strip():
                return make_response(NAME, model, record["id"], record["family"], False,
                                     None, tm.started, tm.latency,
                                     error_class="invalid_infrastructure",
                                     error_detail="empty content in 200 response", **common)
            last_raw = content
            obj = _extract_json(content)
            if obj is None:
                last_detail = "unparseable JSON"
                continue
            ans, why = _validate_and_normalize(rec, obj)
            if ans is None:
                last_detail = why
                continue
            usage = raw_resp.get("usage", {}) or {}
            return make_response(NAME, model, record["id"], record["family"], True, ans,
                                 tm.started, tm.latency,
                                 tokens={"input": usage.get("prompt_tokens"),
                                         "output": usage.get("completion_tokens")},
                                 raw_excerpt=content[:500], **common)
    return make_response(NAME, model, record["id"], record["family"], False, None,
                         tm.started, tm.latency, error_class="valid_task_failure",
                         error_detail=f"output failed validation after {max_attempts} attempts: {last_detail}",
                         raw_excerpt=str(locals().get("last_raw") or "")[:500], **common)
