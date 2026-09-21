#!/usr/bin/env python3
"""AMBER decision-axis 评测管道 driver (WO-DEC-001-r1)。

用法:
  # 真跑基线模型(冒烟):
  python3 driver.py --adapter openai-compatible-baseline --model glm-5.3-flash \
      --dataset data/smoke-12.jsonl --tag smoke-g53f-1
  # dry-run(Jev/OpenRouter 形状核对):
  python3 driver.py --adapter typesafe-native --dry-run --dataset data/smoke-12.jsonl --tag dryrun-ts
  # 空 state 基线(区分度闸):
  python3 driver.py --adapter openai-compatible-baseline --model glm-5.3-flash \
      --dataset data/smoke-12.jsonl --tag empty-g53f --empty-state
  # 只重评分(完整性重验 + 行数/id 对账 + 指标重算, 零调用):
  python3 driver.py --score-only runs/<tag>/responses.jsonl \
      --adapter openai-compatible-baseline --model glm-5.3-flash \
      --dataset data/smoke-12.jsonl --tag rescore-<tag>
  # 复核历史 run(重算 manifest 数值与 report 对账):
  python3 driver.py --verify-run <tag> --dataset data/smoke-12.jsonl

诚信闸(r1, WO-DEC-001-r1):
  1. 题级完整性 = HMAC-SHA256(secret, 整条响应记录)。secret 只经环境变量
     `AMBER_DECISION_HMAC_SECRET` 或 0600 密钥文件(路径见 signing.py), 绝不落进本目录。
     r0 的公开无钥 sha256(adapter|model|qid|answer) 已废除 —— 知道公式不再够。
  2. `--score-only` 强制对账: responses 的 question_id 集合 == 数据集 id 集合,
     行数一致, 且每条记录内嵌的 dataset_sha256 == 当前数据集文件哈希。缺行/多行即 rc≠0。
  3. manifest 记全跑参数(effort/timeout/max_tokens/max_attempts/temperature/seed/
     run_nonce)+ report.json 与 responses.jsonl 的 sha256, 可用 `--verify-run` 重算对账。
  4. 同一 --tag 二次运行默认拒绝(防静默覆盖证据), 需 `--force` 显式同意。

manifest.jsonl 用 fcntl 锁 append。密钥只经环境变量或 0600 文件, 不落盘。
"""
import argparse
import datetime
import fcntl
import hashlib
import json
import os
import secrets
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from adapters import ADAPTERS  # noqa: E402
from scoring import metrics  # noqa: E402
from scoring.validate import DatasetError, load_dataset  # noqa: E402
import signing  # noqa: E402

DRIVER_VERSION = "dec001-r1.1.0"
LEGACY_ALGO = "sha256-legacy-unkeyed"
ROOT = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(ROOT, "runs", "manifest.jsonl")
PRICES = os.path.join(ROOT, "config", "prices.json")


class GateError(Exception):
    """诚信闸拒绝出分。main() 捕获 → rc≠0。"""


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_prices():
    try:
        with open(PRICES) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def price_cost(model, tokens, prices):
    if not tokens:
        return None
    entry = prices.get(model)
    if not entry:
        return None
    pin, pout = entry.get("input_per_1M"), entry.get("output_per_1M")
    if pin is None or pout is None:
        return None
    return (tokens.get("input") or 0) * pin / 1e6 + (tokens.get("output") or 0) * pout / 1e6


def run_dataset(records, adapter_name, model, dry_run, effort, timeout_s, empty_state,
                run_nonce, dataset_sha256, max_tokens, max_attempts, seed):
    mod = ADAPTERS[adapter_name]
    ctx = {"run_nonce": run_nonce, "dataset_sha256": dataset_sha256}
    responses = []
    for rec in records:
        r = dict(rec)
        if empty_state:
            r["state"] = "(no context provided)"
        kw = {"ctx": ctx}
        if adapter_name == "openai-compatible-baseline":
            kw.update({"effort": effort, "max_tokens": max_tokens,
                       "max_attempts": max_attempts, "seed": seed})
        resp = mod.ask(r, model=model, dry_run=dry_run, timeout_s=timeout_s, **kw)
        # invalid_infrastructure 按 AMBER 规矩重跑一次再判
        if resp["error_class"] == "invalid_infrastructure" and not dry_run:
            resp2 = mod.ask(r, model=model, dry_run=dry_run, timeout_s=timeout_s, **kw)
            resp2["error_detail"] = (f"retry after infra failure; first: {resp['error_detail']!r}; "
                                     f"then: {resp2['error_detail']!r}")
            resp2["integrity"] = None
            resp2 = _resign(resp2)
            resp = resp2
        responses.append((r, resp))
        print(f"  {rec['id']}: ok={resp['ok']} err={resp['error_class']} "
              f"lat={resp['latency_s']}s", flush=True)
    return responses


