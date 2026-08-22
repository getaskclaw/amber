# AMBER Distribution Protocol

Draft v0.2, 2026-08-21. Companion to AMBER Core Specification v0.2.2. This protocol is intended to preserve Core invariants (§4) and boundaries (§5) without weakening; v0.2 was re-verified against the frozen Core before publication. Where this protocol and Core conflict, Core wins.

*v0.2, 2026-08-21. Incorporates every accepted correction from the structured review of the v0.1 draft: egress-scoped eligibility, transport-layer seal probe with scoped positive control, signed manifests, the public hash index, pinned bundle construction, the run-state split, and the explicit verification matrix.*

## 1. The split: public spec, private cases

AMBER separates into two channels with no exceptions:

- **Public channel** (e.g. the public spec repository): the Core specification, case-building tooling, the manifest schema, and a hash-only case index — an integrity reference proving that a case exists and is unmodified, carrying no content.
- **Private channel** (an access-restricted forge or store): `base.bundle`, `oracle.pack`, the full `manifest.yaml`, and the results store.

Rationale: a case's value is its controlled leak status (Core §5.1). Case content reaching a public channel burns the case permanently — future candidates may train on it (§6 of this protocol).

## 2. Spec pinning

Every Case Manifest records `spec_sha256` — the SHA-256 of the exact Core specification bytes — not a version string alone. Cross-host results are comparable only when `spec_sha256` matches. Pinning to "latest" is a comparability failure: version strings move, hashes do not.

## 3. Case package: three parts

A case is three artifacts, produced by one forge-neutral build script:

| Artifact | Contents | Visibility |
|---|---|---|
| `base.bundle` | `git bundle create` of the source repository's history up to the cutoff commit | candidate-visible |
| `oracle.pack` | post-cutoff commits/patch/tests, the preregistered rubric, evaluator materials | sealed |
| `manifest.yaml` | provenance, `cutoff_utc`, the resolved cutoff commit, the time-to-topology mapping rule and its evidence class, the preregistered cutoff rule and its script-output hash, `spec_sha256`, sha256 of both artifacts, the declared `candidate_input_bundle` (Core §4.4), the available-information manifest (Core §5.2), the eligibility determination and its evidence class (§5), producer identity and signature (§5), the leak-check procedure and its last run date, retirement state, and the sha256 of this protocol document | private |

### 3.1 Bundle construction (pinned)

`base.bundle` is built from a single temporary ref at the cutoff commit — never `--all`, no tags, no notes. The bundle must be self-contained (no thin ranges); the receiver runs `git bundle verify` before acceptance. The manifest records the git version, the bundle format version, the hash algorithm, the bundle size, and the bundle sha256. Submodules and LFS objects are vendored into the bundle or the case is ineligible — an LFS pointer reachable only through the network is a leak path under the egress rule (§5).

`git bundle` is forge-neutral: any git host (self-hosted forge, public forge, bare repo) produces and consumes it. AMBER case tooling must not depend on any one forge's API.

### 3.2 Cutoff semantics

The manifest records `cutoff_utc` (UTC, second-or-finer precision, per Core §4.2), the resolved commit, and the time-to-topology mapping rule with its evidence class (e.g. forge push log, event log). Committer dates are attacker-controlled and never suffice as the mapping's evidence on their own.

## 4. The public index

The public channel carries an append-only, producer-signed case index. Each entry:

`case_id` · manifest sha256 · `base.bundle` sha256 · `oracle.pack` sha256 · `spec_sha256` · `cutoff_utc` · state (`active` / `retired` + date)

Rules:

- The index entry — including `oracle.pack` sha256 — is published **before the case's first run**. Runs predating publication are not Core results (Core §4.6: preregistration).
- Retirement writers are authenticated; entries are never edited or deleted, only superseded by later append-only entries.
- Every conformant host consults the index before running a case; the run record carries `index_version` and the retirement-check result (§7).

## 5. Cross-forge, cross-host operation

### 5.1 Transfer and trust

