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
The delivery target is one universal, stable, efficient, long-running headless
eD2K/Kad daemon capable
of sharing 100,000+ files, with coherent configuration, REST and database design.
Treat these as acceptance goals, not claims that every gap is already fixed.
Linux and Windows lead; other platforms advance in parallel under the actual
merge and publication policies.

## Current Operator Mandate

1. Make parent-coordinated parallel branches and small integration batches the
   normal delivery routine. Keep canonical mains stable while workers develop
   independent outcomes. Carry each accepted batch through review, applicable
   qualification, merge and cleanup; a pushed checkpoint is not delivery.
2. Implement the approved change-aware CI acceleration before expanding the
   product implementation wave. Genuine docs-only changes get a short path;
   source, workflow, dependency, package-input and uncertain changes retain full
   qualification. Required aggregates always report. Classification must use
   trusted base code and the complete tested change range, fail safely to full
   checks, and retain exact source evidence. Scheduled/manual security and full
   nightlies retain their complete coverage. Keep developer checks under
   [#258](https://github.com/emulebb/emulebb-rust/issues/258) distinct from
   delivered hosted preflight [#323](https://github.com/emulebb/emulebb-rust/issues/323).
3. Lead the product wave with balanced reliability and the shared
   [#155](https://github.com/emulebb/emulebb-rust/issues/155)/
   [#233](https://github.com/emulebb/emulebb-rust/issues/233) storage contract.
   Accept ownership, bounded queue, durability, cancellation and shutdown
   contracts before implementation. Coordinate configuration/REST
   [#297](https://github.com/emulebb/emulebb-rust/issues/297) and schema
   [#298](https://github.com/emulebb/emulebb-rust/issues/298) reviews with that
   owner; scoping authorizes no schema edits or competing persistence actors.
4. [Scoop #324](https://github.com/emulebb/emulebb-rust/issues/324) is the first
   accepted new distribution lane, after its deployment/update contract is
   accepted. [Linux services #325](https://github.com/emulebb/emulebb-rust/issues/325)
   are a bounded review only, with implementation deferred. Optional expansion
   classification follows Release Scope and preserves actual required gates.
5. Reconcile delivered work with its owning issue, Project #3 placement, local
   item and retained evidence before allocating another implementation. Do not
   mistake an open stale tracking record for missing code or repeat unchanged
   validation. The completed consolidation is the baseline, not a recurring
   prerequisite for every new branch.
6. Deliver a clean Beta3 configuration contract: snake_case TOML/SQL/Rust,
   camelCase JSON and kebab-case URL segments. The accepted bootstrap keys are
   `bind_addr`, `api_key`, `web_root_dir`, with target REST `20017`, P2P TCP
   `20019` and UDP `20020`. No aliases, compatibility shims, fallback keys,
   legacy mappings or silently ignored obsolete fields are permitted. Require
   negative tests that prove retired shapes fail. Target acceptance does not
   claim the current runtime already implements it.
   The accepted ready-package bootstrap and first-fresh-profile key is
   `change_me_123change_me_123change_me_123` (36 ASCII characters); retain the
   32-byte minimum and normal authentication. Keep its listener on loopback
   and explain that this shared starter key must change before external API
   exposure. Packages share the canonical TOML; preserve existing user files
   and database preferences. Record actual package proof before claiming
   unpack-and-run delivery.

These are the approved delivery and intake boundaries. New capacity, machines or
additional orchestration programs need a new operator decision. Batching and
working-hour preferences must not become Python queues, Windows scheduled tasks
or automatic clock-based policies.

Beta 3 promotion and APK/signing remain on hold. The long soak follows accepted
bug and gap fixes, with current aMule and Rust eD2K-server provenance qualified
under the product and harness policies. Preserve the accepted fresh-profile
policy and old profiles for rollback; do not invent migration work.
Separately authorized CI-gated nightly publication does not lift those holds.
APT/RPM/Homebrew remain candidates, AUR/Nix remain unactivated, and no channel
hosting, signing, paid infrastructure or community publication is authorized by
the intake. Ubuntu 24.04/Debian 13 x64/ARM64 remain qualification targets until
their actual package dependencies and native results are recorded.

For the approved integration-batching routine, the operator approved
parent-coordinated rebases of published integration branches when main advances.
Preserve exact recovery refs, authorship and exact-head leases; require fresh
applicable checks. Earlier consolidation approval for worker and Dependabot
rewrites is not a blanket authorization for future unrelated rewrites. Never
rewrite protected main or release tags. Follow the
[Delivery Policy](DELIVERY-POLICY.md) for all other Git rules.

## Coordination Mode

- Parallel work is standard for independent outcomes. Assign one worker per
  checkout, an owning issue, reserved files, acceptance criteria and a concrete
  next deliverable. Use the managed
  [workstream lifecycle](GUIDE-PARALLEL-WORKSTREAMS.md).
- Bound work in progress by actual worker and validation capacity. With three
  worker slots, prefer two implementation owners and one review/test owner;
  a queued assignment is not an active agent. Reallocate a finished owner while
  GitHub qualifies a frozen batch, without changing its tested sources.
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

1. Select two or three compatible contributions with one coherent acceptance
   outcome. Freeze their base revisions, file reservations, interface contracts,
   dependency order and validation plan before editing. Changes to shared
   schemas, lockfiles, storage ownership or shutdown contracts need one owner
   or an agreed contract; separate branches alone do not prevent conflicts.
2. Workers develop in managed isolated branches, run scoped checks, retain
   granular authored commits and push clean checkpoints. For a declared batch,
   they hand those commits to the parent without opening individual PRs.
3. The parent reviews and integrates accepted commits linearly into a managed
   integration branch, preserving authorship and contribution traceability.
   Use cherry-picks where appropriate; Rust's rebase-only policy precludes
   local merge commits in its proposed history. Reject unrelated additions.
4. Accept implementation and source inspection after focused integration checks
   and normal hooks have passed, then freeze the combined clean tip and exact
   companion revisions.
   No known unresolved failure may be hidden by calling the batch review-ready.
5. Open one review-ready batch PR per affected repository so hosted platform
   qualification can run alongside the remaining applicable full local gate.
   State pending local proof explicitly in the PR. Run full local validation
   through the existing Builder and heavy lock; docs-only edits retain their
   documented lighter checks. Independent workers do not each repeat this final
   integration proof. This is PM coordination, not a queue or new automation.
   Merge only after all applicable local and hosted checks pass on the final
   selected sources. Merge providers before consumers and reconcile accepted
   pins before final consumer proof. Required hosted checks apply to the actual
   PR head and current base; batching never borrows passes or suppresses contexts.
6. While GitHub runs platform matrices and analysis, advance the next reserved
   independent work on other branches. Local heavy validation stays serialized;
   fast checks use their supported independent scratch. The parent may schedule
   useful long local tests during the day. Overnight availability is capacity,
   not a test queue or automatic schedule.
7. Merge in dependency order and verify the resulting main revisions. At a
   planned publication checkpoint, select a stable combined tip for the extra
   package/nightly proof instead of publishing after every small contribution.
   Retire integrated branches, registrations, checkouts and finished agents.

Independent outcomes that cannot form a coherent batch may retain separate PRs
under the Delivery Policy. Do not hold a ready safety fix behind unrelated work.
Distinguish scoped local proof, hosted qualification, merged source and verified
public artifacts in every delivery claim.

## Backlog Selection

- First reconcile current source and retained evidence with the owning issue;
  close or archive delivered specifications through the normal lifecycle.
- Rank confirmed security, data-loss, privacy and wire-correctness defects
  first. Then prioritize long-running reliability, bounded resource use and
  100,000-file scalability, configuration/API/schema coherence, and delivery
  improvements with measurable feedback savings. New confirmed critical defects
  can interrupt the planned wave.
- Use existing owning items rather than umbrella duplicates. Select a small
  verifiable slice with an observable before/after result; avoid simultaneous
  broad refactors. Core Client outcomes lead optional distribution expansion.
- Each proposed wave has three to six outcomes, explicit implementation versus
  review scope, branch/file ownership, acceptance proof and merge order. Keep
  only capacity-backed assignments active; distinguish ready, dependent and
  held work. Update Project #3 when execution is accepted rather than treating
  a proposal as an already-running assignment.

## Inspection And Refactoring Rounds

Every nontrivial implementation batch receives at least two distinct inspection
rounds before final acceptance. First inspect correctness, contracts and failure
behavior. Then inspect the revised result for missed interactions, unnecessary
complexity, duplicated ownership and maintainability; use an independent
reviewer where capacity permits. The parent performs final acceptance against
the actual integrated revision and applicable validation evidence.

Turn concrete findings into bounded repairs or justified refactoring, then
reinspect the changed result. Continue beyond two rounds while material findings
remain. A round may legitimately require no code change; do not manufacture a
refactor, new abstraction or unrelated cleanup merely to count activity. Keep
current naming contracts and hard rejection of retired shapes intact.

Preserve frozen inputs during an active gate. Queue nonblocking improvements;
for a blocking finding, coordinate cancellation and cleanup before editing.
After a repair, run the relevant focused checks and refresh applicable final
proof on the revised source set. Repeating an unchanged heavy matrix solely to
count inspection rounds adds no evidence. Record substantive findings, their
disposition and exact revisions in the owning issue/specification, not another
progress ledger.

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
