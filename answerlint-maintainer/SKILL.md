---
name: answerlint-maintainer
description: Maintain and extend the AnswerLint TypeScript/Node.js CLI while preserving its deterministic AEO/GEO audit, scoring, reporting, CI, and product-truth contracts. Use for repository work involving audits or recommendations, crawler inputs, CLI commands and exit codes, report or diff schemas, llms.txt generation/linting, the zero-token TUI, GitHub Action behavior, tests and coverage, dependency security, releases, or user-facing capability documentation.
---

# AnswerLint Maintainer

Make repository changes from shipped behavior outward. Keep the core deterministic, evidence-backed, reusable across interfaces, and compatible with the supported Node.js range.

## Ground the task

1. Read `CLAUDE.md` and the files directly involved in the request.
2. Inspect `git status --short`; preserve unrelated user changes.
3. Read [architecture.md](references/architecture.md) for an unfamiliar subsystem.
4. Read [change-matrix.md](references/change-matrix.md) for the affected change type.
5. Read [assurance-and-truth.md](references/assurance-and-truth.md) before changing dependencies, CI, releases, security controls, claims, counts, examples, or visuals.
6. Treat implementation and executable tests as the authority for shipped behavior. Treat `docs/requirements.md` as product intent that may include future work. Reconcile `docs/capability-map.md` and `README.md` with the code instead of copying a stale statement.

## Preserve the core contracts

- Prefer deterministic heuristics over model judgment. Do not silently turn the zero-token core into an API-backed workflow.
- Return evidence with every audit outcome. Keep claims directional; never promise rankings, citations, or automatic rewriting.
- Reuse `Report`, `ComparisonReport`, `BatchReport`, and audit data rather than recalculating the same concept in each presenter.
- Keep local-only paths independent from live-network checks. `runAudits` is synchronous and powers the TUI; `runNetworkAudits` is async and belongs in the full audit pipeline.
- Preserve exit semantics: `0` success, `1` quality/regression gate, `2` crawl or runtime failure, and `3` invalid input/config/report.
- Preserve Node.js `>=18.17.0`, strict TypeScript, the CommonJS bundle, and the early `src/polyfills/node-web.ts` import in the CLI entrypoint.
- Respect robots rules, bounded concurrency, rate limits, timeouts, and partial-result behavior for live crawling.

## Route the change

### Add or change an audit

1. Put a pure content heuristic under `src/audits/aeo` or `src/audits/geo` and accept `AuditContext`.
2. Put an outbound HTTP check behind `runNetworkAudits`; give it a timeout and bounded concurrency.
3. Return a stable snake-case `id`, valid category/status, binary `score`, specific evidence, and an intentional weight.
4. Register the audit in `src/audits/runner.ts`.
5. Add its default scoring weight to `DEFAULT_WEIGHTS` in `src/types/index.ts`. Scoring reads configured weights by ID, while recommendation priority/impact can read the audit's own weight; keep both values aligned.
6. Add a recommendation in `src/recommendations/index.ts` only when the failure has a concrete, honest fix.
7. Cover pass, fail, warning/insufficient-data, malformed input, and network failure where applicable. Update exact audit-count assertions.
8. Check terminal, JSON, CSV, HTML, SARIF, comparison/diff, and TUI consumers for assumptions about IDs, counts, status, or recommendation presence.

### Add or change a CLI capability

1. Define shared option/output types before wiring Commander flags.
2. Keep command orchestration in `src/cli/commands`; keep reusable domain logic outside `src/cli`.
3. Validate mutually exclusive inputs, numbers, formats, and required pairs before doing work.
4. Choose the documented exit class deliberately. A quality gate is not a runtime failure.
5. Propagate schema changes through reporters, diff/comparison code, the composite action, examples, and integration tests as applicable.
6. Update `README.md` command reference and `docs/capability-map.md` only to match behavior that now exists.

### Change a report or comparison contract

1. Update the canonical types in `src/types` or `src/diff/types.ts`.
2. Compute the signal once in the report/diff layer.
3. Render the same signal consistently across every supported output.
4. Keep JSON machine-readable and exhaustive; keep SARIF limited to non-passing findings with stable rule IDs.
5. Add contract-level tests and an end-to-end CLI write/read test.
6. Treat report JSON consumed by `action.yml` and its helper modules under the target repository's `scripts/` directory as a compatibility boundary.

### Change llms.txt or TUI behavior

- Keep `src/llms` generation and linting deterministic. Validate structure, budgets, links, timeouts, concurrency, strictness, and CI behavior separately.
- Keep the TUI an adapter over the same audit/scoring/recommendation pipeline. Do not fork scoring rules into the renderer.
- Avoid content leakage in JSON debug events and preserve watch debounce/error recovery.

### Change dependencies or repository controls

- Follow [assurance-and-truth.md](references/assurance-and-truth.md).
- Add dependencies through `npm run deps:add -- <package> [options]`; do not bypass its ignore-scripts, OSV, GuardDog, signature, rebuild, and rollback sequence.
- Make vulnerability exceptions narrow, development-only when true, reasoned, and time-bounded. Never refresh an expiry without re-verifying the locked graph and upstream remediation.
- Pin third-party GitHub Actions by full commit SHA and keep permissions least-privilege.

## Verify proportionately

Run the narrowest useful test during iteration, then widen before handoff:

```bash
npm run lint
npm run build
npm test
npm run test:coverage
```

Also run:

- `npm run test:cli-smoke` for CLI entrypoint, packaging, or Node compatibility changes.
- `npm run size:pack` when changing published files, templates, action scripts, or package metadata.
- The relevant `security:*` command and safe-install flow for dependency changes.
- A real local CLI smoke command against `examples/` when behavior or output changes.

Do not claim a check passed if it was skipped, unavailable, or blocked by network/tooling. Report the exact command and limitation.

## Finish the change

1. Re-read the diff for duplicated logic, stale counts, overclaims, and unintended generated artifacts.
2. Confirm tests assert behavior rather than only snapshots or file existence.
3. Update user documentation and capability claims in the same change when behavior changed.
4. Use conventional commit semantics when preparing a commit: `fix:` for patch behavior, `feat:` for user-facing capability, and `feat!:` or `BREAKING CHANGE:` for incompatible contracts.
