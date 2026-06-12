# CI-035 RC1 Proof Evidence Log

Dated proof, package-hash, and reset evidence for the `0.7.3-rc.1` final
proof item [CI-035](../../active/items/CI-035.md). This is the historical
evidence trail moved out of the active item to keep the item a current
spec; current status lives in CI-035 `Current Proof`. Entries are in the
order they were recorded and may reference superseded heads.

## 2026-06-05 Campaign Refactor And Blocked RC Quick Attempt

Implemented and pushed campaign-shape fixes:

- build-tests `86bd168`: split `installer-controller-surface` into a quick
  profile and an on-demand `installer-controller-surface-soak` monitor profile;
  made Hyper-V VM proof rows nonblocking/on-demand for RC.
- build `cf24d7d`: exposed the soak profile through the supported
  `python -m emule_workspace test live-e2e` wrapper.
- build `f4b7148`: release-campaign execution now writes run-owned
  `release-campaign-run-result.json` evidence with repo heads, command status,
  per-scenario evidence paths, and package manifest hash summaries.

Local-only follow-up waiting for network restore and push:

- build `fb6e286`: forwards `--vpn-guard-live-config` through
  `test certification`, fixing the fast certification child in aggregate
  release-campaign execution.

Latest dry-run:

- command:
  `python -m emule_workspace test release-campaign --campaign emulebb-0.7.3 --execute --dry-run --test-network all --continue-on-failure --live-wire-inputs-file repos\emulebb-build-tests\live-wire-inputs.local.json --vpn-guard-live-config repos\emulebb-build-tests\vpn-guard-live.local.json`
- report:
  `workspaces\workspace\state\release-campaign-runs\20260605T200148Z-emulebb-0.7.3\release-campaign-run-result.json`
- result: `planned`, `18/18` commands. The three former VM proof commands are
  not in the default RC quick gate.

Latest aggregate attempt:

- command:
  `python -m emule_workspace test release-campaign --campaign emulebb-0.7.3 --execute --test-network all --continue-on-failure --live-wire-inputs-file repos\emulebb-build-tests\live-wire-inputs.local.json --vpn-guard-live-config repos\emulebb-build-tests\vpn-guard-live.local.json`
- report:
  `workspaces\workspace\state\release-campaign-runs\20260605T200214Z-emulebb-0.7.3\release-campaign-run-result.json`
- result: `failed`, `18/18` commands completed because
  `--continue-on-failure` was used.
- blocker observed: outbound TCP 443 failed for both `github.com` and
  `nodejs.org` from Ethernet `192.168.1.210` and `hide.me` `10.54.226.231`.
  Live seed refresh, Node fallback download, public live-wire lanes, and REST
  probes reported `WinError 10051` / unreachable network. The local push of
  `fb6e286` also failed for the same reason.

Candidate package refresh from the failed aggregate run:

- package root:
  `workspaces\workspace\state\release\emulebb-v0.7.3-rc.1`
- provenance in manifests:
  - app `330ecb0f`
  - build `f4b7148`
  - build-tests `86bd168`
  - tooling `2a96b85`
  - aMuTorrent `3330109`

Candidate package hashes:

| Asset | SHA-256 |
|---|---|
| `Bootstrap-eMuleBBSuite.ps1` | `12681210589912f42578e211f12877daf13c874f47b150dfd007dfdabeda6ae6` |
| `emulebb-0.7.3-rc.1-x64.zip` | `20c667d7ac7f4d20faae4dfb1806f80f1c3c5bbbe783b6cdb9129642dc7c6a8f` |
| `emulebb-0.7.3-rc.1-diagnostics-x64.zip` | `a85a868f5bcd1fedf09a1141d86517d4d640b1af912726e8ff4c2e343aec14d4` |
| `emulebb-0.7.3-rc.1-arm64.zip` | `2c4edac659076fb313bb11a34a25219bf36db0c7fc51cbdeac5ec698afa7f894` |
| `emulebb-0.7.3-rc.1-diagnostics-arm64.zip` | `6ea4821f15c145c752fd3d3fdaabbac396d61b5254876a2afa795112c290d75e` |
| `emulebb-0.7.3-rc.1-amutorrent-x64.zip` | `125052bea370909864c29f66b7efc6b0927dc2a64117369e740781289cb3945d` |

Candidate SBOM hashes:

| SBOM | SHA-256 |
|---|---|
| `emulebb-0.7.3-rc.1-x64.sbom.spdx.json` | `09fa5c70754131cebbc0bb383c6f3a9e7f2accffb29c66a3f0055f23f6dd7064` |
| `emulebb-0.7.3-rc.1-diagnostics-x64.sbom.spdx.json` | `5627ea2367514d8a238d90ed635a2a2404f87e5d22b1bcd954397f799a83eb0b` |
| `emulebb-0.7.3-rc.1-arm64.sbom.spdx.json` | `ca3e62f0b8ecd2baec4b98bd0a6c7b5cfbceb0c173bdbf8b310506b1b265c1e5` |
| `emulebb-0.7.3-rc.1-diagnostics-arm64.sbom.spdx.json` | `994553e02342f1a914be48ac516c0a0a5aa8c5916f07616672a8c15a2d9a3f7f` |
| `emulebb-0.7.3-rc.1-amutorrent-x64.sbom.spdx.json` | `8caa2b6814b210690be4123b2a04b79243e7f28c3e487aa467c2de8d5fc1cfcf` |

