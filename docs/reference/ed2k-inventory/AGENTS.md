# eD2K Inventory Maintenance

These rules apply to every file in this directory. They also govern refreshes
of the parent dashboard at `../ED2K-PROJECT-INVENTORY.md`.

## Required Workflow

1. Read `methodology.md` before researching or editing entries.
2. Preserve the parent dashboard path and its nine category headings so old
   links and category fragments keep landing on a useful index.
3. Search canonical upstreams, GitHub/GitLab/Codeberg, broader web results, and
   available local research archives. Do not limit discovery to GitHub stars.
4. Recheck canonical URLs, redirects, archive state, default-branch activity,
   releases, licenses, and visible CI for every project whose facts change.
5. Date every statistics snapshot. Keep unavailable values as unknown instead
   of estimating them.
6. Treat README and release claims as project-authored until source review,
   retained traces, or independent live evidence confirms them.
7. Keep servers, bootstrap lists, clients, controllers, libraries, adjacent
   protocols, historical mods, and archives in their existing category files.
8. Give every project exactly one detailed heading, one colored `Status` line,
   and one `Assessment` line covering activity, adoption, maturity, relevance,
   and participation mode.
9. Apply the activity/adoption tiers and historical preservation tiers from
   `methodology.md`. Within each tier, sort by verified activity date, adoption
   evidence, then project name.
10. Keep verified download-only or non-contributing clients visible under the
    red capability-warning tier and exclude them from healthy-peer rankings.
    Judge behavior, not developer nationality or project origin.
11. Preserve useful negative and incomplete evidence. Do not delete a stale,
    obscure, or low-quality project merely to improve the headline totals.
12. Update the parent dashboard totals, status mixes, adoption mixes,
    competitive snapshot, and category links whenever details change.

## Delivery Checks

- Confirm project-heading, `Status`, and `Assessment` counts match.
- Confirm category counts sum to the dashboard total and every status/adoption
  mix matches its detailed page.
- Check internal Markdown links and category anchors after moving content.
- Run `git diff --check` and the repository documentation validator.
- Build MkDocs and report unrelated pre-existing failures separately.
- Do not commit, push, merge, or change PR state unless the current user request
  explicitly authorizes that action.
