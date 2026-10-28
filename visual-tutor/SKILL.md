---
name: visual-tutor
description: Teach a topic from first principles through advanced application with a researched, interactive lesson, working examples, and synchronized animated explanations. Use when someone wants deep understanding of how something works and how to build, apply, adapt, or debug it.
---

# Visual Tutor

Turn a topic, even a one-line request, into a complete learning experience. The learner should be able to explain the mechanism, build or apply an example, change it, and diagnose a failure. Deliver the lesson, not just a plan, outline, or collection of links.

## Establish the learning boundary

Use the request and available context to identify the central question, the learner's starting point, and a useful application. Default to a curious beginner who can follow plain language. Define unfamiliar words before relying on them. Ask only if a missing answer materially changes the lesson, such as which platform a runnable implementation must target. Otherwise state the assumption and proceed.

Show the topic map before the details: prerequisites, foundations, intermediate concepts, advanced concepts, and adjacent subjects. Give the main path a clear finish line. A full picture means the necessary connections and explicit boundaries, not an unbounded encyclopedia. Label optional branches and important omissions. Do not force every topic into a software architecture or a build exercise; use worked cases, experiments, or manipulable models where those teach it better.

## Research and design the explanation

Read [the teaching method](references/teaching-method.md). Research the topic using available tools. Prefer primary sources for technical claims; verify changing APIs, commands, installation paths, and product behavior. Separate general principles from host-specific implementation. Link material claims to supporting sources in the lesson and date the research snapshot. Resolve disagreements or mark them as uncertain. If research access is unavailable, disclose the limit and avoid inventing citations or current facts.

Choose one useful example that can evolve across the lesson. Start with the problem that makes the concept necessary. Introduce only the machinery needed to explain the next step. Trace causes and consequences, expose a misconception, change an input, and explain the resulting behavior. Use additional examples when the central example cannot honestly explain a concept.

Use Philip Roberts' event-loop explanation as a teaching reference: a small explicit model, visible intermediate states, progressively richer examples, and consequences the learner can reason about. Do not claim comparable quality merely because a diagram moves. Do not copy the talk's wording or treat its historical technical details as current documentation.

## Build the complete lesson

Default to a portable local browser lesson with two synchronized panes:

- **Left:** the problem, first-principles explanation, concrete working example, and current cause-and-effect step.
- **Right:** a clearly labeled infographic showing the same entities and state changes. Motion must represent a meaningful transition, dependency, flow, or comparison.

Every main-path concept needs a specific explanation and relevant visual. Do not reuse a generic pipeline with renamed boxes for unrelated mechanisms. The supplied node-and-edge renderer suits relationships and flows; replace or extend it with spatial, chart, timeline, geometric, or other visual forms when required. Preserve the left/right teaching relationship.

Deliver foundations, intermediate, and advanced sections in a navigable artifact in the initial run. Allow jumping between concepts and opening deeper details. Provide play/pause, previous/next step, replay, and concrete variations or failure cases. On narrow screens, stack each explanation with its matching visual. Include keyboard-operable controls, readable labels, a text account of each visual state, and reduced-motion support.

Use [the lesson format](references/lesson-format.md) and `assets/lesson-shell.html` for a self-contained HTML lesson without runtime dependencies. Author the content as JSON, then run:

```bash
python3 <skill-dir>/scripts/build_lesson.py <lesson.json> --output <lesson-directory>/index.html
```

Keep the JSON, runnable examples, and generated HTML together in a task-owned output directory. The shell is a starting point, not a ceiling on visual quality. For a topic that needs a different visual grammar, author a bespoke lesson in that output directory using the same teaching and verification criteria; do not modify the installed template or invent graph nodes just to satisfy its schema. A host's inline visualization feature may supplement the lesson when available; it is not required. Do not require a website account or deployment for a local lesson.

## Make examples honest and useful

For code topics, provide runnable source, prerequisites, an exact run command, expected result, and actual validation evidence. Run the example when tools permit. A browser animation of a program is a model unless driven by real execution. Prefer actual recorded traces or a deterministic model checked against the runnable example. Label modeled sequencing and omissions beside the visual.

For non-code topics, use explicit inputs, assumptions, a reproducible calculation or worked case, and a meaningful variation. Distinguish observed data, sourced facts, generated examples, and simulations. A limitation belongs next to the claim it limits.

Include optional prediction prompts, an adaptation challenge, and a broken or counterexample case. Offer hints before solutions. Exercises must require reasoning or transfer, not repeating a definition. Deliver the complete explanation even if the learner chooses not to answer. Never report mastery merely because they viewed a lesson.

## Verify and deliver

Run the JSON builder and any new or changed example scripts. Check that an adaptation produces the expected change and the failure case exposes the intended misconception. Inspect the rendered artifact at desktop and narrow widths. Exercise navigation, play/pause, variants, hints, and source links. Verify both panes show the same concept and step, the final step is reachable, text is not clipped, and reduced motion preserves meaning.

If a browser or runtime is unavailable, run possible checks and state which remain unperformed. Structural validation cannot establish teaching quality or factual truth.

Return the lesson, the runnable example when applicable, and a concise description of what the learner can explore. Show the lesson in the available local preview. Keep source citations near the concepts they support. Explain how to invoke this skill again when useful. Publishing, installing software, and connecting external accounts are separate actions unless requested.

For follow-up questions, continue from the existing lesson and refine the relevant concept, example, or visual. Preserve original source files. Do not silently claim long-term learner memory: use explicitly saved lesson notes when the user asks to retain progress.

## Reference implementation

`examples/agent-skills/` is a worked lesson and quality benchmark. Consult it when an example of the content format is useful; do not load its whole subject matter for unrelated topics. It includes a real small skill, deterministic helper, sample inputs, and verification evidence. Its product-specific facts have a research date and need refreshing when reused.