Required next actions:

1. Restore outbound HTTPS connectivity for GitHub, nodejs.org, public eD2K
   seed downloads, and the live-wire/VPN proof path.
2. Push local build commit `fb6e286`.
3. Rerun the RC quick campaign with the same runtime input files.
4. Confirm or regenerate package hashes after the successful campaign, then
   rerun the clean-worktree audit.
5. Wait for a separate operator instruction before creating any tag.

## 2026-05-17 Release Freeze and Test Hold

The operator froze 0.7.3 RC1 and paused eMule test execution plus
test-harness edits. This checkpoint is documentation-only; it does not add final
proof evidence and does not close any acceptance row.

Known non-final proof state at the time of the hold:

- `CI-038` is now superseded by the 2026-05-23 current-head
  `ui-resource-depth` pass recorded below.
- The latest observed fast certification artifact failed in a live/UI lane.
- The latest observed overnight certification artifact was not final release
  evidence.
- Existing x64, ARM64, and optional aMuTorrent x64 package hashes remain
  non-final because package evidence, including SBOM hashes, must be
  regenerated from the selected heads after proof succeeds.

No feature, refactor, UI polish, warning-debt, dependency refresh, or roadmap
work may enter 0.7.3 RC1 unless a current release gate exposes a direct
blocker and the promotion is recorded explicitly.

## 2026-05-14 Closeout Prep Audit

Release closeout prep was performed without running live E2E, regenerating
packages, or creating tags. Current repo heads at the audit point:

- App `main`: `201d2ad`
- Build orchestration `main`: `4a8bf07`
- Build tests `main`: `b5e0735`
- Tooling docs `main`: `ce35476`

Documentation hygiene:

- The completed qBittorrent-style keyboard/menu slice is now tracked as
  historical `FEAT-057`.
- Active `FEAT-056` remains reserved for post-`0.7.3` release proof automation and
  operator evidence UX.
- The already-pushed implementation commit messages that mention `FEAT-056`
  are left intact as historical commit metadata.

Recent live-report audit:

- `repos\emulebb-build-tests\reports\live-e2e-suite\20260513-204910-emulebb-main-release`
  passed `rest-api`, `amutorrent-browser-smoke`, `prowlarr-emulebb`,
  `radarr-emulebb`, and `sonarr-emulebb` with no inconclusive suites. This is
  useful controller-surface signal, but it predates current app head `201d2ad`
  and is not final current-head proof.
- `repos\emulebb-build-tests\reports\live-e2e-suite\20260514-115418-emulebb-main-release`
  passed focused `shared-files-ui` only. It is not full live release proof.
- `repos\emulebb-build-tests\reports\live-e2e-suite\20260514-124016-emulebb-main-release`
  passed focused `preference-ui` only. It is not full live release proof.
- `repos\emulebb-build-tests\reports\live-e2e-suite\20260516-213444-emulebb-main-release`
  passed the full `release-expanded` weak-path profile on current heads with
  `100/100` required REST live download triggers. The aggregate recorded
  `rest-cold-start-dump-stress` as inconclusive because that extra cold-start
  lane found only `40/150` safe active-download candidates; all other children
  passed.

Package audit:

- Existing x64 and ARM64 package manifests were generated from app commit
  `805dda8`, build commit `24b5b04`, build-tests commit `b7477a3`, and tooling
  commit `dac7389`.
- Those packages remain rehearsal evidence only. Final x64 and ARM64 packages,
  manifests, SBOMs, and SHA-256 hashes must be regenerated from current
  release-ready heads after proof resumes.

## 2026-05-17 Non-UI Package Evidence

The operator requested the non-UI/package portion of release closeout while
holding UI testing. The following packages were regenerated and passed package
content verification, but this does not complete final proof because
`ui-resource-depth`, `certification --profile fast`, and the current quick
release proof gates were not run.

Selected package provenance recorded by the manifests:

> These rehearsal outputs used the earlier `0.7.3` release path and are not
> final RC1 assets. Final `CI-035` proof must regenerate packages under
> `emulebb-v0.7.3-rc.1` with `emulebb-0.7.3-rc.1-*` artifact names.

- App `main`: `3ab2744`
- Build orchestration `main`: `d9ce06f`
- Build tests `main`: `f314423`
- Tooling docs `main`: `03d6d79`
- aMuTorrent `main`: `b32efc5` for the optional aMuTorrent controller package

Core x64 package:

- command: `python -m emule_workspace package-release --config Release --platform x64`
- build summary:
  `workspaces\workspace\state\build-logs\20260517-135916\summary.json`
- package:
  `workspaces\workspace\state\release\emulebb-v0.7.3\emulebb-0.7.3-x64.zip`
- manifest:
  `workspaces\workspace\state\release\emulebb-v0.7.3\emulebb-0.7.3-x64.manifest.json`
- SHA-256:
  `4e8929cd1f1ce7f8c8ec27862a349a4fcc2037b7d48afa6f9ca7e663e76a87ca`
