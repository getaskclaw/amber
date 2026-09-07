## What

<!-- One paragraph: which document(s), what changed, why. -->

## Checklist

- [ ] **No case content.** Nothing in this PR (commits, description, attachments) is or identifies `base.bundle`, `oracle.pack`, a full `manifest.yaml`, Oracle material, run records, or a Source Event. See `CONTRIBUTING.md`.
- [ ] If a normative document changed: version bumped in its header and a dated changelog entry added (patch = editorial, minor = normative).
- [ ] If a normative document changed: documents pinning to the old version updated (`Companion to …` lines, `PLAN.md`).
- [ ] If `AMBER-Core-Specification.md` changed: the change is intentional and versioned — every byte change alters `spec_sha256`.
- [ ] No Core invariant (§4) or boundary (§5) is weakened; Core `§` citations checked against the current text.
- [ ] Relative links resolve (CI link check passes).
