---
name: build-evidence-gated-agent-workflows
description: Design, implement, or review evidence-backed agent workflows that research, verify, generate, evaluate, and request human approval before external actions. Use when building multi-step research agents, content or code generation crews, novelty and competitive analysis, autonomous pull-request workflows, or any agent that must cite sources, refuse unsupported claims, expose progress, persist typed results, and combine model judgment with deterministic safety and quality gates.
---

# Build Evidence-Gated Agent Workflows

Build the workflow around inspectable evidence and explicit gates, not around agent personas. Make unsupported claims, invalid output, and unsafe side effects impossible to silently promote into a completed result.

Read `references/workflow-contracts.md` when creating a new workflow, changing its state model, or designing its tests.

## Define the decision before the agents

1. Name the user decision the workflow supports.
2. Define the artifact it may produce and the external action it may eventually take.
3. State the claims that require evidence, the minimum acceptable evidence, and the refusal conditions.
4. Separate reversible computation from side effects such as publishing, sending, deploying, or opening a pull request.
5. Put a human approval boundary immediately before any material external side effect unless the user has explicitly authorized autonomous execution.

## Choose the smallest effective topology

Default to one bounded model execution when research, comparison, and synthesis share the same context and output contract. Multiple named agents add latency, cost, and handoff loss; use them only when there is a measurable reason such as parallel tool access, independent critique, different trust boundaries, or genuinely separable outputs.

Keep prompt configuration separate from runtime composition:

- Put roles, goals, task descriptions, and expected outputs in declarative configuration when the framework supports it.
- Put tools, schemas, validation, persistence, retries, and provider boundaries in code.
- Keep tools small, read-only by default, and attributable to a provider.
- Disable free-form delegation unless the workflow requires and constrains it.

## Implement the evidence pipeline

### 1. Validate intake

Parse the request into a typed input contract. Confirm ambiguous, high-impact fields before research. Assign a run ID at the boundary so events, traces, costs, and persisted artifacts correlate.

### 2. Collect attributable evidence

Prefer canonical product pages, primary documentation, authoritative datasets, and repository metadata. Store source URL, title, relevant excerpt or fact, provider, retrieval time, and uncertainty. Distinguish direct evidence, adjacent precedent, and internal evidence instead of flattening them into one confidence signal.

### 3. Verify claims

Represent claims separately from sources. Mark each claim verified, rejected, conflicting, or unknown and attach the supporting source IDs and reason. Preserve `null` or `unknown` when a URL, license, number, or fact cannot be verified. Never invent a citation to satisfy the schema.

### 4. Generate only from the verified set

Pass the generator an allowlisted set of verified claims and sources, not the entire untrusted research transcript. Validate the generated artifact against a strict schema and domain invariants before persistence. Do not persist model output as a successful result before it passes validation.

### 5. Apply deterministic gates

Use code for rules that can be expressed deterministically: schema validity, required sections, score bounds, exact category coverage, citation presence, forbidden rejected claims, before/after improvement, path constraints, or policy thresholds. Keep each check explainable with a stable ID, weight or severity, pass/fail state, and detail.

Do not use an LLM judge for a rule that normal code can evaluate reliably. Use model review only for semantic judgments and keep its output separate from deterministic gate evidence.

### 6. Decide and escalate

Move to `awaiting_approval` only when required gates pass. Escalate with the missing evidence and rejected claims when the artifact cannot be supported safely. Fail closed when validation, research, or a required provider fails.

### 7. Execute the side effect

Re-read the persisted, approved artifact before execution. Verify that the approval still targets the same digest or revision. Perform the narrow external action, record its identifier or URL, and make retries idempotent.

## Make the run observable

Persist structured status, bounded subtasks, and domain events so the UI can show progress without exposing chain-of-thought. Capture duration, model, provider, tokens, cost, tool failures, gate results, and correlation IDs. Keep prompt and output capture off by default when it may contain private data; enable it only under an approved data policy.

Provide a deterministic demo or fixture mode that exercises the complete state machine without paid providers. Keep provider secrets only in the runtime that makes the call; never leak backend keys into a browser bundle.

## Verify the implementation

Test happy path, no-evidence refusal, conflicting sources, malformed model output, provider timeout, rejected-claim leakage, non-improving output, approval mismatch, duplicate execution, and recovery after partial progress. Assert state transitions and immutable evidence, not just final prose.
