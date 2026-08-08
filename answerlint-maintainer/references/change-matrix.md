# AnswerLint change matrix

Use the relevant row as a minimum impact check, then inspect imports and consumers for the exact change.

| Change | Primary implementation | Required test surface | Documentation/contract checks |
|---|---|---|---|
| Audit heuristic | Audit file, runner, `DEFAULT_WEIGHTS`, optional recommendation | Unit pass/fail/boundary; runner count; score/recommendation effects | Audit list/count, capability claims, examples |
| Network audit | GEO audit, `runNetworkAudits`, crawler concurrency utilities | Timeout/error/redirect/status; concurrency; local-file degradation | Network limitations, runtime expectations |
| Config/rule | `src/config`, shared types, consuming layer | Merge/default/invalid/duplicate cases; CLI config error | Config JSON example and supported values |
| Crawler/input | `src/crawler`, `AuditOptions`, CLI flags | robots, malformed input, rate/concurrency, partial failure | Input table, command reference, limitations |
| CLI command/flag | `src/cli/index.ts`, command module, shared types | Validation and exit code; integration; packaged smoke | Command reference, examples, CI contract if applicable |
| Report field/format | Shared types, audit command, reporters/templates | Serializer contract; file output; escaping; all variants | Output docs; action/diff compatibility |
| Competitor compare | Audit command comparison builders, reporters | Missing IDs, tie/lead/gap, priorities, target-only gate | URL-only limitation and target gate semantics |
| Before/after diff | `src/diff`, diff command/reporters | Positive/negative/zero deltas; malformed report; gate flags | CI examples and baseline/head semantics |
| llms.txt generation | discover/extract/render/types/command | Local and web discovery; stable ordering; budgets; escaping | Deterministic/no-key claim and command reference |
| llms.txt lint | lint/types/command | Error vs warning; strict/CI; redirect/link timeout/concurrency | Exit behavior and network-check controls |
| TUI/watch | `src/tui`, TUI command, shared score pipeline | Initial render, debounce, refresh, invalid/empty file, debug privacy | Zero-token/read-only/editor boundary |
| Composite action | `action.yml`, its helper modules under the target repository's `scripts/` directory, package files | Valid/invalid reports; comment marker/update; floor/drop failure | Action inputs, pinned version, permissions |
| Dependency | package manifests, security config/workflow | Build/test/coverage/package; OSV/GuardDog/signatures | Trust model and any narrow exception |
| Release/build | package metadata, tsup, semantic-release, workflow | Node matrix, bundle start, pack contents | Versioning/release notes and published files |
| Product docs/visual | README, capability map, relevant command output/assets | Verify every command and count against code/tests | Separate shipped, stubbed, planned, unsupported |

## Test selection

- Use `tests/audits.test.ts` for individual heuristics and the synchronous registry.
- Use `tests/core.test.ts` for scoring, recommendations, report serialization, comparison/diff domain logic, config, and crawler helpers.
- Use `tests/commands.integration.test.ts` for real command flows, files, HTTP fixtures, outputs, and exit codes.
- Use `tests/priority-features.test.ts` for custom rules, bounded concurrency, batch JSON, and SARIF.
- Use `tests/llms.test.ts` for generation/linting internals and `tests/tui.test.ts` for the watch adapter/controller/renderer.
- Reuse `tests/helpers.ts` and temporary directories. Do not write smoke artifacts into the repository root.

## Review prompts

Before finishing, ask:

1. Did a shared type or JSON field change without updating every consumer?
2. Did a new audit update both registry and configured weights?
3. Did a network call leak into the zero-token local path?
4. Does an error use the correct exit class?
5. Did an exact audit count or capability claim become stale?
6. Does the test cover failure and malformed/partial data, not only success?
7. Will the built package contain every runtime template/action script it references?
