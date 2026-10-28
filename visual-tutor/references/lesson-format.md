# Authoring a lesson

Create `lesson.json` beside its generated `index.html`. Put example files in a subdirectory, with documented commands relative to the lesson directory. The builder validates references and embeds data safely. It does not execute the examples, verify facts, or judge teaching quality.

Use plain text in all content fields. The renderer inserts text as text, not HTML or Markdown. It preserves code whitespace and adds line numbers. Each concept has its own diagram and scenarios. The bundled renderer uses labeled nodes and directed edges with normalized positions; it is appropriate for flows and relationships. For other subjects, extend the renderer to use a representation that actually explains the mechanism.

## Root object

- `version`: `1`.
- `title`, `subtitle`, `outcome`: concise text explaining the topic and learner outcome.
- `research_date`: `YYYY-MM-DD`.
- `scope`: `prerequisites`, `includes`, and `boundaries`, each a list of text items. State explicit assumptions and omitted adjacent subjects.
- `sources`: list of `{id, title, url}` with stable unique identifiers and HTTP(S) primary-source links. An empty list is allowed when sources are unavailable; disclose that in the lesson.
- `chapters`: concept objects, normally in dependency order, covering the levels `Foundations`, `Intermediate`, and `Advanced`.
- `resources`: optional list of `{label, path}`. Paths must be relative files inside the lesson directory. The builder checks their presence relative to the output HTML.

## Concept object

```json
{
  "id": "why-skills",
  "level": "Foundations",
  "title": "Why package instructions?",
  "why": "You keep explaining the same procedure in new conversations.",
  "explanation": ["Start with the reusable task...", "Derive the need for a stored procedure..."],
  "example": {
    "label": "A recurring task",
    "language": "text",
    "code": "Summarize these notes.\nPreserve unanswered questions.",
    "evidence": {"kind": "model", "note": "Illustrative task; no agent run is claimed."}
  },
  "diagram": {
    "label": "Instructions guide the work",
    "note": "Conceptual model, not an internal runtime trace.",
    "nodes": [
      {"id": "request", "label": "Request", "detail": "The user's goal", "x": 20, "y": 50},
      {"id": "agent", "label": "Agent", "detail": "Uses instructions", "x": 80, "y": 50}
    ],
    "edges": [{"id": "guide", "from": "request", "to": "agent"}]
  },
  "steps": [
    {"title": "State the task", "text": "The request identifies the desired result.", "active": ["request"], "lines": [1]},
    {"title": "Guide the work", "text": "The instructions constrain how the agent prepares that result.", "active": ["agent"], "edges": ["guide"], "lines": [2], "values": {"agent": "Preserves unknowns"}}
  ],
  "variants": [],
  "deep_dive": [{"title": "Where this model stops", "text": "Selection and execution depend on the host."}],
  "exercise": {"prompt": "What changes if the instructions omit uncertainty?", "hint": "Consider gaps in the notes.", "solution": "The output has less guidance for preserving unknowns; test that behavior rather than assuming it."},
  "sources": ["skills-spec"]
}
```

This is one concept, not a complete three-level lesson. Replace example language with researched, substantive content; do not ship instructional placeholders.

## States and variations

Each `steps` entry updates both panes. `active` lists highlighted nodes, `edges` lists highlighted edges, and `lines` gives one-based example line numbers. `values` optionally changes node details; changes accumulate within the scenario until replaced by another step. Moving backward reconstructs the values at that earlier step. Changing scenarios resets the values to the diagram's defaults. The final step should show a concrete result or conclusion.

A `variants` entry contains `name`, a full `steps` list, and optionally a replacement `example`. Reuse node identities when the same entities participate. A variant without `example` inherits the main example; make the text and highlights consistent with that choice. Use changed inputs, failure cases, or counterexamples, not cosmetic variations. At least one adaptation and one diagnostic case should appear across the lesson.

Node coordinates are percentages, between 15 and 85. Common layouts are two columns at x=22/78 or three at x=18/50/82; rows at y=18/50/82. Avoid more than nine nodes in one frame. Keep labels short and details meaningful. Nodes retain stable positions across steps. The shell derives arrow endpoints from rendered node sizes, and respects reduced-motion preference.

## Evidence

- `model`: an illustrative example or simplified simulation. Name what is omitted.
- `sourced`: a documented pattern not executed in this lesson. Cite its source on the concept.
- `executed`: a real observed run. Requires `command`, `output`, and `note`. Preserve the output from the run; do not fill it with an anticipated result. If the visual is a manual reconstruction, say so in `diagram.note`.

`example.file` optionally links the downloadable runnable source. The renderer does not run arbitrary Python, shell, or agent instructions in the browser. A scenario control changes the model, not the actual environment. State this clearly.

## Build and inspect

```bash
python3 <skill-dir>/scripts/build_lesson.py lesson.json --output index.html
python3 <skill-dir>/scripts/build_lesson.py lesson.json --output index.html --check
```

Open the output directly or serve the lesson directory locally. Inspect desktop and narrow layouts, step changes, scenario changes, all navigation, the last step, reduced motion, exercises, sources, and example links. Compare modeled results against real runs where applicable. Never claim browser or execution checks that were not performed.
