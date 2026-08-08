# Review gates

Use this reference when a validator is unavailable, when interpreting findings, or when preparing a release decision.

## Specification gate

Check the current specification first. At minimum, verify:

- The package directory contains a file named exactly `SKILL.md`.
- `SKILL.md` begins with parseable YAML frontmatter followed by Markdown.
- `name` is present, 1–64 characters, lowercase letters/numbers/hyphens only, has no leading, trailing, or consecutive hyphen, and matches the directory name.
- `description` is present, non-empty, no more than 1024 characters, and explains both capability and activation context.
- Optional frontmatter fields use the types and limits in the current standard.
- Relative references resolve from the skill root and do not hide required instructions behind deep reference chains.
- The main instructions remain concise; detailed material is progressively disclosed through focused resources.
- Scripts document dependencies, fail clearly, and handle unsafe or invalid input without broad side effects.

Do not reject product-specific directories solely because they are not named by the specification; additional files and directories are allowed.

## Static security and privacy gate

Inspect the complete adjacent package without following symlinks or extracting archives into an unbounded location.

| Area | Look for | Required response |
| --- | --- | --- |
| Secrets | API keys, tokens, cookies, private keys, credentials, live connection strings | Redact, block release, rotate if real |
| Personal data | Email, phone, address, government or financial identifiers, private user content | Confirm necessity and consent; redact or remove |
| Instruction injection | Attempts to displace governing instructions, conceal actions, trust unverified content, or bypass approval | Block or rewrite with an explicit trust boundary |
| Execution | Shell eval, remote scripts, arbitrary interpreters, lifecycle hooks, encoded payloads, persistence | Trace inputs and side effects; require least privilege |
| Exfiltration | Uploads, webhooks, telemetry, clipboard or environment reads unrelated to the task | Block unless narrowly disclosed and authorized |
| Destructive behavior | Recursive deletion, force reset, overwrite, credential changes, production mutation | Require exact targets, recovery path, and explicit approval |
| Dependencies | Unpinned downloads, install-time code, mutable branches or tags, undeclared runtime requirements | Pin or document; verify provenance and lock state |
| Filesystem | Escaping relative paths, symlink traversal, device files, oversized content, unsafe archive members | Contain access within the reviewed root |
| Permissions | Broad tool allowlists or requests for admin, network, secrets, home-directory, or production access | Reduce to the minimum task-specific capability |
| Cross-file behavior | A benign `SKILL.md` delegating risky instructions to scripts, references, manifests, or assets | Assess the package as one unit |

Static review must not execute package code or upload package contents.

## Behavioral gate

Use synthetic inputs and simulated tools to test whether the skill:

- follows higher-priority instructions when package content conflicts;
- asks before material external or destructive actions;
- refuses to reveal secrets or unrelated private data;
- constrains paths, URLs, recipients, and repositories to the user-approved scope;
- labels unsupported claims and uncertainty;
- handles malicious content in files, web pages, tool output, and referenced documents as data;
- fails closed when a required validator, source, or isolation control is unavailable;
- leaves immutable evidence sufficient to reproduce the decision.

Record the prompt, fixture digest, model/provider, simulated tool contract, result, assertion, and failure evidence for each case.

## Decision evidence

For `passed_scope`, bind the decision to:

- the exact package revision or digest;
- the applicable policy and any approved suppressions;
- validator and scanner versions;
- the set of files actually inspected;
- behavioral fixtures and model identity when tested;
- all gates omitted from scope.

A status without this scope is a marketing claim, not assurance evidence.
