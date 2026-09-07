# AMBER Distribution Protocol

Draft v0.3, 2026-09-07. Companion to AMBER Core Specification v0.2.2. This protocol is intended to preserve Core invariants (§4) and boundaries (§5) without weakening; each revision is re-verified against the frozen Core before publication. Where this protocol and Core conflict, Core wins. This document follows Core's revision policy (patch = editorial, minor = normative addition or clarification).

*v0.2, 2026-08-21. Incorporates every accepted correction from the structured review of the v0.1 draft: egress-scoped eligibility, transport-layer seal probe with scoped positive control, signed manifests, the public hash index, pinned bundle construction, the run-state split, and the explicit verification matrix.*

*v0.3, 2026-09-07. Closes the post-publication review findings on v0.2: manifest signature made detached (`manifest.yaml.sig`) so coverage is well-defined (§3, §5.1); redacted manifest summary's field set enumerated (§5.1); leak-window runs routed to `pending_adjudication` and validity keyed to the leak date, not the retirement date (§6); verification matrix corrected — external consumers verify `spec_sha256` by possession and the `base.bundle` / `oracle.pack` hashes by value against the signed index (§7.1); `spec_sha256` byte definition and computation fixed (§2); index described as content-free, not hash-only, with the public `cutoff_utc` disclosure recorded as a limit (§1, §4, §8); two Core miscitations corrected (§1, §8). Review round on the v0.3 draft: comparability extended to `cutoff_utc` (§7); `index_version` defined as a property of the index, not an entry field (§4); the manifest records the leak check's result, not only its date (§3); run records asserted to external consumers must be producer-signed (§7, §7.1). Normative clarifications → minor bump.*

## 1. The split: public spec, private cases

AMBER separates into two channels with no exceptions:

- **Public channel** (e.g. the public spec repository): the Core specification, case-building tooling, the manifest schema, and a content-free case index — artifact hashes plus the minimal metadata enumerated in §4 (`cutoff_utc`, state). It is an integrity reference proving that a case exists and is unmodified; it carries no case content.
- **Private channel** (an access-restricted forge or store): `base.bundle`, `oracle.pack`, the full `manifest.yaml` and its signature, and the results store.

Rationale: a case's value is its controlled leak status (Core, Purpose and use; Core §5.3, candidate boundary). Case content reaching a public channel burns the case permanently — future candidates may train on it (§6 of this protocol).

## 2. Spec pinning

Every Case Manifest records `spec_sha256` — the SHA-256 of the exact Core specification bytes — not a version string alone. Cross-host results are comparable only when `spec_sha256` matches. Pinning to "latest" is a comparability failure: version strings move, hashes do not.

"Exact bytes" means the file as committed to the public channel: UTF-8, LF line endings, no byte-order mark, computed over the whole file (`sha256sum AMBER-Core-Specification.md`). The public repository enforces this encoding through `.gitattributes`; a checkout that rewrites line endings or re-encodes the file yields a different hash and must not be used as the pinning source. The same rule applies to the protocol self-hash recorded in the manifest (§3).

## 3. Case package: three artifacts, one detached signature

A case is three artifacts plus the detached signature of the manifest, produced by one forge-neutral build script:

| Artifact | Contents | Visibility |
|---|---|---|
| `base.bundle` | `git bundle create` of the source repository's history up to the cutoff commit | candidate-visible |
| `oracle.pack` | post-cutoff commits/patch/tests, the preregistered rubric, evaluator materials | sealed |
| `manifest.yaml` | provenance, `cutoff_utc`, the resolved cutoff commit, the time-to-topology mapping rule and its evidence class, the preregistered cutoff rule and its script-output hash, `spec_sha256`, sha256 of both artifacts, the declared `candidate_input_bundle` (Core §4.4), the available-information manifest (Core §5.2), the eligibility determination and its evidence class (§5), producer identity and signing-key identifier (§5), the leak-check procedure, its last run date, and its result (`passed` / `failed`), retirement state, and the sha256 of this protocol document | private |
| `manifest.yaml.sig` | detached signature over the exact bytes of `manifest.yaml`, made with the key identified in the manifest (§5.1) | private |

