# AMBER Core Specification v0.2.2

**AMBER — Archived-Moment Behavioral Evaluation Replay**

Pronounced `ˈæm-bər` (the fossil resin). Draft v0.2.2, 2026-08-20. Renames **SHRE (Sealed Historical Replay Evaluation)**; method unchanged.

> A mosquito in amber is not a model of a mosquito — it is the actual moment, preserved, examined later as it was. AMBER does this to real work: a real event frozen at an exact cutoff, later evidence sealed in the resin, the candidate works the moment again.
>
> **Read first:** `sealed` = the candidate cannot reach post-cutoff evidence *at run time*; it says nothing about training data (§6).

- Chinese formal name: `琥珀式封存历史回放评测`
- Chinese plain line: `封进琥珀，重做当时的题。`

## Purpose and use

Why AMBER exists: public benchmarks are static public question sets — training contamination is common and unauditable, scores inflate, and static Q&A does not measure what real work demands: multi-step diagnosis, abstention, refusal, and escalation under uncertainty. AMBER replays real, auditable events whose leak status is checkable because the source is controlled, and scores behavior against preregistered criteria.

What AMBER is for: periodic behavioral regression checks and deep re-tests before selection decisions — alongside public benchmarks, never as their replacement (§6). Results are dimension-wise and deployment-specific; they certify nothing outside the cases actually run.

## 1. Provenance and rename

| | |
|---|---|
| Method coined | 2026-07-13 as **Sealed Historical Replay Evaluation (SHRE)**, by an AI agent from the owner's problem statement and cross-domain insight |
| Source corpus | `SHRE-Core-Specification-v0.1` (2026-07-24), the v0.1 dotnet software-engineering profile (2026-07-13), and the companion evaluation-design skill |
| Renamed | 2026-08-20 by owner decision after a structured naming review (candidates: AMBER, HERMETIC, AMNESIA) |
| Rename mapping | `SHRE` → `AMBER` in front matter, titles, and prose; adoption rules in §9 |

Label-only change: every normative statement restates or inherits SHRE v0.1 without weakening.

## 2. Definition

AMBER is a formal evaluation method: take a real, auditable historical event; restore its exact pre-outcome state; give the candidate only cutoff-available information; physically seal later evidence and evaluator materials; let the candidate diagnose, decide, act, abstain, refuse, or escalate; judge against criteria fixed before any output is viewed; preserve configuration, evidence, and disposition for audit.

Beginner line: restore a real case to just before the answer was known, give the candidate only what was knowable then, hide later evidence, judge with an independent protected evaluator.

**Key terms:**

- **Candidate Input Bundle** — all the candidate receives: the Base State plus cutoff-available information. Nothing else.
- **Case Manifest** — the evaluator's control-plane record: provenance, available-information manifest, Oracle materials, scoring controls. Never candidate-visible.

## 3. Mechanism flow

1. choose a real historical event (Source Event);
2. set an exact cutoff timestamp, UTC, second-or-finer precision;
3. reconstruct what was knowable then (Base State);
4. seal later evidence and evaluator materials (the amber);
5. candidate works the case: diagnose, decide, communicate, act, abstain, refuse, or escalate;
6. judge against preregistered behavioral criteria;
7. preserve configuration, evidence, and disposition for audit.

## 4. Core invariants

Every conformant AMBER deployment must preserve:

1. an auditable real Source Event;
2. an explicit cutoff timestamp, UTC, second-or-finer precision;
3. a reconstructable Base State;
4. a declared Candidate Input Bundle, separate from the control-plane Case Manifest;
5. physical isolation of post-cutoff evidence and the Oracle from the candidate;
6. criteria and budgets fixed before candidate results are viewed;
7. coherent run states and audit records;
8. the historical outcome treated as evidence, never the unique correct answer.

## 5. Boundaries

1. **Real history:** cases come from auditable Source Events. Synthetics labeled `synthetic_supplement` never count as Core results.
2. **Temporal boundary:** every case carries an exact cutoff + a manifest of what was knowable by then.
3. **Candidate boundary:** provenance, references, known-bad responses, Oracle material, scoring controls stay outside candidate reach.
4. **Rule boundary:** Historical Rules at the cutoff ≠ current Evaluation Controls (protecting people/data/infrastructure); controls must not leak later knowledge.
5. **Oracle boundary:** alternatives, abstention, clarification, refusal, rollback, or a finding of no valid solution are acceptable when predeclared criteria support them.
6. **Run boundary:** terminal states `valid_task_success` / `valid_task_failure` / `invalid_infrastructure` / `protocol_violation`, plus non-terminal `pending_adjudication`. Candidate-caused resource failure = task failure; deliberate control bypass = protocol violation.
7. **Governance boundary:** profiles may strengthen Core, never weaken sealing/audit/preregistration/data controls.
8. **Declaration boundary:** every profile declares the Oracle's identity + independence, the adjudication authority behind `pending_adjudication`, and the max pending time per run.

