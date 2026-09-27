# Reused Progress Studio source

Reference repository: https://github.com/Suzanoo/progress-studio/tree/89a6b80c06b986c4ec412b2717dc3e248a3537ec

- distribution/auto.py, curves.py, distribution_rules.json: copied from
  progress_studio/services/distribution/, without arithmetic changes.
- export_theme.py: copied from progress_studio/infrastructure/excel/.
- dashboard_theme.json: copied from progress_studio/config/.
- domain.distribute: coordinate-free adaptation of distribution_workbook.distribute.
- workbook.py: adapts progress_workbook, monthly_main_workbook (accepted MS-2 total
  fix), and Live Dashboard DF-1 display formulas to Bluebird's workbook layout.
- amount.py and model.py monetary-field extraction: adapted from PS MS-2
  services/xml_amount_service.py, domain/amount_field.py and schedule_xml
  P6/MSP adapters at the same reference. Bluebird deliberately retains milestone
  money separately and validates it under PO-approved Policy A (2026-09-26),
  unlike PS's combined amount/weight assignment. Uses immutable internal activity
  keys, not display IDs, for workbook monetary mapping.

No runtime dependency on the Progress Studio repository. Source identities and
XML normalization reuse the Bluebird F0 adapter with explicit F1 policy options.
No F0 proof formula is silently promoted to the production progress contract.

## Structure and readability — Trial #1

PO authorized 2026-09-27; input baseline e2bc355. Reuses PS 89a6b80
schedule_xml/p6_adapter.py SequenceNumber/source_order and normalized_reader.py
source-specific traversal; schedule_workbook.py split_plan_actual_values supplies
only the presentation concept, not its cell clearing or monetary formulas.

model.py retains source_order on WBS/Activity and P6 sequence_number. P6 sibling
WBS use available SequenceNumber first with encounter-order tie/fallback; direct
activities precede child WBS. MSP sibling groups merge by shared XML task encounter
index. Without complete MSP ordering metadata, preserve legacy child-WBS then
activity group order. Never infer numeric/lexical code ordering. IDs and canonical
activity indices are unchanged. Missing P6 sequence falls back to stored encounter
order/list order. Sequence parsing follows PS integer conversion, with non-finite
values treated as unavailable rather than crashing.

write_main builds ordered paired records before formulas; Monthly and Activity
Amount consume those records. Summary physical ranges remain subtree bounded.
Additive optional ordering fields serialize through existing metadata; absent
fields default to None. This does not implement old-XLSX import/refresh or recover
source order missing from an old workbook. F3 must review its reader compatibility.

style_row uses number format ;;; on A-row columns A/B/C/E/G/H/M in both Main and
Monthly. Values/formulas remain intact (including Row Type used by aggregation).
P/A, basis/weight, cumulative progress and Actual timescale stay visible; hidden
level/identity columns remain. Static values are still available in the formula
bar, not deleted. No change to the renderer's calculation, chart or monetary model.

Focused tests: spikes/f0/test_structure_readability.py. Excel visual and lifecycle
acceptance is separate from package tests; use the delivered Trial #1 report.
