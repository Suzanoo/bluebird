# Bluebird

Start with [Project Design](PROJECT_DESIGN.md) for product direction and the
[documentation map](docs/README.md) to find authoritative rules and the current task.

The repository has an existing Next.js starter. The
[M0 application foundation specification](docs/milestones/M0-application-foundation.md)
is prepared for review; its application work has not started.

## Local development

Use the repository's npm lockfile:

```bash
npm ci
npm run dev
```

Open http://localhost:3000. The App Router source is under `src/app/`.

Existing checks:

```bash
npm run lint
npm run build
```

Before changing application code, follow [AGENTS.md](AGENTS.md), including its
instruction to consult the installed Next.js documentation. This documentation
delivery does not run or certify an application build or deployment.
