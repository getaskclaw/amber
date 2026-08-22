# PLAN — AMBER build-out

Status, milestones, and open design questions for turning the published
specification into an executable evaluation. Companion to the Core
Specification; where this file and Core conflict, Core wins.

## Status (2026-08)

- **Published:** AMBER Core Specification v0.2.2; Distribution Protocol v0.2.
- **Not yet published:** `schemas/`, `profiles/`, case-building tooling, and a
  reference runner. A conformant run is **not executable from this repository
  alone today** — this file exists to make that gap explicit and to sequence
  the work that closes it.

## Milestones

- **M1 — Case tooling.** The forge-neutral build script promised by
  `protocols/distribution.md` §3 (produces `base.bundle`, `oracle.pack`,
  signed `manifest.yaml`); manifest JSON Schema + validator.
  *Exit:* build a case from an arbitrary git repository; validator rejects
  malformed manifests; bundle passes `git bundle verify`.
- **M2 — Reference runner.** Fixed-harness candidate runner: an external
  agent runtime as the candidate scaffold, launched inside an isolated
  container (no default route; egress only through the manifest-declared
  allowlist); evaluator-side seal probe with scoped positive control per
  Distribution §5.3; structured run records per §7.
  *Exit:* one end-to-end Core-conformant run of a reference case whose
  artifacts verify against the manifest hashes.
- **M3 — Oracles and judging.** Executable-oracle adapter (restore, build,
  test); LLM-judge protocol covering judge pinning, blinding, and drift
  checks — expected to become its own document under `protocols/`.
- **M4 — Statistics protocol.** Repeated runs, paired comparison, and
  reporting rules, as a companion document under `protocols/`.
- **M5 — Public index bootstrap.** Reference implementation of the
  append-only signed index (Distribution §4), including key management and
  rotation.

## Open design questions

Raised by external review (2026-08); resolve in the milestone that owns them:

1. **Judge mechanics** (M3): Core §5.8 requires declaring the Oracle's
   identity and independence, but drift, blinding, and agreement mechanics
   for LLM judges are unspecified.
2. **Index trust root** (M5): the index is single-producer-signed; key
   rotation and third-party witnessing are unspecified.
3. **Difficulty calibration** (M4): no guidance with teeth against
   saturation — a single easy case cannot discriminate (observed in pilot
   work: near-ceiling pass rates on an easy-medium repair case).
4. **Transition identifiers** (M1): the SHRE→AMBER identifier mapping
   required by Core §9.3 must ship together with `schemas/`.

## Non-goals

- Cases, `oracle.pack` artifacts, and results live in the **private channel**
  by design (Distribution §1) and are never published here.
- AMBER runs alongside public benchmarks; it does not replace them (Core,
  Purpose and use).
