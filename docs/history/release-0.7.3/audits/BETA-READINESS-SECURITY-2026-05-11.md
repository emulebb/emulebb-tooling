# Beta Readiness Review: Security

> Historical snapshot: this audit preserves the 2026-05-11 findings. Current
> beta 0.7.3 release source and pending execution status are controlled by
> [RELEASE-0.7.3-EXECUTION-PLAN](../../../active/plans/RELEASE-0.7.3-EXECUTION-PLAN.md).

## Executive Summary

Historical security audit. The beta candidate had solid evidence of bounded
REST parsing, static-file containment, release package naming, and
disabled-by-default REST/WebServer exposure, but this audit found security
issues in the update/release trust path, authenticated web surface, IP-filter
update transport, and Crypto++ dependency truth.

2026-05-13 release-owner disposition: only the update/release trust path remains
beta-blocking. Legacy WebServer session-token hardening is Wont-Fix for beta
`0.7.3`; IP-filter HTTP update transport is accepted as not release scope; and
Crypto++ 8.9 refresh is deferred post-beta.

## Review Checklist

- [x] Read `AGENTS.md` and `repos\emulebb-tooling\docs\WORKSPACE-POLICY.md` before reviewing.
- [x] Ran `git status --short --branch` before drawing conclusions in `repos\emulebb-tooling`, `repos\emulebb-build`, `repos\emulebb-build-tests`, `repos\emulebb`, active app worktrees, and relevant third-party dependency worktrees.
- [x] Confirmed assigned report file did not exist before writing it.
- [x] Reviewed active app worktree `workspaces\v0.72a\app\eMule-main` at `main` commit `df1191e`.
- [x] Reviewed parity baseline `workspaces\v0.72a\app\eMule-v0.72a-community` at `release/v0.72a-community` commit `c63f6e0`.
- [x] Reviewed broadband stabilization worktree `workspaces\v0.72a\app\eMule-v0.72a-broadband` at `release/v0.72a-broadband` commit `57dd9f7`.
- [x] Reviewed update-check, release packaging, REST/API auth, WebServer sessions, static-file serving, direct download, IP-filter update, and dependency pin evidence.
- [x] Verified `repos\emulebb-build-tests` had pre-existing modified/untracked files and did not modify them.
- [ ] Re-run security-focused validation after fixes land: update-check tests
      and package-release rehearsal.
- [ ] Reconcile dependency status docs with actual topology before tagging.

## Findings

### Critical: Release Update Checker Trusts The Wrong GitHub Repository

Severity: Critical

Affected area: Release/update mechanism, public beta package trust, product naming/version policy

Evidence:

- `srchybrid\Preferences.cpp:3654` returns `https://github.com/itlezy/eMule/releases`.
- `srchybrid\Preferences.cpp:3659` returns `https://api.github.com/repos/itlezy/eMule/releases/latest`.
- `srchybrid\EmuleDlg.cpp:964-976` uses `ReleaseUpdateCheck::CheckLatestRelease()` and opens the returned `strReleaseUrl` when a newer release is found.
- `repos\emulebb-build-tests\src\release_update_check.tests.cpp:17` builds test JSON with `https://github.com/itlezy/eMule/releases/tag/...`, so the test suite currently preserves the wrong owner.
- Workspace policy requires the GitHub organization/code name/URL slug to be `emulebb`, tags to use `emule-bb-vMAJOR.MINOR.PATCH`, and first public beta to be `emule-bb-v0.7.3`.

Impact:

An enabled update check can direct users to releases from a repository outside the policy-owned `eMulebb` namespace. Because the evaluator accepts any JSON from the configured latest-release endpoint if the tag and asset names match, the wrong repository owner becomes part of the release trust boundary. For a public beta this is a supply-chain and brand-trust blocker even though the code does not auto-install the asset.

Recommended fix:

