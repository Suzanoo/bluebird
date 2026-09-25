# Bluebird — Project Design

- Status: Approved
- Last Updated: 2026-09-21
- Authority: Product vision, scope, and high-level product direction
- Stage: M0 merged; F0 accepted; F1 authorized; F2–F6 sequence approved, not started

## Approved file-oriented V1 direction (2026-09-14)

First useful delivery: upload P6/MSP XML, explicitly choose an initial weighting
method, and download a Progress Workbook (.xlsx). The application is free and
file-oriented. Authentication, database/cloud Project persistence, Workspace UI,
teams and billing are deferred. See the [Progress contract](docs/features/progress-contract.md)
for approved weighting and Activity Amount semantics.

The earlier broad scope and M1–M9 sequence below are retained as future planning,
not initial V1 prerequisites. DEC-001 BOQ timing is deferred; Activity Amount input
comes first. DEC-003 applies when persisted Project creation is introduced.
F0 is accepted; its proof assumptions are not universal product rules. F1 now has
an approved delivery specification and explicit implementation authorization
(2026-09-23). The [approved F1–F6 sequence](docs/milestones/file-workbook-roadmap.md)
owns delivery order and milestone intent; the older sequence below is superseded.

## Accepted product alignment (2026-09-21)

The Product Owner approved Landing concept A (Clear Blue): retain Home as app
presentation, followed by the Create workflow. The user journey is
Landing → Upload P6/MSP XML → Configure → Generate → Download Progress Workbook.
The target users are construction engineers/planners preparing progress workbooks
for normal Desktop Excel use. The target workbook outcome follows Progress Studio,
delivered incrementally; it is not limited to the F0 proof output.

Earned Value and Payment remain in the approved delivery direction. Financial
Forecast is excluded. Reuse Progress Studio workbook themes; defer the Theme Editor.
Web branding and workbook styling are separate concerns. Concept imagery is a
layout reference, not approval of every illustrated field or feature.

Create configuration includes Weighting, Weekly Cutoff Day and Plan Distribution.
Their business semantics and unresolved defaults belong to the
[Progress contract](docs/features/progress-contract.md). No new persisted Project,
account, database or cloud storage is required by these controls.

Approval of this direction and milestone order does not approve unresolved
edge-case policies, implementation details or immediate execution of F1.

## Product direction

Bluebird is a construction management web application focused primarily on
**Progress**, **Cost**, and future integration between them. It grows from practical
construction workflows; it is not intended to reproduce P6, Microsoft Project,
or a full ERP.

**Document Management is currently out of scope**, including RFI, submittals,
drawing/document control, transmittals, NCR, safety, and photo management.

Progress is the first delivery focus. EV and Payment follow in the approved
file-workbook sequence; their detailed contracts remain to be specified.
Other Cost candidates are not approved modules; Financial Forecast is excluded.

## Product scope

The file-oriented product delivers schedule ingestion, progress weighting,
workbook Actual inputs, weekly/monthly workbook reporting and a workbook Dashboard,
followed by the capabilities in the approved delivery sequence. XLSX is the output;
detailed calculation and output contracts remain subject to feature specifications.
Persisted project creation/configuration and web-native progress management remain
future scope, not prerequisites for the initial file workflow.

Planned schedule inputs are P6 XML and MSP XML. Native Microsoft Project
`.mpp` support remains a feasibility/scope question, not a V1 commitment.
Round-trip schedule export is not part of the initial import delivery;
preserving identity does not constitute an export guarantee.

### DEC-001 — BOQ workbook approach (after core Progress; see F4)

Users may upload an existing BOQ workbook. If they have none, Bluebird exports a
standard workbook template, the user completes it externally, and uploads it.
A native BOQ editor is excluded initially to keep the delivery focused.
BOQ must not block useful Progress operation.

Earned Value and Payment are sequenced in the approved roadmap and still require
separate detailed specifications. A BOQ Dashboard and native BOQ management remain
future possibilities, not approved initial capabilities.

## Workflow and UX

Earlier persisted-project concept only; not the current file workflow:

Create Project → Configure Project → Import Schedule → Resolve Progress Weighting
→ Progress Dashboard / Native Progress Update → BOQ / Mapping.

The current file workflow and Landing direction are defined above. Detailed
appearance controls beyond the reused workbook theme remain deferred; desktop
dialogs and navigation trees are not automatically web requirements.

### DEC-003 — Minimal Project Creation (future persisted Projects)

Creating a Project requires only these two user-facing fields:

- Project Name — required.
- Project Code — required.

All other project information and configuration belongs after project creation
in Project Configuration. Its detailed field contract remains TBD until the
relevant feature design.

Internal identity and ownership follow the
[architecture foundation](docs/architecture/foundation.md#project-identity) and
[Workspace ownership decision](docs/architecture/decisions/ADR-001-workspace-ownership.md);
they do not introduce additional user-facing creation fields.

For the approved reporting and weighting rules, use the
[Progress contract](docs/features/progress-contract.md).
For ownership and identity, use the
[architecture foundation](docs/architecture/foundation.md).

## Open product questions

- Detailed output parity/acceptance for each milestone in the approved sequence.
- Detailed validation of Project Name/Code and Project Configuration fields;
  the two required creation fields are settled by DEC-003.
- Detailed BOQ template/validation and mapping workflow.
- Output contracts and detailed Progress Update UX.

Reporting/business TBDs have their single home in the
[Progress contract](docs/features/progress-contract.md#unresolved-business-rules).
Technical TBDs are tracked in the
[architecture foundation](docs/architecture/foundation.md#decision-timing).

## DEC-002 — Living requirements and authority

This document remains editable as decisions evolve. An Approved status applies
to explicit decisions, not to sections labeled conceptual, candidate, or TBD.
Unknown rules must not be guessed.

Detailed technical decisions, feature contracts, and milestone scope have their
own authoritative homes under the [documentation map](docs/README.md).
They are referenced here rather than copied into a growing all-purpose document.
Product owners approve changes to product/business direction.

## Earlier M0–M9 roadmap — future planning, sequencing superseded

This table retains M0–M9 as a high-level planning sequence, not authorization
to implement all milestones.

| Milestone | Direction |
| --- | --- |
| M0 | Application foundation — [approved specification](docs/milestones/M0-application-foundation.md) |
| M1 | Project management and required persistence |
| M2 | Schedule import |
| M3 | Progress engine |
| M4 | Native progress update |
| M5 | Progress Dashboard and reporting |
| M6 | Cost foundation; separate design required |
| M7 | BOQ and mapping; separate design required |
| M8 | Progress/Cost integration; separate design required |
| M9 | Overall production readiness and hardening |

Production readiness is incremental, governed by the
[decision timing gates](docs/architecture/foundation.md#decision-timing);
M9 is not the starting point for those concerns.

## Consolidation record

2026-09-12: broadened the original schedule-first vision; clarified input scope;
replaced generated-amount wording with the referenced weighting contract;
separated authoritative technical/business rules from product direction;
retained the BOQ workbook decision; replaced the original bootstrap acceptance
section with a link to the distinct M0 specification.

2026-09-21: recorded PO-approved Landing A, PS workbook direction including EV/Payment,
Financial Forecast exclusion and Create configuration; linked the approved delivery
sequence and canonical Progress semantics. No implementation authorization granted.

## F1 authorization update — 2026-09-23

PO accepted the [F1 specification](docs/milestones/F1-core-progress-workbook.md) and authorized F1 only.
The Progress contract owns final defaults, strict Duration and Live Rebuild
Dashboard Actual display. Earlier pending-authorization statements are historical.
F2–F6, Git operations and deployment remain unauthorized.
