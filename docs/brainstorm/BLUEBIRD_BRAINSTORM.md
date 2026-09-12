# Bluebird --- Product & Architecture Brainstorm

**Status:** Review (historical exploration; not authority)\
**Project Stage:** Product Discovery / Requirements\
**Date:** 2026-09-12\
**Audience:** Product owners and implementation reviewer (Work)

> This document captures ideas, decisions, pain points, candidate
> architecture, and open questions discussed before implementation.
>
> **It is not an implementation specification.**\
> [PROJECT_DESIGN.md](../../PROJECT_DESIGN.md) owns approved product direction.
> Use the [documentation map](../README.md) for current technical and feature authority.
>
> Review this document critically before implementation. Do not treat
> every brainstorm item as an approved requirement.

> Consolidation note — 2026-09-12: The body below is retained as the original
> exploration record, not maintained as a second rulebook. "Agreed" and "Decision"
> labels, old review-task instructions, proposed fields, and milestone details
> reflect that earlier discussion only. Current approved rules are linked in the
> documentation map above. In particular, old generated-amount terminology, the
> dependency diagram, ownership TBD, and M9-only production concerns are not
> implementation instructions. Read this file only when explicitly requested.

------------------------------------------------------------------------

## 1. Why Bluebird

Bluebird is intended to become a practical **construction management
application**, with the initial product focus on:

-   **Progress management**
-   **Cost management**
-   Integration between progress and cost

The goal is not to reproduce every function of a large
construction-management platform. The first product should remain
focused and useful.

### Current Scope Direction

Likely core areas:

-   Project setup
-   Schedule import
-   Progress calculation
-   Progress updating
-   Progress dashboard and reporting
-   Cost
-   BOQ and mapping
-   Future integration between schedule, progress, BOQ, cost, payment,
    and earned value

### Explicitly Out of Current Scope

**Document Management is not part of the current product scope.**

Do not expand the initial product into RFI, submittals, drawings,
transmittals, NCR, document control, safety, photo management, etc.
unless this is explicitly reconsidered later.

------------------------------------------------------------------------

## 2. Product Philosophy

Bluebird should be designed as a **web-native product**, not as a web
copy of Progress Studio, BOQ Studio, or the existing OKD application.

Those products provide useful business knowledge and lessons learned,
but their implementation constraints should not automatically become
Bluebird constraints.

Core principles currently favored:

1.  Start small.
2.  Separate product decisions from implementation decisions.
3.  Reuse lessons learned, not legacy constraints.
4.  Keep domain/business logic independent from source-file formats and
    UI.
5.  Do not invent business rules when requirements are unknown.
6.  **Unknown / TBD is a valid answer.**
7.  Avoid premature infrastructure and features.
8.  Design for future Progress + Cost integration.
9.  Project customization should be optional.
10. Preserve source-system identity without making it the application's
    primary identity.

------------------------------------------------------------------------

## 3. Proposed Product Flow

Current conceptual flow:

``` text
Create Project
    ↓
Project Config
    ↓
Import Schedule
    ↓
Resolve Amount / Weighting
    ↓
Progress Dashboard
    ↓
Progress Update
    ↓
BOQ / Mapping
    ↓
Future Cost / EV / Payment integration
```

This sequence is conceptual and may change after technical/product
review.

Important: **BOQ must not block creation of a Progress Dashboard.**

------------------------------------------------------------------------

## 4. Project Creation

### Agreed Direction

Creating a project should be fast.

**Required fields only:**

-   Project Name
-   Project Code

Do not require Client, dates, logo, schedule, currency, theme, etc.
during project creation.

After creation, the user enters Project Configuration.

### Decision

**DEC --- Minimal Project Creation**

Bluebird requires only `Project Name` and `Project Code` to create a
project. Other project information and preferences belong to Project
Configuration and can be edited later.

------------------------------------------------------------------------

## 5. Project Configuration

Current conceptual structure:

``` text
PROJECT CONFIG
│
├── Project Information
│
├── Reporting
│
└── Appearance
```

### 5.1 Project Information

Current candidate fields:

-   Project Name
-   Project Code
-   Location
-   Client
-   Contract Start
-   Contract Finish
-   Duration

