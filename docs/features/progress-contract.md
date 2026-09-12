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

## Unresolved business rules

- Actual percentage semantics and allowed fields.
- Historical correction/reopening and whether Actual percentage may decrease.
- Monthly actual derivation from weekly updates.
- Missing actuals, carry-forward, freshness, and report revision policy.
- Reporting calendar/frequency and dates outside contract duration.
- Weight selection/generation, source cost selection, and planned progress curve.
- Schedule/re-import reconciliation and historical report reproducibility.

These require product decisions before the relevant feature milestone.
Do not select convenient defaults and silently treat them as approved rules.
