# F1 — Core Progress Workbook and Landing A

- Status: F1 implementation and Windows Desktop Excel lifecycle accepted by PO 2026-09-25; closure recorded
- Implementation: F1 + cumulative R2 integrated at f37fbde; PO acceptance confirmed

## Required reading

AGENTS.md, docs/README.md, Engineer Contract/Workflow, Coordinator Contract;
[Progress contract](../features/progress-contract.md#f1-final-specification--po-accepted-2026-09-23),
[foundation](../architecture/foundation.md), [sequence](file-workbook-roadmap.md),
accepted F0 evidence. No F0 gate is reopened.

## Scope

Landing A / Clear Blue -> Create -> P6/MSP XML -> Generate -> Download XLSX.
Explicit Equal/Duration; Friday cutoff and auto distribution configurable.
Weekly Main, Monthly Summary, Dashboard/S-curves, Activity Amount, helpers/guide.
Reuse PS themes/rules and F0 architecture. Final PO adjustment selects Live Rebuild
Actual display; the earlier normal-Create chart recommendation is superseded.

No F2 Amount method/field picker; F3 refresh/applyAmount; F4–F6; Forecast;
Theme Editor; Gantt; accounts/persistence; or new infrastructure.

## Acceptance checklist

- W1–W7 / M1–M7 reference cases, nested WBS, milestone zero weight/retained money.
- Strict durations; all weekdays/distributions, boundary dates and reporting range.
- Dashboard gaps, explicit zero, before first Actual, monthly lookup from weekly
  history, cutoff between/outside points, chart/KPI consistency, source blanks.
- Artifact formulas, outlines, protections, theme, safe strings, chart relationships.
- Both sources/methods, runtime errors/limits, existing F0 regressions, Next lint/build.
- Desktop Excel first-open, Actual entry/correction, F9, Monthly early/late totals,
  charts, Amount retention, Save/Close/Reopen: PO verification required.
- Separately authorized deployed browser Upload -> Generate -> Download.
- Engineering tests do not equal Desktop Excel/deployed/PO acceptance.

## Implementation boundary

Reuse source/canonical/runtime patterns; domain has no Excel/web dependencies.
Cell addresses belong to renderers. Keep one Python service, bounded processing,
no raw upload logging/storage. Preserve F0 endpoint and tests. No Git or deployment.

## Engineering evidence and open gates

41 Python tests pass (22 existing F0 + 19 F1); Next lint/build pass. Tests inspect
serialized formulas, package integrity and planning oracles, not Desktop Excel
evaluation. [Reproduction and owner acceptance guide](../guides/developer/F1-acceptance.md).
Desktop Excel, local browser visual checks, deployed browser and final PO acceptance
remain unproven. Compact Dashboard layout differs from PS desktop presentation;
review the guide's explicit limitations before accepting visual parity.

### Drawing investigation R1/R2 — 2026-09-24

PO reported Mac integration: 41 Python tests, lint/build, local Vercel Services
startup and conversion HTTP 200 passed; Desktop Excel first-open failed.
Round 1 corrected a confirmed dangling axis reference (date axis 500 versus
value-axis crossAx 10), with 44 automated tests passing. PO subsequently
reported that BOTH Round 1 workbooks still prompted for recovery. Round 1 was
not integrated into the PO branch and is not accepted; the axis defect was
not a complete explanation of the Excel failure.

Round 2 found an independent DrawingML line-fill choice violation: all three
charts wrote both noFill and solidFill on marker/cutoff series lines. The shared
factory now assigns solidFill only to the two curve lines, while retaining
marker colors and the red dashed cutoff error bar. Reciprocal axis IDs 10/100
and the three Round 1 regression tests are retained. Calculations, categories,
series, anchors, Activity Amount and F0 behavior are unchanged.

Engineering evidence: 46 Python tests pass. Two new tests cover exclusive line
fills, source/method combinations, marker/cutoff preservation, serialization
round-trip and the exact conflicting-fill negative case. Controlled artifacts
isolate the line-fill delta; this does not prove Excel compatibility. Desktop
Excel Gate remains FAIL pending PO first-open and Save/Close/Reopen retest.
Round 2 handoff is self-contained relative to the original F1 handoff. No Git
operation, deployment or new product decision was performed.

## F1 PO Acceptance and Closure — 2026-09-25

Repository: Suzanoo/bluebird
Branch: feat/f1-core-progress-workbook
Accepted implementation: f37fbde
Baseline: main d965b7b

### Automated verification

- Mac Python 3.12: 46 tests PASS.
- Windows Python 3.12: 46 tests PASS.
- Next.js lint/build: PASS, reported during Mac integration.
- Local conversion HTTP 200: PASS, reported during Mac integration.

### Windows Desktop Excel — PO Accepted

- First Open: PASS, no Repair Warning.
- Planned S-Curve display: PASS.
- Recalculation: PASS.
- Weekly Actual updates Project Actual and chart: PASS.
- Monthly aggregation: PASS.
- Dashboard Planned/Actual consistency: PASS.
- Save/Close/Reopen after Actual entry: PASS.

### Compatibility observation

Excel for Mac displayed chart frames but not the plotted curve.
The same retest workbook displayed the curve in Windows Excel.
The Mac installation showed an Office activation notice.
Root cause remains unverified.

### Closure boundaries

F1 Windows Desktop Excel acceptance is complete.

Deployed browser acceptance is not established by this record.
Financial Forecast, F2–F6, deployment and release remain outside
this closure.

The earlier R1/R2 investigation results remain as historical evidence.
This acceptance record supersedes their pending Desktop Excel gate status.