`Duration` should preferably be calculated from Contract Start and
Contract Finish rather than manually entered.

This list is **extensible and not considered complete**.

### 5.2 Reporting

Current candidates:

-   Reporting Frequency
    -   Weekly
    -   Monthly
    -   Weekly + Monthly
-   Week Ending Day
-   Monthly Reporting Basis
-   Reporting Calendar

Reporting Calendar can potentially derive from Contract Start / Contract
Finish rather than being duplicated configuration.

### Important Reporting Decision

Bluebird should **not** introduce a global `Actual Data Cutoff`.

Bluebird should also not store `Current Reporting Date` as project
configuration.

Instead:

``` text
Progress Dashboard
Reporting Date [ user selects ▼ ]

Progress Update
Reporting Date [ user selects ▼ ]
```

Actual progress should be stored historically by reporting period/date.
The user chooses the relevant reporting date when performing an
operation.

This intentionally avoids carrying an Excel-specific global cutoff
concept into the web application.

### Still TBD

-   Whether Reporting Frequency needs to be configurable or merely
    controls enabled views.
-   Whether Monthly Reporting Basis needs configuration in V1 if Month
    End is the only supported basis.
-   Whether Reporting Calendar requires explicit override fields.
-   Whether historical reporting dates can be reopened/edited.
-   Whether Actual % can decrease.
-   How monthly actual is determined from weekly updates.

Work should not decide these business rules without discussion.

### 5.3 Appearance

Candidate optional configuration:

-   Project Logo
-   Theme
-   Background
-   Accent

All customization must be optional.

If the user supplies nothing, Bluebird should remain fully usable with
defaults.

Possible fallback behavior:

-   Bluebird default theme
-   Default background
-   Default accent
-   Bluebird mark or project initials if no logo exists

**Principle:** Project customization must never be required to create or
operate a project.

------------------------------------------------------------------------

## 6. Schedule Inputs

Currently intended schedule inputs:

-   Primavera P6 XML
-   Microsoft Project XML
-   Native Microsoft Project `.mpp` --- desired, but feasibility/scope
    is not yet decided

Native `.mpp` is a binary Microsoft Project format and should not be
assumed to have the same ingestion path as MSP XML.

Do not commit native MPP support to V1 until technical feasibility for
the chosen web/Vercel architecture is evaluated.

------------------------------------------------------------------------

## 7. Schedule Import Architecture

Strong candidate architecture:

``` text
P6 XML ─────────┐
                │
MSP XML ────────┼→ Source Adapter
                │       ↓
Future formats ─┘   Normalize / Validate
                        ↓
               Bluebird Canonical
                 Activity Model
                        ↓
              Project Schedule Dataset
                        ↓
                  Progress Engine
```

### Principle

**The importer does not own the domain model.**

Each importer converts its source format into a Bluebird canonical
schedule/activity model.

The Progress engine and UI should not directly depend on P6 XML
elements, MSP XML elements, or source-specific objects.

This should make future CSV, Excel, API, or other schedule adapters
possible without redesigning the Progress domain.

------------------------------------------------------------------------

## 8. Canonical Activity Contract --- Candidate V1

### Required

Import cannot produce a usable activity without:

``` text
activity_name
plan_start
plan_finish
```

### Identity

``` text
bluebird_activity_id
source_activity_id
source_format
source_object_id
```

### Structure

``` text
wbs_code
wbs_name
wbs_path
```

### Schedule

``` text
planned_duration
calendar_ref
```

Potential later fields:

``` text
predecessor_links
constraint_type
constraint_date
```

### Progress / Status Data

``` text
progress_percent
physical_percent
actual_start
actual_finish
```

The exact canonical semantics of progress percentage still require care
because P6 can distinguish percentage types.

### Baseline

Preserve when available:

``` text
baseline_start
baseline_finish
baseline_duration
```

Baseline data does not necessarily need to drive the first Progress
Dashboard.

### Internal Identity

`bluebird_activity_id` should be generated and controlled by Bluebird
and remain immutable.

Do **not** use P6 Activity ID, MSP ID, task name, or another editable
source identifier as the database primary identity.

------------------------------------------------------------------------

