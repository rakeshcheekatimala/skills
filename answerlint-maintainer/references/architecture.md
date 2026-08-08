# AnswerLint architecture

Use this map to find the canonical layer before editing. Verify it against the current tree because the project is active.

## Runtime flow

```text
Commander CLI
  -> command validation/orchestration
  -> crawler or local parser
  -> synchronous audits + optional network audits
  -> recommendations
  -> configured weighted scores
  -> Report / BatchReport / ComparisonReport
  -> terminal + HTML / JSON / CSV / SARIF
  -> optional CI exit gate
```

The TUI reuses synchronous audits, recommendations, scoring, and citation readiness for local Markdown. It deliberately excludes network audits from its edit-refresh loop.

The diff command starts from two existing JSON reports rather than crawling content. The composite GitHub Action consumes diff JSON, exports scores, updates a PR comment, and enforces floors/drop limits.

## Canonical locations

| Concern | Canonical files |
|---|---|
| Shared audit/report/config contracts | `src/types/index.ts` |
| Audit context construction and registration | `src/audits/runner.ts` |
| AEO/GEO heuristics | `src/audits/aeo/`, `src/audits/geo/` |
| Declarative repository rules | `src/audits/custom-rules.ts`, `src/config/index.ts` |
| Configured score calculation | `src/scoring/index.ts` |
| Citation-readiness signal | `src/scoring/citation-readiness.ts` |
| Fix catalog | `src/recommendations/index.ts` |
| Input acquisition | `src/crawler/` |
| Commander surface | `src/cli/index.ts` |
| Audit orchestration and comparison | `src/cli/commands/audit.ts` |
| Before/after comparison | `src/diff/`, `src/cli/commands/diff.ts` |
| Output serialization | `src/reporters/`, `templates/report.hbs` |
| llms.txt feature | `src/llms/`, `src/cli/commands/llms.ts` |
| Local watch UI | `src/tui/`, `src/cli/commands/tui.ts` |
| Composite action contract | `action.yml`, helper modules under the target repository's `scripts/` directory |
| Tests and fixtures | `tests/`, `examples/`, `tests/helpers.ts` |
| Build/package | `tsup.config.ts`, `package.json` |

## Non-obvious contracts

- `runAudits` strips script/style/noscript only from cloned text; it keeps the original Cheerio tree so schema audits can inspect JSON-LD.
- Audit `score` is currently binary even though status can be `warn`. Configured weights, not `AuditResult.weight`, drive `computeScores`.
- `AuditResult.weight` still drives recommendation priority/estimated impact fallbacks. Keep it synchronized with `DEFAULT_WEIGHTS`.
- Custom rule IDs are rendered as `custom:<configured-id>` and may have no catalog recommendation.
- Sitemap crawling skips disallowed or failed pages and preserves input order through `mapWithConcurrency`.
- Compare mode accepts exactly one target URL plus one competitor URL. Its CI threshold applies to the target score; competitor data is informational.
- Batch JSON is exhaustive. CSV is a batch summary. SARIF reports non-passing audits and does not support competitor compare.
- The CLI bundle is CommonJS, but TypeScript source imports use `.js` suffixes for emitted module resolution.
- Tests import compiled modules from `.test-dist`; `npm run build:test` must precede direct Node test runs.
