#!/usr/bin/env python3
"""AMBER 挂案归因表 builder (W38) — hard-fact layer, rule-based, no LLM.

Inputs (all read-only / already-extracted):
  * hard-facts.jsonl                      — per bench session hard facts
  * lane-registry.json                    — profile -> lane token -> model
  * <repo>/results/*.md full matrices     — ✗ cells (the fail list)

Output: attribution-W38.md  (public aliases only; internal case ids never emitted)

Attribution layers:
  A. endpoint/tooling causes (invalid causes first): timeout, billing_exhausted
  B. capability-adjacent signals: tool_failure, test_modified
Plus a completion-claim consistency column (declared vs published ✗).

Honesty rules: a ✗ cell with no hard-fact signal is labelled `unknown`, never
force-fitted. Cells with no discoverable transcript are labelled `no_transcript`.
"""
import glob
import json
import os
import re
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
FACTS = os.path.join(HERE, "hard-facts.jsonl")
REG = os.path.join(HERE, "lane-registry.json")
RES = os.path.expanduser("~/2606")
RUNDIR = os.path.expanduser("~/2608/sandbox/amber-run")
OUT = os.path.join(HERE, "attribution-W38.md")

ALIAS_RE = re.compile(r"A-[0-9a-f]{8}")
KNOWN_FACES = {"req-drift", "text", "ops", "build", "review", "verify", "vision",
               "ui-build", "convergence", "delivery", "orchestration"}

# ---- repo -> contributing bench profiles (evidence: manifest session-id join,
#      see build_lane_registry.py / run->profile map) ----
REPO_PROFILES = {
    "amber-gpt": ["amber-gpt", "amber-gpt-luna", "amber-gpt-sol"],
    "amber-ollama": ["amber-ollama-g53f", "amber-ollama-d4f", "amber-ollama-d41f",
                     "amber-oll2-g53f", "amber-b", "amber-ollama-g53"],
    "amber-crof": ["amber-crof", "amber-crof-d4fv", "amber-crof-g53f",
                   "amber-crof-q35", "amber-crof-q38"],
    "amber-commandcode": ["amber-cc"],
    "amber-opencode": ["amber-ocgo"],
    "amber-deepseek": ["amber-ds41"],
    "amber-workbuddy": ["amber-wb"],
    "amber-devin": [],                      # bench ran on external Devin host — no local transcript
    "amber-doubao": ["amber-doubao"],
    "amber-kimi": ["amber-ollama-kk3", "amber-k28"],
    "amber-goldenpotato": ["amber-gp27b"],
}

# published run-identity, transcribed from each repo's results md
REPO_META = {
    "amber-gpt": ("gpt-6-astra-900k / gpt-5.6-luna-900k / gpt-5.6-sol-900k", "OpenAI codex lane", "low/medium/high/xhigh/max"),
    "amber-ollama": ("glm-5.3-flash / deepseek-v4-flash:0731", "Ollama Cloud", "high"),
    "amber-crof": ("qwen3.8-27b / qwen3.5-9b / glm-5.3-flash / deepseek-v4-flash-0731 / deepseek-v4-flash-vision-exp", "CrofAI", "high"),
    "amber-commandcode": ("deepseek-v4.1-flash", "CommandCode", "high"),
    "amber-opencode": ("deepseek-flash", "OpenCode Go", "high"),
    "amber-deepseek": ("deepseek-flash / deepseek-v4.1-flash-exp", "DeepSeek official", "high"),
    "amber-workbuddy": ("hy4-preview-f / deepseek-v4.1-flash / hy3", "WorkBuddy ACP", "high"),
    "amber-devin": ("swe-2-max/high/medium / swe-1-7-medium / glm-5-2", "Devin (external host)", "uid-suffix"),
    "amber-doubao": ("doubao-seed-evolving", "Volcengine Ark Agent Plan", "high"),
    "amber-kimi": ("k3 / kimi-for-coding", "Kimi coding endpoint", "high"),
    "amber-goldenpotato": ("Qwen3.8-27B", "goldenpotato community endpoint", "high"),
}


