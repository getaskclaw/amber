# SHRE → AMBER identifier mapping

Core Specification §9.3 requires every deployment adopting the AMBER name to
"publish a `shre`↔`amber` identifier mapping for audit reconciliation" during the
transition window. This file is that mapping, shipped together with `schemas/`
as PLAN.md's open design question #4 requires.

It is an **audit reconciliation table**, not a rename instruction. §9.4 is the
binding rule: machine-readable identifiers change **only with an explicit
schema-version bump, never silently**. Nothing here authorises a quiet rename of
any identifier that appears in a schema, a manifest, or a stored record.

Core §8 still governs while the adoption pass is incomplete: the SHRE v0.1 corpus
remains normative, and `AMBER-Core-Specification.md` is the controlling front
matter.

## 1. Provenance of this table

Two kinds of evidence are used, and they are labelled:

- **Core (§1, §8, §9)** — the rename mapping, the layering note, and the six
  adoption rules. Authoritative for all prose, titles, and front matter.
- **SHRE v0.1 corpus identifiers** — the concrete `shre`-prefixed identifiers
  that actually occur in the v0.1 corpus (schema-version strings, filenames,
  script names). These are what an auditor would meet in an existing record.

Where the SHRE side of a row is drawn from the corpus rather than from Core, the
`shre` cell carries the literal identifier with a backtick so it can be grepped
for. Where a row cannot be completed from public material, it is marked **TBD**
and the missing artefact is named — see §3. No value in this table is supplied
from guesswork.

## 2. The mapping

### 2.1 Names and documents (Core §1, §9.1, §9.2)

| Identifier class | `shre` form | `amber` form | Change rule |
|---|---|---|---|
| Method name | SHRE | AMBER | Free to use in prose; Core §9.2 switches titles/headings/prose, content otherwise unchanged |
| Method expansion | Sealed Historical Replay Evaluation | Archived-Moment Behavioral Evaluation Replay | Prose only |
| Core specification file | `SHRE-Core-Specification-v0.1` | `AMBER-Core-Specification.md` | §9.1: the v0.1 spec is kept unchanged as the historical record; new copies carry the AMBER name and their own versions |
| Core front-matter version | SHRE v0.1 | AMBER v0.2.2 (current) | AMBER versions are independent; §10 of Core defines the acceptance checklist |
| Domain-profile file | SHRE v0.1 `<domain>` profile | `profiles/<domain>.md` (planned) | §9.2; the target directory is not yet published (PLAN.md M1) |

### 2.2 Machine-readable schema identifiers (Core §9.4 — bump required)

These are the identifiers that live inside records. Each one is renamed, if at
all, only in the same change that bumps the schema version. The AMBER side shows
the identifier under the AMBER name **if that schema has been published**; `TBD`
means the AMBER schema does not exist yet, so nothing may be renamed — the old
`shre` identifier stays valid in existing records.

| Identifier class | `shre` form | `amber` form | Status |
|---|---|---|---|
| Case Manifest schema | — (no manifest schema in the v0.1 corpus) | `amber-manifest-0.1` | **Published** in this repo (`schemas/manifest.schema.json`). This is the first AMBER-versioned manifest identifier. |
| Core run manifest schema | `shre-core-run-0.1` | TBD | No AMBER run-record schema published |
| Core replay-case (task) schema | `shre-core-task-0.1` | TBD | No AMBER case-task schema published |
| Software-engineering profile task schema | `shre-software-task-0.1` | TBD | `profiles/` not published |
| Subscription-agent run manifest schema | `shre-subscription-agent-run-0.1` | TBD | `profiles/` not published |
| Run identifier prefix | `shre-run-` | TBD | Tied to the run-manifest schema, above |
| YAML keys carrying `shre` | any key containing `shre` | rename only with a schema-version bump | No `shre` key occurs in the published AMBER repo today; if one is ever required it must not be introduced silently |

### 2.3 Tool and skill filenames (Core §9.5)