def _resign(resp):
    """字段被驱动层改写后重签(只用整条记录 HMAC, 不碰 answer 语义)。"""
    rec = dict(resp)
    rec["integrity"] = None
    rec["integrity"] = signing.sign_record(rec)
    return rec


def verify_integrity(responses, allow_legacy=False):
    """逐题重验 HMAC。被篡改 → 拒。legacy(r0)记录须显式放行且不获得信任。"""
    tampered, legacy = [], []
    for _rec, resp in responses:
        algo = resp.get("integrity_algo")
        if not algo or algo == LEGACY_ALGO:
            legacy.append(resp["question_id"])
            continue
        if not signing.matches(resp):
            tampered.append(resp["question_id"])
    if tampered:
        raise GateError(
            "TAMPER DETECTED: integrity mismatch on " + ", ".join(tampered) +
            "; refusing to score. 响应文件被改, 签名覆盖整条记录(含 answer/ok/error_class/"
            "latency_s/cost_usd/tokens/run_nonce/dataset_sha256), 只重算旧公开公式无效。")
    if legacy and not allow_legacy:
        raise GateError(
            "LEGACY ARTIFACT: " + ", ".join(legacy) +
            " 无 r1 HMAC 签名(r0 公开无钥公式, 不可信)。要重算请显式加 --allow-legacy-unkeyed; "
            "那样出的报告会被标注 integrity_assurance=legacy-unkeyed(NOT cryptographic)。")
    return {"tampered": tampered, "legacy": legacy}


def reconcile(responses, records):
    """行数 + question_id 集合 + 内嵌 dataset 哈希 对账。缺行/多行/串集 → 拒。"""
    expected = [r["id"] for r in records]
    got = [resp["question_id"] for _rec, resp in responses]
    exp_set, got_set = set(expected), set(got)
    problems = []
    if len(got) != len(expected):
        problems.append(f"row count {len(got)} != dataset size {len(expected)}")
    if got_set != exp_set:
        missing = sorted(exp_set - got_set)
        extra = sorted(got_set - exp_set)
        if missing:
            problems.append(f"missing question_id(s) {missing} (rows dropped)")
        if extra:
            problems.append(f"unknown question_id(s) {extra} (rows not in dataset)")
    if len(got) != len(got_set):
        problems.append("duplicate question_id rows present")
    if problems:
        raise GateError("RECONCILIATION FAILED: " + "; ".join(problems) +
                        "; refusing to score (denominator cannot be trusted).")
    return {"n_expected": len(expected), "n_received": len(got)}


def reconcile_dataset_hash(responses, dataset_sha256, allow_legacy=False):
    """响应内嵌的 dataset_sha256 必须等于当前数据集哈希(签名已覆盖该字段)。"""
    bad = []
    for _rec, resp in responses:
        if not resp.get("integrity_algo") or resp.get("integrity_algo") == LEGACY_ALGO:
            if allow_legacy:
                continue
            continue
        if resp.get("dataset_sha256") != dataset_sha256:
            bad.append(resp["question_id"])
    if bad:
        raise GateError(
            f"DATASET MISMATCH: {len(bad)} response row(s) ({', '.join(bad[:5])}...) were signed "
            f"against a different dataset hash; refusing to score against {dataset_sha256[:16]}...")