## 6. Limits that must never be simplified away

- Runtime sealing ≠ weight purity: `sealed` covers runtime evidence only, not whether training excluded future facts.
- The historical outcome is evidence, not necessarily the sole correct answer.
- One vague total score must not replace distinct capability, risk, cost, and reliability dimensions.

## 7. Naming review (six axes)

| Axis | AMBER | SHRE (previous) |
|---|---|---|
| Semantic fidelity | amber = the sealing metaphor itself | literal |
| Pronunciation | immediate | needs coaching (`shree`) |
| Search/spelling | common-word dilution; `AMBER evaluation` recovers | blurred with share/shred |
| Collisions | npm `amber`=Smalltalk (unrelated); AmberMD (molecular dynamics); no agent-eval collision | none found |
| Extensibility | Core/Profiles/Cases read naturally | acronym-only |
| Overclaim risk | low | `Sealed` invites the weight-purity misreading |

Scan 2026-08-20 (not a trademark/availability claim; recheck before publication/registration): npm `amber`=Smalltalk v0.22.x; PyPI inconclusive; amber-eval.com/.dev, amberbench.com: no DNS.

## 8. Document layering

Layered corpus — no file is explainer, standard, manual, and schema at once:

```text
AMBER.md                        # one-page human entry point (planned)
AMBER-Core-Specification.md     # this document: normative cross-domain invariants
protocols/                      # pilot, statistics, security, governance (inherit SHRE v0.1)
schemas/                        # machine-readable Case and Run records (inherit)
profiles/                       # domain profiles, e.g. dotnet software engineering (inherit)
```

Until the §9 adoption pass completes, the SHRE v0.1 corpus remains normative; this document is the controlling front matter.

## 9. Adoption rules (SHRE → AMBER)

Any deployment adopting the new name must:

1. Keep the v0.1 spec unchanged as the historical record; new copies carry the AMBER name and their own versions.
2. Switch titles/headings/prose `SHRE`→`AMBER`; content otherwise unchanged.
3. During any transition window, publish a `shre`↔`amber` identifier mapping for audit reconciliation.
4. Machine-readable identifiers (`shre` in YAML keys, schemas, run manifests) change only with an explicit schema-version bump — never silently.
5. Scripts/tool filenames keep legacy names until their next logic change; rename then.
6. Re-run the §7 scan before any public release, package publication, or domain registration.

## 10. Acceptance of this document

- name, expansion, metaphor, and Chinese names as above;
- all eight invariants and eight boundaries restated without weakening;
- both epistemic limits present;
- rename mapped, adoption rules defined;
- naming scan dated and hedged;
- no site-, host-, or deployment-specific content: generic and portable;
- key terms defined at first use; cutoff precision mandated; Oracle/adjudication declaration required; transition identifier mapping required.

*v0.1, 2026-08-20. AMBER selected from a structured naming review; candidate set: AMBER, HERMETIC, AMNESIA.*
*v0.1.1, 2026-08-20. Removed all site-, host-, and persona-specific content (provenance, layering note, adoption rules, colophon); spec now fully generic; genericity added to §10. No normative change.*
*v0.2, 2026-08-20. External-review fixes: key terms (Candidate Input Bundle / Case Manifest) defined; cutoff must be UTC with >=1s precision; read-first warning on the limits of `sealed` moved to the front; declaration boundary added (5.8) requiring Oracle independence and adjudication authority; transition identifier-mapping mandate added (9.3). Normative additions -> minor bump per the revision policy.*
*v0.2.1, 2026-08-20. Editorial compression; §10 count fixed (seven -> eight boundaries, matching 5.8); revision-policy digits updated. No normative change -> patch bump.*
*v0.2.2, 2026-08-20. Added the unnumbered Purpose and use section (why the method exists, what it is for, not a benchmark replacement). Explanatory only, no normative change -> patch bump.*

## Revision policy

Patch (0.x.y): editorial/portability fixes, no normative change. Minor (0.x): normative additions or clarifications. The §1 rename mapping is fixed history and does not change.
