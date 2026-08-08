---
name: deploy-nextjs-opennext-cloudflare
description: Configure, migrate, review, or verify Next.js App Router applications deployed to Cloudflare Workers through @opennextjs/cloudflare. Use when adding OpenNext and Wrangler configuration, separating build-time public variables from Worker or backend-provider secrets, configuring assets, R2 incremental cache or service bindings, previewing Workers locally, hardening deployment checks, or diagnosing Cloudflare-specific build and runtime failures.
---

# Deploy Next.js with OpenNext on Cloudflare

Treat package versions and current official documentation as authoritative. Next.js, OpenNext, Wrangler, and Workers compatibility changes quickly; do not copy configuration from an older project without verifying it.

## Inspect before changing configuration

1. Read the repository's `AGENTS.md` and other local instructions.
2. Inspect `package.json`, the lockfile, `next.config.*`, `open-next.config.*`, `wrangler.jsonc`, environment examples, deployment docs, and existing CI.
3. Read the installed Next.js documentation required by the repository and the current official Cloudflare, Wrangler, and OpenNext documentation.
4. Activate any available Cloudflare, Workers best-practices, and Wrangler skills for current platform guidance.
5. Map the application topology: browser, Next.js Worker, external backend, data stores, queues, caches, and the runtime that makes each outbound call.

Read `references/deployment-checklist.md` when creating the environment map, reviewing bindings, diagnosing a failure, or preparing deployment evidence.

## Separate configuration by runtime

Classify every value before adding it:

- Put browser-visible `NEXT_PUBLIC_*` values in the build environment. They are inlined at build time and are not secrets.
- Put Worker runtime secrets in the Cloudflare secret store, never in `wrangler.jsonc` or committed environment files.
- Put external-backend secrets in that backend's deployment environment when the backend makes the call. Do not duplicate them into the frontend Worker.
- Put non-secret runtime configuration in Wrangler variables only when the Worker reads it at runtime.
- Declare bindings for R2, KV, D1, services, queues, or other resources only when application or adapter code uses them.

Document where each value lives without including its real value. Keep local examples as placeholders.

## Build version-compatible configuration

Use the repository's package manager and keep the lockfile consistent. Add scripts for the current adapter commands: build, local preview, deploy, and Wrangler type generation. Keep a normal `next build` script when the project also needs framework-native validation.

Generate `open-next.config.*` with only the overrides the application requires. Add incremental cache configuration only when the app uses ISR and the current adapter documentation requires it.

Generate or update `wrangler.jsonc` from the current schema. Verify:

- `main` matches the worker file actually emitted under `.open-next/`;
- the compatibility date and flags are supported by the installed stack;
- the assets directory and binding match the adapter output;
- observability is configured intentionally;
- binding names match both code and adapter expectations;
- no duplicate binding points at the same resource under unexplained names;
- a self-reference service binding exists only when the current adapter feature needs it.

Do not guess R2 incremental-cache binding names from memory. Confirm them against the installed adapter and current documentation.

## Verify before deployment

Run the repository's tests, typecheck, lint, framework build, OpenNext build, and type generation as applicable. Inspect generated output and configuration warnings. Start a local OpenNext/Workers preview and smoke-test static assets, server rendering, API routes, authentication callbacks, database access, and cache behavior that the app actually uses.

Check the repository diff and history for committed credentials, production connection strings, or copied command examples containing live values. Verify that `.env.local` and equivalent secret files are ignored.

Do not deploy merely because the build passes. Confirm required Cloudflare resources and secret names exist in the target environment, and confirm build-time public variables were present during the OpenNext build.

## Deploy and verify the result

Deploy only when the user explicitly requests the external change. Record the Worker name, target environment, version or deployment ID, and public URL. Then test HTTPS, static assets, one server-rendered route, one API route, authentication behavior, and each critical external binding.

If a smoke test fails, preserve the deployment evidence and diagnose before retrying. Never rotate, replace, or reveal a secret as an implicit troubleshooting step.
