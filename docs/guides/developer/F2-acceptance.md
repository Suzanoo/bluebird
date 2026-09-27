# F2 integration and acceptance

Scope: [F2 milestone](../../milestones/F2-xml-amount-weighting.md).
Rules: [Progress contract](../../features/progress-contract.md#f2-xml-amount-weighting--po-authorized-2026-09-26).
Baseline: `6db3e6665cb57cac8bfc5fa06f64454991c994fd`.

## Integrate and test (Coordinator)

Copy only the files in the handoff manifest to the same repository-relative paths.
Review any newer baseline changes before overwriting files. No dependency update
or new environment variable is needed. From repository root, with Python 3.12:

```sh
python -m pip install -r spikes/f0/requirements-test.txt
python -m unittest discover -s spikes/f0 -p 'test_*.py' -v
npm ci
npm run lint
npm run build
npx --yes vercel@59.23.2 dev -L --listen 127.0.0.1:3000 --yes
```

In another terminal in the same network namespace:

```sh
python spikes/f0/acceptance/f2_http.py http://127.0.0.1:3000
```

Services now routes `/api/progress/amount-preview` to the existing converter
before the web catch-all, alongside `/api/progress/convert`. No Next server proxy,
storage, login, queue or external hosting is added. Existing input/output limits,
admission lock, error/cleanup behavior and 60-second completion target remain.
Preview shares the bounded upload path, returns no-store JSON, and does not
generate XLSX. The server revalidates on Generate, not trusting a client flag.
The browser supplies the preview's source hash to reject changed bytes.

## Browser gate (local and authorized deployed URL separately)

1. Open `/create`: no default weight; Friday/auto unchanged.
2. Select XML, expand XML Amount, Inspect fields. No automatic field selection.
   Verify source-qualified field identity/type, including identical display names.
3. Select the allocated Contract Value field, Validate. Review all raw activity
   values, zero/positive counts, milestone warnings and ordinary basis total.
4. Amount becomes selectable only after valid preview. Select it explicitly,
   Generate, download an intact workbook, then test download again.
5. Change file or field: old preview/Amount readiness must clear. Invalid ordinary
   Amount or invalid present milestone Amount must prevent Amount Generate.
6. No declared numeric field: accurate message; Equal/Duration still available.
   These methods must not import or validate an unused monetary field.
7. Test malformed XML, oversized upload, retries, keyboard/mobile controls and
   no console/hydration error. Home/navigation/F0 page remain usable.

For reproducible synthetic inputs (no private projects), from repository root:

```sh
python -c "import sys; from pathlib import Path; sys.path.insert(0,'spikes/f0'); from test_f2 import amount_xml; Path('f2-msp.xml').write_bytes(amount_xml('msp')); Path('f2-p6.xml').write_bytes(amount_xml('p6'))"
```

Keep these generated files outside any integration commit. They contain ordinary
Amounts 100/300/0 and milestone 500. Additional blank/invalid cases are generated
by `amount_xml(source, ('100','300','0',None))` or last value `'bad'`.

## Windows Desktop Excel — PO-run, not automated acceptance

1. Generate both sources in Amount mode. Record Excel version. First open must
   have no repair prompt; verify all sheets and three charts.
2. Synthetic ordinary weights: 25%, 75%, 0%; milestone: 0%. Main project basis
   is 400, not 900. Activity Amount retains 100/300/0/500 independently.
3. Missing/blank milestone is blank, warned in preview/Guide/Amount formatting;
   explicit zero stays numeric zero. Invalid present milestone blocks Generate.
4. Enter first-week Actual 20%/40%/100%/100%: project Actual is 35%, not a monetary
   total. Leave later cells blank, then enter an explicit zero and another update.
   F9: verify weekly totals, month-of-cutoff summary and live Dashboard behavior.
5. Change cutoffs/Weekly-Monthly view: latest Actual carries only for chart
   display through cutoff. Source blanks stay blank; KPI and curve agree.
6. Main/Monthly overlays and Dashboard retain all lines/markers/cutoff indicator.
7. Edit Activity Amount only: weights must not change (F3 Apply not implemented).
8. Save, close and reopen: no repair; values/formulas/charts remain intact.
9. Smoke-test Equal/Duration; retain their accepted behavior and blank monetary
   input initialization. Preserve original files when reporting any failure.

## Deployed gate

Do not deploy from the engineering handoff. After separate authorization,
Coordinator uses the existing project/Services settings and checks both routes
and the complete browser workflow at the actual Preview URL. No paid plan or
new environment/configuration beyond the route in vercel.json is requested.
Record URL, integrated revision, timings, sizes and PO results. Local tests are
not deployed or Desktop Excel acceptance.
