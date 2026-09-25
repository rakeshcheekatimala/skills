# Skills

Reusable Agent Skills distilled from real project work. Install them with the [skills CLI](https://github.com/vercel-labs/skills) for supported coding agents such as Codex, Claude Code, and Cursor.

## Available skills

- [`answerlint-maintainer`](answerlint-maintainer/SKILL.md): Maintain and extend AnswerLint across audits, scoring, crawling, CLI commands, reports, `llms.txt`, the local TUI, CI, dependency security, releases, and capability documentation.
- [`audit-agent-skill-packages`](audit-agent-skill-packages/SKILL.md): Audit skill packages for specification compliance, deterministic security and privacy findings, simulated behavioral risk, and scoped trust decisions.
- [`build-evidence-gated-agent-workflows`](build-evidence-gated-agent-workflows/SKILL.md): Build agent workflows that collect attributable evidence, verify claims, apply deterministic gates, expose progress, and require approval before material side effects.
- [`deploy-nextjs-opennext-cloudflare`](deploy-nextjs-opennext-cloudflare/SKILL.md): Configure and verify Next.js/OpenNext applications for Cloudflare Workers with correct runtime boundaries, bindings, previews, and deployment evidence.
- [`no-dash-style`](no-dash-style/SKILL.md): Write or rewrite prose without unnecessary hyphens or dashes while preserving commands, code, paths, and technical names.

Each skill keeps its triggering metadata and core workflow in `SKILL.md`, with task-specific details loaded from `references/` only when needed.

## Browse and install

You need Node.js, npm (which includes `npx`), and Git.

List the skills available in this repository without installing them:

```bash
npx skills add rakeshcheekatimala/skills --full-depth --list
```

Install a skill for the current project:

```bash
npx skills add rakeshcheekatimala/skills --full-depth --skill no-dash-style
```

Install it for your user account across projects:

```bash
npx skills add rakeshcheekatimala/skills --full-depth --skill no-dash-style --global
```

Replace `no-dash-style` with any name in the catalog above. Use `--agent codex`, `--agent claude-code`, or another supported agent to choose a specific target. Without an explicit target, the installer detects agents or prompts you to choose. Keep `--full-depth` to include the skill folders directly under the repository root.

Check your global installations:

```bash
npx skills ls -g
```

Global destinations depend on the agent. Common defaults are `~/.codex/skills/`, `~/.claude/skills/`, and `~/.cursor/skills/`. With symlink installation, these locations may point to a shared copy. The installer reports the actual destinations.

## Use a skill

Ask your agent to use the installed skill, for example:

```text
Use the no-dash-style skill for the prose in this task. Preserve technical syntax.
```

Installation makes a skill available; it does not force the agent to apply it to every response. Some skills describe workflows that require tools or services available in the target environment. See the [CLI documentation](https://github.com/vercel-labs/skills) for supported agents and options.

## Maintain this catalog

Keep one folder per skill with a `SKILL.md` that begins with YAML metadata:

```yaml
---
name: example-skill
description: Explain what the skill does and when to use it.
---
```

The `name` should match its folder. Add a catalog link above whenever you add a skill. Optional `agents/openai.yaml` files provide display metadata for compatible interfaces.

Before publishing, run from the repository root:

```bash
npx skills add . --full-depth --list
```

Confirm that every intended skill appears without metadata warnings. Commit and push the changed files to GitHub, then rerun the repository listing command above. Remote installs read the published repository, so local edits are unavailable to other users until they are pushed. An npm package is not required.