| Identifier class | `shre` form | `amber` form | Change rule |
|---|---|---|---|
| Validator script | `validate_shre_core.py` | `validate_amber_core.py` (TBD) | §9.5: scripts and tools keep their legacy names until their next logic change; rename then. Not renamed by this repository. |
| Skill reference documents | `shre-core-extraction.md`, `shre-methodology.md`, `shre-communication-and-naming.md` | `amber-*.md` | §9.2 prose; the skill is not part of this repository |

### 2.4 Case and run identity (public handle ↔ private identifier)

AMBER separates the public case handle from the private identifier. The public
repo publishes only the hash-derived alias; the internal case number, the variant
name, and the task description are private-channel material (CONTRIBUTING, "What
never goes here"; `hash-index/v2026-09.md`).

| Identifier class | `shre` form | `amber` form | Note |
|---|---|---|---|
| Case identity, private | `shre` task identifier (internal case number) | AMBER `case_id` (private) | The manifest's `case_id` (Distribution §3) is the private control-plane identifier |
| Case identity, public | not defined in the v0.1 corpus | `A-xxxxxxxx` alias (hash-derived) | The public handle; `hash-index/v2026-09.md` publishes alias + truncated `bundle_sha256`/`oracle_sha256` |
| Private↔public correspondence | — | — | The internal-case-number ↔ alias mapping lives in the private channel and is **not published** (Distribution §1). Audit reconciliation against it happens there, not here. |
| Model/evaluation arm identity | not defined in the v0.1 corpus | `arm_id` = `model@lane` (with `:band` where the lane separates bands) | Introduced by the results-side tooling, not by this schema; recorded here so an audit knows the AMBER arm handle is `model@lane`, not a bare model name |
| Run identity | `run_id` (e.g. `shre-run-<id>`) | TBD | Tied to the unpublished run-record schema |

## 3. TBD — what is missing, and what would close it

Each item below cannot be mapped from public material today. The missing artefact
is named so the gap is actionable; no value is invented to fill the cell.

1. **AMBER run-record schema ids.** `shre-core-run-0.1`, `shre-core-task-0.1`,
   `shre-software-task-0.1`, `shre-subscription-agent-run-0.1`, and the
   `shre-run-` prefix have no AMBER counterpart because **no run-record schema
   and no `profiles/` are published yet** (PLAN.md M1/M2). They close when those
   schemas ship — each with its own explicit version bump (§9.4).
2. **The SHRE v0.1 corpus itself.** The concrete `shre` identifiers in §2.2/§2.3
   are listed here from the v0.1 corpus, which is **not published in this repo**.
   A full byte-level reconciliation (every `shre` occurrence, not every
   identifier class) needs the historical v0.1 record and must happen where that
   record lives; this table maps identifier **classes**, not every instance.
3. **Private↔public case correspondence.** The internal-case-number ↔
   `A-xxxxxxxx` alias mapping is private-channel data by design (Distribution §1)
   and will never appear in this file. Reconciliation is a private-channel
   operation.
4. **`validate_shre_core.py` → `validate_amber_core.py`.** Deferred by §9.5 until
   the script's next logic change; no AMBER name exists yet, so the cell stays
   TBD rather than being pre-announced.
5. **Whether the AMBER manifest schema should reuse `shre`-prefixed keys.**
   Decided and recorded in §2.2: it does not. `amber-manifest-0.1` is a new
   identifier under the AMBER name, so the §9.4 bump is satisfied by publication
   rather than by a rename of an existing key.

## 4. Sources

- `AMBER-Core-Specification.md` §1 (provenance and rename), §8 (document
  layering), §9 (adoption rules), §10 (acceptance).
- `protocols/distribution.md` §1 (public/private split), §3 (manifest contents),
  §4 (public index).
- `hash-index/v2026-09.md` (public case handles).
- `CONTRIBUTING.md` (what never goes here).
- SHRE v0.1 corpus identifiers, as cited inline in §2.
