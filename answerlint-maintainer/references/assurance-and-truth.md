# Repository assurance and product truth

Read this reference for dependency, CI, workflow, release, documentation, example, or visual changes.

## Dependency trust flow

Use the repository wrapper:

```bash
npm run deps:add -- <package> [npm install options]
```

It installs with lifecycle scripts disabled, runs OSV, GuardDog, and npm signature checks, then rebuilds only after the gates pass. On failure it restores `package.json`, `package-lock.json`, and the prior dependency tree.

Keep `.husky/pre-commit` and `.husky/pre-push` as local convenience gates, not the sole enforcement point. CI must independently enforce the checks because hooks can be bypassed.

Review `osv-scanner.toml` exceptions as temporary risk acceptances:

- Match the exact locked package/version and correct dependency group.
- Confirm the advisory does not affect AnswerLint's runtime or build use.
- Record a concrete reason and a near-term `effectiveUntil` date.
- Remove the exception when the graph can take a fixed version.
- Never extend an expired entry merely to make CI green.

## Workflow invariants

- Pin third-party actions to a full commit SHA; retain the readable release tag in a comment when useful.
- Default to `contents: read`; add job-level permissions only where required, such as SARIF upload.
- Keep PR/push path filters synchronized with every file that changes the gate.
- Retain coverage artifacts even when useful diagnostic steps fail, without masking the original exit result.
- Test the supported Node matrix. Give Node 18 a packaged CLI smoke path because startup/polyfill regressions can differ from source tests.
- Enforce the 85% line floor through `scripts/run-test-coverage.mjs`; do not weaken or bypass parsing to pass CI.
- Check `npm pack --dry-run` whenever runtime files or the `files` allowlist changes.

## Release invariants

- Release from `main` through semantic-release.
- Use `fix:` for a patch, `feat:` for a minor, and a breaking marker for a major.
- Keep the package version, action's default `answerlint-version`, README examples, and release behavior synchronized when a release changes those contracts.
- Preserve the public package contents required at runtime: `dist`, `templates`, `assets`, `action.yml`, and action helper scripts unless the implementation intentionally changes them.

## Truth hierarchy

Use this order to decide what is shipped:

1. Current executable source and package configuration.
2. Tests that exercise the source or built CLI.
3. `docs/capability-map.md` as the concise claim registry, corrected when stale.
4. `README.md` as user guidance, corrected when stale.
5. `docs/requirements.md` as intent and phased design, not proof of implementation.

Verify dynamic facts instead of trusting prose: built-in audit count, accepted inputs, formats, CLI flags, defaults, thresholds, exit codes, network behavior, and package version.

## Claim rules

- Say the tool audits, scores, surfaces evidence, prioritizes fixes, and estimates citation readiness.
- Do not say it automatically rewrites content, guarantees citation/ranking, edits inside the TUI, browser-renders client-side apps, or runs real LLM probes unless code and tests now prove that behavior.
- Describe `--probe` as reserved/stubbed while it remains unimplemented.
- Distinguish target-vs-competitor URL comparison from before-vs-after JSON report diffing.
- Describe scores as deterministic heuristics and prioritization signals, not measured citation probability.
- Make visuals follow the product sequence: add content, inspect clarity and trust, fix what matters, edit and recheck.

For any user-facing example, run the command or trace it through Commander and the command implementation. Ensure quoted shell variables, report paths, failure retention, and provider-specific syntax remain valid.
