# F0 deployment gate — not executed on Vercel

Observed access: Vercel list_teams returned an empty teams array. Project listing
requires a teamId; there is no resolved team/project link, local .vercel/project.json,
VERCEL_TOKEN or installed Vercel CLI. Do not invent a team or deploy to an
unresolved project. This is an access limitation, not an engine/platform failure.

Executed: local HTTPServer using the headless Python handler, real MSP/P6 in
Equal and Duration, application/xml request, XLSX response, 208 activity rows,
method metadata, no-store, length headers, and no worksheet temp files left after
successful requests. Does not prove failure cleanup or concurrency safety.

The handler exports the file-based Python `handler` convention. Current official
docs describe /api Python functions and recommend Services for Python beside
another framework. Neither a same-project routing arrangement nor a deployed
Next.js->Python roundtrip has passed. No Vercel config or M0 UI was changed.

Smallest remaining step once the actual team/project is accessible: on an F0
preview only, package this engine and openpyxl as a Python conversion endpoint
alongside the unchanged Next.js shell using a supported routing arrangement.
POST both exact XML files under both methods; compare IDs, basis and formulas
with real_file_evidence.json. Check cold + warm responses, content headers,
request/output caps, transient cleanup and build dependencies. Keep production
untouched. Do not launch F1 UI, services unrelated to conversion, auth or storage.

https://vercel.com/docs/functions/runtimes/python
https://vercel.com/docs/functions/runtimes/python/api-directory
https://vercel.com/docs/functions/limitations


Final closure retry (2026-09-14): the same discovery result was observed again:
`list_teams` returned `teams: []`; no project/team was resolved. This blocked
preview target selection before a deployment could be submitted. There is no
failed build/runtime log or preview URL to claim. An empty account list does not
prove the user has no Vercel projects, only that this connection exposes none.

First restore access to the actual Bluebird team/project (or provide its linked
project context). Then perform the preview steps above without changing the
accepted application or adding a full upload UI. Independently restore GitHub
Contents write permission for the connection to Suzanoo/bluebird so the exact
local commit can be delivered on the designated F0 branch. The latest create-ref
request returned HTTP 403. Do not repeat desktop acceptance merely because these
account permissions remain unresolved.