- The producer host builds the case from its own forge and transfers to the evaluation host: `base.bundle` and the **full signed `manifest.yaml`**. The evaluation host is trusted — it will hold `oracle.pack` in its sealed store — so redaction never applies to it. The manifest signature covers the entire manifest, which embeds both artifact hashes; the evaluation host verifies the signature and the bundle hash before any run. Transfer is authenticated.
- The producer may additionally publish a **redacted manifest summary** for external parties who need provenance without private-channel access. The summary has an enumerated field set and redaction rules (no oracle paths, no rubric, no source-identifying provenance). Its audience is external consumers — never the candidate, and never a substitute for the full manifest at the evaluation host.

### 5.2 Eligibility and isolation

- The candidate runtime is network-isolated by default. Any egress is a manifest-declared allowlist.
- A case is eligible only if no post-cutoff evidence is reachable through the declared egress. Cases whose source is publicly reachable (public-source cases) qualify only under full isolation (empty allowlist). The eligibility determination is recorded in the signed manifest with an evidence class, mirroring the cutoff mapping (§3.2).
- The candidate works a local clone extracted from `base.bundle`. **No forge credentials exist at run time.** Issue/PR/tracker context is not in the bundle; if a case needs it, the producer attaches an explicit export listed in the manifest.
- The seal is the network boundary: `oracle.pack` lives on infrastructure the candidate cannot reach, not merely a repository it lacks permission to read. Repository permissions are policy; the seal must be physical (Core §4.5).

### 5.3 The seal probe

Before every run, an evaluator-executed probe runs from the candidate's network vantage, before the candidate starts. "From inside" describes position, not control.

- The probe attempts to read the sealed store and **must fail at the transport layer** (no TCP/TLS handshake). Any application-layer answer (401/403/…) is a failed probe and aborts the run as `invalid_infrastructure`.
- **Positive control, scoped:** for runs with a non-empty egress allowlist, a known-reachable endpoint from the same vantage must succeed, else the run aborts as `invalid_infrastructure` — this kills vacuous passes caused by unrelated outages. For full-isolation runs no external endpoint is reachable by design, so the positive control does not apply; instead the isolation mechanism itself is verified: no default route, egress firewall active, allowlist empty and enforced at the hypervisor/container layer. This mechanism-level check is what makes the original source unreachable by construction, and it is recorded in the run record.
- A pre-start probe failure is `invalid_infrastructure`. Candidate tampering with the probe or the seal is `protocol_violation` (Core §5.6, deliberate control bypass).

## 6. Leak means retirement

If any case artifact's content reaches a public channel, the case is permanently retired: the index marks it `retired` with the date, and it is never reused for a Core result. There is no partial leak and no re-sealing of burned material. A suspected leak maps to `pending_adjudication` (Core §5.6). Runs completed before the retirement date remain valid.

## 7. Run records and comparability

Every run emits a structured record: manifest sha256, `index_version` and the retirement-check result, the seal-probe results (including the mechanism-level isolation check for full-isolation runs), candidate provider/model, per-criterion scores, the terminal state (Core §5.6), and sha256 of every artifact produced. Records are collected to the results store in the private channel; the public channel carries at most rubric-structure-free aggregates.

Comparability across hosts requires equal `spec_sha256` AND equal `base.bundle` sha256 AND equal `oracle.pack` sha256 AND equal construction parameters (git version, bundle format version, hash algorithm) — same ruler, same exam; construction parameters plus hashes, never hashes alone.

### 7.1 Verification matrix

| Verifier | Can verify |
|---|---|
| Evaluation host | all three artifact hashes + manifest signature (it holds the bytes) |
| External result consumer | `spec_sha256` and `base.bundle` sha256 against the index; the `oracle.pack` leg only via the signed manifest |

## 8. Honest limits

- A git bundle carries git history only; everything else (issues, reviews, chat logs) is an explicit manifest-listed export or absent.
- The seal probe verifies physical unreachability at probe time; continuity between probe and run is unverified.
- The eligibility rule's guarantee for full-isolation runs rests on the mechanism-level isolation check (§5.3), not on producer assertion.
- The original-source path is a named residual risk: post-cutoff evidence may exist at the case's source outside any sealed store; only full isolation plus the mechanism check closes it.
- The index proves integrity, not quality; retirement is reactive to discovered leaks.
- The same model evaluated from two different hosts is two independent contexts, not model diversity.
- Distribution does not fix case selection bias (documented in Core §6 and the profile layer); it only moves cases safely.
