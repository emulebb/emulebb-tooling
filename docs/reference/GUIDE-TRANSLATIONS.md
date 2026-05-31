# eMuleBB Translations And Localization

This guide defines how user-facing eMuleBB documentation should handle
translation without creating stale, misleading manuals.

## Current Strategy

The long-form product manuals in `repos\emulebb-tooling\docs` are
English-canonical. The public homepage in `repos\emulebb-pages` has localized
entry pages and should link users back to the maintained manuals.

Do not create broad translated Markdown copies of the product guides unless
there is an owner who will keep them current. Partial, stale translations are
worse than a clear canonical guide with a stable glossary.

Best current path:

1. Keep the full source manuals current in English.
2. Keep headings, glossary terms, screenshots, and field names stable.
3. Localize short public homepage summaries in `repos\emulebb-pages`.
4. Link localized homepage pages to the canonical guide sections.
5. Translate narrow high-value quickstart pages only when review capacity
   exists.

## What Should Stay Untranslated

Keep these exact in every language:

- executable and package names: `emulebb.exe`, `eMuleBB`, `aMuTorrent`
- command-line options: `-c`, `--help`, `--generate-webserver-cert`
- file names: `preferences.ini`, `server.met`, `nodes.dat`, `known.met`
- API routes: `/api/v1`, `/api/v2`, `/indexer/emulebb/api`
- HTTP headers: `X-API-Key`
- script names: `Register-aMuTorrent.ps1`, `Register-Prowlarr.ps1`,
  `Register-ArrStack.ps1`
- category identifiers used as config values: `emulebb-radarr`,
  `emulebb-sonarr`
- Torznab categories when used as numeric values: `2000`, `5000`, `7000`
- Windows paths and commands shown as examples

Translate the explanation around those terms, not the identifiers themselves.

## Glossary

| English Term | Translation Guidance |
|---|---|
| eMuleBB | Product name. Do not translate. |
| eMule broadband edition | Full product name. Translate "broadband edition" only when natural. |
| profile | User config/state directory. Avoid translating as a social profile. |
| config directory | Directory containing `preferences.ini` and state files. |
| temp directory | Incomplete `.part` file directory. Preserve technical meaning. |
| incoming directory | Completed download directory. |
| shared files | Files intentionally published to eD2K/Kad peers. |
| shared directories | Directories selected for sharing. |
| monitored shares | Directories watched for share changes. |
| eD2K | Network/protocol name. Do not translate. |
| Kad | Network/protocol name. Do not translate. |
| High ID | eD2K connectivity state. Keep the term recognizable. |
| Low ID | eD2K connectivity state. Keep the term recognizable. |
| firewalled | Kad/connectivity state. Translate as blocked by firewall if needed. |
| REST | API style. Do not translate. |
| WebServer | Product settings surface name. Keep recognizable. |
| API key | Authentication secret. Translate only the descriptive word "key". |
| Torznab | Adapter protocol name. Do not translate. |
| qBittorrent-compatible | Compatibility claim. Do not imply full qBittorrent feature parity. |
| Prowlarr | Product name. Do not translate. |
| Radarr | Product name. Do not translate. |
| Sonarr | Product name. Do not translate. |
| aMuTorrent | Product name. Do not translate. |
| Arr apps | Family term for Radarr, Sonarr, and related tools. Explain once. |
| bind address | Network listener address. Translate as network bind/listen address. |
| UPnP | Router feature. Do not translate. |
| port forwarding | Router/firewall operation. Translate normally. |
| diagnostic snapshot | Support evidence bundle. Translate as diagnostic report if clearer. |

## Style Rules

- Keep translated pages practical and task-first.
- Prefer short paragraphs and concrete steps.
- Preserve warning strength around profile sharing, API keys, and destructive
  transfer actions.
- Do not soften security wording in translation.
- Keep field names and UI paths exact when they match real application text.
- When a UI label is not translated in the app, keep the English label in the
  guide and translate only the surrounding explanation.
- Keep examples realistic but never include real API keys, live media titles,
  private server names, or private profile paths.

## Screenshot Rules

Screenshots help power users faster than long prose, but they also go stale.

Use screenshots when they show:

- the intended controller surface
- exact settings fields
- a before/after state
- a diagnostic screen that users must recognize

Do not localize screenshots separately unless the translated UI exists and can
be refreshed. If the screenshot is English-only, provide translated alt text
and translated explanation around it.

Screenshots must not expose:

- API keys
- private IP addresses unless they are example/private ranges
- real media titles from live-wire tests
- private filesystem paths
- user names, hostnames, or account identifiers

## Homepage Translation

Localized public homepage pages live in `repos\emulebb-pages`. They should:

- describe eMuleBB in the user's language
- link to the canonical documentation site
- avoid copying long guide sections
- use the same product claims as the source docs
- avoid announcing a stable release before release docs approve it

When the homepage needs a new translated sentence, update the structured source
used by the pages renderer, regenerate the static pages, and validate the pages
site. Do not manually edit each generated locale page.

## Manual Translation Workflow

For a narrow translated guide or quickstart:

1. Choose one source section, not the whole manual tree.
2. Record the source file and heading.
3. Preserve commands, paths, API routes, file names, and config keys exactly.
4. Translate the explanation.
5. Review the output against the glossary above.
6. Check links back to the canonical English guide.
7. Add a note that the English source is authoritative for current behavior.

Use this shape at the top of a translated quickstart:

```markdown
> This page is a localized quickstart. The English product guide remains the
> current source of truth for release behavior and API details.
```

## Machine Translation

Machine translation may be used as a draft aid, but not as an unattended bulk
replacement.

Acceptable:

- translating a short homepage summary
- translating a quickstart checklist
- generating a first draft for human review
- checking glossary consistency

Not acceptable:

- bulk translating the full manual tree without review
- translating API fields or command examples
- replacing stock eMule UI strings outside the release localization workflow
- changing legacy translation text without an explicit reason

Release-facing app resource strings are governed by the workspace release
localization policy and the release language helper scripts, not by this docs
guide.

## Related Docs

- [Product Guide](GUIDE-EMULEBB.md)
- [Setup Guide](GUIDE-SETUP.md)
- [Stack Integration Guide](GUIDE-STACK-INTEGRATIONS.md)
- [Documentation Policy](../DOCS-POLICY.md)
- [Workspace Policy](../WORKSPACE-POLICY.md)
