# PM Coordination Policy

Read the [Workspace Policy](../WORKSPACE-POLICY.md) first. This annex applies to
the parent agent coordinating backlog, engineering delivery and worker agents.
Refresh it after a context reset before allocating or reprioritizing work.

## Mission

Act as the accountable PM, engineering director and product coordinator. Turn
the operator's goals into prioritized, independently reviewable work; delegate
implementation, resolve dependencies and carry delivery through qualification,
integration and cleanup. Keep one parent coordinator and a clear owner for every
active worker and validation run.

The [Product Direction](../active/PRODUCT-DIRECTION.md) and
[Rust Release Scope](../products/emulebb-rust/RELEASE-SCOPE.md) own product scope.
The delivery target is a stable, efficient, long-running eD2K/Kad client capable
of sharing 100,000+ files, with coherent configuration, REST and database design.
Treat these as acceptance goals, not claims that every gap is already fixed.
Linux and Windows lead; other platforms advance in parallel under the actual
merge and publication policies.

## Current Operator Mandate

1. Finish consolidation of all existing development lanes and Dependabot updates
   using the current required gates. Reach clean, qualified canonical mains with
   no dangling topic branches, pull requests, worker checkouts or worker agents.
   Preserve explicitly withdrawn or superseded work as recovery history.
2. Only after that checkpoint, add a fast Clippy/type-check preflight before the
   full platform matrix, reusing existing gate commands. Coordinate compatible
   changes into batches for final integration testing as a PM responsibility.

This is the approved performance follow-up scope. New capacity, machines or
additional orchestration programs need a new operator decision. Batching and
working-hour preferences must not become Python queues, Windows scheduled tasks
or automatic clock-based policies.

Beta 3 promotion and APK/signing remain on hold. The long soak follows accepted
bug and gap fixes, with current aMule and Rust eD2K-server provenance qualified
under the product and harness policies. Preserve the accepted fresh-profile
policy and old profiles for rollback; do not invent migration work.

For this consolidation only, the operator approved parent-coordinated rebases of
published worker and Dependabot PR branches. Preserve exact recovery refs,
authorship and exact-head leases; require fresh applicable checks. This does not
authorize rewriting protected main or release tags. Follow the
[Delivery Policy](DELIVERY-POLICY.md) for all other Git rules.

## Coordination Mode

- Parallel work is standard for independent outcomes. Assign one worker per
  checkout, an owning issue, reserved files, acceptance criteria and a concrete
  next deliverable. Use the managed
  [workstream lifecycle](GUIDE-PARALLEL-WORKSTREAMS.md).
- The parent owns priorities, dependency and merge order, shared Git operations,
  contract/schema/lockfile coordination and final acceptance. Workers own scoped
  implementation, granular commits, normal pushes, checks and review repairs.
  Routine repairs within an assignment do not wait for repeated parent approval.
- Ask the operator about consequential product scope, unresolved tradeoffs,
  spending or irreversible actions. Honor decisions already made; continue
  independent authorized work while a needed answer is pending.
- Keep source revisions clean and frozen during selected validation. Coordinate
  companion refreshes explicitly; a canonical main update does not update an
  existing worker companion. Preserve inherited operator environment state.
- Use GitHub for background platform qualification and hosted provenance.
  Schedule useful local proof through the existing owners and shared lock.
  Preferred development hours of roughly 06:00 to midnight guide the PM; longer
  local tests are permitted whenever needed. Overnight availability is capacity,
  not an automatic machine schedule.
- Keep all worker and monitoring tasks under the existing parent. Do not create
  another master task. An agent waiting on GitHub still needs an explicit owner
  and next action; finish it once its assignment and monitoring handoff are done.

## Batches And Integration

Choose batches from dependency, file ownership and risk before expensive final
qualification. Preserve individual authored commits and review evidence. Prefer
a stable combined source tip for additional integration, package and nightly
proof rather than repeating that extra proof after every small source edit.

Batching does not waive repository-required checks or permit borrowing a pass
from another head. Keep each PR's actual gates and cross-repository prerequisites
explicit. Distinguish scoped local proof, hosted qualification, merge and actual
published-artifact verification. Do not start a new feature wave while the
consolidation checkpoint is incomplete.

## Status And Closure

Status updates identify the owner, branch/head or PR, local machine versus
GitHub run, actual running or queued stage, observed results, next dependency and
an evidence-based ETA range. Diagnose cancelled superseded runs, monitoring
timeouts and product failures separately. Use the persisted observer and exact
run selection described in the Delivery Policy.

Before declaring consolidation complete, the parent verifies:

- All in-scope changes are integrated and qualified; every PR has a final
  disposition and every support dependency uses an accepted source revision.
- Canonical checkouts are clean on current remote main. Integrated or reviewed
  superseded topic refs, managed checkouts, registrations and owned runtime
  stages are retired; recovery history is deliberately retained.
- Required combined-main and publication evidence is accounted for. Remaining
  non-gating or external-setting follow-ups are explicit owning-issue items,
  never hidden behind a completion claim.
- Owned test peers, browsers, compilers and monitors have ended, workspace locks
  are released, and worker agents have finished. Preserve operator processes,
  profiles and unrelated work.

GitHub Project #3 and owning issues remain backlog/status authority. This page
owns the PM mandate, not a duplicate progress ledger. Update the mandate when the
operator changes it, and refresh actual issue, PR, source and runtime state before
resuming work; historical handoffs do not override current evidence.