## 9. Major Pain Point --- P6 ↔ MSP Round Trip

This requirement comes from a real workflow/problem.

Typical workflow:

``` text
P6
 ↓
Export XML for Microsoft Project
 ↓
Another user opens and modifies schedule in MSP
 ↓
Exports XML
 ↓
Schedule is brought back to P6
```

A real problem occurred because the activity/task identity did not
survive the round trip reliably.

The P6 Activity ID is not simply equivalent to Microsoft Project's task
`<ID>`.

MS Project has its own UID/ID concepts, while P6-origin identifiers may
be carried through extended/custom attributes. After editing/exporting,
those mappings can be lost or changed.

Consequences can include:

-   Activity identity mismatch
-   Changed IDs
-   Existing activities interpreted as different/new activities
-   Relationship problems
-   WBS/link corruption
-   Unsafe round-trip updates

### Design Principle

> **Activity identity must survive cross-system round trips
> independently from display IDs.**

Conceptually:

``` text
bluebird_activity_id
    = immutable Bluebird identity

source_activity_id
    = source/user-facing identifier such as P6 A1000

source_object_id / external identity
    = source-native metadata
```

If Bluebird later supports schedule export and re-import, a possible
strategy is to carry the immutable Bluebird activity identity in a
controlled custom/extended field.

Conceptual example only:

``` text
Bluebird → MSP
BluebirdActivityId stored in a controlled Extended Attribute

Bluebird → P6
BluebirdActivityId stored in a controlled UDF/custom field
```

Potential re-import matching hierarchy:

``` text
1. Match Bluebird immutable identity
2. Else match trusted source identity
3. Else require explicit resolution / flag ambiguity
```

This is **architecture direction, not yet an approved round-trip
implementation spec**.

### V1 Scope Recommendation

Do not implement P6/MSP round-trip export in the first schedule-import
milestone.

However, the initial data model and import architecture must not destroy
source identity or make safe round-trip support unnecessarily difficult
later.

------------------------------------------------------------------------

## 10. Observations From Actual P6 / MSP Files

Actual project files were inspected during brainstorming.

### P6 XML

Observed activity information includes fields corresponding to:

-   Activity Id
-   Name
-   WBS reference
-   Planned Start / Finish
-   Start / Finish
-   Planned Duration
-   Percent Complete
-   Physical Percent Complete
-   Actual Start / Finish
-   Status
-   Remaining / At Completion Duration
-   GUID / Object identity

P6 WBS structure is referenced from activities and represented
separately as a hierarchy.

This supports the adapter approach: the P6 adapter should resolve the
source WBS tree into Bluebird's canonical structure.

### MSP XML Converted From P6

The converted MSP XML demonstrated that Microsoft Project task ID should
not be assumed to be the original P6 Activity ID.

The XML also carries hierarchical information such as WBS / outline /
summary tasks and can preserve schedule, progress, baseline, calendar,
relationship, and constraint information.

A P6-origin identifier may appear in an Extended Attribute rather than
the normal MSP `<ID>`.

### Important Result

This observation is the reason Bluebird should distinguish:

``` text
Internal immutable identity
Source activity identifier
Source-native object/task identity
```

rather than flattening all three into an `activity_id` column.

------------------------------------------------------------------------

## 11. WBS Normalization

P6 and Microsoft Project represent structure differently.

Conceptual normalization:

``` text
wbs_code
wbs_name
wbs_path
```

Example:

``` text
wbs_code = "2.5"
wbs_name = "Lift"
wbs_path = ["Structure", "Lift"]
```

Bluebird domain logic should consume the normalized structure instead of
knowing how P6 WBS objects or MSP Summary/Outline tasks work.

Summary/WBS rows from source files should not automatically be treated
as construction activities.

Exact adapter behavior should be verified against representative source
files.

------------------------------------------------------------------------

## 12. Amount / Weighting

Progress Dashboard should not be blocked merely because a schedule lacks
cost/amount data.

Current direction:

-   If a source clearly contains the desired amount/cost field, use it.
-   If multiple candidate cost/amount fields exist, ask the user which
    one should be used.
-   If no amount exists, Bluebird can generate/use a fake amount or
    weighting so progress calculations remain possible.

