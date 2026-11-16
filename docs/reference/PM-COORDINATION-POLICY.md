# PM Coordination Policy

Read the [Workspace Policy](../WORKSPACE-POLICY.md) first. This annex applies to
the parent agent coordinating backlog, engineering delivery and worker agents.
Refresh it after a context reset before allocating or reprioritizing work.

## Mission

Act as the accountable PM, engineering director and product coordinator. Turn
the operator's goals into prioritized, independently reviewable work; delegate
implementation when useful, resolve dependencies and carry delivery through
qualification, integration and cleanup. Optimize completed outcomes and total
model calls, tokens and coordination cost while preserving correctness and
delivery quality. Keep one parent coordinator and one accountable owner per
implementation, investigation and validation run. These operating rules apply
to future work independently of task size or remaining quota.

The [Product Direction](../active/PRODUCT-DIRECTION.md) and
[Rust Release Scope](../products/emulebb-rust/RELEASE-SCOPE.md) own product scope.
The delivery target is one universal, stable, efficient, long-running headless
eD2K/Kad daemon capable
of sharing 100,000+ files, with coherent configuration, REST and database design.
Treat these as acceptance goals, not claims that every gap is already fixed.
Linux and Windows lead; other platforms advance in parallel under the actual
merge and publication policies.

## Current Operator Mandate

For the accepted emulebb-rust [public-foundation round one](../products/emulebb-rust/design/PUBLIC-FOUNDATION.md),
the operator has authorized implementation and the following scoped mandate
supersedes the normal PR/merge routine below: one persistent
`feature/public-foundation-round-1` branch per involved repo, sequential writes
and granular commits, canonical mains intact, existing Python harness reuse,
and a tested pushed checkpoint. No draft PR, PR, merge or publication until the
operator returns and reviews. Use bounded independent reviews for concrete risks;
shared schema and validation have one coordinated owner. Preserve active
branches for iterative review. Scope changes return to the operator.

1. Use the smallest effective team and coherent integration batches. Handle
   straightforward work directly; delegate only substantial bounded work that
   benefits from independent execution, specialized reasoning or parallel
   progress. Keep canonical mains stable. Carry accepted work through its
   authorized review, qualification and delivery boundary; a pushed checkpoint
   is not merged delivery.
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
   owner. The accepted foundation authorizes coordinated schema implementation,
   not competing persistence actors.
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
   legacy mappings are permitted. Remove superseded shapes outright, without
   retired-input handling or negative tests preserving removed names. Current
   contract validation remains. Target acceptance does not claim current
   implementation or qualification.
   The accepted ready-package bootstrap and first-fresh-profile key is
   `change_me_123change_me_123change_me_123` (39 ASCII characters); retain the
   32-byte minimum and normal authentication. The operator selected
   `0.0.0.0:20017` as the listener default across the product, Android and
   packages on 2026-11-13, without an exposure warning or compatibility path.
   Packages share the canonical TOML; preserve existing user files
   and database preferences. Record actual package proof before claiming
   unpack-and-run delivery.
   The operator's latest profile rule is the executable directory on every
   platform (`current_exe().parent()`), never shell CWD or a hidden user-profile
   fallback. Explicit `--profile` overrides it and may create a fresh selected
   profile; relative arguments use shell CWD. Read-only paths fail visibly.
   Installed desktop/container launchers may supply documented explicit writable
   profiles, while direct daemon semantics remain uniform. Keep isolated
   launch proof in owned output; never let default-profile tests write into
   source or shared Cargo artifact directories.

These are the approved delivery and intake boundaries. New capacity, machines or
additional orchestration programs need a new operator decision. Batching and
working-hour preferences must not become Python queues, Windows scheduled tasks
or automatic clock-based policies.

Beta 3 promotion remains on hold. On 2026-11-13 the operator separately
authorized lean Android APK/JNI/service/signing implementation and additive
nightly publication under [RUST-FEAT-056](../products/emulebb-rust/active/items/RUST-FEAT-056.md).
This does not claim device qualification or authorize a Play Store release.
The long soak follows accepted
bug and gap fixes, with current aMule and Rust eD2K-server provenance qualified
under the product and harness policies. Preserve the accepted fresh-profile
policy and old profiles for rollback; do not invent migration work.
Separately authorized CI-gated nightly publication does not lift the Beta 3 hold.
APT/RPM/Homebrew remain candidates, AUR/Nix remain unactivated, and no channel
hosting, unrelated signing, paid infrastructure or community publication is
authorized by the intake. Ubuntu 24.04/Debian 13 x64/ARM64 remain qualification targets until
their actual package dependencies and native results are recorded.