- package content check: 53 entries, 43 language DLLs
- package build warnings: 0

Core ARM64 package:

- command:
  `python -m emule_workspace package-release --config Release --platform ARM64`
- build summary:
  `workspaces\workspace\state\build-logs\20260517-135931\summary.json`
- package:
  `workspaces\workspace\state\release\emulebb-v0.7.3\emulebb-0.7.3-arm64.zip`
- manifest:
  `workspaces\workspace\state\release\emulebb-v0.7.3\emulebb-0.7.3-arm64.manifest.json`
- SHA-256:
  `5c7712ae327a0f3cd49d68c6783e8bbe5431cc4ae8b29a484c1169a9d5d4c10c`
- package content check: 53 entries, 43 language DLLs
- package build warnings: 564

Optional aMuTorrent x64 controller package:

- command:
  `python -m emule_workspace package-amutorrent --config Release --platform x64`
- package:
  `workspaces\workspace\state\release\emulebb-v0.7.3\emulebb-0.7.3-amutorrent-x64.zip`
- manifest:
  `workspaces\workspace\state\release\emulebb-v0.7.3\emulebb-0.7.3-amutorrent-x64.manifest.json`
- SHA-256:
  `1b4d2c74728c9752b335dd0e8dd4f62f5233c0137b5ca8f400c54d2020416117`
- package content check: 6624 entries

Cleanliness:

- `python repos\emulebb-tooling\ci\check-clean-worktree.py` passed.
- `python -m emule_workspace status` reported all managed repos clean.
- The interrupted `ui-resource-depth` process tree was stopped before package
  generation, and no `emulebb.exe`, `ui-resource-depth`, or `resource-ui-smoke`
  process remained afterward.

## 2026-06-05 Superseded Earlier Final-Proof Record

This section is retained as historical provenance only. It is not the current
RC1 state after the later campaign-profile, evidence-runner, and tray-refresh
changes. No tag should be created from this section.

Final quick RC1 leaf proof was rerun on 2026-06-05 with the operator-supplied
`hide.me` bind interface and VPN guard allow list
`176.10.104.0/22,149.88.27.0/24,98.98.148.0/23`. The tracked clean-worktree
audit passed before this evidence update.

Selected final provenance:

- App `main`: `abe374dd3378`
- Build orchestration `main`: `bb432ca2d91b`
- Build tests `main`: `c8336f5f201f`
- Tooling docs `main`: `e9d3fc513947`
- aMuTorrent `main`: `d25452a4889c`

Fast certification:

- command: `python -m emule_workspace test certification --profile fast`
- report:
  `workspaces\workspace\state\certification\20260605T123804Z-fast\certification-result.json`
- result: `passed`

Live E2E quick gates:

- `ui-resource-depth`: `passed`
  - report:
    `workspaces\workspace\state\test-reports\live-e2e-suite\20260605T124837Z-emulebb-main-release-10896\live-e2e-suite-result.json`
  - child suites: `resource-ui-smoke`, `preference-ui`
- `controller-surface`: `passed`
  - live controller suites: `rest-api`, `amutorrent-browser-smoke`,
    `prowlarr-emulebb`, `radarr-emulebb`, `sonarr-emulebb`
  - VPN proof observed public IP `149.88.27.82`
- `release-expanded-quick`: `passed`
  - report:
    `workspaces\workspace\state\test-reports\live-e2e-suite\20260605T162512Z-emulebb-main-release-13172\live-e2e-suite-result.json`
  - child suites: `command-line-smoke`, `preference-ui`, `shared-files-ui`,
    `config-stability-ui`, `search-ui-live`, `shared-hash-ui`,
    `startup-diagnostics`, `shared-directories-rest`,
    `shared-cache-invalidation`, `unc-mapped-drive-identity`,
    `vhd-long-path-special-names`, `rest-api`, `disk-space-guard-live`,
    `vhd-partfile-recovery`, `admin-volume-cleanup-audit`,
    `rest-cold-start-dump-stress`
- `cpu-heavy-quick`: `passed`
  - report:
    `workspaces\workspace\state\test-reports\live-e2e-suite\20260605T164632Z-emulebb-main-release-10136\live-e2e-suite-result.json`
- `stabilization-stress-quick`: `passed`
  - report:
    `workspaces\workspace\state\test-reports\live-e2e-suite\20260605T164749Z-emulebb-main-release-14664\live-e2e-suite-result.json`

aMuTorrent live add-on rows:

- `amutorrent-clean-startup`: `passed`
  - report:
    `workspaces\workspace\state\test-reports\amutorrent-clean-startup\20260605T170153Z-emulebb-main-release-15384\amutorrent-clean-startup-result.json`
- `amutorrent-emulebb-ui`: `passed`
  - report:
    `workspaces\workspace\state\test-reports\amutorrent-emulebb-ui-live\20260605T170215Z-emulebb-main-release-15652\amutorrent-emulebb-ui-live-result.json`
- `amutorrent-resilience`: `passed`
  - report:
    `workspaces\workspace\state\test-reports\amutorrent-resilience-live\20260605T170243Z-emulebb-main-release-7200\amutorrent-resilience-live-result.json`

