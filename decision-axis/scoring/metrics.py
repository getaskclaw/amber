"""评分指标: 全部自计算, 无任何锚定答案。
- per-family accuracy
- 校准分桶 (confidence bucket accuracy)
- ECE (expected calibration error, equal-width buckets)
- 阈值扫描 (auto-execute rate + accuracy per threshold)
输入: [(record, ResponseRecord)], 其中 ok 且 answer 非 null 的参与准确率和校准。

判分口径(r1 起统一, WO-DEC-001-r1 Blocker 5; 契约 contracts/golden-jsonl.md「判分规则」):
  唯一 oracle = 模型**自报答案**(choice→answer.choice; score→answer.score;
  noul→answer.noul 阈值 0.5)。probabilities 的 argmax **只作交叉校验**, 不参与判对。
  - r0 的双口径(choice 看 argmax / score 看 round(score))已废除。
  - score 的取整用**显式 half-up** `floor(x+0.5)`(不用 Python 裸 round, 其银行家
    舍入会让 0.5 分界点归属随整数奇偶变化)。
  - choice 概率平票(tie)无自报答案可用时 → **判错**。理由: 平票说明模型没有给出
    唯一偏好, 决策轴上等于「未作出决定」; 判错是与 gold 无关的确定性规则, 不依赖
    dict 键序, 也不会因键序碰巧排对而给分。noul 恰为 0.5 同样判错(同一理由)。
"""
import math
from collections import defaultdict

THRESHOLD = 0.5


def round_half_up(x):
    """显式 half-up 取整(0.5 向上)。非负输入。取代裸 round() 的银行家舍入。"""
    return int(math.floor(float(x) + 0.5))


def _probabilities_of(resp):
    a = resp.get("answer") or {}
    probs = a.get("probabilities")
    return probs if isinstance(probs, dict) and probs else None


def _argmax_key(probs):
    """概率最大的键的确定性集合与取值。平票 -> 多个键。"""
    if not probs:
        return None, []
    top = max(probs.values())
    return top, sorted(k for k, v in probs.items() if v == top)


def predicted(record, resp):
    """按统一口径给出模型自报的预测值; 无法给出(平票/缺字段) -> None。

    choice: a["choice"](自报选项键)
    score : 显式 half-up 取整并钳制到等级范围
    noul  : a["noul"] >= 0.5
    """
    t = record["question"]["type"]
    a = resp.get("answer")
    if not isinstance(a, dict):
        return None
    if t == "choice":
        return a.get("choice")
    if t == "score":
        n = len(record["question"]["criteria"])
        v = a.get("score")
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            return None
        return min(max(round_half_up(v), 0), n - 1)
    v = a.get("noul")
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return None
    if v == THRESHOLD:
        return None          # 恰在中点 = 未表态, 按平票口径判错
    return v > THRESHOLD


def cross_check(record, resp):
    """自报答案与 argmax 的一致性交叉校验(不进准确率, 只记数)。

    返回 (consistent: bool|None, note: str)。
    """
    a = resp.get("answer")
    if not isinstance(a, dict):
        return None, "no answer"
    t = record["question"]["type"]
    if t == "noul":
        return None, "noul has no discrete probabilities to cross-check"
    probs = _probabilities_of(resp)
    if probs is None:
        return None, "no probabilities to cross-check"
    _top, tied = _argmax_key(probs)
    if len(tied) != 1:
        return False, f"tie over {tied}; stated={_stated(record, a)!r}"
    if t == "choice":
        ok = a.get("choice") == tied[0]
        return ok, f"stated={a.get('choice')!r} argmax={tied[0]!r}"
    n = len(record["question"]["criteria"])
    v = a.get("score")
    stated = min(max(round_half_up(v), 0), n - 1) if isinstance(v, (int, float)) \
        and not isinstance(v, bool) else None
    int_keys = [k for k in tied if str(k).lstrip("-").isdigit()]
    ok = stated is not None and len(int_keys) == 1 and int(int_keys[0]) == stated
    return ok, f"stated={stated} argmax={tied[0]!r}"


def _stated(record, a):
    t = record["question"]["type"]
    if t == "choice":
        return a.get("choice")
    if t == "score":
        v = a.get("score")
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            return None
        n = len(record["question"]["criteria"])
        return min(max(round_half_up(v), 0), n - 1)
    return a.get("noul")


def correctness(record, resp):
    """单题判对, 统一口径见模块 docstring。"""
    pred = predicted(record, resp)
    if pred is None:
        return False        # 平票/缺字段: 未作出决定 = 判错(确定性, 不依赖键序)
    return pred == record["gold"]


def confidence_of(record, resp):
    """置信度: choice/score = max 概率; noul = max(p, 1-p)。平票无概率时取 0.5。"""
    t = record["question"]["type"]
    a = resp.get("answer") or {}
    if t == "noul":
        v = a.get("noul")
        if not isinstance(v, (int, float)) or isinstance(v, bool):
            return THRESHOLD
        return max(v, 1.0 - v)
    probs = _probabilities_of(resp)
    if probs is None:
        return THRESHOLD
    return max(probs.values())


def per_family_accuracy(scored):
    """scored: list of (record, resp, correct). 返回 {family: {n, correct, accuracy}}"""
    fams = defaultdict(lambda: {"n": 0, "correct": 0})
    for rec, _resp, ok in scored:
        fams[rec["family"]]["n"] += 1
        fams[rec["family"]]["correct"] += int(ok)
    out = {}
    for fam, d in fams.items():
        out[fam] = {**d, "accuracy": d["correct"] / d["n"] if d["n"] else None}
    return out


