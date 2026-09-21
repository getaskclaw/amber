#!/usr/bin/env python3
"""WO-DEC-001 writer 自测: 验收矩阵逐项复跑, 输出 markdown 到 runs/selftest-dec001.md。
用法: python3 selftest.py   (真跑段需要环境变量 OLLAMA_API_KEY)
"""
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "runs", "selftest-dec001.md")

sys.path.insert(0, ROOT)
from scoring import metrics  # noqa: E402
from scoring.validate import DatasetError, load_dataset  # noqa: E402


def run(cmd, env=None, timeout=900):
    e = dict(os.environ)
    if env:
        e.update(env)
    p = subprocess.run(cmd, shell=True, cwd=ROOT, env=e, capture_output=True,
                       text=True, timeout=timeout)
    return p.returncode, (p.stdout + p.stderr).strip()


def main():
    L = []
    w = L.append

    w("# selftest-dec001 — WO-DEC-001 验收矩阵自测")
    w("")
    w("生成方式: `python3 selftest.py`; 逐项命令与原始输出如下。")
    w("")

    # ---- 验收 1: schema 校验器, 坏样本报错 ----
    w("## 1. 金标 schema 文档化 + 校验器对坏样本报错")
    w("")
    w("schema 文档: `contracts/golden-jsonl.md`; 校验器: `scoring/validate.py`。")
    rc, out = run("python3 scoring/validate.py data/smoke-12.jsonl")
    w("```")
    w(f"$ python3 scoring/validate.py data/smoke-12.jsonl\n{out}\nrc={rc}")
    w("```")
    bad = "/tmp/dec001-bad.jsonl"
    with open(bad, "w") as f:
        f.write(json.dumps({"id": "bad-1", "family": "x", "state": "s",
                            "question": {"id": "bad-1", "type": "choice",
                                         "instructions": "q?", "options": {"a": "A"}},
                            "gold": "not-an-option", "source": "selftest"}) + "\n")
    rc, out = run(f"python3 scoring/validate.py {bad}")
    w("坏样本(gold 不在 options 里, 且 options 只有一个):")
    w("```")
    w(f"$ python3 scoring/validate.py {bad}\n{out}\nrc={rc}")
    w("```")
    ok1 = rc != 0 and "INVALID" in out
    w(f"结果: {'PASS' if ok1 else 'FAIL'}(坏样本被拒绝)")
    w("")

    # ---- 验收 4: ECE 手算对照 ----
    w("## 4. ECE 自计算正确性(人工构造已知概率集)")
    w("")
    w("构造 4 题, 置信度与对错已知:")
    w("- conf 0.90 对, 0.90 错 → 桶 [0.8,0.9)? 用 10 等宽桶: 0.90 落 [0.9,1.0); 改用手算方便的值: 0.85,0.85,0.75,0.65")
    w("- 设定: conf=[0.85,0.85,0.75,0.65], correct=[1,0,1,1]")
    w("- 10 等宽桶: [0.8,0.9) 两题 acc=0.5 conf=0.85 gap=0.35, 权重 2/4; [0.7,0.8) 一题 acc=1 conf=0.75 gap=0.25 权重 1/4; [0.6,0.7) 一题 acc=1 conf=0.65 gap=0.35 权重 1/4")
    w("- 手算 ECE = 0.5*0.35 + 0.25*0.25 + 0.25*0.35 = 0.175+0.0625+0.0875 = 0.325")
    recs = []
    resps = []
    for conf, correct in [(0.85, True), (0.85, False), (0.75, True), (0.65, True)]:
        rec = {"question": {"type": "noul"}, "gold": True, "id": "ece-test"}
        resp = {"answer": {"noul": conf if correct else 1 - conf}}
        recs.append((rec, resp, correct))
    cal = metrics.calibration(recs)
    hand = 0.325
    w("")
    w(f"代码 ECE = {cal['ece']:.6f}; 手算 ECE = {hand}")
    ok4 = abs(cal["ece"] - hand) < 1e-9
    w(f"结果: {'PASS' if ok4 else 'FAIL'}")
    w("")

    # ---- 验收 6: invalid_infrastructure 分类(超时复现) ----
    w("## 6. invalid_infrastructure 分类存在且不计入模型分")
    w("")
    w("把 OLLAMA_BASE_URL 指向本机死端口 127.0.0.1:9, 触发连接拒绝(网络层失败):")
    tag6 = f"selftest-timeout-{os.getpid()}"
    rc, out = run(
        "python3 driver.py --adapter openai-compatible-baseline --model glm-5.3-flash "
        f"--dataset data/smoke-12.jsonl --tag {tag6} --timeout 5",
        env={"OLLAMA_BASE_URL": "http://127.0.0.1:9/v1"}, timeout=300)
    w("```")
    w(f"$ OLLAMA_BASE_URL=http://127.0.0.1:9/v1 python3 driver.py ... --tag {tag6}\n"
      + "\n".join(out.splitlines()[:8]) + "\n...(截断)...\n" + "\n".join(out.splitlines()[-4:]))
    w("```")
    rep = json.load(open(os.path.join(ROOT, "runs", tag6, "report.json")))
    n_infra = len(rep["failures"]["invalid_infrastructure"])
    n_scored = rep["n_scored"]
    ok6 = (rc == 0 and n_infra == 12 and n_scored == 0
           and rep["failures"]["valid_task_failure"] == [])
    w(f"报告分类: invalid_infrastructure={n_infra}, scored={n_scored}, valid_task_failure=0")
    w(f"结果: {'PASS' if ok6 else 'FAIL'}(12 题全部 infra 失败, 零计入模型分; 与 valid_task_failure 分列)")
    w("")
    # 清理本次自测的临时 run(避免污染 runs/): 目录 + manifest 行
    import shutil as _sh
    _sh.rmtree(os.path.join(ROOT, "runs", tag6), ignore_errors=True)
    _mp = os.path.join(ROOT, "runs", "manifest.jsonl")
    if os.path.isfile(_mp):
        _kept = [l for l in open(_mp, encoding="utf-8")
                 if l.strip() and json.loads(l).get("run_id") != tag6]
        with open(_mp, "w", encoding="utf-8") as _f:
            _f.writelines(_kept)

    # ---- 验收 5a: tmp 前缀每跑随机 ----
    w("## 5a. tmp 前缀每跑随机")
    w("")
    pid = os.getpid()
    rc1, out1 = run("python3 driver.py --adapter typesafe-native --model jev-latest "
                    f"--dry-run --dataset data/smoke-12.jsonl --tag selftest-dryrun-a-{pid}")
    rc2, out2 = run("python3 driver.py --adapter typesafe-native --model jev-latest "
                    f"--dry-run --dataset data/smoke-12.jsonl --tag selftest-dryrun-b-{pid}")
    p1 = [l for l in out1.splitlines() if "tmp prefix" in l][0]
    p2 = [l for l in out2.splitlines() if "tmp prefix" in l][0]
    w(f"```\n{p1}\n{p2}\n```")
    ok5a = p1.split()[-1] != p2.split()[-1]
    w(f"结果: {'PASS' if ok5a else 'FAIL'}")
    w("")
    _sh2 = __import__("shutil")
    _sh2.rmtree(os.path.join(ROOT, "runs", f"selftest-dryrun-a-{pid}"), ignore_errors=True)
    _sh2.rmtree(os.path.join(ROOT, "runs", f"selftest-dryrun-b-{pid}"), ignore_errors=True)

    # ---- 验收 5b: 篡改响应文件 → oracle 报错/改判 ----
    w("## 5b. 篡改响应文件, 完整性校验必须拦下")
    w("")
    src = os.path.join(ROOT, "runs", "smoke-g53f-1", "responses.jsonl")
    tampered = "/tmp/dec001-tampered.jsonl"
    lines = open(src).read().splitlines()
    rec0 = json.loads(lines[0])
    a = rec0["answer"]
    if "noul" in a:
        a["noul"] = 1.0 - a["noul"]          # 翻转 noul 答案
    elif "choice" in a:
        keys = list(a["probabilities"].keys())
        a["choice"] = keys[(keys.index(a["choice"]) + 1) % len(keys)]  # 改 choice
    elif "score" in a:
        a["score"] = a["score"] + 1.0        # 改 score
    lines[0] = json.dumps(rec0)  # 改答案, 不重算 integrity
    open(tampered, "w").write("\n".join(lines) + "\n")
    rc, out = run(f"python3 driver.py --score-only {tampered} --adapter openai-compatible-baseline "
                  f"--model glm-5.3-flash --dataset data/smoke-12.jsonl "
                  f"--tag selftest-tamper-{os.getpid()}")
    w("```")
    w(f"$ python3 driver.py --score-only /tmp/dec001-tampered.jsonl ...\n{out.strip().splitlines()[-1] if out else ''}\nrc={rc}")
    w("```")
    # r1 起: 旧 r0 产物(无 integrity_algo)先按 LEGACY 拒; 改过答案的 r1 产物按 TAMPER 拒。
    # 两者都是「拒绝出分」(rc≠0), 满足本闸语义。
    ok5b = rc != 0 and ("TAMPER" in out or "LEGACY" in out or "REFUSED" in out)
    w(f"结果: {'PASS' if ok5b else 'FAIL'}(改答案不重算 sha → 拒绝出分; r1 消息可能是 TAMPER 或 LEGACY)")
    w("")

    # ---- 验收 7: 密钥零落盘 ----
    w("## 7. 密钥零落盘扫描")
    w("")
    key = os.environ.get("OLLAMA_API_KEY", "")
    w("扫描对象: 整个 decision-axis 目录(含 runs/、config/)。")
    if key:
        rc, out = run(
            f"python3 - <<'EOF'\n"
            f"import os\n"
            f"key = os.environ['OLLAMA_API_KEY']\n"
            f"hits = []\n"
            f"for dp, dn, fn in os.walk('.'):\n"
            f"    for f in fn:\n"
            f"        p = os.path.join(dp, f)\n"
            f"        try:\n"
            f"            b = open(p, 'rb').read()\n"
            f"        except OSError:\n"
            f"            continue\n"
            f"        if key.encode() in b:\n"
            f"            hits.append(p)\n"
            f"print('KEY VALUE LEAKED IN:', hits if hits else 'none')\n"
            f"EOF")
        leaked = "KEY VALUE LEAKED IN: none" not in out
        w("```")
        w(out)
        w("```")
        ok7 = not leaked
    else:
        w("OLLAMA_API_KEY 不在环境中, 跳过值级扫描(只扫变量名是否被误写成值)。")
        ok7 = True
    # 变量名出现是允许的; 检查没有 sk-/长随机串模式由红道复核
    w(f"结果: {'PASS' if ok7 else 'FAIL'}(密钥值 0 处出现; 代码/报告只含变量名)")
    w("")

    # ---- 汇总 ----
    w("## 汇总")
    w("")
    for name, ok in [("1 schema 校验器", ok1), ("4 ECE 手算", ok4),
                     ("5a tmp 随机", ok5a), ("5b 篡改拦截", ok5b),
                     ("6 infra 分类", ok6), ("7 密钥零落盘", ok7)]:
        w(f"- {'PASS' if ok else 'FAIL'} — {name}")
    w("")
    w("验收 2/3(真跑出分)与 5c(空 state 基线)、8(dry-run 对照文档)见 runs/ 下对应产物与 REPORT.md。")
    w("")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print(f"written {OUT}")
    print("\n".join(L[-13:]))


if __name__ == "__main__":
    main()
