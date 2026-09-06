# PLAN — AMBER build-out

Status, milestones, and open design questions for turning the published
specification into an executable evaluation. Companion to the Core
Specification; where this file and Core conflict, Core wins.

## Status (2026-09)

- **Published:** AMBER Core Specification v0.2.2; Distribution Protocol v0.3
  (v0.3 closes every finding left open by the review of the v0.2 publication:
  detached manifest signature, enumerated redacted summary, leak-date
  validity window, corrected verification matrix, `spec_sha256` byte
  definition, Core citation fixes).
- **Not yet published:** `schemas/`, `profiles/`, case-building tooling, and a
  reference runner. A conformant run is **not executable from this repository
  alone today** — this file exists to make that gap explicit and to sequence
  the work that closes it.
- **Repository controls in place:** `.gitattributes` pins LF/UTF-8 so
  `spec_sha256` is checkout-stable; CI checks relative links and spec-file
  encoding; `CONTRIBUTING.md` states the no-case-content rule and the
  revision policy.

## Milestones

- **M1 — Case tooling.** The forge-neutral build script promised by
  `protocols/distribution.md` §3 (produces `base.bundle`, `oracle.pack`,
  `manifest.yaml`, and the detached `manifest.yaml.sig`); manifest JSON
  Schema + validator; the redacted-summary generator restricted to the
  closed field set of Distribution §5.1.
  *Exit:* build a case from an arbitrary git repository; validator rejects
  malformed manifests and summaries containing any excluded field; bundle
  passes `git bundle verify`; signature verifies against the published key.
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
   rotation and third-party witnessing are unspecified. Distribution §5.1
   now states where the key is published (next to the index) and explicitly
   defers rotation and witnessing here.
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
