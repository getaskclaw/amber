#!/usr/bin/env python3
"""Step 0 deliverable: profile -> lane -> bench session count map.

Evidence (all read-only):
  * sessions.source  = `amber-lib-<case...>-<lane-token>-<band>` for bench runs
  * sessions.model   = the pinned model id for those runs
  * runs-*/manifest.jsonl session-id join = which result lane a run belongs to

Output: profile-lane-map-W38.md
"""
import glob
import json
import os
import re
import sqlite3
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
PROFDIR = os.path.expanduser("~/.hermes/profiles")
RUNDIR = os.path.expanduser("~/2608/sandbox/amber-run")
OUT = os.path.join(HERE, "profile-lane-map-W38.md")
BENCH_RE = re.compile(r"^amber-lib-(?P<rest>.+)$")

# profile -> published result lane (hand-verified from manifest session-id join
# + each lane's run-identity table). None = no local transcript lane published.
PROFILE_LANE = {
    "amber-gpt": "amber-gpt",
    "amber-gpt-luna": "amber-gpt",
    "amber-gpt-sol": "amber-gpt",
    "amber-ollama-g53f": "amber-ollama",
    "amber-ollama-d4f": "amber-ollama",
    "amber-ollama-d41f": "amber-ollama",
    "amber-oll2-g53f": "amber-ollama",
    "amber-ollama-g53": "amber-ollama (W36 pre-clean-room)",
    "amber-ollama-d4p": "— (deepseek-v4-pro:0813; probe, no 2606 repo)",
    "amber-b": "amber-ollama (glmflash low probe)",
    "amber-crof": "amber-crof",
    "amber-crof-d4fv": "amber-crof",
    "amber-crof-g53f": "amber-crof",
    "amber-crof-q35": "amber-crof",
    "amber-crof-q38": "amber-crof",
    "amber-cc": "amber-commandcode",
    "amber-ocgo": "amber-opencode",
    "amber-ds41": "amber-deepseek",
    "amber-wb": "amber-workbuddy",
    "amber-doubao": "amber-doubao",
    "amber-ollama-kk3": "amber-kimi (k3)",
    "amber-k28": "amber-kimi (kimi-for-coding)",
    "amber-gp27b": "amber-goldenpotato",
    "amber-step5p": "— (step-5-preview; no 2606 results repo)",
    "amber-cline-d4f": "— (cline-pass lane; no 2606 results repo)",
    "amber-cline-g53f": "— (cline-pass lane; no 2606 results repo)",
    "amber-cline-q35": "— (cline-pass lane; no 2606 results repo)",
    "amber-cline-q38": "— (cline-pass lane; no 2606 results repo)",
    "amber-a": "— (early foreman-round1 / r1-r2 probes)",
    "amber-orch-k3": "— (seat-avail001 orchestration probes)",
    "amber-ualpha": "— (union-alpha; refuse-walled probe)",
}


def main():
    rows = []
    for p in sorted(glob.glob(os.path.join(PROFDIR, "amber-*", "state.db"))):
        prof = os.path.basename(os.path.dirname(p))
        c = sqlite3.connect(f"file:{p}?mode=ro", uri=True, timeout=20)
        sess = list(c.execute("SELECT source, model FROM sessions"))
        c.close()
        bench = [(s, m) for s, m in sess if (s or "").startswith("amber-lib-")]
        cases = Counter()
        bands = Counter()
        models = Counter()
        for s, m in bench:
            mm = BENCH_RE.match(s)
            rest = mm.group("rest") if mm else s
            toks = rest.split("-")
            bands[toks[-1] if toks else "?"] += 1
            models[m or "?"] += 1
            # case token = everything up to the lane token; approximate by known ids
            cases[rest.rsplit("-", 2)[0] if rest.count("-") >= 2 else rest] += 1
        rows.append({
            "profile": prof,
            "lane": PROFILE_LANE.get(prof, "?"),
            "sessions": len(sess),
            "bench": len(bench),
            "other": len(sess) - len(bench),
            "models": models.most_common(3),
            "bands": bands.most_common(),
            "cases": len(cases),
        })

    out = ["# AMBER 第 0 步：profile → lane → bench 会话数 映射表（W38）", ""]
    out.append("判据：`sessions.source` 形如 `amber-lib-<案>-<lane>-<band>`；`sessions.model` 为钉住模型。")
    out.append("lane 归属由 `runs-*/manifest.jsonl` 的 session-id 实证 join（见 `lane-registry.json`）与各成绩仓 run-identity 表核对。")
    out.append("")
    out.append("| profile | 对应 lane (2606 成绩仓) | 总会话 | bench 会话 | 非 bench | 模型 | 档位 |")
    out.append("|---|---|---:|---:|---:|---|---|")
    tot_bench = 0
    for r in rows:
        tot_bench += r["bench"]
        md = ", ".join(f"{k}×{v}" for k, v in r["models"])
        bd = ", ".join(f"{k}×{v}" for k, v in r["bands"])
        out.append(f"| {r['profile']} | {r['lane']} | {r['sessions']} | {r['bench']} | "
                   f"{r['other']} | {md} | {bd} |")
    out.append("")
    out.append(f"合计 bench 会话 = **{tot_bench}**（= `hard-facts.jsonl` 行数）")
    out.append("")
    out.append("## 说明")
    out.append("")
    out.append("- 一个 2606 成绩仓可由多个 bench profile 贡献（例如 amber-ollama 由 g53f/d4f/d41f/oll2 四个 profile 拼成，跨 W36/W37）。")
    out.append("- 非 bench 会话 = smoke/probe/quota/test/orchestration 等，不属成绩卷面；已在提取器中按 `source LIKE 'amber-lib-%'` 排除。")
    out.append("- `—` = 有 bench transcript 但 2606 无对应公开成绩仓（cline-pass / step5p / union-alpha / 早 foreman 探针），这些 lane 的成绩真源须另找，归因表按 `no_transcript`/无成绩处理。")
    out.append("- amber-devin 道在外部 host 上跑，local state.db 无 transcript —— 该仓的 ✗ 案在归因表中标 `no_transcript`。")
    out.append("")

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")
    print(f"wrote {OUT}: {len(rows)} profiles")


if __name__ == "__main__":
    main()
