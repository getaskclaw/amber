# Contributing

This repository is the **public channel** of AMBER (Distribution Protocol §1). It holds the specification and its companion documents, and nothing that belongs to a case. Contributions are welcome within those bounds.

## What never goes here

The public/private split has no exceptions. Do not submit, attach, or paste — in a commit, a PR description, an issue, or a review comment:

- `base.bundle`, `oracle.pack`, or any `manifest.yaml` (redacted summaries excluded);
- rubrics, expected outputs, post-cutoff patches, known-bad responses, or any other Oracle material;
- run records, per-criterion scores, or candidate transcripts;
- anything that identifies a case's Source Event (repository, commit, issue, cutoff commit).

Case content that reaches this repository — even briefly, even in a closed PR — retires the case permanently (Distribution §6). Git history is public; there is no undo. If you are unsure whether something is case content, do not post it; describe the problem abstractly instead.

## Documents and how they change

Every normative document carries its own version and a dated changelog inline, at the top of the file. The revision policy is Core's and applies to all of them:

| Change | Bump | Example |
|---|---|---|
| Editorial, portability, or citation fix; no normative change | patch (`0.x.y`) | fixing a wrong `§` reference |
| Normative addition or clarification | minor (`0.x`) | a new required manifest field |
| Anything that weakens sealing, audit, preregistration, or data controls | not accepted | Core §5.7 |

A PR that changes a normative document must, in the same PR:

1. bump the version in the header line and add a changelog entry stating what changed and which bump it is;
2. update any document that pins to the old version (for example, a protocol's "Companion to Core vX.Y.Z" line, `PLAN.md`);
3. re-verify that no Core invariant (§4) or boundary (§5) is weakened, and say so in the PR.

`PLAN.md` and `README.md` are not normative and need no version bump. Where they conflict with Core, Core wins.

### The Core specification is hash-pinned

`AMBER-Core-Specification.md` is pinned by `spec_sha256` in every Case Manifest (Distribution §2). **Every byte change to that file changes the hash** and breaks comparability between cases built before and after it. Consequences:

- do not reformat, re-wrap, or "clean up" whitespace in Core without a versioned reason;
- files are stored with LF line endings, enforced by `.gitattributes`; UTF-8 validity and the no-BOM rule are enforced by CI (`.github/workflows/docs.yml`) — do not override either locally;
- when Core does change, expect producers to treat existing cases as pinned to the old hash; that is the design working, not a bug.

Compute the hash of the current Core bytes with `sha256sum AMBER-Core-Specification.md` on a clean checkout.

## Style

- Normative documents are written in English; `README.md` is Chinese with an English pointer to the normative entry point. Keep it that way unless a maintainer decides otherwise.
- Cite Core by section (`Core §4.5`), and cite the Core-unnumbered "Purpose and use" section by name. Check the citation against the current Core text; wrong section numbers were the most common finding in past reviews.
- Prefer stating a limit honestly over stating a guarantee vaguely (Core §6, Distribution §8).
- Relative links between documents must resolve; CI checks them.

## Review

Normative changes go through review before merge; the maintainers have used structured multi-reviewer passes for every published version so far. Open the PR with the checklist in the template filled in. If a reviewer's finding is accepted but deferred, record it in `PLAN.md` (open design questions) so it is not lost.

## License

By contributing you agree that your contributions are licensed under the Apache License 2.0 (see `LICENSE`).
