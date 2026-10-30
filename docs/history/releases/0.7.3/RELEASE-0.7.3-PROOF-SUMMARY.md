# eMuleBB MFC 0.7.3 Release Proof Summary

Status: published historical release evidence.

Stable `emulebb-v0.7.3` was published on 2026-07-05 from reviewed app commit
`9402251c`. The prior `emulebb-v0.7.3-rc.3` tag remains historical evidence at
app commit `fd17a04`. The stable tag started the bounded `release/0.7.x`
maintenance line.

The accepted shipped-scope proof included:

- clean validation and build execution for the locked RC3 source set;
- 1,439 Python harness tests, with 1,436 passes and three accepted Rust preview
  failures outside the MFC release scope;
- rebuilt x64 and ARM64 standard and diagnostics packages;
- rebuilt aMuTorrent x64 companion package;
- successful Pages `install.ps1` end-to-end dry-run;
- clean-worktree audit, manifests, SPDX SBOMs, SHA-256 hashes, and GitHub
  artifact attestations; and
- explicit operator acceptance for the remaining stable live, soak, and
  Windows-VM proof rows.

The final package and SBOM hashes are retained in the
[stable changelog](RELEASE-0.7.3-STABLE-CHANGELOG.md). Public release context is
retained in the [release notes](RELEASE-0.7.3-NOTES.md). Detailed intermediate
checklists, dated audits, rehearsals, and superseded execution plans remain
recoverable from Git commit `191c7c4dcf615e67fc89b3f24d44da951a4ef6ee`.