Final package refresh commands:

- `python -m emule_workspace package-release --platform x64 --config Release --release-version 0.7.3-rc.1 --clean --build-output-mode ErrorsOnly`
- `python -m emule_workspace package-release --platform ARM64 --config Release --release-version 0.7.3-rc.1 --clean --build-output-mode ErrorsOnly`
- `python -m emule_workspace package-amutorrent --platform x64 --config Release --release-version 0.7.3-rc.1 --clean --build-output-mode ErrorsOnly`

Final build recaps:

- `workspaces\workspace\state\build-logs\20260605T170416Z-package-release\build-result.json`
- `workspaces\workspace\state\build-logs\20260605T170634Z-package-release\build-result.json`

Final package hashes:

| Asset | SHA-256 |
|---|---|
| `Bootstrap-eMuleBBSuite.ps1` | `12681210589912f42578e211f12877daf13c874f47b150dfd007dfdabeda6ae6` |
| `emulebb-0.7.3-rc.1-x64.zip` | `4e36f4d50fd395a7bf9478ca8e2145e2c4956e2547b91d3bdb1506a9bbfdf7dc` |
| `emulebb-0.7.3-rc.1-diagnostics-x64.zip` | `4e64b88accb682a89f4715514c5e377d7f16be0ea26cc72639c2c79fecab2309` |
| `emulebb-0.7.3-rc.1-arm64.zip` | `dda0169108b809555cf5118eaad1b59e97c2848d6ab0147dafbc2d18b6f40eb9` |
| `emulebb-0.7.3-rc.1-diagnostics-arm64.zip` | `73ec265af1015a84ec4eaae14276a9d07357aa1babed5a02afac9960e612c511` |
| `emulebb-0.7.3-rc.1-amutorrent-x64.zip` | `1f023f8dd0b2b698dc49107f3819c2ad0afa0b2428f740168f8e2b20e829f38b` |

Final SBOM hashes:

| SBOM | SHA-256 |
|---|---|
| `emulebb-0.7.3-rc.1-x64.sbom.spdx.json` | `1ff24520c829de63a99eea5e4fc399ca94da40c706171dfd72f5552ca920a54c` |
| `emulebb-0.7.3-rc.1-diagnostics-x64.sbom.spdx.json` | `a1339acc5a3595bb2b98c52fe9d03a7135653e68fcd6060a95c3ce0712889ed8` |
| `emulebb-0.7.3-rc.1-arm64.sbom.spdx.json` | `6ca1832cbc6218c1e0b88a6c674ed4bb53408ea7b00e5182863fda5ca9c2b1f6` |
| `emulebb-0.7.3-rc.1-diagnostics-arm64.sbom.spdx.json` | `ddd3241a624128a22dc6e23622e7c2fcb32576f210371c86b4c63b7604e1303b` |
| `emulebb-0.7.3-rc.1-amutorrent-x64.sbom.spdx.json` | `b10f56df620746345fafaeaecf2b725bd6230e77cec1d6292f56d37303303ab1` |

Package manifest checks:

- x64 and ARM64 standard and diagnostics manifests record `43` language DLLs.
- x64 and ARM64 standard and diagnostics packages contain no legacy
  `webserver` payload entries.
- optional aMuTorrent x64 package contains no `webserver` payload entries.
- manifests record ZIP SHA-256, executable SHA-256, SBOM path/hash,
  bootstrapper asset/hash/path, and per-file package hashes.

Clean-worktree audit:

- command: `python repos\emulebb-tooling\ci\check-clean-worktree.py`
- result before this evidence update: `Tracked worktree cleanliness audit passed.`

The full overnight certification and full-duration overnight campaign remain
deferred soak/confidence evidence, not part of the quick RC1 publication gate.

Annotated RC1 tag:

- operator confirmation: received on 2026-06-05 after final clean proof
- tag: `emulebb-v0.7.3-rc.1`
- target: `abe374dd3378e6a1b292a363f9dfe1ae6f2f74dc`
- tag object: `6f251ec88f72deafa1a32c8df79d6ae9dcaf559b`
- push result: `refs/tags/emulebb-v0.7.3-rc.1` created on `origin`

## 2026-06-05 Package Refresh And 2026-06-04 Installer VM Proof

Current-head package assets were regenerated on 2026-06-05 after the stale
bootstrapper evidence mismatch was found. The latest installer-controller VM
proof is still the 2026-06-04 clean Win10/Win11 pass recorded below; rerun that
VM proof if the operator requires post-refresh package execution evidence.

Selected package provenance recorded by the manifests:

- App `main`: `22c5606d`
- Build orchestration `main`: `cd714f5`
- Build tests `main`: `09915b2`
- Tooling docs `main`: `8786574`
- aMuTorrent `main`: `d25452a` for the optional aMuTorrent controller package

Package refresh commands:

- `python -m emule_workspace package-release --config Release --platform x64 --release-version 0.7.3-rc.1 --build-output-mode ErrorsOnly`
- `python -m emule_workspace package-release --config Release --platform ARM64 --release-version 0.7.3-rc.1 --build-output-mode ErrorsOnly`
- `python -m emule_workspace package-amutorrent --config Release --platform x64 --release-version 0.7.3-rc.1 --build-output-mode ErrorsOnly`