def score(responses, n_expected=None):
    scored, per_q = [], []
    for rec, resp in responses:
        if resp["error_class"] == "dry_run":
            per_q.append({"id": rec["id"], "classification": "dry_run"})
            continue
        if resp["error_class"] == "invalid_infrastructure":
            per_q.append({"id": rec["id"], "classification": "invalid_infrastructure",
                          "detail": resp["error_detail"], "latency_s": resp["latency_s"]})
            continue
        if not resp["ok"] or resp["answer"] is None:
            per_q.append({"id": rec["id"], "classification": "valid_task_failure",
                          "detail": resp["error_detail"], "latency_s": resp["latency_s"]})
            continue
        ok = metrics.correctness(rec, resp)
        scored.append((rec, resp, ok))
        per_q.append({"id": rec["id"], "classification": "scored",
                      "family": rec["family"], "type": rec["question"]["type"],
                      "correct": ok,
                      "predicted": metrics.predicted(rec, resp),
                      "confidence": round(metrics.confidence_of(rec, resp), 4),
                      "latency_s": resp["latency_s"], "cost_usd": resp["cost_usd"]})
    report = metrics.full_report(scored, per_q, n_expected=n_expected,
                                 n_received=len(responses))
    report["failures"] = {
        "invalid_infrastructure": [q for q in per_q if q["classification"] == "invalid_infrastructure"],
        "valid_task_failure": [q for q in per_q if q["classification"] == "valid_task_failure"],
    }
    return report


def append_manifest(row):
    os.makedirs(os.path.dirname(MANIFEST), exist_ok=True)
    with open(MANIFEST, "a", encoding="utf-8") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
        fcntl.flock(f, fcntl.LOCK_UN)


