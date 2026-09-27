# Documentation map

- Status: Approved
- Last Updated: 2026-09-27
- Authority: Documentation ownership, lifecycle, and reading rules

## Current accepted state and current task

- Accepted product: F2 — XML Amount Weighting, PO accepted / merged / closed; [closure evidence](milestones/F2-xml-amount-weighting.md#po-closure-record--2026-09-27).
- Accepted product revision: main `7ed9eef77a88d23bc13c92fe94d6251551c57d7f`. This is not a claim about the latest repository HEAD.
- Current task: `WF-20260927` — Durable Project Knowledge / Workflow Refinement.
- Mode / input baseline: documentation implementation only / the accepted product revision above.
- State: awaiting review/action — engineering handoff prepared; PO acceptance of these changes remains open.
- Owner / next actor: Engineer owns the handoff; Coordinator briefs PO, then PO decides acceptance.
- Authorization / scope: PO authorization dated 2026-09-27, recorded [below](#workflow-refinement-authorization--2026-09-27).
- Latest handoff: `BLUEBIRD_WORKFLOW_REFINEMENT_REPORT.txt` and `BLUEBIRD_WORKFLOW_REFINEMENT_CHANGED_FILES.zip`, delivered together in ChatGPT Library, folder `Bluebird`; resolve by exact filename. No incomplete checkpoint is pending.
- Next action: Coordinator reviews the delivered report/files and requests PO acceptance; Git requires separate explicit authorization.
- Not authorized by this task: Structure/Readability, F3–F6, Dashboard polish, ENG/THA product changes, Git or deployment. [Sequence and milestone boundaries](milestones/file-workbook-roadmap.md).
- Procedure trial: next two real authorized engineering tasks after adoption; no task completions counted yet. [Trial procedure](ENGINEER_WORKFLOW.md#two-task-procedure-trial).

Coordinator maintains this compact state under the [state/closure responsibility](COORDINATOR_CONTRACT.md#current-state-and-closure-responsibility).
Gate evidence belongs to its milestone/task report; business and architecture rules remain in their canonical homes.
This handoff is not yet integrated. Artifact filenames identify external deliveries, not repository-relative files.

## Collaboration entry points

- [Coordinator Contract](COORDINATOR_CONTRACT.md) — roles, product discussion, acceptance briefing and Git authority
- [Engineer Contract](ENGINEER_CONTRACT.md) — standing engineering boundaries
- [Engineer Workflow](ENGINEER_WORKFLOW.md) — task execution and read order

These Bluebird-owned documents implement the approved collaboration model;
product, architecture and milestone authority remain in their existing homes.

## Current entry points

- [F2 XML Amount weighting](milestones/F2-xml-amount-weighting.md) — scope, Policy A and dated closure evidence
- [Product direction](../PROJECT_DESIGN.md)
- [Architecture foundation](architecture/foundation.md)
- [Workspace ownership ADR](architecture/decisions/ADR-001-workspace-ownership.md)
- [Progress contract](features/progress-contract.md) — approved F1 business rules; later capabilities partial
- [F1 Core Progress Workbook](milestones/F1-core-progress-workbook.md) — scope and dated acceptance evidence
- [M0 specification](milestones/M0-application-foundation.md) — implemented and merged; historical acceptance evidence retained

- [F0 proof and acceptance](milestones/F0-file-workbook-proof.md) — accepted / closed per Product Owner; historical evidence retained

- [Approved F1–F6 delivery sequence](milestones/file-workbook-roadmap.md) — sequence and milestone intent approved; detailed specifications and implementation authorization remain separate

## One authoritative home for each rule

| Home | Responsibility |
| --- | --- |
| docs/README.md current-state block | Current accepted product revision and current task navigation; not business rules |
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

## F1 authorization update — 2026-09-23

Historical authorization is retained in the [roadmap record](milestones/file-workbook-roadmap.md#historical-f1f2-authorization-record--2026-09-23-and-2026-09-26). Use the current-state block above for live authorization.

## Workflow refinement authorization — 2026-09-27

PO accepted Decisions 1–3 from `BLUEBIRD_AGENT_WORKFLOW_REVIEW.txt`
(ChatGPT Library, Bluebird folder; investigation record `libfile_dfb42debcad88191811d9ed10cf3260f`).
This dated record captures the authorized scope, not acceptance of the delivered edits:

- Refine this index, Engineer Workflow and Coordinator Contract; clean stale/live status only in PROJECT_DESIGN, the file-workbook roadmap, F1/F2 milestones and architecture foundation.
- Adopt recoverable checkpoints using engineering judgment, with no mandatory duration or quota-based time boxes.
- Trial existing procedures on two subsequent authorized engineering tasks before considering standalone skills; capture only meaningful evidence in normal handoffs.
- No new repository files/framework, product/runtime/test changes, Paperclip dependency, infrastructure, Git or deployment; no product milestone implementation.
- Deliver complete changed files/manifest and TXT report, validate links/state/authority/history, then stop for PO review.

Approved workflow details live in the linked contracts/procedure, not in the earlier investigation's illustrative scheduling examples.