Build recaps:

- `workspaces\workspace\state\build-logs\20260605T062213Z-package-release\build-result.json`
- `workspaces\workspace\state\build-logs\20260605T062537Z-package-release\build-result.json`

Installer-controller VM proof:

- command:
  `python -m emule_workspace test windows-vm --matrix win10,win11 --profile installer-controller-surface-vm --release-version 0.7.3-rc.1 --local-swarm-mode execute`
- report:
  `workspaces\workspace\state\test-reports\windows-vm\20260604T124345Z\windows-vm-summary.json`
- result: `passed` on `win10` and `win11`
- campaign scenario: `emulebb.flow.controller.installer-swarm.v1`
- local-swarm network contract: control bind `lan`, aMuTorrent bind `lan`,
  P2P mode `local-swarm`, P2P bind scope `lan`
- selected VM suites passed on both guests: `command-line-smoke`,
  `amutorrent-browser-smoke`, `package-helper-integration`, and
  `godzilla-local-swarm`

Package hashes:

| Asset | SHA-256 |
|---|---|
| `Bootstrap-eMuleBBSuite.ps1` | `12681210589912f42578e211f12877daf13c874f47b150dfd007dfdabeda6ae6` |
| `emulebb-0.7.3-rc.1-x64.zip` | `b474d512997de10b43b5970b27952c06ed3e8a86f86468864a2f34d3f8e06f44` |
| `emulebb-0.7.3-rc.1-diagnostics-x64.zip` | `530539cb2284de8375afbacc8bb9feef338b74393f81891085fbd00293aaa932` |
| `emulebb-0.7.3-rc.1-arm64.zip` | `bf9a3c2a60ff2358d50cfba5b86dd3130a1c5096d2d92f9c1b4b281fa290b49c` |
| `emulebb-0.7.3-rc.1-diagnostics-arm64.zip` | `ace4fbcc0147158b2b66640272d680bc855ddf765c4186bda58d4a85dddd96e1` |
| `emulebb-0.7.3-rc.1-amutorrent-x64.zip` | `9e0c313e799431afb0c575ec63b1acfa4bbae01f46d705f002e69cbeae3518db` |

SBOM hashes:

| SBOM | SHA-256 |
|---|---|
| `emulebb-0.7.3-rc.1-x64.sbom.spdx.json` | `5287a6d3467b499e4008c48a8436bcdd27eb11299bcda374ed3258a2167aad1d` |
| `emulebb-0.7.3-rc.1-diagnostics-x64.sbom.spdx.json` | `6a0134b4dae10f91894ba73a352378a5d787d90aff18d42af27ff69b393efe12` |
| `emulebb-0.7.3-rc.1-arm64.sbom.spdx.json` | `0b7fe8d9ec89bea0b69178426ae75486cbf8254b6bbf6a2c9acfb3db20003312` |
| `emulebb-0.7.3-rc.1-diagnostics-arm64.sbom.spdx.json` | `3b8ef2be47064fa2192e2c731a59b572ea7a6eb8d9ca35a1e514a8d43223929b` |
| `emulebb-0.7.3-rc.1-amutorrent-x64.sbom.spdx.json` | `b6ac20bf3e40128f2d56943d26981bc7d8411de49588c1ff2689be665daa8dd6` |

Package content verification:

- x64 standard and diagnostics packages: 77 entries each, 43 language DLLs,
  no `webserver` payload entries.
- ARM64 standard and diagnostics packages: 77 entries each, 43 language DLLs,
  no `webserver` payload entries.
- optional aMuTorrent x64 package: 6624 entries and no `webserver` payload
  entries.
- manifests record package SHA-256, executable SHA-256, SBOM path/hash,
  per-file package hashes, bootstrapper asset name, bootstrapper SHA-256, and
  bootstrapper hash path.

Focused validation:

- 2026-06-05 package refresh:
  - `python -m pytest tests/test_powershell_policy.py tests/test_suite_installer.py tests/test_release.py -q`:
    `98 passed`
  - `python -m emule_workspace validate`: passed
  - byte-for-byte check confirmed the regenerated x64 package contains the
    current tracked copies of all eight package runtime PowerShell scripts.
- `python -m pytest tests/python/test_package_helper_integration.py -q`:
  `2 passed`
- `python -m pytest tests/python/test_rest_api_smoke.py -q`: `131 passed`
- `python -m pytest tests/python/test_windows_vm_profile_smoke.py -q -k "installer_controller or package"`:
  `2 passed, 15 deselected`
- `python -m emule_workspace test native --suite-name web_api --config Release --platform x64 --build-output-mode ErrorsOnly`:
  `79 passed`, `1890` assertions
- `python -m emule_workspace test live-e2e --suite package-helper-integration --test-network offline --fail-fast --dependency-mode auto-download --dependency-channel pinned`:
  passed with Prowlarr, Radarr, and Sonarr registrations
- `python -m pytest tests/test_ci_workflows.py -q`: `6 passed`
- `python -m emule_workspace validate`: passed

