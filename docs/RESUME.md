# Current Handoff

## 2026-05-17 stopped release campaign

Testing was stopped on operator request during the first full release-campaign
execution after the campaign-runner work landed. The active campaign process
tree was terminated with `taskkill /PID 15248 /T /F`; the terminated child
processes included the live E2E runner, `shared-files-ui-e2e.py`, and the
launched `emule.exe` child. A follow-up process check found no remaining
campaign, live-E2E, or eMule child process from that run.

The interrupted report remains marked `running` because the runner was killed
before it could write a terminal status. Treat this run as operator-stopped,
not successful and not a clean failure.

Primary evidence paths:

- `EMULE_WORKSPACE_ROOT\workspaces\workspace\state\release-campaign-runs\20260517-182933-emule-bb-0.7.3\result.json`
- `EMULE_WORKSPACE_ROOT\workspaces\workspace\state\release-campaign-runs\20260517-182849-emule-bb-0.7.3\result.json`
- `EMULE_WORKSPACE_ROOT\workspaces\workspace\state\certification\20260517-182936-fast\result.json`
- `EMULE_WORKSPACE_ROOT\workspaces\workspace\state\certification\20260517-195542-overnight\result.json`
- `EMULE_WORKSPACE_ROOT\repos\eMule-build-tests\reports\live-e2e-suite-latest\result.json`

Recent pushed commits that were under test:

- app main: `b5dd003 REF-021 normalize app command line parsing`
- build tests: `9a8c811 REF-021 add command line release smoke coverage`
- build orchestration: `33b44b1 CI-003 add release campaign executor`
- tooling head while testing: `79aad48 docs: catalog eD2K server ecosystem`

Known completed verification before the full campaign:

- app Debug x64 build passed.
- app Release x64 build passed.
- tests Debug x64 build passed.
- tests Release x64 build passed.
- native `startup` and `parity` suites passed for Debug x64 and Release x64.
- Python harness passed with `521 passed`.
- command-line smoke passed directly for Debug and Release.
- aggregate live E2E `command-line-smoke` passed for Release.
- `python -m emule_workspace validate` passed.
- `python -m pytest tests` in `repos\eMule-build` passed with `85 passed`.
- release campaign dry-run with nonblocking commands passed/planned 16/16.

The full campaign command was:

```text
python -m emule_workspace test release-campaign --workspace-root EMULE_WORKSPACE_ROOT --execute --include-nonblocking --continue-on-failure --build-output-mode ErrorsOnly
```

Recorded campaign progress before the stop:

| Command | Status | Duration |
|---|---:|---:|
| `python -m emule_workspace validate` | passed | 3.341s |
| `python -m emule_workspace test certification --profile fast` | failed | 257.982s |
| `python -m emule_workspace test python --quiet` | passed | 19.801s |
| `python -m emule_workspace test protocol-parity` | passed | 1.768s |
| `python -m emule_workspace test community-core-coverage` | passed | 93.181s |
| `python -m emule_workspace test all` | passed | 13.283s |
| `python -m emule_workspace test live-e2e --profile controller-surface` | failed | 375.435s |
| `python -m emule_workspace test live-e2e --profile release-expanded --fail-fast --live-wire-inputs-file repos\eMule-build-tests\live-wire-inputs.local.json` | failed | 68.965s |
| `python -m emule_workspace test live-e2e --profile release-expanded` | failed | 3641.780s |
| `python -m emule_workspace test live-e2e --profile ui-resource-depth --fail-fast` | failed | 2.079s |
| `python -m emule_workspace test live-e2e --profile stabilization-stress --fail-fast` | failed | 691.134s |

The campaign was stopped while the next planned command,
`python -m emule_workspace test certification --profile overnight`, was running.
The overnight certification report recorded the static/build/native/Python
steps as passed, then recorded live failures in `live-fast-ui-rest`,
`live-controller-surface`, and `live-full-release` before the process was
stopped during later overnight work.

Fast certification failed only at `live-fast-ui-rest`; the preceding validate,
build, Python harness, and native all-tests steps passed.

Planned campaign commands not completed by the stopped run:

- `python -m emule_workspace test certification --profile overnight`
- `python -m emule_workspace package-release --config Release --platform x64`
- `python -m emule_workspace package-release --config Release --platform ARM64`
- `python -m emule_workspace package-amutorrent --config Release --platform x64`
- `python repos\eMule-tooling\ci\check-clean-worktree.py`

Immediate next work should focus on live E2E failure triage before rerunning the
campaign. The failures are all live-suite exits, not compile failures. Do not
treat the interrupted `running` certification or campaign reports as release
proof.
