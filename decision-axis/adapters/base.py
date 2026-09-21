"""Adapter 公共件: 归一化响应构造 + 题级完整性 HMAC。
契约: contracts/adapter-interface.md

完整性口径(r1 起, WO-DEC-001-r1 Blocker 1):
  integrity = HMAC-SHA256(secret, canonical_json(record 除 integrity 外的全部字段))
  secret 只经环境变量 `AMBER_DECISION_HMAC_SECRET` 或 0600 密钥文件, 见 signing.py。
  r0 的公开无钥公式 sha256(adapter|model|qid|json(answer)) 已废除: 知道公式不再够。
"""
import json
import time

from signing import ALGO, sign_record  # noqa: F401  (ALGO re-exported for driver)


def integrity_hash(record):
    """题级完整性标签。

    签名覆盖整条记录(含 answer/ok/error_class/latency_s/cost_usd/tokens/
    run_nonce/dataset_sha256), 只有 integrity 自身不在其内。
    注意: r1 起签名对象是**整条记录**, 不再是 (adapter, model, qid, answer) 四元组;
    只重算旧四元组的人算不出有效标签(这正是要拦的攻击面)。
    """
    return sign_record(record)


def legacy_unkeyed_hash(adapter, model, question_id, answer):
    """r0 的公开无钥公式, 仅供**验旧存证**(--allow-legacy-unkeyed)。

    保留它不是为了信任它, 而是为了能对 r0 产物做「至少没被改答案」的最低限度检查,
    并在报告里如实标注 legacy-unkeyed = 无密码学保证。
    """
    import hashlib as _h
    import json as _j
    payload = _j.dumps(answer, sort_keys=True, separators=(",", ":"))
    s = f"{adapter}|{model}|{question_id}|{payload}"
    return _h.sha256(s.encode("utf-8")).hexdigest()


def make_response(adapter, model, question_id, family, ok, answer, started, latency_s,
                  cost_usd=None, tokens=None, error_class=None, error_detail=None,
                  raw_excerpt: str = "", run_nonce=None, dataset_sha256=None):
    rec = {
        "adapter": adapter,
        "model": model,
        "question_id": question_id,
        "family": family,
        "ok": bool(ok),
        "answer": answer,
        "latency_s": round(latency_s, 3),
        "cost_usd": cost_usd,
        "tokens": tokens,
        "error_class": error_class,
        "error_detail": error_detail,
        "raw_excerpt": raw_excerpt[:500],
        "started_unix": started,
        "run_nonce": run_nonce,
        "dataset_sha256": dataset_sha256,
        "integrity_algo": ALGO,
        "integrity": None,
    }
    rec["integrity"] = integrity_hash(rec)
    return rec


class Timer:
    def __enter__(self):
        self.t0 = time.monotonic()
        self.started = time.time()
        return self

    def __exit__(self, *a):
        pass

    @property
    def latency(self):
        return time.monotonic() - self.t0