GitHub controlled smoke now includes a native Windows ARM64 lane:

- workflow: `.github\workflows\controlled-smoke.yml`
- runner: `windows-11-arm`
- ARM64 coverage: `package-release --platform ARM64`, extraction of the
  generated ARM64 ZIP, and direct `command-line-smoke.py` execution against the
  packaged ARM64 `emulebb.exe`

GitHub controlled smoke result:

- run:
  `https://github.com/emulebb/emulebb/actions/runs/26959062075`
- app commit: `ba82ca3b`
- build orchestration commit used by the reusable workflow: `ee5dc81`
- result: `success`
- x64 job:
  `Package and smoke (x64, windows-2022) / workspace command`, `success`
- ARM64 job:
  `Package and smoke (ARM64, windows-11-arm) / workspace command`, `success`
- ARM64 command step:
  `package-release --platform ARM64` plus direct extracted-ZIP
  `command-line-smoke.py` completed successfully

Release-campaign plan audit:

- command:
  `python -m emule_workspace test release-campaign --campaign emulebb-0.7.3`
- result: completed successfully as a plan/evidence audit
- current required gaps reported by the audit:
  controller-surface evidence, live-wire-release evidence, stabilization-stress
  evidence, and the manual clean-worktree packaging-provenance row
- packaging-provenance status reported by the audit:
  x64 package present, ARM64 package present, optional aMuTorrent x64 package
  present, Windows VM package smoke passed, and Windows VM package-helper
  install passed

Clean-worktree audit:

- command:
  `python repos\emulebb-tooling\ci\check-clean-worktree.py`
- result: `Tracked worktree cleanliness audit passed.`

UI resource-depth proof:

- stale harness expectation fixed in build-tests commit `2dbdbdf`
- command:
  `python -m emule_workspace test live-e2e --profile ui-resource-depth --fail-fast`
- report:
  `workspaces\workspace\state\test-reports\live-e2e-suite\20260604T152240Z-emulebb-main-release-11344\live-e2e-suite-result.json`
- result: `passed`
- child suites: `resource-ui-smoke` passed for release-language scope and
  `preference-ui` passed
- follow-up plan audit:
  `emulebb.flow.ui.resources.release-languages.v1` and
  `emulebb.flow.ui.preferences.resource-depth.v1` both report `passed`

Remaining `CI-035` work after this evidence:

- Run or accept the remaining quick release-campaign proof on the selected
  heads.
- Confirm the release checklist rows against these hashes and the final clean
  workspace state.
- Leave the annotated tag step blocked until the operator gives the separate
  tag instruction.

## 2026-05-23 0.7.3 RC1 Identity And Language Gate Refresh

Release package tooling and the release campaign were aligned with the
documented 0.7.3 RC1 identity before final package proof:

- Build orchestration commit `5dd105b` defaults `package-release` and
  `package-amutorrent` to `0.7.3-rc.1`, accepts `MAJOR.MINOR.PATCH-rc.N` and
  `MAJOR.MINOR.PATCH-beta.N` package labels, and compares only the base
  `MAJOR.MINOR.PATCH` value against the app `MOD_RELEASE_VERSION`.
- Build-tests commit `d63feb0` updates the campaign package evidence paths to
  `release\emulebb-v0.7.3-rc.1\...`.
- Focused validation passed:
  - `python -m pytest tests\test_release.py tests\test_cleanup.py tests\test_cli.py -q`
  - `python -m pytest tests\python\test_release_campaigns.py tests\python\test_release_coverage.py -q`
  - `python -m emule_workspace test release-campaign --campaign emulebb-0.7.3`

`CI-038` current-head proof passed:

- command:
  `python -m emule_workspace test live-e2e --profile ui-resource-depth --fail-fast`
- app commit: `ae562c1`
- build commit: `5dd105b`
- build-tests commit: `d63feb0`
- tooling commit: `88877cb`
- aggregate:
  `workspaces\workspace\state\test-reports\live-e2e-suite\20260523T192728Z-emulebb-main-release-8228\live-e2e-suite-result.json`
- resource smoke:
  `workspaces\workspace\state\test-reports\resource-ui-smoke\20260523T192729Z-emulebb-main-release-11900\resource-ui-smoke-summary.json`
- Preferences companion:
  `workspaces\workspace\state\test-reports\preference-ui-e2e\20260523T193413Z-emulebb-main-release-15452\preference-ui-e2e-summary.json`
- result: aggregate `passed`; `resource-ui-smoke` `passed` with 43 selected
  release languages, no missing language DLLs, isolated profile launches,
  representative view-command dispatch, and Preferences tree verification;
  Preferences companion `passed`.

Fast certification was attempted after the `CI-038` pass:

- command: `python -m emule_workspace test certification --profile fast`
- certification report:
  `workspaces\workspace\state\certification\20260523T193804Z-fast\certification-result.json`
- result: `failed` after 1123.698 seconds at `live-fast-ui-rest`
- passed before the live failure: validate; app builds for Debug x64, Release
  x64, and Release ARM64; test builds for Debug x64 and Release x64; Python
  harness; native Debug x64 tests; native Release x64 tests.
