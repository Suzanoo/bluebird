# F2 — XML Amount field selection and weighting

- Status: Approved scope and implementation authorized by PO (2026-09-26)
- Baseline: Bluebird main 6db3e6665cb57cac8bfc5fa06f64454991c994fd
- Reference: Progress Studio main 89a6b80
- Authority: F2 delivery scope; business rules live in the Progress contract
- Implementation: engineering handoff; automated checks recorded in the TXT report;
  Desktop Excel and deployed browser gates remain open

## Required reading

AGENTS.md; docs/README.md; Engineer Contract/Workflow and Coordinator Contract;
[Progress contract F2 rules](../features/progress-contract.md#f2-xml-amount-weighting--po-authorized-2026-09-26);
[approved sequence](file-workbook-roadmap.md). Prior investigation:
BLUEBIRD_F2_IMPLEMENTATION_REPORT.txt (2026-09-26 readiness report); its sole
blocking milestone-input decision is resolved by PO approval of Policy A.

## Authorized scope

Extend existing source adapters/canonical model, weighting, Create preview and
XLSX rendering to select real XML Amount and initialize Contract Value separately
from Progress Weight. Preserve Equal/Duration, identity, runtime limits, F1
calculations, R2 repairs and overlays. No Progress Studio changes.

## Acceptance

- P6/MSP typed discovery and explicit selection, safe invalid/no-field feedback.
- Server-side validation on preview and Generate, including approved Policy A.
- Positive ordinary total, correct zero-weight milestones with retained money.
- Metadata/source provenance and editable monetary input remain consistent.
- Full relevant F0/F1/F2 regressions, Next.js lint/build and HTTP workflow.
- PO Windows Excel first-open, F9, charts/overlays and Save/Close/Reopen.
- PO/Coordinator deployed browser upload/select/preview/generate/download.

Commands and owner-run steps: [F2 acceptance guide](../guides/developer/F2-acceptance.md).

## Exclusions / stop

No F3 apply/refresh, BOQ, EV, Payment, Forecast, theme polish or infrastructure.
No Git or deployment. Deliver changed files/manifest and concise TXT report;
stop for Coordinator integration and PO acceptance.
