# Documentation map

- Status: Approved
- Last Updated: 2026-09-20
- Authority: Documentation ownership, lifecycle, and reading rules

## Collaboration entry points

- [Coordinator Contract](COORDINATOR_CONTRACT.md) — roles, product discussion, acceptance briefing and Git authority
- [Engineer Contract](ENGINEER_CONTRACT.md) — standing engineering boundaries
- [Engineer Workflow](ENGINEER_WORKFLOW.md) — task execution and read order

These Bluebird-owned documents implement the approved collaboration model;
product, architecture and milestone authority remain in their existing homes.

## Current entry points

- [Product direction](../PROJECT_DESIGN.md)
- [Architecture foundation](architecture/foundation.md)
- [Workspace ownership ADR](architecture/decisions/ADR-001-workspace-ownership.md)
- [Progress contract](features/progress-contract.md) — approved constraints; not implemented
- [M0 specification](milestones/M0-application-foundation.md) — implemented and merged; historical acceptance evidence retained

- [F0 proof and acceptance](milestones/F0-file-workbook-proof.md) — Desktop Excel accepted by Product Owner; deployed runtime gate outstanding

## One authoritative home for each rule

| Home | Responsibility |
| --- | --- |
| docs/COORDINATOR_CONTRACT.md and docs/ENGINEER_CONTRACT.md | Roles, authority and standing collaboration boundaries |
| docs/ENGINEER_WORKFLOW.md | Engineer execution procedure; not product requirements |
| Accepted engineering notes (when present, linked by the relevant milestone) | Reusable accepted knowledge and baseline; reference canonical rules rather than redefine them |
| Source code and tests | Current executable implementation evidence; not automatic product approval |
| Root PROJECT_DESIGN.md | Product vision, scope, major direction, and high-level product decisions |
| docs/brainstorm/ | Exploration only; never implementation authority |
| docs/architecture/ | Current technical architecture and constraints |
| docs/architecture/decisions/ | Significant architectural decisions, alternatives, and rationale |
| docs/milestones/ | Approved delivery scope, exclusions, and acceptance criteria |
| docs/features/ | Current business contracts for implemented or actively designed capabilities |
| docs/guides/user/ | User instructions; no new business rules |
| docs/guides/developer/ | Development, testing, deployment, and maintenance |
| docs/archive/ | Superseded material retained for historical usefulness; never authority |

Create directories only when useful content exists; guides and archive need not
exist yet. Root README currently owns the short local development instructions.
Move those instructions into a developer guide only when needed, replacing the
original content with a link.

A topic may be mentioned in several documents, but normative rules must be
maintained once. Reference the canonical section elsewhere. Milestones and guides
must not redefine product, feature, or architecture rules.
On conflict, identify the owning document and resolve with the product owner;
never use "newest file wins." Implementation that disagrees with an approved
contract is a discrepancy to resolve, not an automatic new source of truth.

## Status and lifecycle

Use a short header: Status, Last Updated, and Authority when useful.
Add Related Milestone only when relevant.

- Draft: incomplete proposal.
- Review: ready for owner review, not approved implementation scope.
- Approved: accepted rules or scope; does not mean implemented.
- Superseded: replaced; include a direct replacement link.
- Archived: historical only.

For a feature or milestone, add a short implementation state when necessary.
This keeps approval separate from delivery and acceptance.
Completed milestones retain their scope and acceptance evidence as history;
they are not the canonical description of current feature behavior.

Ideas may lead to decisions; decisions update the owning product, architecture,
or feature document; milestone specs reference those decisions; implementation
updates the affected current contract and relevant guidance.
Do not require every idea to produce an ADR or a full chain of documents.

Use an ADR for consequential alternatives or costly-to-reverse decisions.
Do not create one for every field, component, or routine convention.
Keep superseded ADRs in place with replacement links. Archive other superseded
material only when useful; remove it from default reading lists.
Start with one document per capability, splitting only when useful, not per milestone.

## Reading strategy for future Work

Start with applicable repository instructions and this map, then follow the
[Engineer Workflow read order](ENGINEER_WORKFLOW.md#2-discover-authority-before-implementation).
Read accepted notes before fresh investigation and verify only relevant repository
deltas. The current authorized task and its milestone determine the necessary scope.

Each milestone must contain Required Reading with direct paths/sections.
A Review-status specification is not implementation authorization.
Do not require whole-repository or whole-documentation rereads.
Read brainstorms, archives, and historical review prompts only when explicitly
requested. Add targeted context only when a concrete dependency requires it.

After work, update only affected canonical documents and the milestone's
implementation/acceptance evidence; link instead of repeating rules.
Goal: minimum necessary context, one source of truth, no repeated documentation.

## Historical exploration — opt-in only

[Original Bluebird brainstorm](brainstorm/BLUEBIRD_BRAINSTORM.md) preserves
pre-consolidation ideas and review instructions. Its internal "Agreed" labels
do not override the current canonical documents.
