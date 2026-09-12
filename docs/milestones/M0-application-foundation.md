# M0 — Application foundation

- Status: Approved
- Last Updated: 2026-09-12
- Related Milestone: M0
- Authority: Approved M0 scope, exclusions, and acceptance criteria
- Implementation: Not started; no acceptance checks executed

## Purpose

Establish a small Bluebird application shell and development foundation on the
existing Next.js starter. This specification authorizes implementation only
through a separate scoped implementation task from the owner.

## Required Reading

1. Applicable [AGENTS.md](../../AGENTS.md) instructions.
2. [Documentation map](../README.md).
3. [Project direction](../../PROJECT_DESIGN.md#product-direction) and
   [Workflow and UX](../../PROJECT_DESIGN.md#workflow-and-ux).
4. [Source adapters and dependency boundaries](../architecture/foundation.md#source-adapters-and-dependency-boundaries).
5. Existing `src/app/` layout/page/styles, package scripts, and relevant config;
   consult installed framework documentation as AGENTS.md requires.

No Progress contract, ownership ADR, brainstorm, or historical milestone is
needed to implement this shell. If a change would need business/ownership rules,
check scope before expanding the reading list.

## Scope

- Bluebird application shell with base layout, typography, and a small consistent
  visual language.
- Minimal navigation between the shell entry and an empty Project Workspace
  preview; exact route names are implementation choices, not business identity.
- Clearly label the workspace as an empty preview, not an existing saved project.
- Use real navigation for destinations that exist, with readable empty-state text.
- Apply documented dependency boundaries without creating unused domain layers.
- Build/lint verification and desktop/mobile and keyboard navigation sanity.

Do not add decorative dashboards, fictional project records, disabled menus for
the full roadmap, or controls that pretend to save data.

## Explicit exclusions

Project CRUD; database/persistence (including browser-based project storage);
authentication; workspace-management UI; Progress or Cost engines; Schedule
Import or P6/MSP parsing; BOQ; Progress Update; Dashboard/reporting;
billing/subscriptions.

No business models, migrations, parser scaffolds, service frameworks, or
infrastructure are required for this shell.

## Acceptance criteria

- The existing starter is adapted rather than replaced with another application.
- The entry and workspace-preview routes open directly and survive browser
  refresh; visible navigation works in both directions.
- Page titles/headings and empty-state language identify Bluebird and make clear
  that no project data has been created.
- At representative desktop and mobile widths, text/navigation remain usable
  without clipped content or unintended horizontal overflow.
- Interactive navigation is keyboard reachable, has visible focus and meaningful
  labels, and can be activated without a mouse; semantic navigation/headings are used.
- Existing `npm run lint` and `npm run build` complete successfully.
- No excluded feature, persistence dependency, or unused architectural layer is added.

Record actual command outcomes and short layout/keyboard observations when M0
is implemented. Do not report these checks as passed during documentation work.
A deployable build is required; a new production deployment is not implied by
this specification.

## Delivery

Deliver the focused changed files and verification results under the Git/delivery
authorization of the implementation task. Reserve tags for meaningful stable
releases, not every milestone or review. Do not advance to M1 automatically.