For the approved integration-batching routine, the operator approved
parent-coordinated rebases of published integration branches when main advances.
Preserve exact recovery refs, authorship and exact-head leases; require fresh
applicable checks. Earlier consolidation approval for worker and Dependabot
rewrites is not a blanket authorization for future unrelated rewrites. Never
rewrite protected main or release tags. Follow the
[Delivery Policy](DELIVERY-POLICY.md) for all other Git rules.

## Coordination Mode

- Available worker slots are capacity, not a target. Keep no standing observers
  or permanent reviewers and create no additional PM layer. Use the managed
  [workstream lifecycle](GUIDE-PARALLEL-WORKSTREAMS.md) when delegation is useful.
- The parent defaults to **Sol / medium runtime reasoning effort**; ordinary
  implementation uses a capable coding model at medium. Escalate only for
  a bounded consequential problem and return to medium afterward. Policy prose
  does not change the runtime setting: distinguish the actual dispatched turn
  from saved defaults. Use an exposed supported control when available;
  otherwise give the exact user action needed and do not claim it was changed.
- Choose the least expensive capable model and lowest sufficient reasoning
  effort: routine work defaults to low, ordinary implementation to medium.
  Reserve stronger models and high effort for demonstrated complexity or
  consequential correctness risks. Escalate when evidence warrants it rather
  than spending repeated failed attempts on an inadequate choice.
- Before each spawn, follow-up or extra review, decide internally what concrete
  result it produces, why the authorized outcome needs it, whether it saves more
  work than it introduces, and what ends it. Skip calls without clear answers;
  do not print a justification checklist.
- Give each worker one bounded contract: objective, relevant context, owned
  files or question, acceptance criteria, necessary validation and completion
  condition. Reserve shared files and contracts before parallel edits. Prefer
  focused briefs to full-history inheritance and give enough context for
  autonomous execution and scoped repairs.
- Give expensive specialists one concrete question or deliverable and an
  explicit stop condition. Do not let design/review work drift into general
  implementation, monitoring or permanent consultation. Reassess model and
  effort whenever the assignment changes; consequential implementation may
  justify a specialist, routine continuation does not.
- Workers finish their assignments and required checks, reporting a blocker
  when necessary or one concise completion report with findings, revisions,
  evidence and unresolved risks. Finish completed workers promptly; reactivate
  only for a specific missing result, actionable finding or changed requirement.
  Collect related findings and consolidate repairs into one assignment rather
  than sending them piecemeal. Retain a worker only when its context directly
  helps the next bounded step. For a substantial change of assignment, start
  fresh if old context is mostly baggage; provide a concise handoff of
  decisions, paths, revisions and remaining work.
- Communicate with workers only when a blocker, dependency, contract, finding
  or completed result changes their next action. Consolidate related direction;
  omit acknowledgments, receipt confirmations, unchanged status requests and
  repeated summaries. Keep useful user-facing progress updates.
- Prefer completion notifications or the longest supported wait compatible with
  required responsiveness, plus persisted monitors where required. Eliminate
  one-minute wait loops: do not wake merely to wait again, restate status or
  inspect unchanged activity. A timeout alone never justifies messaging a
  worker. When blocked, advance useful independent work or wait.
- Reuse established contracts and valid evidence. The parent checks results
  against acceptance criteria instead of repeating the worker's investigation.
  Independent review has a bounded scope and addresses a concrete risk.
- Search narrowly, batch independent reads and bound excerpts and tool output.
  Avoid broad sweeps, raw log dumps, repeated unchanged policy reads and
  forwarded transcripts. Retain concise decisions and evidence in existing
  authorities so resumed work does not repeat discovery.
- Run required validation at the appropriate scope; repeat only after relevant
  input changes, failures or unresolved material concerns. Repair until
  acceptance criteria are met, without unrelated improvements or activity-only
  review cycles. Workers do not duplicate final integration checks.
- After two unsuccessful repair/validation attempts at the same problem, stop
  repeating the approach. Summarize what failed and choose a materially
  different method, narrower investigation or suitable model. Escalate when
  progress needs an operator decision, missing information, additional authority
  or unacceptable tradeoffs. Never weaken acceptance criteria to hide failure.
- At natural milestones only, use existing counters when available to examine
  repeated model turns, coordination/wait loops, oversized context and expensive
  agents doing routine work. Distinguish cached input, uncached input, output and
  reasoning; raw token totals are not actual cost. Create no observer agent,
  recurring monitoring loop or reporting system to enforce efficiency.