def calibration(scored, n_buckets=10):
    """equal-width buckets over [0,1]。
    返回 {buckets: [{lo,hi,n,acc,conf,gap}], ece}。
    ECE = sum(|B|/N * |acc(B)-conf(B)|), 空桶贡献 0。"""
    buckets = [{"lo": i / n_buckets, "hi": (i + 1) / n_buckets,
                "n": 0, "correct": 0, "conf_sum": 0.0} for i in range(n_buckets)]
    total = len(scored)
    for rec, resp, ok in scored:
        conf = confidence_of(rec, resp)
        idx = min(int(conf * n_buckets), n_buckets - 1)
        b = buckets[idx]
        b["n"] += 1
        b["correct"] += int(ok)
        b["conf_sum"] += conf
    out = []
    ece = 0.0
    for b in buckets:
        acc = b["correct"] / b["n"] if b["n"] else None
        conf = b["conf_sum"] / b["n"] if b["n"] else None
        gap = abs(acc - conf) if b["n"] else None
        if b["n"]:
            ece += (b["n"] / total) * gap
        out.append({"lo": round(b["lo"], 3), "hi": round(b["hi"], 3), "n": b["n"],
                    "acc": acc, "conf": conf, "gap": gap})
    return {"buckets": out, "ece": ece, "n_buckets": n_buckets}


def threshold_scan(scored, thresholds=None):
    """每个阈值 t: auto_execute_rate = conf>=t 占比; 其准确率。"""
    if thresholds is None:
        thresholds = [i * 0.05 for i in range(21)]
    rows = []
    total = len(scored)
    for t in thresholds:
        sub = [(rec, resp, ok) for rec, resp, ok in scored if confidence_of(rec, resp) >= t]
        n = len(sub)
        rows.append({
            "threshold": round(t, 2),
            "auto_execute_rate": n / total if total else None,
            "n": n,
            "accuracy": sum(int(ok) for _r, _p, ok in sub) / n if n else None,
        })
    return rows


def oracle_stats(scored):
    """统一口径的可观测统计: tie 题数、自报 vs argmax 不一致题数。"""
    ties, inconsistent, checked = 0, 0, 0
    for rec, resp, _ok in scored:
        t = rec["question"]["type"]
        if t == "choice":
            probs = _probabilities_of(resp)
            _top, tied = _argmax_key(probs)
            if len(tied) > 1:
                ties += 1
        if t == "noul":
            v = (resp.get("answer") or {}).get("noul")
            if isinstance(v, (int, float)) and not isinstance(v, bool) and v == THRESHOLD:
                ties += 1
        cons, _note = cross_check(rec, resp)
        if cons is not None:
            checked += 1
            if not cons:
                inconsistent += 1
    return {"oracle": "stated-answer (argmax cross-check only)",
            "tie_rule": "tie or exact 0.5 -> judged wrong (deterministic)",
            "rounding": "explicit half-up floor(x+0.5), not Python round()",
            "n_ties": ties, "n_cross_checked": checked, "n_inconsistent": inconsistent}


def full_report(scored, per_q, n_expected=None, n_received=None):
    """scored: ok 且可评分项。per_q: 全部题(含失败分类)的明细。
    返回报告 dict(纯 JSON 可序列化)。"""
    n = len(scored)
    acc = sum(int(ok) for _r, _p, ok in scored) / n if n else None
    cal = calibration(scored)
    fams = per_family_accuracy(scored)
    by_type = defaultdict(lambda: {"n": 0, "correct": 0})
    for rec, _resp, ok in scored:
        t = rec["question"]["type"]
        by_type[t]["n"] += 1
        by_type[t]["correct"] += int(ok)
    types = {t: {**d, "accuracy": d["correct"] / d["n"] if d["n"] else None}
             for t, d in by_type.items()}
    lat = [r["latency_s"] for _rec, r, _ok in scored]
    costs = [r["cost_usd"] for _rec, r, _ok in scored if r.get("cost_usd") is not None]
    n_abstained = sum(1 for q in per_q if q["classification"] == "valid_task_failure")
    return {
        "n_scored": n,
        "n_expected": n_expected,
        "n_received": n_received,
        "coverage_note": (
            f"denominator = {n} scored of {n_expected} expected; "
            f"{n_abstained} valid_task_failure (abstentions raise accuracy -- read alongside this line)"
            if n_expected else None),
        "abstentions": {
            "n_valid_task_failure": n_abstained,
            "rate": (n_abstained / n_expected) if n_expected else None,
            "note": "valid_task_failure is excluded from the denominator per AMBER rule; "
                    "this count is surfaced so a high abstention rate cannot hide.",
        },
        "accuracy": acc,
        "oracle": oracle_stats(scored),
        "by_type": types,
        "by_family": fams,
        "calibration": cal,
        "threshold_scan": threshold_scan(scored),
        "latency": {
            "mean_s": sum(lat) / len(lat) if lat else None,
            "max_s": max(lat) if lat else None,
            "per_question_s": {rec["id"]: r["latency_s"] for rec, r, _ok in scored},
        },
        "cost": {
            "per_decision_mean_usd": sum(costs) / len(costs) if costs else None,
            "total_usd": sum(costs) if costs else None,
            "n_priced": len(costs),
            "note": None if costs else "no price table entry for this model; cost left null rather than fabricated",
        },
        "questions": per_q,
    }
