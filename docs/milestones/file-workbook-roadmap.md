# File-oriented workbook delivery sequence

- Status: Approved sequence and milestone intent; detailed specifications pending
- Last Updated: 2026-09-21
- Authority: Delivery order and milestone boundaries; not business-rule ownership
- Implementation: F0 accepted; F1 authorized 2026-09-23; F2–F6 not started/unauthorized
- Decision source: PO Acceptance of Revised Milestone Proposal, 2026-09-21

## Required reading

- [Repository instructions](../../AGENTS.md) and [documentation map](../README.md)
- [Engineer Contract](../ENGINEER_CONTRACT.md) and [Workflow](../ENGINEER_WORKFLOW.md)
- [Product direction](../../PROJECT_DESIGN.md#accepted-product-alignment-2026-09-21)
- [Progress contract](../features/progress-contract.md)
- [Architecture foundation](../architecture/foundation.md)
- [Accepted F0 evidence](F0-file-workbook-proof.md#current-accepted-state--recorded-2026-09-21)

## Approval boundary

The Product Owner accepted F1 → F2 → F3 → F4 → F5 → F6, including Earned Value
before Payment. This supersedes the earlier M1–M9 delivery order. It does not
approve unresolved edge-case policies, every detail of prior engineering reports,
or commencement of any milestone. Obtain a scoped specification and explicit
implementation authorization before starting each milestone.

Product scope lives in Project Design; weighting, monetary meaning and reporting
rules live in the Progress contract. Refer to them rather than redefining them here.

## Approved sequence and intended user value

| Milestone | Intended result | Boundary / dependencies |
| --- | --- | --- |
| F1 — Core Progress Workbook + Landing A | Landing presentation and XML → weekly Main, Monthly, Dashboard/S-curves and Activity Amount workbook | Uses accepted F0; Equal/Duration; approved Create configuration and reused PS workbook themes; no Amount method, refresh, BOQ, EV, Payment or Theme Editor |
| F2 — XML Amount Weighting | Explicit XML numeric-field choice, preview/validation and Amount-weighted output | Builds on F1; detailed Amount readiness/source support specification required; no inferred actual cost or post-creation switch |
| F3 — Workbook Refresh / Explicit Apply Amount | Upload saved workbook, preserve inputs and refresh affected output; explicitly apply Amount | Builds on F1/F2; identity, recalculation and history policies required; no arbitrary structural edits or schedule re-import assumed |
| F4 — BOQ Allocation Foundation | Simple workbook-based BOQ allocation for subsequent monetary workflows | Builds on workbook lifecycle; allocation and authority/reconciliation contract required; no full BOQ Studio or universal arbitrary-BOQ importer assumed |
| F5 — Earned Value Workbook | EV output with defined monetary inputs, Status Date and workbook lifecycle | F4 monetary prerequisites and EV specification; no Financial Forecast or Actual Cost inferred from Activity Amount |
| F6 — Payment Workbook Workflows | Payment Input, standard Payment and Payment Breakdown with scoped refresh | After F5 by approved priority; preserve Progress/EV and user inputs; detailed Payment contract required |

F5-before-F6 is delivery priority, not a claim that Payment intrinsically depends
on EV calculations. The earlier review found complete BOQ Mapping is required by
current Progress Studio EV; XML Amount alone does not establish EV readiness.
Any departure requires a separate reviewed decision. Financial Forecast remains
excluded across this sequence. No SaaS infrastructure is introduced.

## Specification and acceptance preparation

Each milestone specification must identify objective/user result, technical scope,
dependencies, exclusions, reusable implementation, expected changed areas and
concrete acceptance criteria. For F1, resolve the applicable
[open Progress rules](../features/progress-contract.md#unresolved-business-rules)
using the PS reference and targeted evidence, not a new whole-repository review.

Keep automated tests, artifact checks, Desktop Excel lifecycle, deployed browser
workflow and PO acceptance separate. Prior F0 acceptance stays closed; changed
rendering/calculation behavior needs its own relevant acceptance. Nothing in this
sequence authorizes Git operations or deployment.

## F1 authorization update — 2026-09-23

PO accepted the [F1 specification](F1-core-progress-workbook.md) and authorized F1 only.
The Progress contract owns final defaults, strict Duration and Live Rebuild
Dashboard Actual display. Earlier pending-authorization statements are historical.
F2–F6, Git operations and deployment remain unauthorized.