The signature is detached rather than embedded so that its coverage is unambiguous: it covers every byte of `manifest.yaml`, and verifying it needs no canonical re-serialization of YAML. Any change to the manifest — including to the artifact hashes it embeds — invalidates the signature.

### 3.1 Bundle construction (pinned)

`base.bundle` is built from a single temporary ref at the cutoff commit — never `--all`, no tags, no notes. The bundle must be self-contained (no thin ranges); the receiver runs `git bundle verify` before acceptance. The manifest records the git version, the bundle format version, the hash algorithm, the bundle size, and the bundle sha256. Submodules and LFS objects are vendored into the bundle or the case is ineligible — an LFS pointer reachable only through the network is a leak path under the egress rule (§5).

`git bundle` is forge-neutral: any git host (self-hosted forge, public forge, bare repo) produces and consumes it. AMBER case tooling must not depend on any one forge's API.

### 3.2 Cutoff semantics

The manifest records `cutoff_utc` (UTC, second-or-finer precision, per Core §4.2), the resolved commit, and the time-to-topology mapping rule with its evidence class (e.g. forge push log, event log). Committer dates are attacker-controlled and never suffice as the mapping's evidence on their own.

## 4. The public index

The public channel carries an append-only, producer-signed case index. Each entry:

`case_id` · manifest sha256 · `base.bundle` sha256 · `oracle.pack` sha256 · `spec_sha256` · `cutoff_utc` · state (`active` / `retired` + date)

The index itself carries a monotonically increasing `index_version` (an append-only sequence number or a head hash covering every entry to date). `index_version` is a property of the index, not an entry field; run records (§7) and redacted summaries (§5.1) cite the `index_version` of the index that carries the corresponding entry.

Rules:

- The index entry — including `oracle.pack` sha256 — is published **before the case's first run**. Runs predating publication are not Core results (Core §4.6: preregistration).
- Retirement writers are authenticated; entries are never edited or deleted, only superseded by later append-only entries.
- Every conformant host consults the index before running a case; the run record carries `index_version` and the retirement-check result (§7).
- Entries carry exactly the fields listed above and nothing else. `cutoff_utc` and state are metadata, not case content, but `cutoff_utc` is a real disclosure: it weakly narrows the set of possible Source Events (§8). It is published because comparability (§7) and retirement checks need it; no other manifest field is ever copied into the index.

## 5. Cross-forge, cross-host operation

### 5.1 Transfer and trust

- The producer host builds the case from its own forge and transfers to the evaluation host: `base.bundle`, the **full `manifest.yaml`**, and its detached signature `manifest.yaml.sig` (§3). The evaluation host is trusted — it will hold `oracle.pack` in its sealed store — so redaction never applies to it. The signature covers every byte of `manifest.yaml`, which embeds both artifact hashes; the evaluation host verifies the signature against the producer's published key, then the bundle hash, before any run. Transfer is authenticated. The producer's public key is published in the public channel next to the index (§4), so the same key verifies both; key rotation and third-party witnessing are outside this protocol and tracked as an open design question of the index implementation.
- The producer may additionally publish a **redacted manifest summary** for external parties who need provenance without private-channel access. Its field set is closed — exactly these fields, no others:
  `case_id` · manifest sha256 · `base.bundle` sha256 · `oracle.pack` sha256 · `spec_sha256` · protocol sha256 · `cutoff_utc` · profile identifier · isolation class of the eligibility determination (`full_isolation` / `allowlisted`; never the allowlist itself) · construction parameters (git version, bundle format version, hash algorithm, bundle size) · producer identity and signing-key identifier · retirement state · `index_version` of the index carrying this case's entry (§4).
  Everything else in the manifest is excluded, in particular: the resolved cutoff commit, source-identifying provenance, the time-to-topology evidence, the available-information manifest, `candidate_input_bundle`, oracle paths, the rubric, the cutoff rule and its script-output hash, and the leak-check procedure. The summary is itself signed (detached, same key). Its audience is external consumers — never the candidate, and never a substitute for the full manifest at the evaluation host.

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