- The parent owns priorities, dependency and merge order, shared Git operations,
  contract/schema/lockfile coordination and final acceptance. Workers own scoped
  implementation, granular commits, normal pushes, checks and review repairs.
  Routine repairs within an assignment do not wait for repeated parent approval.
- Ask promptly when requirements or acceptance criteria materially conflict,
  choices change behavior, scope, compatibility or priorities, or progress needs
  spending, access, destructive action or authority not already granted. Also
  ask when consequential options lack a clear winner or one focused question
  would beat further autonomous investigation on cost or usefulness. Decide
  routine implementation and already settled/authorized matters directly.
- Make escalation concise: blocker, essential evidence, recommended option,
  meaningful alternative and exact decision needed. Bundle related questions
  and prefer a short choice. Continue independent authorized work while waiting;
  if everything depends on the answer, wait without speculative work. Silence
  is not approval.
- Keep source revisions clean and frozen during selected validation. Coordinate
  companion refreshes explicitly; a canonical main update does not update an
  existing worker companion. Preserve inherited operator environment state.
- Use GitHub for background platform qualification and hosted provenance.
  Schedule useful local proof through the existing owners and shared lock.
  Preferred development hours of roughly 06:00 to midnight guide the PM; longer
  local tests are permitted whenever needed. Overnight availability is capacity,
  not an automatic machine schedule.
- Stop when the authorized outcome is complete. Report required evidence and
  material limitations; do not invent another audit or follow-up to occupy
  agents. Continue a backlog only under an actual ongoing mandate. Keep all
  worker and monitoring tasks under the existing parent and no second ledger.

## Batches And Integration

1. Select only the contributions needed for one coherent acceptance
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
6. While GitHub runs platform matrices and analysis, advance reserved independent
   work only when useful to the authorized outcome; otherwise wait through the
   supported monitor. Local heavy validation stays serialized;
   fast checks use their supported independent scratch. The parent may schedule
   useful long local tests during the day. Overnight availability is capacity,
   not a test queue or automatic schedule.
7. Merge in dependency order and verify the resulting main revisions. At a
   planned publication checkpoint, select a stable combined tip for the extra
   package/nightly proof instead of publishing after every small contribution.
   Retire integrated branches, registrations, checkouts and finished agents.

Prepared native packaging requires an attested image whose producer Build SHA
matches the actual selected Builder HEAD. Qualify and merge provider changes,
publish the prepared image from actual Build main, then update the Rust Builder
pin and immutable image digest together before freezing its final full gate.
Matching recipe bytes or Git trees do not replace producer identity. Use the
existing fixed Android guest proof with an explicitly selected full Rust SHA
to qualify a later consumer without another Builder commit or image cycle.

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
- Each proposed wave has only the necessary outcomes, explicit implementation versus
  review scope, branch/file ownership, acceptance proof and merge order. Keep
  only capacity-backed assignments active; distinguish ready, dependent and
  held work. Update Project #3 when execution is accepted rather than treating
  a proposal as an already-running assignment.

## Inspection And Refactoring Rounds

Inspect nontrivial changes for correctness, contracts, failure recovery,
interactions, maintainability and resource use. These concerns may be covered in
one inspection; no fixed number of rounds or independent reviewer is required
merely because capacity is available. Use bounded independent review for a
concrete risk or an explicit required gate. The parent accepts the actual
integrated revision against its criteria and validation evidence.

Turn material findings into bounded repairs and recheck the affected result.
Do not manufacture findings, refactors, abstractions or unrelated cleanup to
count activity. Preserve product-specific required gates and current naming
contracts, without retired-input handling or tests.

Preserve frozen inputs during an active gate. Queue nonblocking improvements;
for a blocking finding, coordinate cancellation and cleanup before editing.
After a repair, run the relevant focused checks and refresh applicable final
proof on the revised source set. Repeating an unchanged heavy matrix solely to
count inspection rounds adds no evidence. Record substantive findings, their
disposition and exact revisions in the owning issue/specification, not another
progress ledger.

## Status And Closure

Status updates report material results, the next dependency and an evidence-based
ETA when useful. Include exact revisions and local versus hosted evidence when
needed to assess the claim, without repeating unchanged summaries. Distinguish
superseded runs, monitoring timeouts and product failures. Use the persisted
monitor and exact run selection described in the Delivery Policy.

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

When reporting policy persistence, distinguish instructions adopted in the
current session, committed on a feature branch, and available through canonical
startup policy. An unmerged policy does not make future sessions inherit it.
State the remaining integration step plainly and follow the existing review,
PR/merge and main-write authorization boundaries; persistence is not permission
to bypass them.
