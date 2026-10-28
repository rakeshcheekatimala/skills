---
name: note-brief
description: Turn supplied study notes into a concise brief and unanswered questions. Use when the user asks to summarize their notes; do not use for independent topic research.
---

# Note Brief

Read the notes supplied by the user. If no notes are supplied or accessible, ask for them.

Read `references/brief-rules.md` to distinguish stated facts from missing information. Use the structure in `assets/brief-template.md` to write the brief. Preserve uncertainty; do not invent answers to fill gaps.

For a saved brief, check its length using Python 3:

```bash
python3 <skill-dir>/scripts/check_brief.py <brief.md> --max-words 80
```

The script counts whitespace-separated tokens, including Markdown markers. If over the limit, shorten the brief without dropping material qualifications, then check again. Return the brief and its unanswered questions. A passing word count does not verify the facts.