def load_facts():
    recs = []
    with open(FACTS, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                recs.append(json.loads(line))
    return recs


def parse_matrices(path):
    """Return [(section, header_cells, row_cells)]. Only full-matrix blocks."""
    lines = open(path, errors="replace").read().splitlines()
    section = ""
    out = []
    pending_header = None
    for line in lines:
        if line.startswith("## "):
            section = line[3:].strip()
        s = line.strip()
        if not s.startswith("|"):
            pending_header = None
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if not cells:
            continue
        if set("".join(cells)) <= set("-: "):     # separator row
            continue
        if cells[0] in ("case", "案号") or ALIAS_RE.fullmatch(cells[0]):
            if ALIAS_RE.fullmatch(cells[0]):
                out.append((section, pending_header, cells))
            else:
                pending_header = cells
        else:
            pending_header = cells
    return out


# ---- column label -> fact filter. A column is either a lane code (d4f, g53f,
#      q35, q38, k3, wb-model) or a band (low/medium/high/xhigh/max), or a
#      whole-lane name. We filter the candidate facts by band_token / lane_token
#      so a ✗ cell is attributed to the right sessions, not pooled. ----
BAND_WORDS = ("low", "medium", "high", "xhigh", "max", "none")
# abbreviated band tokens used in published headers (e.g. "sol h", "luna xh")
BAND_ABBR = {"m": "medium", "h": "high", "xh": "xhigh", "l": "low",
             "med": "medium", "max": "max"}
# model-name hints used in published headers (gpt repo)
MODEL_HINTS = ("luna", "sol", "astra", "terra", "spark", "gpt56")
LANE_CODE_RE = {
    "d4f": "d4f", "d4fv": "d4fv", "d4p": "d4p", "g53f": "g53f", "g53": "g53",
    "q35": "q35", "q38": "q38", "k3": "kk3", "kk3": "kk3", "k28": "k28",
    "hy3": "hy3", "hy4": "hy4", "wb": "workbuddy",
}


def resolve_filter(col):
    """Return (bands:set|None, lane_substr:str|None, model_hint:str|None)."""
    c = col.lower().replace("*", "").strip()
    bands = {b for b in BAND_WORDS if re.search(rf"\b{b}\b", c)}
    for tok in re.findall(r"[a-z]+", c):
        if tok in BAND_ABBR:
            bands.add(BAND_ABBR[tok])
    lane = None
    for code, t in LANE_CODE_RE.items():
        if re.search(rf"\b{re.escape(code)}\b", c):
            lane = t
            break
    model = None
    for h in MODEL_HINTS:
        if h in c:
            model = h
            break
    return (bands or None, lane, model)


# ---- some result repos print CROSS-VENDOR reference columns (e.g. amber-deepseek
#      reprints crof/ollama cells). Those cells have no local transcript — mark
#      them `ref_column` and attach nothing rather than mis-crediting our own
#      lane's sessions to another vendor's row. ----
FOREIGN_MARKERS = {
    "amber-commandcode": ["opencode", "官方", "crof", "ollama"],
    "amber-opencode": ["commandcode", "官方"],
    "amber-deepseek": ["crof", "ollama"],
    "amber-workbuddy": ["官方", "对照"],
    "amber-kimi": [],
    "amber-ollama": ["crof"],
    "amber-crof": ["ollama", "官方"],
}


def is_ref_column(repo, col):
    c = col.lower()
    return any(m in c for m in FOREIGN_MARKERS.get(repo, []))


# ---- files whose matrix headers carry no model hint but were run on one model
#      (e.g. amber-gpt W36 = the five-band astra sweep). Without this the band
#      columns would pool luna/sol/astra high runs together. ----
FILE_MODEL_DEFAULT = {
    ("amber-gpt", "2026-W36.md"): "astra",
}


def pick_facts(by_alias_prof, alias, profs, col, repo=None, fn=None):
    """Facts for this alias restricted to the given repo profiles, then by the
    column's band/lane/model hint. Returns (facts, exactness) where exactness is
    'column' (hint matched), 'profile' (profile-only), or 'none'."""
    bands, lane, model = resolve_filter(col)
    if model is None and repo and fn:
        model = FILE_MODEL_DEFAULT.get((repo, fn))
    pool = []
    for p in profs:
        pool += by_alias_prof.get((alias, p), [])
    if not pool:
        return [], "none"
    f = pool
    if bands:
        fb = [r for r in f if (r.get("band_token") or "").lower() in bands]
        if fb:
            f = fb
    if lane:
        fl2 = [r for r in f if lane in (r.get("lane_token") or "").lower()
               or lane in (r.get("source") or "").lower()]
        if fl2:
            f = fl2
    if model:
        fm = [r for r in f if model in (r.get("model") or "").lower()
              or model in (r.get("source") or "").lower()]
        if fm:
            f = fm
    # generic fallback: match model-id-looking tokens from the column against
    # each fact's model/source (handles whole-lane columns like "glm-5.3-flash",
    # "deepseek-v4.1-flash", "v4.1-flash-exp（官方，W37）").
    if f is pool:
        toks = [t for t in re.findall(r"[a-z][a-z0-9]*(?:[.-][a-z0-9]+)+", col.lower())
                if len(t) >= 4 and t not in BAND_WORDS]
        if toks:
            def score(r):
                blob = ((r.get("model") or "") + " " + (r.get("source") or "")).lower()
                return sum(1 for t in toks if t in blob)
            scored = [(score(r), r) for r in pool]
            best = max(s for s, _ in scored)
            if best > 0:
                f = [r for s, r in scored if s == best]
    exact = "column" if f is not pool else "profile"
    return f, exact


def load_manifest_stats():
    """Aggregate run terminal states per result repo (for the endpoint-vs-capability split)."""
    run_terminals = defaultdict(Counter)
    run_invalid_cause = defaultdict(Counter)
    for mf in sorted(glob.glob(os.path.join(RUNDIR, "runs-*", "manifest.jsonl"))):
        run = os.path.basename(os.path.dirname(mf))
        for line in open(mf, errors="replace"):
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except Exception:
                continue
            t = d.get("terminal") or "unknown"
            run_terminals[run][t] += 1
            if t == "invalid_infrastructure":
                err = str(d.get("err_tail") or "")
                cause = "harness_timeout" if ("timeout" in err.lower() or d.get("rc") == 124) \
                    else ("infrastructure_missing" if ("unknown option" in err or "budget" in err)
                          else "other")
                run_invalid_cause[run][cause] += 1
    repo_runs = defaultdict(list)
    prof2repo = {}
    for repo, profs in REPO_PROFILES.items():
        for p in profs:
            prof2repo[p] = repo
    reg = json.load(open(REG, encoding="utf-8")) if os.path.exists(REG) else {"runs": {}}
    for run, info in reg.get("runs", {}).items():
        for prof in info.get("profiles", {}):
            r = prof2repo.get(prof)
            if r and run not in repo_runs[r]:
                repo_runs[r].append(run)
    return run_terminals, run_invalid_cause, repo_runs


def main():
    facts = load_facts()
    by_alias_prof = defaultdict(list)
    for r in facts:
        if r.get("case_alias"):
            by_alias_prof[(r["case_alias"], r["profile"])].append(r)

    RUN_TERMINALS, RUN_INVALID_CAUSE, REPO_RUNS = load_manifest_stats()
    TOTAL = Counter()
    for run, c in RUN_TERMINALS.items():
        for t, n in c.items():
            TOTAL[t] += n

    # ---- collect fail cells from all repos ----
    fail_rows = []
    seen = set()
    for path in sorted(glob.glob(os.path.join(RES, "amber-*", "results", "*.md"))):
        repo = os.path.basename(os.path.dirname(os.path.dirname(path)))
        fn = os.path.basename(path)
        for section, header, cells in parse_matrices(path):
            alias = cells[0]
            face = cells[1] if cells[1] in KNOWN_FACES else "?"
            for i, cell in enumerate(cells[2:], start=2):
                if "✗" not in cell:
                    continue
                col = header[i] if header and i < len(header) else f"col{i}"
                key = (repo, fn, section, alias, col)
                if key in seen:
                    continue
                seen.add(key)
                fail_rows.append({
                    "repo": repo, "file": fn, "section": section,
                    "alias": alias, "face": face, "col": col, "cell": cell,
                    "wall": "∅" in cell,
                })

    # ---- attach facts via explicit repo->profile map ----
    labels = Counter()
    inconsistency = {"ran_verify_oracle_fail": 0, "no_or_unverified_claim": 0,
                     "claimed_and_published_fail": 0}
    rows_rendered = 0

    by_repo = defaultdict(list)
    for fr in fail_rows:
        by_repo[fr["repo"]].append(fr)

    out = ["# AMBER 挂案归因表 — W38（硬事实层 v0.1）", ""]
    out.append("生成器: `failure-taxonomy/build_attribution.py` + `extract_hard_facts.py`（纯规则，无 LLM）。")
    out.append("数据源: 各 `amber-<lane>/results/*.md` 的 full matrix（挂案真源）+ bench session transcript 硬事实。")
    out.append("join: repo → bench profile 映射由 manifest session-id 实证（见 `lane-registry.json`）；")
    out.append("标签按「该 lane 该案的所有 transcript 会话」聚合，一行可多标签。")
    out.append("纪律: 只有公开别名；内部案号不出现在本文件。端点/工具故障（invalid causes）优先于能力归因；信号不够一律标 `unknown`，不硬塞。")
    out.append("")
    out.append("## 图例")
    out.append("")
    out.append("| 标签 | 含义 |")
    out.append("|---|---|")
    out.append("| `timeout` | transcript 命中超时帽（1800s/3600s/7200s 墙钟附近，或 rc=124 + 帽文本） |")
    out.append("| `billing_exhausted` | transcript 机器信封出现配额/计费耗尽信号 |")
    out.append("| `tool_failure` | 工具调用非零 exit / error（端点或候选环境故障，非直接能力判定） |")
    out.append("| `test_modified` | 写操作落在测试文件路径上（路径信号） |")
    out.append("| `completion_claimed` | 最后一条 assistant 消息含完成声明 |")
    out.append("| `unknown` | 有 transcript 但硬事实层没命中任何信号 |")
    out.append("| `no_transcript` | 找不到对应 bench session（外部 host 上跑 / 墙前未成交 / 早于记账） |")
    out.append("")

    for repo in sorted(by_repo):
        meta = REPO_META.get(repo, ("?", "?", "?"))
        profs = REPO_PROFILES.get(repo, [])
        out.append(f"### {repo} — {meta[0]} @ {meta[1]} ({meta[2]})")
        out.append("")
        out.append("| 案别名 | face | lane列 | 硬事实标签 | 证据 (profile/session@ts) | 声明-结果一致性 |")
        out.append("|---|---|---|---|---|---|")
        for fr in sorted(by_repo[repo], key=lambda x: (x["alias"], x["col"])):
            if is_ref_column(repo, fr["col"]):
                labs, ev, cons = ["ref_column"], "— (跨厂商引用列，无本地 transcript)", "n/a"
                labels["ref_column"] += 1
                rows_rendered += 1
                out.append(f"| {fr['alias']} | {fr['face']} | {fr['col']} | {', '.join(labs)} | {ev} | {cons} |")
                continue
            fl, exact = pick_facts(by_alias_prof, fr["alias"], profs, fr["col"],
                                   fr["repo"], fr["file"])
            labs = []
            ev = "—"
            cons = "n/a"
            if not fl:
                labs = ["no_transcript"]
            else:
                labset = set()
                evparts = []
                claimed = verified = False
                for r in fl:
                    s = r["signals"]
                    if s["timeout"]["hit"]:
                        labset.add("timeout")
                        e = s["timeout"]["evidence"][0]
                        evparts.append(f"{r['profile']}/{r['session_id']}@{int(e.get('ts') or 0)}")
                    if s["billing_exhausted"]["hit"]:
                        labset.add("billing_exhausted")
                    if s["tool_failure"]["count"] > 0:
                        labset.add("tool_failure")
                    if s["test_modified"]["hit"]:
                        labset.add("test_modified")
                    if s["completion_claimed"]["hit"]:
                        labset.add("completion_claimed")
                        claimed = True
                    if s["verification_run"]["hit"]:
                        verified = True
                if not labset:
                    labset.add("unknown")
                labs = sorted(labset)
                if exact == "profile":
                    labs.append("scope=profile")
                if evparts:
                    ev = "; ".join(evparts[:2])
                else:
                    ev = f"{fl[0]['profile']} ({len(fl)} sess, e.g. {fl[0]['session_id']})"
                if claimed:
                    inconsistency["claimed_and_published_fail"] += 1
                    if verified:
                        cons = "① 跑了验证但 oracle 判挂"
                        inconsistency["ran_verify_oracle_fail"] += 1
                    else:
                        cons = "② 未跑验证/未过仍称完成（假报）"
                        inconsistency["no_or_unverified_claim"] += 1
                else:
                    cons = "—"
            for l in labs:
                labels[l] += 1
            rows_rendered += 1
            out.append(f"| {fr['alias']} | {fr['face']} | {fr['col']} | {', '.join(labs)} | {ev} | {cons} |")
        out.append("")

    out.append("## 汇总")
    out.append("")
    out.append(f"- 挂案行数（去重后，按 lane 列计）: **{rows_rendered}**")
    out.append("- 硬事实标签计数: " + ", ".join(f"`{k}`={v}" for k, v in labels.most_common()))
    out.append(f"- 声明-结果不一致: ① 跑了验证但 oracle 判挂 = **{inconsistency['ran_verify_oracle_fail']}**；"
               f"② 未跑/未过仍称完成（假报）= **{inconsistency['no_or_unverified_claim']}**"
               f"（合计声称完成且 published 判挂 = {inconsistency['claimed_and_published_fail']}）")
    out.append("")
    out.append("标签为会话级硬事实；一个挂案行可带多标签。`timeout`/`billing_exhausted` 属 invalid causes，优先于能力归因。")
    out.append("")

    out.append("## 端点故障 vs 能力答错（先分，invalid causes 优先）")
    out.append("")
    out.append("口径：本表主体来自 transcript 硬事实；下面这节来自各 `runs-*/manifest.jsonl` 的 run 终态")
    out.append("（scoring 真源，含无 session 记录的考墙卷）。`invalid_infrastructure` / `driver_exception` 属端点/工具故障，")
    out.append("不得计入模型能力。")
    out.append("")
    out.append("| lane | valid_task_success | valid_task_failure | invalid_infrastructure | driver_exception | 挂案(invalid/failure 分列) |")
    out.append("|---|---:|---:|---:|---:|---|")
    for repo in sorted(by_repo):
        runs_for = REPO_RUNS.get(repo, [])
        agg = Counter()
        for run in runs_for:
            for t, c in RUN_TERMINALS.get(run, {}).items():
                agg[t] += c
        out.append(f"| {repo} | {agg.get('valid_task_success',0)} | {agg.get('valid_task_failure',0)} | "
                   f"{agg.get('invalid_infrastructure',0)} | {agg.get('driver_exception',0)} | "
                   f"端点故障 {agg.get('invalid_infrastructure',0)+agg.get('driver_exception',0)} / "
                   f"能力判挂 {agg.get('valid_task_failure',0)} |")
    out.append("")
    out.append(f"全库合计：valid_success={TOTAL.get('valid_task_success',0)} "
               f"valid_failure={TOTAL.get('valid_task_failure',0)} "
               f"invalid_infrastructure={TOTAL.get('invalid_infrastructure',0)} "
               f"driver_exception={TOTAL.get('driver_exception',0)}")
    out.append("")
    out.append("invalid_infrastructure 明细（考墙/基建卷，按 lane）：")
    out.append("")
    for repo in sorted(by_repo):
        causes = Counter()
        for run in REPO_RUNS.get(repo, []):
            for cause, c in RUN_INVALID_CAUSE.get(run, {}).items():
                causes[cause] += c
        if causes:
            out.append(f"- {repo}: " + ", ".join(f"`{k}`={v}" for k, v in causes.most_common()))
    out.append("")

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")
    print(f"wrote {OUT}: {rows_rendered} fail rows")
    print("labels:", dict(labels))
    print("inconsistency:", inconsistency)


if __name__ == "__main__":
    main()
