# F0 runtime proof — Preview gate OPEN

- Status: Implementation handoff; deployed acceptance pending
- Last updated: 2026-09-20
- Authority: F0 runtime reproduction and acceptance procedure
- Scope/acceptance authority: [F0 milestone](../../../docs/milestones/F0-file-workbook-proof.md)

## Implemented boundary

The approved A1 experiment uses one Vercel project: Next.js serves `/f0-runtime`,
and the browser posts raw XML to same-origin `/api/f0/convert?method=Equal` or
`Duration`. The top-level service rewrite routes directly to Python. There is no
Next server proxy, external service, account, storage or job queue.

`vercel.json` uses current `services` configuration (not `experimentalServices`).
Web root remains `.`; converter root is `spikes/f0`, FastAPI entrypoint `app:app`.
The endpoint retains the full public request path. Python is pinned to 3.12;
requirements.txt pins runtime dependencies including unchanged openpyxl 3.1.5.
The existing model.py, workbook.py and run.py are unchanged.

The endpoint enforces 4,000,000 bytes while reading, not only Content-Length.
The existing renderer output cap remains 4,000,000 bytes. One conversion per
Python process is admitted at a time; contention returns 503, with no queue.
This is not a global traffic limit or a demonstrated public capacity envelope.

`maxDuration: 60` requests a platform duration limit. A completed conversion that
finishes after the 60-second target is rejected, but CPU work is not forcibly
cancelled by the application. The browser aborts its request after 65 seconds.
Neither client abort nor local `vercel dev` proves hosted execution terminates
at 60 seconds. Hard platform termination can bypass Python cleanup.

## Privacy and scratch files

XML and XLSX stay in request memory; no uploaded file or workbook is written by
application code to durable storage. openpyxl uses temporary worksheet files
under the runtime temp directory. Normal save removes them. The serialized
adapter also removes only newly registered openpyxl scratch paths on catchable
failure, preserving pre-existing/unowned files. It does not sweep /tmp or mutate
global temp-directory settings. Cleanup failures leave the path registered for
openpyxl process-exit cleanup; hard kills and filesystem failures cannot promise
immediate erasure. This is coupled to pinned openpyxl 3.1.5 and has a regression
test that injects failure during actual archive writing.

No XML/workbook payload or traceback is returned in error messages or explicitly
logged. Provider/dev-server HTTP metadata can still be logged. Platform log
retention and residual scratch behavior are distinct from application persistence.
The CLI may start its generic local Queue/Cache emulators; this app uses neither.

## Local reproduction

From repository root, Python 3.12 and Node 24:

```sh
npm ci
python -m pip install -r spikes/f0/requirements-test.txt
python -m unittest discover -s spikes/f0 -p 'test_*.py' -v
npm run lint
npm run build
npx --yes vercel@59.23.2 dev -L --listen 127.0.0.1:3000 --yes
```

In another terminal on the same machine/network namespace:

```sh
python spikes/f0/acceptance/runtime_http.py http://127.0.0.1:3000
```

Open `http://127.0.0.1:3000/f0-runtime`. Direct `next dev` alone does not supply
Python routing. No project login is required by `vercel dev -L`.
The runtime smoke reuses existing tiny fixtures; its Duration variants add
synthetic duration fields using the same pattern as existing adapter tests.
It keeps generated workbooks in memory. Original no-duration fixtures must be
rejected for Duration; that is accepted behavior, not a runtime failure.

Observed: 22 Python tests passed; Next lint/build passed; local Services HTTP
conversion passed for both sources/methods. See engineering handoff for timings
and exact execution details. Local browser automation was blocked by environment
browser startup/download capability; do not label local HTTP as browser acceptance.
No real XML or Desktop Excel acceptance was repeated.

## Preview procedure — Coordinator only after separate authorization

1. Review/integrate the changed-file handoff against accepted branch baseline
   `571abb9aadb75926ea944ddea856c9e90ed1db4e`; preserve newer accepted work.
   A Git push can trigger a Preview automatically if connected, so coordinate
   that deployment permission before pushing to a deployment-enabled branch.