If any case artifact's content reaches a public channel, the case is permanently retired: the index marks it `retired` with the date, and it is never reused for a Core result. There is no partial leak and no re-sealing of burned material. A suspected leak maps to `pending_adjudication` (Core §5.6).

Validity of earlier runs is keyed to the **leak date** — when the content became reachable — not to the retirement date, which is only when the leak was discovered:

- Runs completed before the leak date remain valid.
- Runs completed between the leak date and the retirement date enter `pending_adjudication`; the adjudication authority declared by the profile (Core §5.8) determines, per run, whether the leaked content was reachable from that run's candidate vantage. Full-isolation runs with a passed mechanism-level check (§5.3) will normally be upheld; allowlisted runs are examined against their egress.
- If the leak date cannot be established, it defaults to the date of the last leak check recorded as passed in the manifest (§3). A case whose manifest records no passed leak check has no valid runs after the leak is confirmed.

## 7. Run records and comparability

Every run emits a structured record: manifest sha256, `index_version` and the retirement-check result, the seal-probe results (including the mechanism-level isolation check for full-isolation runs), candidate provider/model, per-criterion scores, the terminal state (Core §5.6), and sha256 of every artifact produced. Records are collected to the results store in the private channel; the public channel carries at most rubric-structure-free aggregates. A run record asserted to an external consumer must be signed by the producer (detached, same key as §5.1); by-value verification (§7.1) consumes only signed run records.

Comparability across hosts requires equal `spec_sha256` AND equal `cutoff_utc` AND equal `base.bundle` sha256 AND equal `oracle.pack` sha256 AND equal construction parameters (git version, bundle format version, hash algorithm) — same ruler, same exam; construction parameters plus hashes, never hashes alone. `cutoff_utc` is asserted directly rather than via manifest sha256 because manifests of the same exam legitimately drift (leak-check dates, retirement state) while the exam's information boundary does not.

### 7.1 Verification matrix

Two different verification strengths are in play. Verification **by possession** recomputes a hash from bytes the verifier holds. Verification **by value** checks that the same hash is asserted consistently by independently signed records (index entry, run record, redacted summary) without holding the bytes.

| Verifier | By possession | By value |
|---|---|---|
| Evaluation host | `spec_sha256`, `base.bundle` sha256, `oracle.pack` sha256, manifest signature — it holds all the bytes | — |
| External result consumer | `spec_sha256` only (the Core specification is public) | `base.bundle` sha256 and `oracle.pack` sha256: signed run record against the signed index entry (§4) and, if published, the signed redacted summary (§5.1). It never holds the bundle or the oracle, so it can confirm that the hashes match, not that the bytes exist or are what the manifest says. |

## 8. Honest limits

- A git bundle carries git history only; everything else (issues, reviews, chat logs) is an explicit manifest-listed export or absent.
- The seal probe verifies physical unreachability at probe time; continuity between probe and run is unverified.
- The eligibility rule's guarantee for full-isolation runs rests on the mechanism-level isolation check (§5.3), not on producer assertion.
- The original-source path is a named residual risk: post-cutoff evidence may exist at the case's source outside any sealed store; only full isolation plus the mechanism check closes it.
- The index proves integrity, not quality; retirement is reactive to discovered leaks, and the leak date it keys on (§6) is itself an investigation finding, not a measurement.
- The public `cutoff_utc` in the index (§4) weakly narrows the set of possible Source Events. It is an accepted disclosure, not a leak of case content; producers of public-source cases should weigh it when choosing cutoffs that coincide with widely known events.
- The same model evaluated from two different hosts is two independent contexts, not model diversity.
- Distribution does not fix case selection bias or difficulty calibration; those are profile-layer and statistics-protocol concerns, and Core §6 does not address them either. This protocol only moves cases safely.
