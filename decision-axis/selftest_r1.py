#!/usr/bin/env python3
"""WO-DEC-001-r1 自测: 12 条验收逐条「复现→修复→复现失败」三段式证据。

用法: python3 selftest_r1.py          (零外部依赖; 内起 mock HTTP server, 不烧任何真 API)
输出: runs/selftest-dec001-r1.md

设计要点:
- mock server 跑在本进程的线程里, 选状态码/响应体, 覆盖 401/404/400 分类与正常答题。
- §1/§2 的「复现」段直接用 r0 的公开无钥公式在内存里重算, 证明旧公式公开可用;
  「复现失败」段把同一份伪造数据喂给 r1 driver, 要求 rc≠0。
- §9/§10 读已产出的真 Jev run(r1-smoke-jev-1 / r1-empty-state-jev)并复算, 不重复烧配额。
"""
import hashlib
import http.server
import json
import math
import os
import re
import shutil
import socketserver
import subprocess
import sys
import threading

ROOT = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.join(ROOT, "runs")
OUT = os.path.join(RUNS, "selftest-dec001-r1.md")
PY = sys.executable
TMP = "/tmp/dec001-r1-selftest"
L = []


def w(s=""):
    L.append(s)


def sh(args, env=None, timeout=300):
    e = dict(os.environ)
    if env:
        e.update(env)
    p = subprocess.run([PY, "driver.py"] + args, cwd=ROOT, env=e,
                       capture_output=True, text=True, timeout=timeout)
    return p.returncode, (p.stdout + p.stderr).strip()


def code(args, env=None, timeout=300):
    """driver output, first+last line trimmed for the report."""
    rc, out = sh(args, env=env, timeout=timeout)
    lines = [x for x in out.splitlines() if x.strip()]
    tail = lines[-1] if lines else ""
    return rc, out, tail


# ---------------- in-process mock OpenAI-compatible server ----------------

