# Bluebird

Start with [Project Design](PROJECT_DESIGN.md) for product direction and the
[documentation map](docs/README.md) to find authoritative rules and the current task.

M0, F0 and [F1](docs/milestones/F1-core-progress-workbook.md) are accepted.
[F2](docs/milestones/F2-xml-amount-weighting.md) adds explicit XML Amount selection
and weighting; its new PO acceptance gates remain open. See the
[F2 acceptance guide](docs/guides/developer/F2-acceptance.md) for integration,
preview/Generate tests and Windows Desktop Excel steps.
See the [F1 acceptance guide](docs/guides/developer/F1-acceptance.md) for full local
Python + Next.js operation. Next.js alone does not serve the converter endpoint.

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
instruction to consult the installed Next.js documentation. Automated tests,
Desktop Excel and deployed browser acceptance are separate gates.