- failing child report:
  `workspaces\workspace\state\test-reports\rest-api-smoke\20260523T195610Z-emulebb-main-release-5332\rest-api-smoke-result.json`
- child status: `failed` at `nat_backend_order`; HTTPS PEM readiness and HTTPS
  certificate validation both passed.
- external blocker observed: the run correctly requested
  `p2p_bind_interface_name=hide.me`, but the local adapter inventory did not
  include an available `hide.me` interface, so eMuleBB disabled networking for
  that session.

Build-tests commit `3e8bd02` now classifies this specific startup log message
as `LiveNetworkUnavailableError` instead of waiting for a generic NAT backend
timeout. Focused validation passed:

- `python -m pytest tests\python\test_rest_api_smoke.py -q` passed with 112
  tests.
- `python -m emule_workspace test live-e2e --suite rest-api --fail-fast --skip-live-seed-refresh`
  produced an inconclusive REST child report at
  `workspaces\workspace\state\test-reports\rest-api-smoke\20260523T200230Z-emulebb-main-release-18976\rest-api-smoke-result.json`
  with `LiveNetworkUnavailableError` for missing `hide.me`.

This failed attempt is superseded by the passed 2026-05-23 fast certification
run below.

Fast certification passed after the `hide.me` interface was restored:

- command: `python -m emule_workspace test certification --profile fast`
- certification report:
  `workspaces\workspace\state\certification\20260523T202011Z-fast\certification-result.json`
- result: `passed` in 1122.13 seconds
- commits:
  - app `main`: `ae562c1f0492`
  - build orchestration: `5dd105b51167`
  - build tests: `3e8bd0223bf0`
  - tooling docs: `ca3f99fb2845`
- passed steps: validate; app builds for Debug x64, Release x64, and Release
  ARM64; test builds for Debug x64 and Release x64; Python harness; native
  Debug x64 tests; native Release x64 tests; `live-fast-ui-rest`.
- live aggregate:
  `workspaces\workspace\state\test-reports\live-e2e-suite\20260523T202122Z-emulebb-main-release-14020\live-e2e-suite-result.json`
- live children: `preference-ui`, `shared-files-ui`, `config-stability-ui`,
  `shared-hash-ui`, `startup-diagnostics`, `shared-directories-rest`, and
  `rest-api` all passed.
- REST child:
  `workspaces\workspace\state\test-reports\rest-api-smoke\20260523T203347Z-emulebb-main-release-6560\rest-api-smoke-result.json`
- local crash dumps: aggregate recorded `0` local dump files.

This closes the fast certification acceptance row. Overnight certification,
expanded live-wire proof, heavy/real-profile stress rows, package regeneration,
SBOM/hash recording, and final clean-worktree proof remain open.

## Stabilization Harness Hardening Before Proof Resume

Before final proof resumed, the `emulebb-build-tests` harness was hardened for the
next release-proof attempt:

- `b271cc5` adds a focused `stabilization-stress` aggregate profile and REST
  stress operation coverage accounting so scheduler starvation cannot pass as a
  green aggregate stress run.
- `447c1b4` keeps pre-crash manual dump evidence separate from crash-time dump
  channels in `local-dumps-crash-smoke`.
- `4369407` requires enabled REST leak churn to collect observable resource
  metrics before resource thresholds can pass.
- `756457c` enriches cold-start resource telemetry with CPU sample counts and
  high-CPU counters.
- `a80e953` records REST socket/TLS adversity and leak-churn settings in
  aggregate live E2E reports.
- `550bcc9` adds compact slowest-request diagnostics and API-key-safe failure
  samples for REST stress latency triage.
- `69108b4` requires `local-dumps-crash-smoke` to prove an access-violation
  exit, not just any process stop, before crash evidence can pass.
- `4a8bf07` exposes the `stabilization-stress` profile through the supported
  `python -m emule_workspace test live-e2e` wrapper.
- `60043bf` records cold-start resource-monitor enable/start/stop state.
- `61213ef` summarizes WER LocalDumps by executable image so eMule dumps are
  distinguishable from diagnostic-tool dumps.
- `d2a0751` fails cold-start stress when enabled resource monitoring produces
  no samples or does not stop cleanly.
- `cc6b952` treats signed and unsigned Windows access-violation exit codes as
  equivalent crash evidence.
- `a373ef8` classifies REST stress response failures as status, kind, body, or
  native JSON mismatches instead of leaving generic/blank reasons.
- `eb328f8` records resource deltas for the REST stop/start-after-churn
  relaunch path.
- `4a8c6c9` lists inconclusive child suite names in aggregate live E2E
  summaries.
- `28b7331` splits REST stress retry recoveries from failures that still needed
  retries.

Non-live verification after these harness changes:

- `python -m emule_workspace test python --workspace-root ..\.. -q` passed
  with 417 tests.
- `python -m emule_workspace validate --workspace-root ..\..` passed.

These changes improve the next proof attempt but do not complete `CI-035`.

## 2026-05-16 Certification Matrix

The release proof flow was rationalized under
[CI-036](../../history/items/CI-036.md). The supported command source of truth
is now:

- `python -m emule_workspace test certification --profile fast`
- `python -m emule_workspace test release-campaign --campaign emulebb-0.7.3`

