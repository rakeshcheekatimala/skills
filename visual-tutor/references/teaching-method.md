# Teaching for transfer

## Start from a need, not a glossary

Describe a situation the learner recognizes, what they want to accomplish, and what their current approach cannot explain or accomplish. Derive the next concept from that gap. A first principle is a stated constraint or basic fact used to reason forward, not simply a definition with “first principles” attached.

For each major concept connect the problem, smallest useful model, concrete input, intermediate states, rule causing each transition, observable consequence, and a variation that tests the model. Show how it enables the next concept. Do not force these into repetitive headings; use a coherent narrative and highlight the current step.

## Build a dependency path

Foundations establish vocabulary and a mental model. Intermediate material combines parts into a useful example. Advanced material tests boundaries, tradeoffs, failure modes, and unfamiliar variations. Advanced does not mean merely adding product names or longer code.

A short central path can coexist with detailed optional explanations. Define adjacent terms where the learner encounters them and show why they are adjacent rather than prerequisites. Distinguish instructions, executable capabilities, packaging, and event-triggered behavior using the chosen host's current definitions.

## One evolving example

Prefer one example carrying the main story. Show its simplest useful form, then add a dependency only when a concrete need appears. Revisit earlier behavior after the model grows. Keep identifiers, inputs, colors, and positions stable so the learner recognizes the same objects.

The example should do something useful at its scale. Avoid a production scaffold that hides the mechanism. Include reproducible setup. Identify outputs from real runs, generated illustrations, and external sources.

## Make the invisible visible

Motion earns its place when it answers “what moved, what changed, or what caused this?” Give each meaningful frame a causal explanation. Highlight the relevant source line, entity, edge, or value. Keep the rest visible for context. Move a token only along a real modeled relationship; do not imply serial order for independent operations.

Choose the representation from the mechanism:

- Queue or lifecycle: stable regions, moving objects, explicit eligibility rules.
- Hierarchy or containment: nested regions and progressive expansion.
- Dependency: a graph highlighting the relevant edge.
- Quantitative change: a plot, number line, or bars using the example's inputs.
- Geometry: positions or shapes encoding the relationship.
- Decision: alternatives and the condition selecting a branch.
- Human or conceptual process: a worked scenario with explicit uncertainty.

Offer steps and replay instead of requiring memory of autoplay. Preserve the information with motion disabled.

## Test understanding without blocking access

Progress from observing to predicting a variation, modifying something, diagnosing a failure, and explaining the fix. Let the learner reveal hints and solutions.

Checks should discriminate mental models. Asking whether placing a file in `scripts/` guarantees it runs is more revealing than asking for a definition of a script. Explain the mistaken causal model in feedback. Never equate clicking or confidence with competence.

## Research and boundaries

Build a compact claim/source ledger before writing. Use primary documentation for implementation and credible domain sources for conceptual claims. Track versions or research dates. Link each source to its relevant concept.

For disagreements identify version, context, assumptions, or uncertainty. Present competing explanations when warranted. Do not turn disputed findings into certainty.

Before delivery, check that a newcomer can tell why each concept exists, trace the example without unexplained jumps, connect prose and visuals, see the simple model's limits, and make a new prediction, adaptation, and diagnosis. An attractive shell and valid data do not establish these qualities.