Move the release-check base and API URLs to `https://github.com/emulebb/emulebb/releases` and `https://api.github.com/repos/emulebb/emulebb/releases/latest`, then add tests that fail on `itlezy/eMule` and pass only for the policy-owned URL family. Keep the existing strict tag and asset-name parsing.

Suggested validation:

- `python -m emule_workspace validate`
- `python -m emule_workspace test native --config Debug --platform x64`
- Targeted native test filter for `release_update_check.tests.cpp` if the harness exposes one.
- Manual smoke with update notifications enabled against a controlled latest-release JSON seam or test double, confirming the notifier opens the `emulebb/emulebb` release URL.

Owner suggestion: App/release engineering.

Execution checklist:

- [ ] Change `CPreferences::GetVersionCheckBaseURL()` and `CPreferences::GetVersionCheckApiURL()` in `srchybrid\Preferences.cpp` to the `emulebb/emulebb` release endpoints.
- [ ] Update `repos\emulebb-build-tests\src\release_update_check.tests.cpp` to build release URLs under `https://github.com/emulebb/emulebb/releases/tag/...`.
- [ ] Add a focused test that rejects or at least detects the old `itlezy/eMule` URL in release-check fixtures.
- [ ] Run the supported validation commands above through `repos\emulebb-build`.

### Critical: Legacy WebServer Sessions Are Predictable

Severity: Critical

Affected area: WebServer authentication/session management

Evidence:

- `srchybrid\WebServer.cpp:438` reseeds the process RNG with `srand((unsigned)time(NULL))` inside request handling.
- `srchybrid\WebServer.cpp:478` creates an admin session id with `(long)(rand() >> 1)`.
- `srchybrid\WebServer.cpp:492` creates a low-rights session id with `(long)(rand() >> 1)`.
- `srchybrid\WebServer.cpp:4213` and `srchybrid\WebServer.cpp:4243` authorize by matching only the numeric `ses.lSession`.
- `srchybrid\Preferences.cpp:3233` shows the WebServer is disabled by default, but `PPgWebServer.cpp:41` presents `0.0.0.0` as the default effective bind address when users enable it.

Impact:

When the legacy WebServer is enabled, session ids are small and predictable from wall-clock time. A remote attacker who can reach the WebServer and infer or race a login can guess the session id and reuse it for authenticated WebServer actions without the password or REST API key. This affects an advertised controller/web surface and should block a public beta until fixed.

Recommended fix:

Replace numeric `rand()`-based sessions with cryptographically random session tokens. Prefer a 128-bit or larger hex token generated by `BCryptGenRandom` or the already-used `CryptoPP::AutoSeededRandomPool`; store it as a string in `Session`; compare exact string tokens; stop reseeding `rand()` per request.

Suggested validation:

- `python -m emule_workspace validate`
- `python -m emule_workspace test native --config Debug --platform x64`
- Add/extend WebServer auth-state seam tests to assert session tokens are non-empty, high-entropy-length strings, and not reproducible after controlling `time(NULL)`.
- Add a smoke test that login succeeds with the generated token and random adjacent/old numeric guesses fail.

Owner suggestion: App WebServer/API owner.

Execution checklist:

- [ ] Change `Session::lSession` in `srchybrid\WebServer.h` to a token string or add a new token field while preserving template/query compatibility during migration.
- [ ] Generate session tokens with a CSPRNG and at least 128 bits of entropy in `CWebServer::_ProcessURL`.
- [ ] Remove request-level `srand((unsigned)time(NULL))` from `CWebServer::_ProcessURL`.
- [ ] Update `_IsLoggedIn`, `_GetSessionByID`, `_IsSessionAdmin`, `_RemoveSession`, and template substitutions to use the new token safely.
- [ ] Add native tests for token unpredictability and failed token guesses.

### High: IP-Filter Update Defaults To Unauthenticated HTTP

Severity: High

Affected area: IP-filter updater, direct download helper, security-list persistence

Evidence:

- `srchybrid\Preferences.h:1394` defaults `GetDefaultIPFilterUpdateUrl()` to `http://upd.emule-security.org/ipfilter.zip`.
- `srchybrid\Preferences.cpp:2871` loads that default into preferences when no explicit value exists.
- `srchybrid\DirectDownload.cpp:285` adds `INTERNET_FLAG_SECURE` only when the URL scheme is HTTPS; HTTP is otherwise accepted.
- `srchybrid\IPFilterUpdater.cpp:183-200` accepts ZIP archives and extracts `ipfilter.dat`, `guarding.p2p`, or `guardian.p2p`.
- `srchybrid\IPFilterUpdater.cpp:204` promotes the extracted file into the active IP-filter path.
- Automatic IP-filter update is disabled by default (`srchybrid\Preferences.cpp:2868`), but manual update and user-enabled automatic update share this transport.

Impact:

The IP filter is a security control. Fetching it over unauthenticated HTTP allows network attackers, captive portals, or mirror compromise on the path to replace the blocklist with attacker-chosen content. The current code rejects empty/markup payloads and promotes atomically, which helps corruption safety, but it does not authenticate origin or content.

Recommended fix:

Require HTTPS for built-in/default update URLs and for automatic updates. For manual updates, warn and require explicit confirmation for HTTP only if compatibility must be preserved. Add optional SHA-256 or signature verification if an official signed list is available; otherwise pin the default to a TLS endpoint and record that integrity is transport-based.

Suggested validation:

- `python -m emule_workspace validate`
- `python -m emule_workspace test native --config Debug --platform x64`
- Existing IP-filter update seam tests plus new cases for HTTPS accepted, HTTP auto-update rejected, and manual HTTP requiring explicit user confirmation.

Owner suggestion: App security/preferences owner.

Execution checklist:

- [ ] Replace `http://upd.emule-security.org/ipfilter.zip` with a vetted HTTPS endpoint or leave the default empty until an HTTPS source is selected.
- [ ] Add URL-scheme validation in `CIPFilterUpdater::QueueBackgroundRefresh()` before `DirectDownload::DownloadUrlToFile`.
- [ ] Add manual-update UI warning/confirmation or rejection for plain HTTP in `CIPFilterUpdater::UpdateFromUrlInteractive`.
- [ ] Add tests in `src\ip_filter.tests.cpp` for URL scheme policy and existing payload validation.

### High: Active Crypto++ Pin Is 8.4 Despite Known 8.4 Exposure And Docs Claiming 8.9

Severity: High

Affected area: Dependency pins, crypto/RNG/signature primitives, release documentation

Evidence:

- `repos\emulebb-build\emule_workspace\topology.py:335` pins `emulebb-cryptopp` to branch `CRYPTOPP_8_4_0-pristine`.
- `repos\emulebb-build\emule_workspace\topology.py:339` uses update baseline `CRYPTOPP_8_4_0`.
- `repos\third_party\emulebb-cryptopp\config_ver.h:53` defines `CRYPTOPP_VERSION 840`.
- `workspaces\v0.72a\app\eMule-main\srchybrid\emule.vcxproj:91` and `:128` link `cryptlib.lib`.
- `repos\emulebb-tooling\docs\dependencies\DEP-STATUS.md:18` and `:30` say the workspace pin is Crypto++ 8.9.0 / `CRYPTOPP_8_9_0`, which is not the active topology state.
- `repos\emulebb-tooling\docs\active\items\REF-034.md:3` tracks the upgrade from 8.4 to 8.9 as still open.
- NVD records CVE-2022-48570 as affecting Crypto++ through 8.4; Crypto++ 8.4 release notes also state the constant-time elliptic-curve revert reactivated CVE-2019-14318.

Impact:

The candidate links an older crypto library while current dependency documentation gives false assurance that 8.9 is already in use. The directly cited CVE is ECDSA-specific and I did not find app use of ECDSA in the reviewed active code, so this is not proof of an immediately exploitable eMule BB remote bug. It is still a release security risk because the dependency is active for RNG, RSA signatures, MD4/MD5/SHA wrappers, stream/datagram obfuscation support, and WebServer API-key generation.

