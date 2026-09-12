# Bluebird — Project Design

- Status: Approved
- Last Updated: 2026-09-12
- Authority: Product vision, scope, and high-level product direction
- Stage: Design consolidation; M0 specification prepared, implementation not started

## Product direction

Bluebird is a construction management web application focused primarily on
**Progress**, **Cost**, and future integration between them. It grows from practical
construction workflows; it is not intended to reproduce P6, Microsoft Project,
or a full ERP.

**Document Management is currently out of scope**, including RFI, submittals,
drawing/document control, transmittals, NCR, safety, and photo management.

Progress is the first delivery focus. Detailed Cost capabilities and the exact
V1 Progress/Cost boundary remain TBD. Future candidates are not approved modules.

## Product scope

The planned product includes project creation/configuration, schedule ingestion,
progress weighting, a Progress Dashboard, native Actual Progress entry, and
weekly/monthly reporting. Output formats and detailed calculations remain TBD.

Planned schedule inputs are P6 XML and MSP XML. Native Microsoft Project
`.mpp` support remains a feasibility/scope question, not a V1 commitment.
Round-trip schedule export is not part of the initial import delivery;
preserving identity does not constitute an export guarantee.

### DEC-001 — BOQ creation in the initial version

Users may upload an existing BOQ workbook. If they have none, Bluebird exports a
standard workbook template, the user completes it externally, and uploads it.
A native BOQ editor is excluded initially to keep the delivery focused.
BOQ must not block useful Progress operation.

Payment, Earned Value, a BOQ Dashboard, and native BOQ management remain future
possibilities requiring separate design. No detailed Cost module list is approved.

## Workflow and UX

Conceptual flow, not a fixed screen sequence:

Create Project → Configure Project → Import Schedule → Resolve Progress Weighting
→ Progress Dashboard / Native Progress Update → BOQ / Mapping.

Project setup should be practical and the visual identity recognizable.
Detailed appearance options, reporting configuration, double-click dialogs,
and navigation trees remain candidates.

### DEC-003 — Minimal Project Creation (Approved, V1)

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

- Problem statement, target user/customer segments, and value proposition.
- Exact V1 boundary and first Cost capability.
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

## Roadmap — planning direction

This table retains M0–M9 as a high-level planning sequence, not authorization
to implement all milestones.

| Milestone | Direction |
| --- | --- |
| M0 | Application foundation — [specification for review](docs/milestones/M0-application-foundation.md) |
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
section with a link to the distinct, not-yet-implemented M0 specification.
