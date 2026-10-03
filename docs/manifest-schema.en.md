# Manifest schema and validator

> Moved from the front-page [README](../README.en.md); text unchanged. Run the commands below from the **repository root**. 中文: [manifest-schema.md](manifest-schema.md)

The Case Manifest is the control-plane record: private-channel material, never candidate-visible (Distribution §1, Core §2). Its field set is taken **entirely from the protocol text**: `protocols/distribution.md` §3 (provenance, `cutoff_utc`, the resolved cutoff commit, the time-to-topology mapping rule and its evidence class, the preregistered cutoff rule and its script-output hash, `spec_sha256`, the sha256 of both artifacts, the declared `candidate_input_bundle`, the available-information manifest, the eligibility determination and its evidence class, producer identity and signing-key identifier, the leak-check procedure / last run date / result, retirement state, and the sha256 of the protocol document), §3.1 (construction parameters: git version, bundle format version, hash algorithm, bundle size), §3.2, §5.1, §5.2. **No field is invented.**

- [schemas/manifest.schema.json](../schemas/manifest.schema.json) — the manifest JSON Schema (2020-12); the top level and every field block are closed (`additionalProperties: false`), so a field the protocol does not enumerate is an error.
- [tools/validate_manifest.py](../tools/validate_manifest.py) — the validator. It checks the manifest against the schema and additionally rejects any **redacted manifest summary** carrying a field outside the closed set of Distribution §5.1.
- [schemas/shre-amber-mapping.md](../schemas/shre-amber-mapping.md) — the `shre`↔`amber` identifier mapping required by Core §9.3; anything unmappable from public material is marked TBD with the missing artefact named.
- [schemas/examples/](../schemas/examples/) — regression fixtures: one valid manifest, three malformed manifests (missing required fields / wrong types and enum values / fields outside the enumerated set) and one redacted summary carrying an excluded field.

Usage (YAML and JSON are both accepted):

```bash
python3 tools/validate_manifest.py schemas/examples/manifest.valid.yaml        # passes, exit code 0
python3 tools/validate_manifest.py schemas/examples/manifest.wrong-types.yaml  # fails, exit code 1 + the offending fields on stderr
python3 tools/validate_manifest.py schemas/examples/summary.invalid-fieldset.yaml   # redacted summary with an excluded field
```

Exit codes: **0** valid; **1** invalid (schema, closed-set, or cross-field violation); **2** unreadable/unparseable, undetectable kind, or schema load failure. JSON input is dependency-free; YAML uses PyYAML when it is installed and otherwise falls back to a bundled conservative parser that *refuses* structures it cannot read safely (anchors, aliases, folded scalars) instead of guessing. Install PyYAML with `python3 -m pip install pyyaml` or `uv run --with pyyaml python3 tools/validate_manifest.py <file>`.
