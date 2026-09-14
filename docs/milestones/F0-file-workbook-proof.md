# F0 — File workflow / runtime / workbook proof

- Status: Review (delivery acceptance)
- Scope authorization: Product Owner F0 prompt, 2026-09-14
- Implementation: Isolated proof delivered; not production-ready; F1 not started
- Authority: F0 scope and acceptance evidence

## Required reading

- ../../PROJECT_DESIGN.md — approved file-oriented V1 direction
- ../README.md — authority rules
- ../architecture/foundation.md — identity and adapter boundaries
- ../architecture/decisions/ADR-001-workspace-ownership.md — future scope
- ../features/progress-contract.md — initial weighting and Planned Budget
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
