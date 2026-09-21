#!/usr/bin/env python3
"""Build the profile -> lane -> model registry from run manifests + state.db.

Evidence chain (all read-only):
  1. each runs-*/manifest.jsonl row carries {'case','model','effort','session',...}
  2. the `session` id joins to a state.db session, whose profile we can read
  3. bench session source `amber-lib-<CASE>-<lane>-<band>` gives a lane token

Output: lane-registry.json  (used by build_attribution.py)
"""
import glob
import json
import os
import re
import sqlite3
from collections import Counter, defaultdict

PROFDIR = os.path.expanduser("~/.hermes/profiles")
RUNDIR = os.path.expanduser("~/2608/sandbox/amber-run")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lane-registry.json")

BENCH_RE = re.compile(r"^amber-lib-(?P<rest>.+)$")


def sessions_index():
    out = {}
    for p in glob.glob(os.path.join(PROFDIR, "amber-*", "state.db")):
        prof = os.path.basename(os.path.dirname(p))
        try:
            c = sqlite3.connect(f"file:{p}?mode=ro", uri=True, timeout=20)
            for sid, src in c.execute("SELECT id, source FROM sessions"):
                out[sid] = (prof, src)
            c.close()
        except Exception:
            pass
    return out


def main():
    sidx = sessions_index()

    # profile -> lane tokens / models / bench session count
    prof_lane_tokens = defaultdict(Counter)
    prof_models = defaultdict(Counter)
    prof_bench = Counter()
    for sid, (prof, src) in sidx.items():
        if not src.startswith("amber-lib-"):
            continue
        prof_bench[prof] += 1
        m = BENCH_RE.match(src)
        rest = m.group("rest") if m else src
        # lane token = 2nd-from-last token of `<case...>-<lane>-<band>`
        toks = rest.split("-")
        if len(toks) >= 3:
            prof_lane_tokens[prof][toks[-2]] += 1

    # run dir -> {models, cases, sessions, profiles}
    runs = {}
    for mf in sorted(glob.glob(os.path.join(RUNDIR, "runs-*", "manifest.jsonl"))):
        run = os.path.basename(os.path.dirname(mf))
        models = Counter(); cases = Counter(); profs = Counter(); n = 0
        for line in open(mf, errors="replace"):
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except Exception:
                continue
            n += 1
            if d.get("model"):
                models[d["model"]] += 1
            if d.get("case"):
                cases[d["case"]] += 1
            sid = d.get("session")
            if sid and sid in sidx:
                profs[sidx[sid][0]] += 1
        runs[run] = {"rows": n, "models": dict(models.most_common(6)),
                     "profiles": dict(profs.most_common(6)),
                     "cases": len(cases)}

    # profile -> models (from manifest evidence)
    for run, info in runs.items():
        for prof, cnt in info["profiles"].items():
            for m in info["models"]:
                prof_models[prof][m] += cnt

    reg = {
        "profiles": {
            prof: {
                "bench_sessions": prof_bench[prof],
                "lane_tokens": dict(prof_lane_tokens[prof].most_common()),
                "models": dict(prof_models[prof].most_common()),
            }
            for prof in sorted(prof_bench)
        },
        "runs": runs,
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(reg, fh, ensure_ascii=False, indent=1)
    print(f"wrote {OUT}")
    print(f"profiles with bench sessions: {len(reg['profiles'])}")
    print(f"run dirs: {len(runs)}")


if __name__ == "__main__":
    main()
