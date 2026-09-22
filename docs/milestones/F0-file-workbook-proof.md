# F0 — File workflow / runtime / workbook proof

- Status: Approved — accepted / closed
- Scope authorization: Product Owner F0 prompt, 2026-09-14
- Implementation: Engineering, real XML, Desktop Excel and deployed workflow accepted by Product Owner; F1 not started
- Authority: F0 scope and acceptance evidence

## Current accepted state — recorded 2026-09-21

The Product Owner confirmed F0 completion, including deployed file-to-workbook,
real MSP/P6 XML and Desktop Excel acceptance, at accepted main baseline
`31f235a43c08c9a0c34bcdc29bc9b220872bcf03` and reported stable tag
`f0-file-workbook-proof-stable`. This is PO-reported acceptance; this documentation
update did not rerun those gates or independently verify the deployment/tag.

Earlier OPEN/CONDITIONAL PASS/access-blocker statements below are historical
handoff evidence, not outstanding gates. Preserve them as the record of what was
known at delivery. Proof appearance remains accepted. Later product semantics
are owned by the [Progress contract](../features/progress-contract.md), not by
historical F0 wording. The [F1–F6 sequence](file-workbook-roadmap.md) is approved;
F1 implementation remains unauthorized.

## Required reading

- ../../PROJECT_DESIGN.md — approved file-oriented V1 direction
- ../README.md — authority rules
- ../architecture/foundation.md — identity and adapter boundaries
- ../architecture/decisions/ADR-001-workspace-ownership.md — future scope
- ../features/progress-contract.md — current weighting and Activity Amount semantics
- ../../spikes/f0/README.md — reproducible proof and limitations

## Scope and evidence

P6/MSP fixtures to canonical model, explicit Equal/Duration, protected Main and
Activity Amount, local synchronous HTTP download, focused automated tests and
synthetic performance samples. No production Next.js route/UI, persistence,
Amount transition, general rebuild, BOQ, EV or Payment.

Run commands and results: ../../spikes/f0/evidence/ and spike README.
Automated tests pass. Desktop Excel lifecycle is accepted by the Product Owner
(see Final closure below). The deployed runtime/payload test remains outstanding.
F1 still needs separate Product Owner authorization.

## Real-file acceptance evidence (2026-09-14)

Both exact 009_MSP.xml and 009_P6.xml: 208 activities, 72 WBS, 67 weeks;
Equal denominator 208 and Duration denominator 34,464 hours. Four generated
workbooks pass automated formula/reference and user-input roundtrip checks.
14 focused regression tests pass. Real local HTTP conversions pass for all four
source/method combinations. Source files remain external to the repository.

The original MSP DurationFormat exclusion was incorrect and is fixed: format 7
means working days. Explicit evidence is now required before using an unlabeled
custom field as business Activity ID; this supplied pair supports FieldID
188743731 by a unique complete population match. These acceptance-specific
corrections do not add F1 functionality or approve universal import semantics.

At the real-file review, the result was CONDITIONAL PASS. The subsequent
Product Owner acceptance below updates that status; the earlier report remains
historical evidence. See spikes/f0/acceptance runners for reproducible checks.

## Final closure status (2026-09-14)

- Desktop Excel Gate: **PASS**, explicitly reported by the Product Owner in the
  final closure instruction. This is owner-run evidence, not an automated Excel
  test. The owner did not supply a version/build in that instruction.
- Proof-level colors/theme are accepted for F0; visual polish is not a failure
  or a condition for closure.
- Initial Equal/Duration and separate Planned Budget input remain unchanged.
- The only remaining technical acceptance gate is a deployed Next.js -> Python
  -> XLSX preview. No F1 implementation is authorized.
- Current recommendation: **CONDITIONAL PASS** pending that deployed proof and
  Product Owner final acceptance.

Repository delivery is separately blocked: retrying designated remote branch
creation returned GitHub HTTP 403 `Resource not accessible by integration`.
Completed work is committed locally for an exact format-patch handoff. No push,
merge, force-push, tag or release occurred. The closure report records the commit.
Deployment discovery also remains blocked: Vercel returned an empty teams array;
no linked project or CLI token is available. These are access limitations, not
proof that the Python runtime is unsuitable. The concrete next validation is
in [DEPLOYMENT_GATE.md](../../spikes/f0/acceptance/DEPLOYMENT_GATE.md).

## A1 runtime implementation handoff (2026-09-20)

Product Owner approved one-project Next.js + Python, direct same-origin browser
POST, no Next server proxy, experimental 4 MB upload and 60-second target.
Git handoff and collaboration adoption are accepted at branch
`feat/f0-file-workbook-proof`, HEAD `571abb9aadb75926ea944ddea856c9e90ed1db4e`.
Earlier GitHub-access blockers above are historical, not current acceptance gates.

Runtime adapter, minimal `/f0-runtime` page and Services config are delivered for
review. The accepted engine/model/renderer are unchanged. Automated tests (22),
Next lint/build and local Services HTTP checks pass. Local browser automation
was blocked by test-environment capability. No deployment was performed.

The selected gate is now browser on the Next.js page -> same-origin Vercel routing
-> Python -> XLSX download, not a Next server relay. The actual Preview browser
gate remains OPEN and requires Product Owner/Coordinator verification.
[Deployment procedure and checklist](../../spikes/f0/acceptance/DEPLOYMENT_GATE.md)
own reproduction/settings details. This handoff does not authorize Git writes,
deployment, purchase or F1. Prior real XML/Desktop Excel acceptance remains PASS.
