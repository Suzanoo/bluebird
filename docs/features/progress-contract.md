# Progress — foundational business contract

- Status: Approved
- Last Updated: 2026-09-21
- Authority: Approved reporting, progress-history, and weighting semantics
- Implementation: F0 proof accepted; production feature contract partial; F1 not started

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
Source-specific duration semantics, eligibility and calendar edge cases still
need production acceptance; the F0 prototype policy is not product approval.

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

Control inclusion is approved, not every default, distribution algorithm or
calendar edge case. Friday/auto remain proposals. The existing explicit/no-default
weight choice remains in force. The F1 specification must resolve applicable
business rules below; do not silently adopt every Progress Studio desktop default.

## Unresolved business rules

- Actual percentage semantics and allowed fields.
- Historical correction/reopening and whether Actual percentage may decrease.
- Monthly actual derivation from weekly updates.
- Missing actuals, carry-forward, freshness, and report revision policy.
- Weekly cutoff default, period boundaries and dates outside contract duration.
- Supported Plan Distribution options, default and rule/calendar behavior.
- Duration source semantics/calendar validation and planned progress curve.
- F2 Amount readiness (missing/partial/zero/invalid values and zero total), currency,
  numeric precision and source-field support; no implicit fallback policy.
- Monetary treatment of retained milestone Contract Value in totals/EV/BOQ.
- F3 Amount transition/recalculation/history policy.
- Schedule/re-import reconciliation and historical report reproducibility.

These require product decisions before the relevant feature milestone.
Do not select convenient defaults and silently treat them as approved rules.
