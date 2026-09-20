# Progress — foundational business contract

- Status: Approved
- Last Updated: 2026-09-12
- Authority: Approved reporting, progress-history, and weighting semantics
- Implementation: Actively designed; not implemented

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

## Approved initial weighting and Activity Amount (2026-09-14)

The user explicitly chooses Equal or Duration for initial XML generation.
There is no default and no initial Amount option. Equal gives every eligible
real activity equal basis; Duration uses an explicitly identified duration basis.
Source-specific duration semantics, eligibility and calendar edge cases still
need production acceptance; the F0 prototype policy is not product approval.

Activity Amount means real Planned Budget allocated to an Activity, not Actual
Cost, fabricated money, or an automatically approved EV BAC. Activity Amount is
separate user-owned workbook input; its WBS, Activity ID and Activity Name derive
from Main. Preserve hierarchy with outline/grouping. Blank is effective zero
but remains distinguishable from explicit zero. Show missing/zero warnings.
Amounts do not affect initial Equal/Duration weights. A later Amount transition
requires its own approved recalculation/history contract.

## Unresolved business rules

- Actual percentage semantics and allowed fields.
- Historical correction/reopening and whether Actual percentage may decrease.
- Monthly actual derivation from weekly updates.
- Missing actuals, carry-forward, freshness, and report revision policy.
- Reporting calendar/frequency and dates outside contract duration.
- Duration source semantics/calendar validation, planned progress curve, and later Amount transition/history policy.
- Schedule/re-import reconciliation and historical report reproducibility.

These require product decisions before the relevant feature milestone.
Do not select convenient defaults and silently treat them as approved rules.
