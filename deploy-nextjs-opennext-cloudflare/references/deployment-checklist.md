# OpenNext Cloudflare deployment checklist

Use this checklist with the versions and official documentation discovered from the target repository. It is a reasoning aid, not a source of pinned package versions.

## Environment map

| Value class | Typical location | Rule |
| --- | --- | --- |
| Browser-visible public value | Build environment, often `.env.local` locally | `NEXT_PUBLIC_*` is inlined; assume users can read it |
| Worker secret | Cloudflare secret store | Set by name; never commit the value |
| Worker non-secret setting | `wrangler.jsonc` variables | Keep domains, modes, and public identifiers here |
| External backend secret | Backend provider environment | Store where the outbound call executes |
| Resource binding | `wrangler.jsonc` plus generated types | Name must match code and current adapter contract |
| Local-only credential | Ignored local environment file | Provide a placeholder in `.env.example` |

For every variable, record: name, secret/public classification, runtime owner, local source, production source, build-time/runtime timing, and consumer.

## Configuration review

- Package scripts use the installed OpenNext CLI and repository package manager.
- `open-next.config.*` contains only required overrides.
- `wrangler.jsonc` validates against the installed Wrangler schema.
- Worker entrypoint and assets path exist after the OpenNext build.
- Compatibility settings satisfy the current Next.js/OpenNext requirements.
- Generated Cloudflare types are current when the code consumes bindings.
- Each declared binding has a consumer and each consumer has a declared binding.
- ISR/cache bindings use the exact current adapter names and only one intentional mapping per resource.
- Secrets are absent from tracked files, examples, docs, output logs, and frontend bundles.
- Public variables required during build are present before the OpenNext build starts.
- OAuth callback URLs, application base URLs, and allowed origins match the target environment exactly.

## Preflight sequence

Use the scripts defined by the repository; do not assume command names. A typical sequence is:

1. install from the lockfile;
2. run unit and integration tests;
3. run typecheck and lint;
4. run the normal Next.js production build;
5. run the OpenNext Cloudflare build;
6. generate or verify Wrangler binding types;
7. start the local Workers preview;
8. smoke-test critical routes and bindings;
9. inspect warnings, generated entrypoints, and repository diff;
10. verify remote resources and secret names without printing values.

Treat warnings about compatibility, missing bindings, unsupported Next.js features, or fallback behavior as review items rather than cosmetic output.

## Failure signatures

| Symptom | Investigate first |
| --- | --- |
| Worker entrypoint not found | Adapter output path versus Wrangler `main` |
| Static assets return 404 | OpenNext build completion, assets directory, and assets binding |
| Browser sees an undefined backend URL | Missing `NEXT_PUBLIC_*` value during build, not missing Worker secret |
| Worker cannot read a secret | Secret exists in the wrong Cloudflare environment or under a different name |
| External backend call lacks a key | Secret was placed in the frontend Worker instead of the executing backend |
| ISR works locally but not remotely | Current cache override, exact R2 binding contract, bucket existence, and permissions |
| Database exhausts connections | Runtime-compatible driver, pooling, connection lifetime, and provider limits |
| OAuth callback fails only in production | Exact scheme, host, callback path, cookies, and application base URL |
| Node API fails in Workers | Current compatibility flags and whether the dependency supports Workers |
| Preview succeeds but deployment fails | Remote resource names, environment-specific bindings, account context, and build-time variables |

## Deployment evidence

Record:

- repository revision and lockfile state;
- Node, package manager, Next.js, OpenNext, and Wrangler versions;
- commands and exit status for each preflight check;
- target Cloudflare account/environment and Worker name;
- required binding and secret names, without values;
- deployment ID/version and URL;
- post-deploy smoke-test results;
- known warnings, deferred checks, and rollback path.