2. Use the existing Bluebird Vercel project, not a new external Python project.
   Confirm correct team/project, Preview permission, plan eligibility and Services
   availability. No paid plan/purchase is authorized. Stop if a plan change or an
   incompatible Services setup is required; do not switch architecture silently.
3. Project Root Directory: repository root. Services configuration owns web root
   `.` and converter `spikes/f0`. Confirm the project supports Services detection;
   if a dashboard framework preset is required, select Services rather than
   forcing the whole project to Next.js or FastAPI. Inspect existing build/install
   overrides for conflicts; do not overwrite unrelated project settings blindly.
   Node 24, Python 3.12, Fluid enabled by configuration; Python maxDuration 60.
   No application environment variables or service secrets are required.
4. With an authorized CLI login to the correct team, link to the existing project:

   ```sh
   npx --yes vercel@59.23.2 link
   npx --yes vercel@59.23.2 deploy
   ```

   These are future commands, NOT executed by Engineer. Verify the linked project
   before the second command. Deploy defaults to Preview; never use `--prod`,
   promote or change the production alias. Alternatively use the project's
   authorized Git Preview flow. No new CI workflow is needed.
5. Record the new Preview URL and exact integrated commit. Inspect both service
   build logs/function metadata: Python dependencies load, converter is Python,
   duration is 60, generated Python bundle excludes fixtures/tests/evidence/.venv
   and XLSX. Confirm the same-origin rewrite reaches Python with the full path.
   Local dev does not prove cloud packaging or settings acceptance.
6. Use the actual Preview URL in a browser. If Preview protection is enabled,
   Coordinator supplies authorized reviewer access; do not disable it implicitly.
   This is deployment review access, not product login implementation.
   For an endpoint accessible to the smoke runner, run:

   ```sh
   python spikes/f0/acceptance/runtime_http.py https://YOUR-PREVIEW-URL
   ```

   The runner has no protection bypass built in. Use authorized browser review or
   separately configured reviewer access where required, never publish credentials.

## Required deployed acceptance checklist

- Both existing Home and Workspace routes load; proof page has no console errors.
- No weighting preselected. Choose file/method, click Generate, observe processing,
  and receive `progress-f0.xlsx`. Verify XLSX ZIP integrity and expected sheets.
- MSP and P6 Equal work. Use suitable synthetic-duration variants for Duration;
  original fixtures with missing duration return a useful rejection.
- Invalid XML, missing file, unsupported method and >4 MB upload fail safely.
  Browser handles non-JSON platform 413/504 and never downloads an error page.
- Capture first/warm request timing, sizes and available runtime memory evidence;
  label cold starts only if observed. Confirm platform duration metadata and
  document timeout/disconnect behavior without claiming hard cancellation from UI.
- Test controlled concurrent requests: independent valid workbooks or explicit
  503; never mixed data. Local contention test is not hosted capacity evidence.
- Check no payload logging, durable files or retained generated-output URL;
  record scratch cleanup and hard-termination limitations.
- Product Owner/Coordinator verifies actual Preview browser Upload -> Generate ->
  Download and explicitly accepts the runtime gate. Local tests alone do not pass F0.

No repeat full Desktop Excel gate is required: renderer/calculation code is
unchanged. If integration later changes those components, identify the affected
gates before claiming preservation. F1 remains unauthorized.

## Platform references used

- https://vercel.com/docs/services
- https://vercel.com/docs/services/config-reference
- https://vercel.com/docs/services/routing
- https://vercel.com/docs/functions/runtimes/python
- https://vercel.com/docs/functions/limitations
- https://vercel.com/docs/plans/hobby

Services is Beta. Docs describe 4.5 MB function payloads; the lower experimental
4,000,000-byte cap is retained. Hosting can cost money even though users pay none;
Hobby is for non-commercial personal use. No plan eligibility or paid expenditure
is inferred by this handoff.
