# Architecture foundation

- Status: Approved
- Last Updated: 2026-09-12
- Authority: Foundational technical constraints
- Implementation: Documentation only; no domain schema or infrastructure implemented

Product scope belongs to [Project Design](../../PROJECT_DESIGN.md).
Workspace ownership is defined once in
[ADR-001](decisions/ADR-001-workspace-ownership.md).

## Project identity

Every Project has an immutable internal `project_id`.
Project Code is user-facing business data, not a database primary identity.
Its validation, uniqueness scope, and edit policy remain TBD; no database schema
is specified here.

## Activity identity and provenance

Bluebird controls an immutable `bluebird_activity_id`.
P6 Activity ID, MSP ID/UID, Activity Name, and WBS path must not be its primary identity.

Preserve source identity separately from internal identity. The eventual model
must be able to represent source system/format, source project identity when
available, source activity/object identity, and import/revision context.
Do not collapse identities from different sources into one assumed universal ID.

An ambiguous match must not be automatically confirmed solely from Activity Name
or WBS. Detailed reconciliation, schedule revision behavior, export mechanisms,
and the canonical field set remain TBD. Identity preservation is not a promise
that lost cross-system identity can be reconstructed.

## WBS identity

WBS nodes have stable internal identity and a parent relationship.
Code, name, and path describe business/display structure; `wbs_path` is not
primary identity because nodes can be renamed or moved.
Exact source hierarchy conversion and summary/activity classification remain
adapter-design work, not an approved schema in this document.

## Source adapters and dependency boundaries

The conceptual data flow is source format → source adapter → normalize/validate
→ canonical Bluebird model → domain/application services → UI/reporting.

This is data flow, not an instruction for Domain to import Infrastructure.
P6/MSP objects, XML tags, UI state, and framework/storage details must not leak
into Progress domain logic. Domain uses semantic models; application services
coordinate adapters. Keep the existing single application and add concrete
boundaries only as capabilities appear; do not build unused abstractions.

Retain the existing Next.js/Vercel/GitHub platform. Runtime limits and source
file characteristics must be assessed when import is designed; no queue,
background worker, database provider, or ORM is selected by this document.

Reporting and weighting semantics are owned by the
[Progress contract](../features/progress-contract.md), not duplicated here.

## Decision timing

Before M1 stores real cloud Project data, explicitly review persistence,
the ownership boundary in ADR-001, authentication/authorization, and migration
implications. Provider/schema choices and any interim access arrangement remain
TBD. M0 is not a place to install these capabilities.

Introduce authorization/security, data integrity, migration discipline, and
recovery when the relevant persisted or multi-user capability appears.
An M9 readiness review does not defer those obligations.

Before M2, resolve canonical schedule field/date/percentage semantics against
representative P6/MSP inputs, source identity handling, file handling, and bounded
import processing. Do not infer native MPP support from XML support.

Detailed revision/reconciliation, file retention, background processing, and
round-trip behavior require later scoped design. Do not implement them merely
because this foundation preserves room for them.
