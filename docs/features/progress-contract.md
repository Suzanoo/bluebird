# Progress — foundational business contract

- Status: Approved
- Last Updated: 2026-09-23
- Authority: Approved reporting, progress-history, and weighting semantics
- Implementation: F0 accepted; F1 specification accepted and engineering authorized; acceptance pending

This is a partial contract, not a complete Progress feature specification.
[Project Design](../../PROJECT_DESIGN.md) owns product scope; the
[architecture foundation](../architecture/foundation.md) owns technical identity
and adapter constraints.

## Reporting Date

Reporting Date is a date-only business concept, distinct from record creation
and update timestamps and from a timezone-dependent instant.
Changes to application/user timezone configuration must not change the meaning
of historical progress dates.

There is no global Actual Data Cutoff. The user selects Reporting Date in the
context of Progress Update, Dashboard, Reporting, or another relevant operation.

## Historical progress

Bluebird-native progress is stored historically by Reporting Date, not solely
as an overwritten current Actual percentage.

Imported schedule progress is distinct from Bluebird-native progress history.
Do not manufacture Bluebird historical snapshots from imported percent-complete
values unless their reporting-date semantics are known.
Schedule re-import must not casually overwrite native historical actuals.
Detailed reconciliation and correction behavior remain TBD.

## Progress weight and Cost

Use `progress_weight` for fallback progress weighting, rather than a fabricated
financial amount. Weighting is semantically distinct from budget, BOQ amount,
cost, payment, and earned value.

Do not assume one Activity maps to exactly one BOQ item. Detailed Progress/BOQ/Cost
mapping remains future design; no cardinality implementation or allocation
formula is specified here.

## Approved weighting and Activity Amount (updated 2026-09-21)

F1 initial XML generation requires an explicit Equal or Duration choice, with no
default. Amount is sequenced for F2, not part of F1. F2 uses explicit XML numeric
field selection with preview/validation; detailed readiness policies remain TBD.
Equal gives eligible ordinary activities equal basis; Duration uses an explicitly
identified duration basis.
Production duration semantics are now owned by the F1 final specification below.
The F0 prototype policy is not product approval.

Activity Amount means real **allocated Contract Value** for an Activity. This
PO decision replaces the earlier Planned Budget wording; it is not Actual Cost,
fabricated money, or an automatically approved EV BAC. Activity Amount is
separate user-owned workbook input; its WBS, Activity ID and Activity Name derive
from Main. Preserve hierarchy with outline/grouping. Blank is effective zero
but remains distinguishable from explicit zero. Show missing/zero warnings.
Amounts do not affect Equal/Duration weights. Applying Amount after creation must
be an explicit user action, sequenced for F3; entering values alone must not switch
the active method. Recalculation/readiness/history policies remain TBD.

Explicit milestone activities have **zero Progress Weight**, while retaining their
entered Contract Value. Do not erase or zero the monetary input to enforce zero
weight. This approved rule applies to the product methods as they are delivered.
It supersedes the F0 Equal proof's one-unit milestone behavior prospectively; F0
acceptance is unchanged and implementation has not been updated by this decision.
Detailed classification of ambiguous source activities remains adapter work.
Treatment/display of retained milestone value in monetary totals and future EV/BOQ
reconciliation remains TBD; a zero-weight rule alone does not settle it.

## Create configuration

Create exposes Weighting, Weekly Cutoff Day and Plan Distribution, following the
Progress Studio approach. Weekly Cutoff Day defines the reporting-week boundary;
it is not a global Actual Data Cutoff or a substitute for operation Reporting Date.
Weighting determines aggregation basis; Plan Distribution determines allocation
over time. These must not be conflated.

Friday/auto are approved defaults; both remain configurable. Explicit/no-default
weight choice remains in force. The F1 final specification below owns the detailed
accepted rules; do not inherit unrelated Progress Studio desktop defaults.

## Unresolved business rules

- Future historical snapshot correction/reopening and report revision policy
  beyond F1's local workbook corrections; F1 rules are closed below.
- F2 Amount readiness (missing/partial/zero/invalid values and zero total), currency,
  numeric precision and source-field support; no implicit fallback policy.