def write_outputs(tag, responses, report, dataset_path, adapter_name, model, extra_meta):
    outdir = os.path.join(ROOT, "runs", tag)
    os.makedirs(outdir, exist_ok=True)
    rp = os.path.join(outdir, "responses.jsonl")
    with open(rp, "w", encoding="utf-8") as f:
        for _rec, resp in responses:
            f.write(json.dumps(resp, ensure_ascii=False) + "\n")
    resp_sha = sha256_file(rp)
    # responses.jsonl 是稳定文件, 其 sha256 可安全内嵌进 report.json 供对账。
    # report.json 自身不内嵌自己的 sha256(自引用哈希不可实现), 改由 manifest 记录。
    report["responses_sha256"] = resp_sha
    rj = os.path.join(outdir, "report.json")
    with open(rj, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    report_sha = sha256_file(rj)

    lines = [f"# Decision-axis run: {tag}", ""]
    lines.append(f"- adapter: `{adapter_name}`  model: `{model}`")
    lines.append(f"- dataset: `{dataset_path}` sha256 `{sha256_file(dataset_path)[:16]}...`")
    lines.append(f"- driver: {DRIVER_VERSION}  tmp_prefix: {extra_meta['tmp_prefix']}")
    lines.append(f"- run_nonce: `{extra_meta.get('run_nonce')}`")
    lines.append(f"- integrity: {extra_meta.get('integrity_algo')} "
                 f"  assurance: {report.get('integrity_assurance')}")
    lines.append(f"- report.json sha256: `{report_sha}`")
    lines.append(f"- responses.jsonl sha256: `{resp_sha}`")
    lines.append("")
    lines.append(f" scored: {report['n_scored']} / expected {report['n_expected']}"
                 f"  accuracy: {report['accuracy']}")
    lines.append(f" abstentions (valid_task_failure, excluded from denominator): "
                 f"{report['abstentions']['n_valid_task_failure']}")
    lines.append(f" oracle: {report['oracle']['oracle']}; tie rule: {report['oracle']['tie_rule']}; "
                 f"rounding: {report['oracle']['rounding']}")
    lines.append(f" ties seen: {report['oracle']['n_ties']}  "
                 f"stated/argmax inconsistent: {report['oracle']['n_inconsistent']}"
                 f"/{report['oracle']['n_cross_checked']}")
    lines.append(f" ECE: {report['calibration']['ece']}")
    lines.append(f" latency mean: {report['latency']['mean_s']}s max: {report['latency']['max_s']}s")
    lines.append(f" cost: {report['cost']}")
    lines.append("")
    lines.append("## by family")
    for fam, d in sorted(report["by_family"].items()):
        lines.append(f"- {fam}: {d['correct']}/{d['n']} = {d['accuracy']}")
    lines.append("")
    lines.append("## calibration buckets (10, equal-width)")
    lines.append("| conf lo-hi | n | acc | conf | gap |")
    lines.append("|---|---|---|---|---|")
    for b in report["calibration"]["buckets"]:
        acc = f"{b['acc']:.2f}" if b["acc"] is not None else "-"
        conf = f"{b['conf']:.2f}" if b["conf"] is not None else "-"
        gap = f"{b['gap']:.3f}" if b["gap"] is not None else "-"
        lines.append(f"| {b['lo']:.1f}-{b['hi']:.1f} | {b['n']} | {acc} | {conf} | {gap} |")
    lines.append("")
    lines.append("## threshold scan")
    lines.append("| threshold | auto_exec_rate | n | accuracy |")
    lines.append("|---|---|---|---|")
    for r in report["threshold_scan"]:
        aer = f"{r['auto_execute_rate']:.2f}" if r["auto_execute_rate"] is not None else "-"
        acc = f"{r['accuracy']:.2f}" if r["accuracy"] is not None else "-"
        lines.append(f"| {r['threshold']:.2f} | {aer} | {r['n']} | {acc} |")
    lines.append("")
    lines.append("## failures")
    for cls, items in report["failures"].items():
        lines.append(f"- {cls}: {len(items)}")
        for it in items:
            lines.append(f"  - {it['id']}: {str(it.get('detail', ''))[:200]}")
    lines.append("")
    lines.append("## per question")
    for q in report["questions"]:
        lines.append(f"- {q['id']}: {q['classification']}" +
                     (f" correct={q['correct']} pred={q.get('predicted')!r} conf={q['confidence']}"
                      if q["classification"] == "scored" else ""))
    with open(os.path.join(outdir, "REPORT.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return outdir, report_sha, resp_sha


def guard_tag(tag, force):
    outdir = os.path.join(ROOT, "runs", tag)
    if os.path.exists(outdir) and not force:
        raise GateError(
            f"RUN DIR EXISTS: runs/{tag}/ already has evidence. Refusing to overwrite "
            "(score-only/runs must not erase prior artifacts). Re-run with --force to replace, "
            "or pick a new --tag.")


def _load_responses(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def _integrity_assurance(responses, allow_legacy):
    n_legacy = sum(1 for _r, x in responses
                   if not x.get("integrity_algo") or x.get("integrity_algo") == LEGACY_ALGO)
    if n_legacy and allow_legacy:
        return ("legacy-unkeyed (NOT cryptographic; r0 public formula, "
                "row/id reconciliation still enforced)")
    return "hmac-sha256 (keyed; whole-record coverage)"


def do_score_only(args, records, dataset_sha256, tmpdir):
    resps = _load_responses(args.score_only)
    by_id = {r["id"]: r for r in records}
    unknown = [r.get("question_id") for r in resps if r.get("question_id") not in by_id]
    if unknown:
        raise GateError(f"SCORE-ONLY: response rows reference unknown question_id(s): "
                        f"{sorted(set(unknown))[:5]}; refusing.")
    responses = [(by_id[r["question_id"]], r) for r in resps]
    verify_integrity(responses, allow_legacy=args.allow_legacy_unkeyed)
    recon = reconcile(responses, records)
    reconcile_dataset_hash(responses, dataset_sha256,
                           allow_legacy=args.allow_legacy_unkeyed)
    report = score(responses, n_expected=recon["n_expected"])
    nonces = {r.get("run_nonce") for _rec, r in responses if r.get("run_nonce")}
    report["run_nonce"] = sorted(nonces)[0] if len(nonces) == 1 else None
    report["integrity_assurance"] = _integrity_assurance(
        responses, args.allow_legacy_unkeyed)
    report["scored_from"] = os.path.relpath(args.score_only, ROOT)
    guard_tag(args.tag, args.force)
    tmpdir2 = tmpdir
    outdir, rsha, osha = write_outputs(args.tag, responses, report, args.dataset,
                                       args.adapter, args.model,
                                       {"tmp_prefix": os.path.basename(tmpdir2),
                                        "run_nonce": report["run_nonce"],
                                        "integrity_algo": args.adapter and
                                        (responses[0][1].get("integrity_algo") or LEGACY_ALGO)})
    print(f"re-scored OK -> {outdir}")
    print(f"  n_scored={report['n_scored']}/{report['n_expected']} "
          f"accuracy={report['accuracy']} ece={report['calibration']['ece']}")
    print(f"  report_sha256={rsha} responses_sha256={osha}")
    return outdir, report, rsha, osha


def do_verify_run(args, records, dataset_sha256):
    """重算 runs/<tag> 的数值并与 report.json / manifest 行对账。"""
    outdir = os.path.join(ROOT, "runs", args.tag)
    rj = os.path.join(outdir, "report.json")
    rp = os.path.join(outdir, "responses.jsonl")
    if not os.path.isfile(rj) or not os.path.isfile(rp):
        raise GateError(f"VERIFY: runs/{args.tag}/ missing report.json or responses.jsonl")
    disk_report = json.load(open(rj, encoding="utf-8"))
    resps = _load_responses(rp)
    by_id = {r["id"]: r for r in records}

    print(f"== verify-run {args.tag} ==")
    rows = []
    legacy = any(not r.get("integrity_algo") or r.get("integrity_algo") == LEGACY_ALGO
                 for r in resps)
    sig_state = "LEGACY (r0 unkeyed; no cryptographic assurance)"
    if not legacy:
        try:
            signing.get_secret(create=False)
            bad = [r["question_id"] for r in resps if not signing.matches(r)]
            sig_state = "hmac-sha256 OK" if not bad else f"HMAC MISMATCH on {bad}"
        except signing.SigningError as e:
            sig_state = f"UNVERIFIABLE: {e}"
    rows.append(("signature", sig_state))

    # 行数/id 对账
    exp = [r["id"] for r in records]
    got = [r.get("question_id") for r in resps]
    rows.append(("row count", f"{len(got)} vs dataset {len(exp)} "
                              f"{'OK' if len(got) == len(exp) else 'MISMATCH'}"))
    rows.append(("id set", "OK" if set(got) == set(exp) else
                 f"MISMATCH missing={sorted(set(exp) - set(got))[:5]} "
                 f"extra={sorted(set(got) - set(exp))[:5]}"))

    # 用 responses 重算指标
    responses = [(by_id[r["question_id"]], r) for r in resps if r.get("question_id") in by_id]
    recomputed = score(responses, n_expected=len(records))
    rows.append(("n_scored", f"recomputed {recomputed['n_scored']} vs report "
                             f"{disk_report.get('n_scored')} "
                             f"{'OK' if recomputed['n_scored'] == disk_report.get('n_scored') else 'MISMATCH'}"))
    rec_acc, disk_acc = recomputed["accuracy"], disk_report.get("accuracy")
    rows.append(("accuracy", f"recomputed {rec_acc} vs report {disk_acc} "
                             f"{'OK' if _eq(rec_acc, disk_acc) else 'MISMATCH'}"))
    rec_ece = recomputed["calibration"]["ece"]
    disk_ece = (disk_report.get("calibration") or {}).get("ece")
    rows.append(("ece", f"recomputed {rec_ece} vs report {disk_ece} "
                        f"{'OK' if _eq(rec_ece, disk_ece) else 'MISMATCH'}"))

    # manifest 对账(先查, 好让 report.json 的 sha256 能对 manifest 里的记录)
    mrow = None
    if os.path.isfile(MANIFEST):
        for l in open(MANIFEST, encoding="utf-8"):
            if not l.strip():
                continue
            m = json.loads(l)
            if m.get("run_id") == args.tag:
                mrow = m

    # 文件哈希
    disk_resp_sha = sha256_file(rp)
    claimed_resp_sha = disk_report.get("responses_sha256")
    rows.append(("responses sha256",
                 "not recorded (pre-r1 artifact)" if not claimed_resp_sha else
                 f"{disk_resp_sha[:16]}... vs report {str(claimed_resp_sha)[:16]}... "
                 f"{'OK' if claimed_resp_sha == disk_resp_sha else 'MISMATCH'}"))
    disk_rep_sha = sha256_file(rj)
    claimed_rep_sha = (mrow or {}).get("report_sha256")
    rows.append(("report sha256",
                 "not recorded (pre-r1 artifact)" if not claimed_rep_sha else
                 f"file {disk_rep_sha[:16]}... vs manifest {str(claimed_rep_sha)[:16]}... "
                 f"{'OK' if claimed_rep_sha == disk_rep_sha else 'MISMATCH'}"))

    if mrow is None:
        rows.append(("manifest", "no manifest row for this tag (dry-run or score-only?)"))
    else:
        rows.append(("manifest accuracy", f"{mrow.get('accuracy')} vs recomputed {rec_acc} "
                                          f"{'OK' if _eq(mrow.get('accuracy'), rec_acc) else 'MISMATCH'}"))
        rows.append(("manifest ece", f"{mrow.get('ece')} vs recomputed {rec_ece} "
                                    f"{'OK' if _eq(mrow.get('ece'), rec_ece) else 'MISMATCH'}"))
        rows.append(("manifest n_scored", f"{mrow.get('n_scored')} vs recomputed "
                                         f"{recomputed['n_scored']} "
                                         f"{'OK' if mrow.get('n_scored') == recomputed['n_scored'] else 'MISMATCH'}"))
        for f in ("effort", "timeout_s", "max_tokens", "max_attempts", "temperature",
                  "seed", "run_nonce", "integrity_algo", "signing_key_source",
                  "n_expected", "n_received", "abstentions_valid_task_failure",
                  "oracle", "tie_rule", "n_ties"):
            rows.append((f"manifest.{f}", repr(mrow.get(f))))

    for k, v in rows:
        print(f"  {k:22s} {v}")
    ok = all("MISMATCH" not in v for _k, v in rows)
    print(f"  => {'RECOMPUTE CONSISTENT' if ok else 'INCONSISTENT (see MISMATCH rows)'}"
          f"{' [legacy artifact: metrics recomputed, integrity not cryptographic]' if legacy else ''}")
    return ok


def _eq(a, b):
    if a is None or b is None:
        return a is b
    try:
        return abs(float(a) - float(b)) < 1e-9
    except (TypeError, ValueError):
        return a == b


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", default=os.path.join(ROOT, "data", "smoke-12.jsonl"))
    ap.add_argument("--adapter", choices=list(ADAPTERS))
    ap.add_argument("--model")
    ap.add_argument("--tag")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--effort", default="low")
    ap.add_argument("--timeout", type=float, default=60.0)
    ap.add_argument("--max-tokens", type=int, default=4096)
    ap.add_argument("--max-attempts", type=int, default=2)
    ap.add_argument("--seed", type=int, default=None,
                    help="sent as the API `seed`; recorded in the manifest (null = not sent)")
    ap.add_argument("--empty-state", action="store_true",
                    help="把每题 state 换成 '(no context provided)' 做区分度基线")
    ap.add_argument("--score-only", metavar="RESPONSES_JSONL",
                    help="不调用任何 adapter, 只重验完整性+行数/id 对账+重算指标")
    ap.add_argument("--allow-legacy-unkeyed", action="store_true",
                    help="允许重算 r0 旧产物(公开无钥公式, 不可信); 报告会标注 legacy-unkeyed")
    ap.add_argument("--verify-run", metavar="TAG",
                    help="重算 runs/<tag> 的数值并与 report/manifest 对账(零调用)")
    ap.add_argument("--force", action="store_true",
                    help="允许覆盖已存在的 runs/<tag>/(默认拒绝, 防证据被静默改写)")
    args = ap.parse_args()

    if not args.verify_run:
        if not args.adapter or not args.model or not args.tag:
            ap.error("--adapter/--model/--tag are required (except with --verify-run)")
    if args.verify_run:
        args.tag = args.verify_run

    tmpdir = tempfile.mkdtemp(prefix="dec001-", dir="/tmp")  # 每跑随机前缀, 不锚定路径
    records = load_dataset(args.dataset)
    dataset_sha256 = sha256_file(args.dataset)
    print(f"dataset: {len(records)} questions, sha256 {dataset_sha256[:16]}..., "
          f"tmp prefix {os.path.basename(tmpdir)}")

    if args.verify_run:
        ok = do_verify_run(args, records, dataset_sha256)
        return 0 if ok else 3

    if args.score_only:
        do_score_only(args, records, dataset_sha256, tmpdir)
        return 0

    # 先过 tag 闸: 不让一次会因目录已存在而被拒的运行白烧 API 调用
    guard_tag(args.tag, args.force)

    prices = load_prices()
    run_nonce = secrets.token_hex(16)
    responses = run_dataset(records, args.adapter, args.model, args.dry_run,
                            args.effort, args.timeout, args.empty_state,
                            run_nonce, dataset_sha256, args.max_tokens,
                            args.max_attempts, args.seed)
    recon = {"n_expected": len(records), "n_received": len(responses)}
    if not args.dry_run:
        verify_integrity(responses)
        recon = reconcile(responses, records)
        reconcile_dataset_hash(responses, dataset_sha256)
        for _rec, resp in responses:
            if resp["ok"] and resp["cost_usd"] is None:
                resp["cost_usd"] = price_cost(resp["model"], resp.get("tokens"), prices)
                _resign(resp)
    report = score(responses, n_expected=recon["n_expected"])
    report["run_nonce"] = run_nonce
    report["integrity_assurance"] = "hmac-sha256 (keyed; whole-record coverage)"
    report["dataset_sha256"] = dataset_sha256
    report["run_config"] = {
        "adapter": args.adapter, "model": args.model, "effort": args.effort,
        "timeout_s": args.timeout, "max_tokens": args.max_tokens,
        "max_attempts": args.max_attempts, "seed": args.seed, "temperature": 0,
        "empty_state_baseline": args.empty_state, "dry_run": args.dry_run,
    }
    outdir, rsha, osha = write_outputs(args.tag, responses, report, args.dataset,
                                       args.adapter, args.model,
                                       {"tmp_prefix": os.path.basename(tmpdir),
                                        "run_nonce": run_nonce,
                                        "integrity_algo": "hmac-sha256"})
    if args.dry_run:
        print(f"dry-run done -> {outdir} (manifest not appended)")
        return 0
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    append_manifest({
        "run_id": args.tag, "ts_utc": ts, "driver": DRIVER_VERSION,
        "adapter": args.adapter, "model": args.model,
        "dataset": os.path.relpath(args.dataset, ROOT),
        "dataset_sha256": dataset_sha256,
        # 运行参数(r1: 红道 Blocker 6 要求可复核)
        "effort": args.effort, "timeout_s": args.timeout,
        "max_tokens": args.max_tokens, "max_attempts": args.max_attempts,
        "temperature": 0, "seed": args.seed,
        "empty_state_baseline": args.empty_state,
        "run_nonce": run_nonce,
        "integrity_algo": "hmac-sha256",
        "signing_key_source": signing.secret_source(),
        "n_questions": len(records),
        "n_scored": report["n_scored"],
        "n_expected": report["n_expected"],
        "n_received": report["n_received"],
        "abstentions_valid_task_failure": report["abstentions"]["n_valid_task_failure"],
        "accuracy": report["accuracy"],
        "ece": report["calibration"]["ece"],
        "oracle": report["oracle"]["oracle"],
        "tie_rule": report["oracle"]["tie_rule"],
        "n_ties": report["oracle"]["n_ties"],
        "mean_latency_s": report["latency"]["mean_s"],
        "total_cost_usd": report["cost"]["total_usd"],
        "invalid_infrastructure_n": len(report["failures"]["invalid_infrastructure"]),
        "valid_task_failure_n": len(report["failures"]["valid_task_failure"]),
        "report_dir": os.path.relpath(outdir, ROOT),
        "report_sha256": rsha,
        "responses_sha256": osha,
    })
    print(f"done -> {outdir}")
    print(f"accuracy={report['accuracy']} ece={report['calibration']['ece']} "
          f"n_scored={report['n_scored']}/{report['n_expected']}")
    print(f"verify with: python3 driver.py --verify-run {args.tag} "
          f"--dataset {args.dataset}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except DatasetError as e:
        print(f"DATASET INVALID: {e}", file=sys.stderr)
        sys.exit(1)
    except GateError as e:
        print(f"REFUSED: {e}", file=sys.stderr)
        sys.exit(2)
    except signing.SigningError as e:
        print(f"SIGNING ERROR: {e}", file=sys.stderr)
        sys.exit(4)