Exact amount-resolution UX and business rules are **TBD**.

Do not invent them during early milestones.

------------------------------------------------------------------------

## 13. Native Progress Update

Weekly/monthly construction reporting requires users to update progress
without repeatedly modifying P6/MSP.

Bluebird should therefore provide native progress input.

Conceptual flow:

``` text
Open Project
    ↓
Progress Update
    ↓
Select Reporting Date
    ↓
Activity List
    ↓
Update Actual %
    ↓
Save
    ↓
Dashboard Updated
```

### Historical Data Principle

Do not simply overwrite one current Actual %.

Store progress historically by reporting date.

Example:

``` text
Activity A101

31 Aug → 12%
07 Sep → 18%
14 Sep → 27%
21 Sep → 35%
```

This history can later support:

-   Weekly reports
-   Monthly reports
-   S-Curves
-   Earned Value
-   Payment
-   Trend/variance analysis

### UX Candidate

A P6/MSP-like interaction where double-clicking an activity opens a
detail popup has been discussed.

This is a **candidate UX only**, not an approved requirement.

Actual % is a known requirement; the other fields in such a popup remain
TBD.

------------------------------------------------------------------------

## 14. BOQ Direction

BOQ should not block schedule/progress use.

Current conceptual branches:

``` text
Has BOQ
    → Upload BOQ

No BOQ
    → Export BOQ Template
    → User fills it in Excel
    → Upload
    → Validate
    → Mapping
```

Bluebird does **not** need a full native BOQ editor in V1.

BOQ Studio should not simply be embedded into Bluebird.

A future BOQ Dashboard may be useful, but it is not part of the
immediate foundation.

------------------------------------------------------------------------

## 15. Cost Direction

Cost is one of Bluebird's two main product pillars, together with
Progress.

However, the Cost domain is not sufficiently designed yet.

Possible future areas include:

``` text
Cost
├── BOQ
├── Budget
├── Actual Cost
├── Commitments
├── Forecast
├── Earned Value
└── Payment
```

These are **future design candidates**, not approved V1 modules.

Avoid creating Cost architecture prematurely based only on this list.

A key future requirement is that Progress and Cost should be able to
integrate cleanly.

------------------------------------------------------------------------

## 16. UX Direction

Bluebird should not feel like a generic CRUD/admin SaaS if a more
construction/project-oriented experience is appropriate.

Current high-level candidate navigation:

``` text
Projects

Project Workspace
├── Overview
├── Progress
├── Cost
└── Settings
```

Progress could later expand into:

``` text
Progress
├── Schedule
├── Update
├── Dashboard
└── Reports
```

This is conceptual. Navigation should not be overbuilt before the
relevant modules exist.

The product should eventually feel like a configurable project
**Studio**, while remaining practical and uncluttered.

------------------------------------------------------------------------

## 17. Architecture Direction

Preferred conceptual layering:

``` text
UI
 ↓
Application / Services
 ↓
Domain
 ↓
Infrastructure
```

Example:

``` text
P6 XML
 ↓
P6 Adapter
 ↓
Canonical Schedule Model
 ↓
Progress Domain / Engine
 ↓
Dashboard / Reporting
```

Avoid:

``` text
P6 parser
 ↓
Dashboard directly
```

Source-format concerns should remain at the adapter/infrastructure
boundary.

Domain logic should use semantic models rather than source-file paths,
XML tags, spreadsheet cell addresses, or UI state.

------------------------------------------------------------------------

## 18. Proposed Main Milestones

These are roadmap candidates. They establish product direction but are
not detailed implementation specs.

### M0 --- Application Foundation

Purpose: make Bluebird a real application shell.

Potential scope:

-   App shell
-   Routing
-   Basic navigation
-   Project workspace shell
-   Design/theme foundation
-   Basic architecture conventions

No business engine required yet.

### M1 --- Project Management

Potential scope:

-   Project List
-   Create Project
-   Project Name / Project Code
-   Project Config
-   Project Information
-   Reporting config
-   Appearance config
-   Required persistence foundation

### M2 --- Schedule Import

Potential scope:

