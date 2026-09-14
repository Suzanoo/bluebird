# F0 isolated engineering proof

Disposable Python 3.12 proof; not integrated into M0 or deployed. Run from repo root:

```
python -m pip install -r spikes/f0/requirements.txt
python -m unittest discover -s spikes/f0 -p 'test_*.py' -v
python spikes/f0/benchmark.py
python spikes/f0/run.py spikes/f0/fixtures/msp_n8.xml msp-equal.xlsx --method Equal
python spikes/f0/run.py spikes/f0/fixtures/p6_n8.xml p6-equal.xlsx --method Equal
python spikes/f0/http_proof.py
```

Local POST `http://127.0.0.1:8765/?method=Equal` with raw XML returns XLSX.
Omit method or choose Amount: rejected. Local server is an HTTP proof, not a
production handler. Tests start/stop it automatically on a random local port.

## Evidence and boundaries

`evidence/tests.txt`: 12 passing tests. `benchmark.json`: measured Linux peak RSS
and stage timings in fresh Python processes, excluding interpreter imports and
network time. Synthetic profiles are capacity samples, not production projects;
durations are invented test durations, never money, and deliberately do not
validate calendar consistency. Fixtures msp_n8/p6_n8 copied unchanged from
Progress Studio c3772c5dc3b954dd55055394451f12a0cf0b5254,
`tests/fixtures/xml/`. Both have two activities and no duration fields.
Duration extensions are synthetic tests. Do not claim exporter coverage.

Main owns schedule and weekly incremental actual inputs. Activity Amount owns
blank monetary inputs. No Amount method. Internal import-scoped UUIDs and full
source metadata are retained. Reimport generates a new import scope; no identity
reconciliation is implemented. WBS has explicit parents; display order is
hierarchical, not guaranteed identical to source order. Outline depth clamps at
7; deeper display must be accepted separately. WBS summaries are Plan only in
this minimal proof. Project totals show both Plan and Actual.

Provisional Duration basis: P6 PlannedDuration interpreted as hours; MSP Duration
PT hours/minutes/seconds, known elapsed DurationFormat codes rejected. This is
as-imported scheduled duration, not remaining duration, work, or approved baseline.
Raw fields/calendar IDs retained. No calendar evaluation, no inferred duration
from date spans. Missing/inconsistent duration blocks Duration, not explicit Equal.
Zero-duration milestones get zero Duration basis and one Equal basis. Nonmilestone
zero rejects Duration. All-zero Duration rejects. No silent fallback.
Production exporter/unit/elapsed/manual-task semantics remain acceptance work.

Flat calendar-day weekly Plan is an explicit F0-only distribution assumption,
independent of working-duration weights; not an approved reporting calendar.
Imported percentages are not turned into historical actuals. Missing weekly Actual
contributes zero in this proof, without claiming zero is an approved history rule.

openpyxl writes formulas but never evaluates them. A restricted test evaluator
checks Main formula references against numeric expectations; it is not Excel.
Automatic calculation flags request recalc. Caches are empty until a real engine
calculates/saves. No macros, no external links, no Python rebuild on ordinary
inputs. Formula/protection/grouping behavior in desktop Excel is NOT yet accepted.
Protection prevents accidental edits, not malicious editing. Inserting/deleting
rows/periods, sorting, and general rebuild are outside the supported input path.

## Manual Excel gate

Use msp-equal.xlsx and p6-equal.xlsx plus synthetic small.xlsx (Duration).
Open in intended desktop Excel version with a fresh Excel session; record version
and app calculation mode. Require no repair prompt. Expand/collapse WBS with
protection on; confirm identity/formulas locked and Actual/Amount cells editable.
For small.xlsx set first activity Actual week 1 to 100%: project Actual must be
1/3 (durations 8 and 16 hours), while Plan final Complete totals 100%.
For Equal fixture set only one activity cumulative Actual to 100%: project 50%.
Enter blank, zero and 1234.50 Amount: state/warnings distinguish them, Equal/Duration
results must not change. Negative input must reject ordinary typing (paste can
bypass validation). Try cumulative Actual >100% and confirm warning.
Press F9; save, close, reopen; confirm values/results/warnings persist. Also repeat
with Excel opened in manual mode beforehand. Record recalculation time on large
sample. If protected grouping does not work in target Excel, resolve before F1.

Requirements installation initially could not fetch defusedxml in this runtime;
final proof instead uses stdlib Expat declaration/depth/count preflight followed
by ElementTree. No DTD/entity support. 4 MB input/output, 2000 activity and 260
period limits are prototype bounds, not proven maximum production capacity.

## Real-file acceptance correction (2026-09-14)

This section supersedes the earlier provisional MSP DurationFormat paragraph.
The first F0 filter was WRONG: 7 is working days, not elapsed days. The adapter
now accepts working formats 3/5/7/9/11 and rejects elapsed/estimated/unknown formats
for Duration. Source values remain hours; no day/week conversion is inferred.
Only the supported real-file case is accepted by automated evidence, not every
possible exporter/calendar. See Microsoft DurationFormat documentation.

The old unconditional Text1 selection is removed. A declared Activity ID alias
can select a field; otherwise source MSP ID is used unless an explicit mapping
is supplied. The acceptance runner proves the field's complete unique match
against the supplied P6 population before explicitly selecting it. It does not
claim the unlabeled MSP XML itself declares the field's business meaning.

MSP WBS codes are already full paths, so the renderer no longer concatenates
every ancestor's full path. Raw source IDs, timestamps, duration format, type,
status and project identity fields are retained in metadata. Display names are
not HTML-decoded a second time: exporter double-escaping remains visible.

Run with the exact underscore-named source files in an external INPUT_DIR:

```
python -m unittest discover -s spikes/f0 -p 'test_*.py' -v
python spikes/f0/acceptance/real_files.py INPUT_DIR OUTPUT_DIR
python spikes/f0/acceptance/http_real.py INPUT_DIR
```

For an individual mapped MSP workbook add `--msp-activity-id-field 188743731`
to run.py. This pair-specific option is not an initial UX requirement or a
universal FieldID contract. No user XML is added to git. Full real-file lifecycle
results and exact manual cell references are in OUTPUT_DIR/real_file_evidence.json.
The runner requires the supplied pair (208 activities); it is an acceptance
assertion, not a production parser restriction. Formula evaluation is limited to
this renderer's Main vocabulary, not Microsoft Excel emulation.

Desktop Excel acceptance subsequently passed according to the Product Owner;
the authoritative current status is in docs/milestones/F0-file-workbook-proof.md.
The Vercel preview remains open. The Vercel
connector exposed no teams; no linked project or CLI token is available. A
GitHub branch-create attempt returned HTTP 403 Resource not accessible by
integration. No remote changes, commit, push or tag were made.


## Closure delivery

The Product Owner accepted Desktop Excel lifecycle behavior. Earlier references
above to manual acceptance describe the historical proof/testing limitation; they
are not a request to repeat the accepted gate. Visual/theme polish is deferred.
See the [F0 milestone](../../docs/milestones/F0-file-workbook-proof.md) for current
acceptance status. Python, weighting, rendering and the local HTTP implementation
are unchanged during closure. Generated XLSX/synthetic XML stay out of git;
benchmark.py regenerates them. Small text/JSON logs are intentionally retained
as historical evidence, and fixtures/ contains only the original PS test fixtures.
