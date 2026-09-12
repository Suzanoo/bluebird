# Bluebird — Project Design

## Document Status

- Status: Living Document
- Project Stage: Product Discovery / Requirements
- Current Milestone: Foundation
- Last Updated: 2026-09-12

---

## 1. Product Vision

Bluebird is a construction management application focused on transforming project schedule data into practical progress management workflows and dashboards.

The product is intended to grow incrementally from real construction-management workflows rather than attempting to reproduce Primavera P6, Microsoft Project, or a full ERP system.

---

## 2. Problem

TBD

---

## 3. Users & Customers

TBD

---

## 4. Value Proposition

TBD

---

## 5. User Workflow

Initial concept:

Create Project  
→ Project Configuration  
→ Import Schedule  
→ Resolve Amount  
→ Progress Dashboard  
→ Progress Update  
→ BOQ / Mapping

This workflow is expected to evolve during development.

---

## 6. Inputs

Planned schedule inputs:

- Microsoft Project
- Microsoft Project XML
- Primavera P6 XML

Cost / amount behavior:

- If an amount/cost field exists, the user selects which field should be used.
- If no amount is available, Bluebird can generate a temporary/fake amount distribution so the project can still produce a progress dashboard.

BOQ:

- User may upload an existing BOQ workbook.
- If no BOQ exists, Bluebird will export a standard BOQ workbook template.
- User completes the workbook externally and uploads it back to Bluebird.

---

## 7. Outputs

Initial outputs may include:

- Progress Dashboard
- Weekly reporting information
- Monthly reporting information
- BOQ template workbook
- Mapping results

Exact output contracts are TBD.

---

## 8. Features

### Planned for Initial Product

- Project creation
- Project configuration
- Schedule import
- Amount selection / generated amount
- Progress Dashboard
- Native progress update workflow
- BOQ template export/import
- Schedule ↔ BOQ mapping

### Future

- Payment
- Earned Value
- BOQ Dashboard
- Native BOQ management

### Out of Scope for Initial Version

- Full BOQ editor
- Full Primavera P6 replacement
- Full Microsoft Project replacement

---

## 9. UX / UI

Bluebird should have a recognizable visual identity rather than a generic construction SaaS interface.

Project configuration may allow the user to customize:

- Theme
- Background
- Accent
- Project identity
- Logo
- Dashboard presentation

Detailed UX is TBD.

---

## 10. Progress Update Workflow

Construction progress is updated periodically for Weekly and Monthly reporting.

The responsible user must be able to enter Actual Progress for individual activities directly inside Bluebird.

Initial UX concept:

Open Project  
→ Select Reporting Date  
→ View Activities  
→ Double-click Activity  
→ Progress Update dialog  
→ Save  
→ Dashboard updates

The Activity Update dialog may take inspiration from familiar Primavera P6 / Microsoft Project workflows without copying their UI.

Progress should preserve reporting history rather than overwrite a single current value.

Example:

- 31 Aug — 12%
- 07 Sep — 18%
- 14 Sep — 27%
- 21 Sep — 35%

Detailed progress fields and calculation rules are TBD.

---

## 11. Domain & Business Rules

TBD

---

## 12. Data Model

Potential domain concepts:

- Project
- WBS
- Activity
- Schedule
- Reporting Period
- Progress Update
- Amount
- BOQ Item
- Mapping

This is conceptual only and does not yet define the database schema.

---

## 13. Architecture

TBD

Initial application platform:

- Next.js
- Vercel
- GitHub

Technology decisions beyond this should be made only when requirements justify them.

---

## 14. Decisions

### DEC-001 — BOQ Creation in Initial Version

Bluebird will not provide a native web-based BOQ editor initially.

If a user does not have a BOQ, Bluebird exports a standard workbook template.

The user completes the workbook externally and uploads it back into Bluebird.

Reason:

Keep the initial product focused on schedule, progress, and mapping.

Future:

A native BOQ module and BOQ Dashboard may be added later.

---

### DEC-002 — Living Requirements

This document is intentionally incomplete.

Requirements, product decisions, UX concepts, architecture decisions, and lessons learned will be added as the product evolves.

Unknown or undecided items should be marked TBD rather than guessed.

---

## 15. Open Questions

TBD

---

## 16. Milestones

### Foundation

- Initialize Next.js application
- Create GitHub repository
- Deploy initial application to Vercel
- Establish PROJECT_DESIGN.md

Future milestones will be defined after product requirements become clearer.

---

## 17. Acceptance Criteria

Foundation is complete when:

- Bluebird runs locally.
- Source is stored in GitHub.
- Production deployment is available on Vercel.
- PROJECT_DESIGN.md exists as the project's living design document.

---

## 18. Lessons Learned

TBD

---

## 19. Change Log

### 2026-09-12

- Created initial Bluebird product-design document.
- Established schedule-first product concept.
- Defined preliminary BOQ workbook workflow.
- Recorded native progress-update requirement.