-   P6 XML
-   MSP XML
-   Source adapters
-   Canonical activity normalization
-   Validation
-   Import preview/summary
-   WBS structure
-   Preserve source identity metadata

No round-trip export required.

### M3 --- Progress Engine

Potential scope:

-   Project activities
-   Plan timeline
-   Reporting periods
-   Weight / Amount
-   Planned progress
-   Actual progress history

### M4 --- Progress Update

Potential scope:

-   Reporting Date selection
-   Activity progress input
-   Save historical progress snapshot
-   Edit workflow subject to final business rules

### M5 --- Progress Dashboard & Reporting

Potential scope:

-   Weekly
-   Monthly
-   S-Curve
-   Plan
-   Actual
-   KPIs
-   Reporting Date selector

No global Actual Data Cutoff.

### M6 --- Cost Foundation

Requires separate design before implementation.

### M7 --- BOQ & Mapping

Requires separate design before implementation.

### M8 --- Progress / Cost Integration

Requires separate design before implementation.

### M9 --- Production Hardening

Potentially includes:

-   Authentication/security
-   permissions
-   data integrity
-   backups/recovery
-   observability
-   performance
-   deployment hardening
-   UX/accessibility
-   migration/versioning

Exact scope depends on earlier architectural decisions.

------------------------------------------------------------------------

## 19. Git / Delivery Philosophy

Bluebird should maintain a clean repository history without excessive
tagging.

Current preference:

``` text
Commits → frequent enough to describe meaningful work
Branches → feature/milestone work
Tags → only important stable/release points
```

Avoid creating a tag for every tiny milestone.

Possible release-level tags later:

``` text
v0.1.0-foundation
v0.2.0-progress
v0.3.0-cost
v1.0.0
```

Exact version naming can be decided later.

### Work / Implementation Safety

For implementation work, prefer a feature branch rather than direct
experimental changes on `main`.

Changes should be reviewed and accepted before merging to `main`.

The exact Git ownership/workflow should be explicitly confirmed before
Work begins making repository changes.

------------------------------------------------------------------------

## 20. Current Technical Foundation

Current repository/application foundation already exists:

-   Repository: `Suzanoo/bluebird`
-   Default branch: `main`
-   Next.js App Router project
-   Next.js 16.x / React 19.x / TypeScript
-   Tailwind available
-   Production deployment already established on Vercel
-   `PROJECT_DESIGN.md` exists as a living design document

The current application itself is intentionally close to empty.

Do not interpret an empty UI as a reason to prematurely build dashboards
or unrelated modules.

------------------------------------------------------------------------

## 21. Lessons Carried Forward

Relevant lessons from previous construction-software work:

### Preserve semantic domain boundaries

Do not make core business logic depend on presentation/storage
implementation details.

### Reuse before inventing

Inspect existing code and patterns before adding new infrastructure.

### Reporting context should be explicit

The user should choose the relevant reporting date/view when using
progress features rather than having an unnecessary global cutoff state.

### Preserve historical actuals

Progress history is valuable business data and should not be reduced to
only a latest value.

### Cross-system identity is dangerous

Editable/display IDs from scheduling tools are not reliable primary
application identities.

### Avoid premature feature integration

A useful Progress workflow should not require BOQ, Cost, Payment, EV, or
Document Management to be complete first.

------------------------------------------------------------------------

## 22. Open Questions

These are intentionally unresolved.

### Product / Business

-   Exact V1 boundary between Progress and Cost
-   Which Cost capability should follow Progress first
-   Exact reporting-calendar behavior
-   Historical progress correction/reopening policy
-   Whether Actual % may decrease and under what conditions
-   Monthly actual aggregation/snapshot rule
-   Amount/weighting selection workflow
-   BOQ mapping UX
-   Future multi-user roles and approval workflow

### Schedule

-   Exact semantics Bluebird should use for P6 planned/current/baseline
    dates
-   Exact progress-percent semantic mapping across P6/MSP
-   Native `.mpp` feasibility and whether it belongs in V1
-   Relationship/constraint scope for early milestones
-   Future safe P6/MSP export and round-trip strategy
-   How ambiguous identity matches should be resolved

### Technical / SaaS

