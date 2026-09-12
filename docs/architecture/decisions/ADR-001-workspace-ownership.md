# ADR-001 — Workspace ownership boundary

- Status: Approved
- Last Updated: 2026-09-12
- Authority: Canonical Workspace/Project ownership decision
- Implementation: Not implemented

## Context

Bluebird may eventually support users operating across multiple workspaces.
Ownership must be explicit before persisted projects appear, without requiring
organization-management features in the initial shell.

## Decision

Every Bluebird Project belongs to a Workspace.
Users relate to Workspaces through membership; a user may eventually own or
belong to one or more Workspaces.

Workspace is the foundational ownership/data boundary, not necessarily an early
UI feature. Personal Workspace creation for a user is an allowed initial option,
not a requirement implemented by this decision.

Do not model projects as globally unowned or tie ownership to a mutable,
user-facing identifier. Project identity is defined in
[Architecture foundation](../foundation.md#project-identity).

## Alternatives and rationale

- Globally unowned projects make later access boundaries implicit and expensive
  to retrofit.
- Direct user-only ownership embeds an assumption that conflicts with eventual
  shared or multiple workspace membership.
- Workspace ownership represents that boundary now while allowing minimal UI.

## Consequences and limits

Future storage/access design must respect the ownership boundary. A workspace
reference alone is not an authorization mechanism.

No membership schema, role matrix, owner lifecycle, transfer policy, invitations,
workspace switching, organization management, billing, or subscription UI is
designed here. Authentication is not introduced in M0.

Use the [decision timing gates](../foundation.md#decision-timing) before
implementing persistence or multi-user access.