- Monetary treatment of retained milestone Contract Value in totals/EV/BOQ.
- F3 Amount transition/recalculation/history policy.
- Schedule/re-import reconciliation and historical report reproducibility.

These require product decisions before the relevant feature milestone.
Do not select convenient defaults and silently treat them as approved rules.

## F1 final specification — PO accepted 2026-09-23

This section owns the accepted F1 rules/defaults. F1 implementation
is authorized; implementation acceptance remains separate. F2/F3 remain future.
Reference: Progress Studio 89a6b80c06b986c4ec412b2717dc3e248a3537ec.

Create: explicit Equal/Duration, no default. Friday weekly cutoff / auto distribution
are defaults, both configurable. Options auto/flat/front/back/bell reuse PS rules
and curves. Auto priority: activity code, WBS, name, then flat. Weeks are seven
inclusive calendar dates ending on the chosen weekday. First/last overlapping
weeks are retained; display X margins are excluded from reporting. Distribution
uses curve weight times calendar-date overlap normalized to 100%; not working hours.
Missing plan dates skip allocation with warning; unusable project range/reversed
dates fail. Native imported percent complete never fabricates weekly Actual history.

Duration uses P6 PlannedDuration / MSP ISO Duration working hours, not elapsed
Start–Finish dates. Missing/malformed/nonfinite/nonpositive ordinary duration fails
with affected IDs; no Equal fallback. Explicit source milestones have zero basis
regardless of duration. Same-day ordinary tasks are not inferred milestones.
Both methods require positive finite total ordinary weight. Retain entered milestone
Contract Value separately; no amount application or monetary report in F1.

| ID | Rule | Acceptance example |
| --- | --- | --- |
| W1 | Weekly Actual is incremental, not cumulative input | .10 + .20 -> .30 |
| W2 | Activity total COUNT-guarded SUM | all blank -> blank; 0/blank -> 0 |
| W3 | Blank or 0..1 validation; total >1 warns, never clamps | .60 + .50 -> 1.10 warning |
| W4 | All descendant activity weights, no summary double counting | bases 1/3, Actual .20/.40 -> .35 |
| W5 | Missing inputs retain denominator; all missing blank | bases 1/3, .20/blank -> .05 |
| W6 | Raw cumulative blank before first/after last numeric; internal gaps carry | .10/blank/.20/blank -> .10/.10/.30/blank |
| W7 | Earlier correction recalculates current workbook, no immutable history | .20 corrected to .05 -> total .15 |
| M1 | Month of weekly cutoff owns week; no daily proration | Jan30/Feb6 -> Jan/Feb |
| M2 | Monthly period Actual COUNT-guarded SUM of weekly | .10/blank/.20 -> .30 |
| M3 | Monthly cumulative last nonblank weekly within month | .60/1/blank -> 1 |
| M4 | Wholly unreported monthly period Actual remains blank; cumulative follows W6/M3, never chart carry | an unreported month after the last observation remains blank |
| M5 | Monthly % Complete uses Monthly reporting columns, not stale weekly offsets | early 1 and late .25/.75 both total 1 |
| M6 | Preserve hierarchy; monthly derives weighted Main | nested WBS counted once |
| M7 | Normal Create monthly numeric activity Plan may be static | arbitrary Plan edits need future refresh |

### Dashboard final reference selection

PO deliberately selected PS Live Rebuild Actual display, replacing the review's
normal-Create recommendation. Carry latest available cumulative Actual for display
at/before a reporting point, masking dates beyond the applicable Actual Cutoff.
Monthly display consults weekly history. Blank and recorded zero remain distinct.
Keep source blanks; do not manufacture records or truncate raw history when cutoff
changes. KPI and chart share cutoff semantics; local view cutoffs are independent.
Do not modify Progress Studio or invent a different progress calculation.

Final workbook: PS manual calculation, calculate-on-save, first-open recalculation
request. F9 evaluates formulas, not Python snapshots. F1 supports weekly Actual
entry/correction, view controls and Amount input storage. Arbitrary Plan/row/schedule
restructuring and server refresh remain outside F1.

### Future-only TBDs

F2 Amount readiness/currency/precision/source field support; F3 transition,
reconciliation/history; monetary milestone treatment in EV/BOQ. F1 approval does
not settle all later capabilities.