Recommended fix:

Either upgrade the active topology and fork to a reviewed Crypto++ 8.9-based branch before beta, or explicitly document a release exception that proves no affected ECDSA/fault-injection path is reachable and schedules the upgrade as the first post-beta hardening item. The dependency status document must match the chosen state.

Suggested validation:

- `python -m emule_workspace validate`
- Full dependency build matrix through `python -m emule_workspace build --config Debug --platform x64`, `--config Release --platform x64`, and `--config Release --platform ARM64`.
- Native tests covering client credits signatures, collection signatures, REST API-key generation, encrypted stream/datagram paths, and package build.

Owner suggestion: Dependency/build owner with app crypto reviewer.

Execution checklist:

- [ ] Decide whether Crypto++ 8.9 upgrade is in-scope for beta or formally accepted as a documented beta exception.
- [ ] If upgrading, update `repos\emulebb-build\emule_workspace\topology.py`, regenerate managed topology artifacts via the supported workspace command path, and refresh `repos\third_party\emulebb-cryptopp`.
- [ ] If deferring, update dependency docs to state the active 8.4 pin, reachable-use analysis, CVE exception, and post-beta target.
- [ ] Run the supported build and native validation commands above.

## Missing Tests / Validation Gaps

- [ ] Release-update tests should assert the configured GitHub owner is `emulebb/emulebb` and should not carry `itlezy/eMule` fixtures.
- [ ] WebServer auth tests should cover session-token entropy, non-predictability under controlled time, failed token guessing, and token invalidation on logout/timeout.
- [ ] IP-filter updater tests should cover URL scheme policy, HTTP auto-update rejection, HTTPS happy path, archive payload limits, and post-update reload behavior.
- [ ] Direct-download tests should cover scheme allowlists and maximum downloaded byte budgets for updater use cases.
- [ ] Dependency validation should fail when `DEP-STATUS.md` claims a different active crypto pin than `repos\emulebb-build\emule_workspace\topology.py`.
- [ ] Final beta proof should re-run native REST/qBit/Torznab contract tests after auth/session changes.

## Cross-review Notes

- `repos\emulebb-build-tests` had pre-existing modified/untracked live-test files at review start; this report treats them as prior work and does not rely on their uncommitted content as final release evidence.
- Release packaging code is aligned with the 0.7.3 naming policy: `emule_workspace\config.py:145` defaults to `0.7.3`, `emule_workspace\release.py:60-64` uses `emule-bb-v0.7.3` and `eMule-broadband-0.7.3-ARCH.zip`, and `srchybrid\Version.h:42-44` defines app release version `0.7.3`.
- The REST/native API surface has meaningful hardening evidence: `WebServerJsonSeams.h` validates API key presence, JSON content type, path/query parsing, allowed routes, and bounded content; `WebSocketHttpSeams.h` caps headers and bodies; `WebServerStaticFileSeams.h` contains static files under the web root with percent-decoding checks.
- The WebServer remains disabled by default, diagnostic REST endpoints are disabled by default, and WebServer UPnP is disabled by default. Those defaults reduce exposure but do not remove the need to fix predictable sessions before public beta.

## Assumptions

- The active beta candidate is `workspaces\v0.72a\app\eMule-main` on `main`, not the broadband stabilization worktree, unless the release manager later gives a separate promotion instruction.
- `release/v0.72a-community` is the parity baseline, not a product release target.
- `analysis\stale-v0.72a-experimental-clean` was not needed for current-state conclusions.
- I did not run build/test/package commands because this was an audit-only task and the user limited file creation to this report.
- External dependency security references were used only to classify the Crypto++ 8.4 pin risk; current workspace files are the evidence for what is actually pinned and linked.

## Beta Readiness Verdict

Do not tag or publish `emule-bb-v0.7.3` until the release-update endpoint is
moved to `emulebb/emulebb` and the accepted non-blocker decisions above are
reflected in the active release docs.