-   Persistence/database choice
-   Authentication strategy and when to introduce it
-   Tenant/account/project ownership model
-   File storage strategy
-   Import job size/runtime limits on Vercel
-   Background processing requirements
-   Audit/history strategy
-   Data versioning/migrations
-   Backup/export/recovery
-   Permissions
-   Production observability

These technical questions should be raised at the point where they
materially affect architecture. Avoid installing infrastructure merely
to answer them prematurely.

------------------------------------------------------------------------

## 23. Questions for Work

Before implementation, review this brainstorm together with
`PROJECT_DESIGN.md`.

**Do not implement yet.**

Please provide a concise review focused on decisions that could cause
expensive rework if missed now.

Specifically identify:

1.  **Critical architectural risks** we may have missed.
2.  **Ambiguous or contradictory requirements.**
3.  **Decisions that must be made before M0/M1**, versus decisions safe
    to defer.
4.  **Simpler alternatives** where the current idea is over-designed.
5.  Important **web/SaaS concerns** that materially affect the initial
    architecture.
6.  **Data-model implications** of schedule identity, progress history,
    WBS, and future Cost integration.
7.  Risks to future **Progress + Cost integration**.
8.  Any recommended change to the **main milestone ordering**.
9.  Anything in this brainstorm that should **not** be implemented as
    currently described.
10. A recommended **minimal M0 boundary**.

### Keep the Review Efficient

We want to conserve implementation/review capacity.

Please:

-   Read the existing repository and `PROJECT_DESIGN.md` first.
-   Do not repeat this document back to us.
-   Do not redesign the entire product.
-   Do not produce code.
-   Do not modify files.
-   Do not perform Git operations.
-   Focus only on high-impact issues and decisions.
-   Separate findings into:
    -   **Must Decide Now**
    -   **Safe to Defer**
    -   **Recommended Changes**
-   Keep the response concise.
-   If the current direction is sound, say so rather than inventing
    additional complexity.

------------------------------------------------------------------------

## 24. Current Working Model

The intended collaboration model is:

``` text
Product Owners
    ↓
Brainstorm / Requirements
    ↓
Work Technical Review
    ↓
Product Decision
    ↓
PROJECT_DESIGN.md
    ↓
Milestone Specification
    ↓
Work Implementation
    ↓
Acceptance
```

Work is encouraged to challenge assumptions and identify technical
risks.

Final product/business decisions remain with the product owners.

------------------------------------------------------------------------

## 25. Immediate Next Step

1.  Work reviews:
    -   repository
    -   `PROJECT_DESIGN.md`
    -   this brainstorm
2.  Work returns only high-impact review findings.
3.  Product owners resolve any Must-Decide-Now items.
4.  Approved decisions are promoted into `PROJECT_DESIGN.md`.
5.  Define M0 acceptance criteria.
6.  Only then begin implementation.

------------------------------------------------------------------------

# Status Summary

### Agreed / Strong Direction

-   Bluebird focuses primarily on **Progress + Cost**.
-   Document Management is currently out of scope.
-   Create Project requires only Name + Code.
-   Project configuration follows creation.
-   Appearance customization is optional with defaults.
-   No global Actual Data Cutoff.
-   Reporting Date is selected in the context of use.
-   Progress should be stored historically.
-   P6 XML and MSP XML use source adapters.
-   Canonical Activity Model is source-independent.
-   Bluebird owns an immutable internal activity identity.
-   Source/display IDs are not primary database identity.
-   BOQ does not block Progress.
-   Native progress updating is required.
-   Initial P6/MSP round-trip export should be deferred.
-   Tags should be reserved for meaningful stable/release points.

### Candidate / Needs Review

-   Exact canonical activity field set.
-   Navigation structure.
-   M0--M9 milestone boundaries.
-   Reporting configuration details.
-   WBS canonical representation.
-   Baseline preservation strategy.
-   Amount/weighting workflow.
-   Git workflow for Work implementation.

### Explicit TBD

-   Cost domain details.
-   Native MPP support.
-   Auth/database/storage choices.
-   Historical correction rules.
-   Monthly actual rule.
-   Safe round-trip export.
-   Detailed Progress Update UX.
-   BOQ mapping UX.

------------------------------------------------------------------------

**End of Brainstorm**
