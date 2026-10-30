# Backlog Process

Active product work is GitHub-primary and documented in the owning product
section. Historical catalogs reserve old IDs but do not represent current work.

## Create Or Activate Work

1. Revalidate the request against current `main`, current product direction,
   and the owning product's scope.
2. Reject speculative, retired-product, or low-value work instead of parking it
   indefinitely.
3. Allocate the next unused product ID against both active and retained history.
4. Create the owning repository issue and add it to eMuleBB Roadmap Project #3.
5. Add the local engineering specification under the product's `active/items/`
   directory and link it from that product's active index.
6. Record constraints, acceptance criteria, validation, and required evidence;
   do not create a parallel plan or review ledger.

Rust items use `RUST-<CLASS>-<NNN>`. The migrated `CI-054` item retains its
legacy ID and must not be renumbered. New MFC maintenance work requires a new
open `emulebb/emulebb` issue and explicit Project #3 placement; the archived
MFC Project #2 is never reactivated for forward work.

## Update Active Work

- GitHub owns workflow status, product, phase, priority, milestone, discussion,
  and pull request linkage.
- The local item mirrors required metadata and owns durable implementation
  detail and evidence.
- Keep acceptance criteria and evidence in the owning item. Delete temporary
  branch plans after reconciliation.

## Close Or Reclassify Work

1. Revalidate the result against current `main`.
2. Update the owning issue and Project #3 status.
3. Record final implementation, evidence, decision, or rejection rationale.
4. Move detailed closed Rust records to the Rust history directory and remove
   them from the active index.
5. For a retired or consolidated product family, add the stable ID and archival
   disposition to its compact catalog and remove the standalone item file.
6. Do not keep `DEFERRED`, closed, ownerless, or superseded items under an
   active directory.

## Validation

```powershell
python scripts\docs-item-taxonomy-check.py
python scripts\docs-structure-check.py
python scripts\github-roadmap-check.py
python scripts\github-roadmap-check.py --product emulebb-rust
python -m mkdocs build --strict
```

Use `--github` with the roadmap checker when the token has project scope and
the task includes live issue/project reconciliation.