The quick release campaign composes the blocking UI, REST, live-network, Arr,
aMuTorrent, stabilization, and crash-smoke lanes. The full overnight campaign
tracks full certification, generated CPU-heavy stress, and real-profile
monitoring as the long-form soak proof set.

This improves the next proof attempt but does not complete `CI-035`; fresh
certification reports and final package hashes still need to be generated on
the selected release-ready heads after proof resumes.

## Partial Evidence Captured Before Pause

These commands are current-head evidence, but they are not a complete final
proof:

- 2026-05-13: `python -m emule_workspace validate` passed.
- 2026-05-13: `python -m emule_workspace build app --config Debug --platform
  x64` passed. Summary:
  `workspaces\workspace\state\build-logs\20260513-115827\summary.json`.
- 2026-05-13: `python -m emule_workspace build app --config Release
  --platform x64` passed. Summary:
  `workspaces\workspace\state\build-logs\20260513-115904\summary.json`.
- 2026-05-13: `python -m emule_workspace build app --config Release
  --platform ARM64` passed. Summary:
  `workspaces\workspace\state\build-logs\20260513-115913\summary.json`.
- 2026-05-13: `python -m emule_workspace build tests --config Debug
  --platform x64` passed. Logs:
  `workspaces\workspace\state\build-logs\20260513-115929`.
- 2026-05-13: `python -m emule_workspace build tests --config Release
  --platform x64` passed. Logs:
  `workspaces\workspace\state\build-logs\20260513-115940`.
- 2026-05-13: `python -m emule_workspace test all --config Debug --platform
  x64` passed.
- 2026-05-13: `python -m emule_workspace test all --config Release --platform
  x64` passed.
- 2026-05-13: `python -m emule_workspace test live-e2e --profile
  controller-surface --fail-fast` stopped at Radarr. REST and Prowlarr passed;
  Radarr app/network/setup checks completed, but Radarr returned HTTP 200 with
  zero eMuleBB release rows until timeout. Report:
  `repos\emulebb-build-tests\reports\radarr-emulebb-live\20260513-120641-emulebb-main-release`.
- 2026-05-13: `python -m emule_workspace test live-e2e --config Release
  --platform x64` was operator-aborted and is not release evidence.

## Rehearsal Package Evidence

These packages were generated during `CI-034` proof, before this docs update.
They prove package flow and provenance recording, but they are not final
`CI-035` release hashes:

- x64 rehearsal SHA-256:
  `3f12e40a33fc02ef9f7b4e7858a7e450ef0524d26eabc72f05d28dc47b47079e`
- ARM64 rehearsal SHA-256:
  `5f4a3735a765a64cb0dea0a488d0ffd9e7d97ecf502d8859997c4e2cc26cb1c3`

Final package hashes must be regenerated and recorded after final proof resumes.

## 2026-05-14 Closeout UX Polish Reset

The operator accepted one last small closeout polish slice under
[FEAT-058](../../history/items/FEAT-058.md). The app README now points
`0.7.3 RC1` release source truth at reviewed `main` proof and no longer
depends on a broadband stabilization branch.

This resets the final candidate heads for proof purposes. The earlier live
reports and package manifests remain supporting or rehearsal evidence only;
final proof, x64/ARM64 packages, manifests, and SHA-256 hashes must be
regenerated from the pushed heads after this polish lands.

Closeout audit report:
`docs\history\release-0.7.3\audits\BETA-CLOSEOUT-UX-POLISH-2026-05-14.md`.

## 2026-05-14 Tray Preference UI Reset

The operator accepted one additional RC UI polish slice under
[FEAT-059](../../history/items/FEAT-059.md). Preferences > Display now places
`Always show tray icon` next to `Minimize to system tray`, and the old Tweaks
tree copy was removed.

This resets the final candidate app head for proof purposes. Final proof,
x64/ARM64 packages, manifests, and SHA-256 hashes must be regenerated from the
pushed heads after this polish lands.

## 2026-05-14 Preference Inventory Reset

The operator accepted preference persistence hardening under
[FEAT-060](../../history/items/FEAT-060.md). The app now centralizes native REST
mutable preference metadata, and `emulebb-build-tests` now guards the
`Preferences.cpp` `CIni` key inventory with Python drift tests.

This resets the final candidate app and build-tests heads for proof purposes.
Final proof, x64/ARM64 packages, manifests, and SHA-256 hashes must be
regenerated from the pushed heads after this hardening lands.

Audit report:
`docs\history\release-0.7.3\audits\BETA-PREFERENCE-INVENTORY-2026-05-14.md`.

## 2026-05-14 Preference Schema Reset

The operator accepted stronger preference schema validation under
[FEAT-061](../../history/items/FEAT-061.md). `emulebb-build-tests` now generates
and validates a section-qualified preference schema with REST and Preferences
UI source bindings.

This resets the final candidate build-tests head for proof purposes. Final
proof, x64/ARM64 packages, manifests, and SHA-256 hashes must be regenerated
from the pushed heads after this schema hardening lands.

Audit report:
`docs\history\release-0.7.3\audits\BETA-PREFERENCE-SCHEMA-2026-05-14.md`.