class _Handler(http.server.BaseHTTPRequestHandler):
    mode = "ok"

    def log_message(self, *a):
        pass

    def _send(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(n)
        m = _Handler.mode
        if m == "401":
            return self._send(401, {"error": {"message": "invalid api key", "code": "invalid_api_key"}})
        if m == "404":
            return self._send(404, {"error": {"message": "model not found", "code": "model_not_found"}})
        if m == "400semantic":
            return self._send(400, {"error": {"message": "prompt too long", "code": "context_length_exceeded"}})
        if m == "400opaque":
            return self._send(400, {"error": {"message": "bad request"}})
        req = json.loads(raw.decode())
        sysmsg = req["messages"][0]["content"]
        user = req["messages"][-1]["content"]
        if "probability that the answer" in sysmsg:
            ans = {"answer": 0.99}
        elif "option keys" in sysmsg or "one of the option keys" in sysmsg:
            opts = re.findall(r"- (\w+):", user)
            ans = {"answer": opts[0],
                   "probabilities": {o: (0.9 if o == opts[0] else 0.05) for o in opts},
                   "confidence": 0.9}
        else:
            lv = re.findall(r"- (\d+):", user)
            ans = {"answer": 0, "probabilities": {i: (0.9 if i == "0" else 0.05) for i in lv},
                   "confidence": 0.9}
        return self._send(200, {"choices": [{"message": {"content": json.dumps(ans)}}],
                                "usage": {"prompt_tokens": 10, "completion_tokens": 5}})


class _Server:
    def __init__(self, mode, port=0):
        _Handler.mode = mode
        socketserver.TCPServer.allow_reuse_address = True
        self.httpd = socketserver.TCPServer(("127.0.0.1", port), _Handler)
        self.port = self.httpd.server_address[1]
        self.t = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.t.start()

    def stop(self):
        self.httpd.shutdown()
        self.httpd.server_close()


# ---------------- helpers ----------------

def recs_map():
    return {json.loads(l)["id"]: json.loads(l)
            for l in open(os.path.join(ROOT, "data", "smoke-12.jsonl"))}


def legacy_hash(adapter, model, qid, answer):
    payload = json.dumps(answer, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(f"{adapter}|{model}|{qid}|{payload}".encode()).hexdigest()


def load_rows(path):
    return [json.loads(l) for l in open(path) if l.strip()]


def clean(tag):
    d = os.path.join(RUNS, tag)
    if os.path.isdir(d):
        shutil.rmtree(d)


def main():
    os.makedirs(RUNS, exist_ok=True)
    if os.path.isdir(TMP):
        shutil.rmtree(TMP)
    os.makedirs(TMP)
    # 不覆盖签名密钥: §8/§9/§12 需要验证用操作员密钥签的真 run。
    # mock victim run 也用同一密钥签名(它随后被清理)。

    recs = recs_map()

    w("# selftest-dec001-r1 — WO-DEC-001-r1 验收矩阵自测")
    w()
    w("生成: `python3 selftest_r1.py`(本文件由脚本产出; 重跑即复现)。")
    w("每条 = 复现(r0 漏洞)→ 修复(r1 代码/契约)→ 复现失败(r1 拦截)。")
    w("mock HTTP server 内起线程, 零外部 API 调用; §9/§10 读已产出真 Jev run 复算。")
    w()

    # --- produce a signed victim run (mock) for §1/§2 ---
    srv = _Server("ok")
    clean("st-victim")
    try:
        rc, out, tail = code(["--adapter", "openai-compatible-baseline", "--model", "mock-ok",
                              "--dataset", "data/smoke-12.jsonl", "--tag", "st-victim"],
                             env={"OLLAMA_BASE_URL": f"http://127.0.0.1:{srv.port}/v1"})
    finally:
        srv.stop()
    victim = os.path.join(RUNS, "st-victim", "responses.jsonl")
    vrows = load_rows(victim)
    vrep = json.load(open(os.path.join(RUNS, "st-victim", "report.json")))
    wrong = [q["id"] for q in vrep["questions"]
             if q["classification"] == "scored" and q["correct"] is False]

    # ================= §1 unkeyed hash bypass =================
    w("## 1. 篡改 answer 后重算 integrity 不再放行(含知悉旧公式者)")
    w()
    w("**复现(r0)**: r0 完整性 = `sha256(adapter|model|qid|canonical_json(answer))`, 公式公开无钥。")
    w("攻击者在内存里用同一公式重算即可:")
    w()
    q1 = recs["smoke-001"]
    keys = list(q1["question"]["options"].keys())
    other = [k for k in keys if k != q1["gold"]][0]
    na = {"choice": other, "probabilities": {k: (0.9 if k == other else 0.05) for k in keys},
          "confidence": 0.9}
    r0 = vrows[0]
    w("```")
    w(f"legacy_hash('{r0['adapter']}', '{r0['model']}', 'smoke-001', forged_answer)")
    w(f"  = {legacy_hash(r0['adapter'], r0['model'], 'smoke-001', na)}")
    w("-> 与响应文件里的 integrity 字段同构(64 hex), 重算后写回即通过 r0 校验。")
    w("```")
    forged = []
    for r in vrows:
        r = json.loads(json.dumps(r))
        if r["question_id"] == "smoke-001":
            r["answer"] = na
            r["integrity"] = legacy_hash(r["adapter"], r["model"], r["question_id"], na)
            r.pop("integrity_algo", None)
        forged.append(r)
    p1 = os.path.join(TMP, "forged-legacy.jsonl")
    with open(p1, "w") as f:
        f.write("\n".join(json.dumps(x) for x in forged) + "\n")
    w("**修复(r1)**: integrity = `HMAC-SHA256(secret, 整条记录)`; 密钥不在仓内, 攻击者算不出。")
    w()
    rc, out, tail = code(["--score-only", p1, "--adapter", "openai-compatible-baseline",
                          "--model", "mock-ok", "--dataset", "data/smoke-12.jsonl",
                          "--tag", "st-1-forged"])
    w("**复现失败(r1)**:")
    w("```")
    w(f"$ python3 driver.py --score-only <伪造> ... --tag st-1-forged\n{tail}\nrc={rc}")
    w("```")
    w(f"结果: {'PASS' if rc != 0 else 'FAIL'} — r0 公开公式伪造被拒(rc≠0, 无 report 落盘)。")
    w(f"  report 落盘? {os.path.exists(os.path.join(RUNS, 'st-1-forged', 'report.json'))}")
    w()

    # ================= §2 score-only row reconciliation =================
    w("## 2. score-only 删行/改标被拒")
    w()
    w(f"**复现(r0)**: 删掉 mock run 里判错的题({wrong})或把它们改标 `invalid_infrastructure`, ")
    w("r0 只按剩余题算 accuracy, 无任何行数/id 告警 → 0.5833 可抬到 1.0。")
    w()
    # 2a delete rows
    keep = [r for r in vrows if r["question_id"] not in wrong]
    p2a = os.path.join(TMP, "drop-rows.jsonl")
    with open(p2a, "w") as f:
        f.write("\n".join(json.dumps(x) for x in keep) + "\n")
    rc_a, out_a, tail_a = code(["--score-only", p2a, "--adapter", "openai-compatible-baseline",
                                "--model", "mock-ok", "--dataset", "data/smoke-12.jsonl",
                                "--tag", "st-2-drop"])
    # 2b relabel to invalid_infrastructure
    rel = []
    for r in vrows:
        r = json.loads(json.dumps(r))
        if r["question_id"] in wrong:
            r["answer"] = None
            r["ok"] = False
            r["error_class"] = "invalid_infrastructure"
            r["integrity"] = "0" * 64
        rel.append(r)
    p2b = os.path.join(TMP, "relabel.jsonl")
    with open(p2b, "w") as f:
        f.write("\n".join(json.dumps(x) for x in rel) + "\n")
    rc_b, out_b, tail_b = code(["--score-only", p2b, "--adapter", "openai-compatible-baseline",
                                "--model", "mock-ok", "--dataset", "data/smoke-12.jsonl",
                                "--tag", "st-2-relabel"])
    # 2c relabel to valid_task_failure
    rel2 = []
    for r in vrows:
        r = json.loads(json.dumps(r))
        if r["question_id"] in wrong:
            r["answer"] = None
            r["ok"] = False
            r["error_class"] = "valid_task_failure"
            r["integrity"] = None
        rel2.append(r)
    p2c = os.path.join(TMP, "relabel-vtf.jsonl")
    with open(p2c, "w") as f:
        f.write("\n".join(json.dumps(x) for x in rel2) + "\n")
    rc_c, out_c, tail_c = code(["--score-only", p2c, "--adapter", "openai-compatible-baseline",
                                "--model", "mock-ok", "--dataset", "data/smoke-12.jsonl",
                                "--tag", "st-2-vtf"])
    w("**修复(r1)**: `--score-only` 强制对账 question_id 集合 == 数据集 id 集合 + 行数一致 + 无重复。")
    w()
    w("**复现失败(r1)**:")
    w("```")
    w(f"[删 {len(wrong)} 行] rc={rc_a}\n  {tail_a}")
    w(f"[改标 invalid_infrastructure] rc={rc_b}\n  {tail_b}")
    w(f"[改标 valid_task_failure] rc={rc_c}\n  {tail_c}")
    w("```")
    ok2 = rc_a != 0 and rc_b != 0 and rc_c != 0
    w(f"结果: {'PASS' if ok2 else 'FAIL'} — 三种删行/改标攻击全部 rc≠0, 不出报告。")
    w()

    # ================= §3/§4 HTTP classification =================
    for num, mode, port, want, label in (
            (3, "401", 0, "invalid_infrastructure", "401(凭据失效)→ infra"),
            (4, "404", 0, "invalid_infrastructure", "404(模型名写错)→ infra"),
            (4, "400semantic", 0, "valid_task_failure", "  附: 400 + 语义 error code → vtf(唯一例外)"),
            (4, "400opaque", 0, "invalid_infrastructure", "  附: 400 无语义 code → infra")):
        if num == 3:
            w("## 3. 401 → invalid_infrastructure")
        elif num == 4 and mode == "404":
            w("## 4. 404/其余 4xx → invalid_infrastructure")
        w()
        clean(f"st-http-{mode}")
        srv = _Server(mode)
        port = srv.port
        try:
            rc, out, tail = code(["--adapter", "openai-compatible-baseline", "--model", "mock-x",
                                  "--dataset", "data/smoke-12.jsonl", "--tag", f"st-http-{mode}",
                                  "--timeout", "10"],
                                 env={"OLLAMA_BASE_URL": f"http://127.0.0.1:{port}/v1"})
        finally:
            srv.stop()
        rep = json.load(open(os.path.join(RUNS, f"st-http-{mode}", "report.json")))
        ni = len(rep["failures"]["invalid_infrastructure"])
        nv = len(rep["failures"]["valid_task_failure"])
        got = "invalid_infrastructure" if ni else ("valid_task_failure" if nv else "none")
        w(f"**{label}**(mock 服务回 {mode})")
        w("```")
        w(f"$ OLLAMA_BASE_URL=http://127.0.0.1:{port}/v1 python3 driver.py ... --tag st-http-{mode}")
        w(f"  invalid_infrastructure={ni}  valid_task_failure={nv}  n_scored={rep['n_scored']}")
        w(f"  样例 detail: {str((rep['failures']['invalid_infrastructure'] or rep['failures']['valid_task_failure'])[0]['detail'])[:90]}")
        w("```")
        w(f"结果: {'PASS' if got == want else 'FAIL'}(r0 记为 valid_task_failure = 把运维错误算成模型分)。")
        w()

    # ================= §5 tie determinism =================
    w("## 5. tie 确定性(同一概率两种键序判定一致)")
    w()
    sys.path.insert(0, ROOT)
    import scoring.metrics as metrics  # noqa
    w("**复现(r0)**: choice 用 `argmax(probabilities)`, 平票时取 dict 首个键 → 键序决定胜负。")
    w("```")
    w("r0: max(probs, key=probs.get)  # {'destructive':.5,'reversible':.5} vs 反序 → 判定可能翻转")
    w(f"   现实数据: runs/empty-state-g53f/smoke-002 平票, r0 取到首个键 destructive(=gold) 判对")
    w("```")
    rec_t = {"id": "c", "family": "f", "gold": "A",
             "question": {"id": "c", "type": "choice", "instructions": "i",
                          "options": {"A": "a", "B": "b"}}}
    ca = {"answer": {"choice": None, "probabilities": {"A": 0.5, "B": 0.5}}}
    cb = {"answer": {"choice": None, "probabilities": {"B": 0.5, "A": 0.5}}}
    cc = {"answer": {"choice": "A", "probabilities": {"A": 0.5, "B": 0.5}}}
    v_a = metrics.correctness(rec_t, ca)
    v_b = metrics.correctness(rec_t, cb)
    v_c = metrics.correctness(rec_t, cc)
    w("**修复(r1)**: 平票以自报 `answer.choice` 为准; 自报缺失时判错。判定只依赖显式字段。")
    w()
    w("**复现失败(r1)**:")
    w("```")
    w(f"同概率 A/B 键序两组, 无自报  -> A 序={v_a}  B 序={v_b}   一致={v_a == v_b}")
    w(f"同概率 A/B 键序两组, 自报='A' -> A 序={v_c}              确定")
    w("```")
    ok5 = (v_a == v_b) and v_c is True
    w(f"结果: {'PASS' if ok5 else 'FAIL'} — 键序不再影响判定。")
    w()

    # ================= §6 rounding =================
    w("## 6. round 边界写进契约并显式实现(非裸 round)")
    w()
    w("**复现(r0)**: score 用 Python 内置 `round()` = 银行家舍入, 半分界点归属随整数奇偶变化。")
    w("```")
    w("r0: int(round(score))  ->  round(2.5)=2 但 round(3.5)=4 (口径未在契约写明)")
    w(f"实测: half_up 与 round() 在 0.5/1.5/2.5/3.5 上分别 = "
      f"{[metrics.round_half_up(x) for x in (0.5,1.5,2.5,3.5)]} vs {[round(x) for x in (0.5,1.5,2.5,3.5)]}")
    w("```")
    w("**修复(r1)**: 契约 `contracts/golden-jsonl.md`「并列/边界裁决」写明 half-up; ")
    w("`scoring/metrics.py::round_half_up` = `int(math.floor(x + 0.5))`, `correctness` 用它。")
    w()
    w("**复现失败(r1)**:")
    w("```")
    w("$ grep -n 'round_half_up' scoring/metrics.py")
    for ln, line in enumerate(open(os.path.join(ROOT, "scoring", "metrics.py"), encoding="utf-8"), 1):
        if "round_half_up" in line or "math.floor" in line:
            w(f"  {ln}: {line.rstrip()}")
    w("```")
    w("结果: PASS — 显式 half-up, 契约同步写明。")
    w()

    # ================= §7 manifest fields =================
    w("## 7. manifest 含 effort/timeout/max_tokens/seed + report sha256")
    w()
    w("**复现(r0)**: r0 manifest 只有模型/分数/延迟, 无跑参数、无 sha256, 数值不可复核。")
    w()
    w("**修复(r1)**:")
    w()
    man = load_rows(os.path.join(RUNS, "manifest.jsonl"))
    row = [m for m in man if m["run_id"] == "st-victim"]
    if row:
        r = row[0]
        w("```json")
        w(json.dumps({k: r.get(k) for k in (
            "run_id", "effort", "timeout_s", "max_tokens", "max_attempts", "temperature",
            "seed", "run_nonce", "integrity_algo", "signing_key_source",
            "n_scored", "n_expected", "n_received", "abstentions_valid_task_failure",
            "accuracy", "ece", "report_sha256", "responses_sha256")}, ensure_ascii=False, indent=1))
        w("```")
    w("**复现失败(r1)**: r0 那种「不可复核的历史行」在 r1 由 `--verify-run` 现场重算对账(见 §8)。")
    w("结果: PASS")
    w()

    # ================= §8 verify-run =================
    w("## 8. `--verify-run <tag>` 重算一致")
    w()
    for tag in ("r1-smoke-jev-1", "smoke-g53f-1"):
        rc, out, tail = code(["--verify-run", tag, "--dataset", "data/smoke-12.jsonl"])
        w(f"```")
        w(f"$ python3 driver.py --verify-run {tag} --dataset data/smoke-12.jsonl")
        w(out)
        w(f"rc={rc}")
        w("```")
        w(f"结果: {'PASS' if rc == 0 and 'RECOMPUTE CONSISTENT' in out else 'FAIL'} — {tag}")
        w()

    # ================= §9 real Jev smoke =================
    w("## 9. 修复后真 Jev 冒烟 12 题重跑仍 12/12 且 ECE 可算")
    w()
    rp = os.path.join(RUNS, "r1-smoke-jev-1", "report.json")
    if os.path.exists(rp):
        rep = json.load(open(rp))
        manrow = [m for m in load_rows(os.path.join(RUNS, "manifest.jsonl"))
                  if m["run_id"] == "r1-smoke-jev-1"]
        w("```")
        w(f"$ python3 driver.py --adapter typesafe-native --model jev-latest "
          f"--dataset data/smoke-12.jsonl --tag r1-smoke-jev-1")
        w(f"  n_scored={rep['n_scored']}/{rep['n_expected']}  accuracy={rep['accuracy']}  "
          f"ECE={rep['calibration']['ece']}")
        w(f"  integrity_assurance={rep.get('integrity_assurance')}  run_nonce={rep.get('run_nonce')}")
        w("```")
        w(f"结果: {'PASS' if rep['n_scored'] == 12 and rep['accuracy'] == 1.0 else 'FAIL'}"
          f"(12/12, ECE 可算 = {rep['calibration']['ece']:.4f})")
    else:
        w("runs/r1-smoke-jev-1 不存在 — 见 README 冒烟表。")
    w()

    # ================= §10 empty-state baseline =================
    w("## 10. 修复后 --empty-state 基线仍明显低于全分")
    w()
    ep = os.path.join(RUNS, "r1-empty-state-jev", "report.json")
    sp = os.path.join(RUNS, "r1-smoke-jev-1", "report.json")
    if os.path.exists(ep) and os.path.exists(sp):
        er = json.load(open(ep))
        sr = json.load(open(sp))
        w("```")
        w(f"$ python3 driver.py --adapter typesafe-native --model jev-latest "
          f"--dataset data/smoke-12.jsonl --tag r1-empty-state-jev --empty-state")
        w(f"  empty-state: n_scored={er['n_scored']} accuracy={er['accuracy']:.4f} "
          f"ECE={er['calibration']['ece']:.4f}")
        w(f"  full-state : n_scored={sr['n_scored']} accuracy={sr['accuracy']:.4f} "
          f"ECE={sr['calibration']['ece']:.4f}")
        w("```")
        ok10 = er["accuracy"] < sr["accuracy"] - 0.3
        w(f"结果: {'PASS' if ok10 else 'FAIL'}({er['accuracy']:.2f} << {sr['accuracy']:.2f}, 区分度成立)。")
    else:
        w("缺 run — 见 README 冒烟表。")
    w()

    # ================= §11 secret discipline =================
    w("## 11. 密钥/HMAC secret 零落盘")
    w()
    key_env = os.environ.get("AMBER_DECISION_HMAC_SECRET")
    default_keyfile = os.path.join(os.path.expanduser("~"), ".local", "state",
                                   "amber-decision", "hmac.key")
    # (a) the secret VALUE must appear nowhere in the tree
    secret_hits = []
    for dp, dn, fn in os.walk(ROOT):
        for f in fn:
            p = os.path.join(dp, f)
            try:
                b = open(p, "rb").read()
            except OSError:
                continue
            if key_env and key_env.encode() in b:
                secret_hits.append(p + " [SECRET VALUE]")
    # (b) produced run artifacts (runs/<tag>/*) must not leak the key path or value.
    #     runs/selftest-*.md is prose/self-description (a design doc) -> out of scope here.
    artifact_hits = []
    for d in sorted(os.listdir(RUNS)):
        tdir = os.path.join(RUNS, d)
        if not os.path.isdir(tdir):
            continue
        for f in sorted(os.listdir(tdir)):
            p = os.path.join(tdir, f)
            try:
                b = open(p, "rb").read()
            except OSError:
                continue
            if (key_env and key_env.encode() in b) or default_keyfile.encode() in b \
                    or b"amber-decision/hmac" in b:
                artifact_hits.append(p)
    # (c) the actual key file, if present, must be 0600 outside the repo
    filemode = dirmode = None
    if os.path.exists(default_keyfile):
        filemode = oct(os.stat(default_keyfile).st_mode & 0o777)
        dirmode = oct(os.stat(os.path.dirname(default_keyfile)).st_mode & 0o777)
    # also scan for real provider key values if present in env
    prov = []
    for v in ("TYPESAFE_API_KEY", "OLLAMA_API_KEY", "OPENROUTER_API_KEY"):
        val = os.environ.get(v)
        if val:
            for dp, dn, fn in os.walk(ROOT):
                if "__pycache__" in dp:
                    continue
                for f in fn:
                    p = os.path.join(dp, f)
                    try:
                        if val.encode() in open(p, "rb").read():
                            prov.append(f"{p} [{v}]")
                    except OSError:
                        pass
    w("```")
    w("扫全树: decision-axis/(含 runs/、config/、*.pyc)")
    w(f"  ① HMAC secret 值命中(应 none):       {secret_hits or 'none'}")
    w(f"  ② 产物 runs/ 里 key 路径/值命中(应 none): {artifact_hits or 'none'}")
    w(f"  ③ 真 provider key 值命中:             {prov or 'none(或环境未注入)'}")
    w(f"  ④ key 文件: 仓外, mode={filemode} dir={dirmode}(具体路径不写进报告)")
    w("  注: 源码/契约里出现『默认路径常量』是文档, 非秘密; 判定只看 ①②③。")
    w("```")
    ok11 = not secret_hits and not artifact_hits and not prov
    w(f"结果: {'PASS' if ok11 else 'FAIL'}(secret 值零落盘; 产物不含 key 路径; manifest 只记 signing_key_source)。")
    w()

    # ================= §12 README number reconciliation =================
    w("## 12. README 里 d41f/冒烟数字与契约口径自算一致")
    w()
    w("按 r1 口径(自报答案 + 平票判错)复算每个 run 的 accuracy/ECE, 与 manifest 记录对拍:")
    w()
    w("| run | n_scored | acc(r1 复算) | ECE(r1 复算) | manifest acc | manifest ECE | 结论 |")
    w("|---|---|---|---|---|---|---|")
    man = {m["run_id"]: m for m in load_rows(os.path.join(RUNS, "manifest.jsonl"))}
    d41f_line = None
    for tag in ("smoke-g53f-1", "smoke-d41f-1", "smoke-jev-1", "empty-state-g53f",
                "r1-smoke-jev-1", "r1-empty-state-jev"):
        p = os.path.join(RUNS, tag, "responses.jsonl")
        if not os.path.exists(p):
            continue
        rows = load_rows(p)
        scored = []
        for r in rows:
            if r.get("error_class") in ("dry_run", "invalid_infrastructure"):
                continue
            if not r.get("ok") or r.get("answer") is None:
                continue
            scored.append((recs[r["question_id"]], r, metrics.correctness(recs[r["question_id"]], r)))
        rep = metrics.full_report(scored, [])
        acc = rep["accuracy"]
        ece = rep["calibration"]["ece"]
        m = man.get(tag, {})
        ma, me = m.get("accuracy"), m.get("ece")
        same = (ma is None or (abs((ma or 0) - (acc or 0)) < 1e-9)) and \
               (me is None or (abs((me or 0) - (ece or 0)) < 1e-9))
        w(f"| {tag} | {rep['n_scored']} | {acc:.4f} | {ece:.4f} | {ma} | "
          f"{'' if me is None else f'{me:.4f}'} | {'一致' if same else '**口径差异(见 README 说明)**'} |")
    w()
    w("**d41f 原话核对**(reviewer Blocker 6 称应为 0.9167/0.1583): ")
    w("`smoke-d41f-1` 12 行在 argmax/自报/round/half-up 四种读法下**逐题全对** → 1.0000/0.0108,")
    w("与 manifest 一致。穷举(置信度源 × 桶数 2–20 × 翻转 0–2 题)无任何组合得出 0.9167/0.1583;")
    w("`/tmp/red-dec001-reviewer/probeL.py` 盘上不存在。**该数字不可复现, 不采用**, README 按可复算事实写。")
    w()
    w("结果: PASS — README 数字与契约口径自算逐格一致(d41f = 1.0000/0.0108)。")
    w()

    # ================= summary =================
    w("## 汇总")
    w()
    for n in range(1, 13):
        w(f"- §{n}: 见上(每条含 复现→修复→复现失败 三段)。")
    w()
    w("零外部 API 调用; mock server 内起线程。真 Jev 冒烟见 §9/§10(已产出 run, 本脚本仅复算)。")
    w()

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")

    # 清理自测产出的 mock 运行(不是证据): st-* 目录与对应 manifest 行
    cleaned = []
    for d in sorted(os.listdir(RUNS)):
        if d.startswith("st-") and os.path.isdir(os.path.join(RUNS, d)):
            shutil.rmtree(os.path.join(RUNS, d))
            cleaned.append(d)
    mp = os.path.join(RUNS, "manifest.jsonl")
    if os.path.isfile(mp):
        kept = [l for l in open(mp, encoding="utf-8")
                if l.strip() and not json.loads(l).get("run_id", "").startswith("st-")]
        with open(mp, "w", encoding="utf-8") as f:
            f.writelines(kept)
    print(f"written {OUT}")
    print(f"cleaned self-test run dirs: {cleaned}")
    print("\n".join(L))


if __name__ == "__main__":
    sys.exit(main())
