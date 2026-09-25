# F1 engineering handoff and acceptance

- Status: Engineering delivery; Desktop Excel, deployed browser and PO gates OPEN
- Baseline: main d965b7b43f5bfc06bc9a8f1e9d9bb1e37970d10a
- Scope: [F1 milestone](../../milestones/F1-core-progress-workbook.md)
- Business rules: [Progress contract](../../features/progress-contract.md)

## Local checks

Use Python 3.12 and the repository npm lockfile. From repository root:

```sh
npm ci
python -m pip install -r spikes/f0/requirements-test.txt
python -m unittest discover -s spikes/f0 -p 'test_*.py' -v
npm run lint
npm run build
npx --yes vercel@59.23.2 dev -L --listen 127.0.0.1:3000 --yes
```

In another terminal in the same network namespace:

```sh
python spikes/f0/acceptance/f1_http.py http://127.0.0.1:3000
```

Open `/create`. The browser calls `/api/progress/convert` directly on the same
origin. The existing F0 endpoint/page remain available for regression. `next dev`
alone does not supply the Python service. No Next proxy is added. No new secrets,
environment variables, storage or runtime dependencies are required.

The converter root remains `spikes/f0` to preserve the accepted Services boundary.
`engine/` owns F1 domain and renderer code; the shared XML normalizer exposes an
explicit production policy. F0 defaults remain unchanged. This physical location
does not make F0's historical business assumptions production rules.

Runtime limits remain 4,000,000 bytes in/out, 2,000 activities, 260 reporting weeks,
60-second completion target and 65-second client deadline. One conversion per
process; contention returns 503, no queue. Client abort is not CPU cancellation.
XML/XLSX remain in memory; openpyxl scratch-file cleanup follows the accepted F0
adapter, including catchable-failure cleanup and hard-termination limitations.

## Desktop Excel — owner-run gate

1. Generate both P6/MSP workbooks with Equal and with valid Duration data. Original
   tiny fixtures have missing durations; HTTP smoke supplies synthetic duration
   variants. Do not expect every original fixture to pass Duration.
2. Open in a fresh Desktop Excel session; record version/platform. No repair dialog.
   Check Dashboard, Main, Monthly, Activity Amount, hierarchy and PS-derived theme.
3. Enter weekly increments in Main (e.g. 10%, blank, 20%). F9: total 30%; blank
   stays blank; a recorded 0 is not erased. Check weighted WBS/project summaries.
4. Correct an earlier entry. Verify Main, Monthly and charts recalculate together.
   Enter 60% + 50%: total 110% is warned, not silently clipped to 100%.
5. Cross a month boundary: each week belongs to its cutoff month, not prorated.
   Check early/late activities' Monthly % Complete and last-nonblank cumulative.
6. Set Dashboard Weekly/Monthly and move cutoff before/at/between/after reporting
   points. Actual display carries latest history only to cutoff, source blanks
   stay blank, KPI agrees with selected reporting category. Check marker/red line
   and date label, especially on first open and after view changes.
7. Check independent Main/Monthly cutoff controls. Raw history must not change.
8. Enter money including an explicit zero and a milestone value. Leave another
   Amount blank. Weights and progress must not change. Verify warnings and grouping.
9. Save, close and reopen. Repeat F9; verify inputs, dates, formulas and charts.
   No server rebuild is required for weekly Actual. Arbitrary Plan/row edits are
   not supported by F1. No Amount weighting/apply action is supplied.

## Preview — only after separate authorization

Coordinator integrates accepted changed files against the exact baseline, or
reviews a newer baseline delta. Git push may trigger deployment: obtain appropriate
permission first. Do not deploy from this handoff autonomously.

Use the existing Vercel project and accepted Services configuration, repository
root, web service `.` and Python `spikes/f0`, Python 3.12 and existing Node settings.
The only routing addition is `/api/progress/convert` -> converter before web catch-all.
No plan purchase or external hosting is required/authorized by this change.
Confirm `engine/` JSON/theme modules are packaged; tests/fixtures/envs stay excluded.

At an authorized actual Preview URL:
- Home -> Create, no default weighting, Friday/auto initially selected.
- Both XML formats, Equal/Duration, cutoff/distribution overrides, Generate ->
  intact download, processing/error/retry and download-again link.
- Invalid XML, no file, invalid duration, oversized input/output, non-JSON platform
  errors do not download HTML as XLSX or expose payloads/tracebacks.
- Keyboard/mobile layout, no browser console/hydration errors; M0 navigation and
  F0 proof route remain intact. Record timings and actual input/output sizes.
- Record exact Preview URL/commit and PO browser result. HTTP alone is not this gate.

## Reference and evidence limitations

PS reference 89a6b80: distribution auto.py/curves.py/rules JSON, export_theme.py and
dashboard_theme.json reused; workbook formulas adapted to Bluebird's separate
Progress Basis/Contract Value ownership. DF-1 raw/display/cutoff separation reused.
No desktop service pipeline or monetary subsystem is imported.

The workbook is a Bluebird renderer using PS rules/palettes, not a byte-for-byte
PS export: dashboard layout is compact (Plan, Actual, Gap); desktop activity-focus
panels, Time Impact card and embedded icons are not reproduced. Visual/layout parity
needs PO review; this handoff does not claim complete PS UI parity.

Automated checks cover serialized formulas, package integrity and numeric planning
oracles; they do NOT evaluate all live formulas in Desktop Excel. Browser automation
could not start in the engineering environment. The report records exact results.
