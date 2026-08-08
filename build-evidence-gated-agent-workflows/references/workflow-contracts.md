# Workflow contracts

Use these shapes as a framework-neutral starting point. Adapt names and fields to the product, but keep evidence, claims, gates, decisions, and side effects distinct.

## Core records

```text
RunInput
  request
  confirmed_fields
  target
  requested_action

Source
  id
  url
  title
  relevant_fact
  provider
  retrieved_at
  source_class: direct | adjacent | internal
  uncertainty

Claim
  id
  text
  status: verified | rejected | conflicting | unknown
  source_ids[]
  reason
  commercial_or_high_impact

CandidateArtifact
  content_or_patch
  claim_ids[]
  source_ids[]
  schema_version
  digest

GateResult
  id
  passed
  severity_or_weight
  detail
  evidence_refs[]

Approval
  artifact_digest
  approver
  approved_at
  permitted_action

SideEffectResult
  idempotency_key
  external_id_or_url
  status
  attempted_at
```

Use runtime schema validation at every boundary. Add domain invariants that a type alone cannot express, such as exactly one recommendation per required category or a public claim always requiring a canonical URL.

## State model

Use explicit states rather than inferring progress from missing fields:

```text
queued
  -> running
  -> awaiting_approval
  -> completed

running
  -> escalated
  -> failed

awaiting_approval
  -> completed
  -> rejected
  -> expired
```

Keep `escalated` distinct from `failed`: escalation is a successful safety outcome when the workflow correctly refuses unsupported or unsafe work.

## Event vocabulary

Prefer stable machine-readable event types with human-readable messages:

- `run.started`
- `plan.created`
- `research.source-found`
- `research.completed`
- `claim.evaluated`
- `artifact.proposed`
- `gate.completed`
- `run.escalated`
- `approval.requested`
- `approval.recorded`
- `side-effect.started`
- `side-effect.completed`
- `run.failed`

Include run ID, step ID, timestamp, status, provider, and bounded structured data. Do not store hidden reasoning.

## Topology decision

| Condition | Prefer |
| --- | --- |
| Shared context, one final schema, tight latency or cost | One bounded agent/tool pass |
| Independent searches that can run concurrently | Parallel workers with a deterministic merge |
| A critique must be independent of the draft | Separate verifier with limited draft context |
| Different credentials or trust zones | Separate runtimes at the boundary |
| Mostly deterministic transformation | Normal code, not another agent |

Measure quality, latency, cost, and failure rate before keeping extra handoffs.

## Minimum gate set

1. Input schema and target scope are valid.
2. Every high-impact claim has sufficient evidence.
3. Rejected or unknown claims do not appear in the candidate.
4. The candidate passes structural and domain invariants.
5. The candidate improves the declared metric when improvement is required.
6. The external target and artifact digest match the approval.
7. The side effect uses an idempotency key and records its result.

## Test matrix

| Case | Expected result |
| --- | --- |
| Strong primary evidence and valid candidate | Await approval |
| No verified high-impact claims | Escalate with missing evidence |
| Sources conflict | Preserve conflict; do not overstate confidence |
| Model returns malformed structure | Reject or retry within a bound; never persist as success |
| Candidate repeats a rejected claim | Fail deterministic safety gate |
| Candidate does not improve required metric | Escalate or reject |
| Approval digest differs from current artifact | Expire approval and request a new one |
| Side effect retried after ambiguous response | Resolve by idempotency key before repeating |
| Observability backend unavailable | Continue only if it is non-critical; record telemetry loss |
| Paid provider unavailable in demo mode | Complete against deterministic fixtures |
