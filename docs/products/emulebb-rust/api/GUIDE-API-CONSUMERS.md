# Use The REST API

The Rust daemon and its embedded browser console share the native `/api/v1`
contract. Start the daemon through [first launch](../reference/GUIDE-GETTING-STARTED.md)
and obtain its private API key. The canonical
[OpenAPI document](REST-API-OPENAPI.yaml) and [contract notes](README.md) define
exact routes, fields and errors; the MFC contract is separate.

## Make A First Request

In Bash, prompt privately for the key instead of placing it in shell history:

```bash
read -r -s -p "API key: " API_KEY
printf '\n'
curl --fail-with-body --include \
  -H "X-API-Key: $API_KEY" \
  http://127.0.0.1:4711/api/v1/capabilities
```

In PowerShell:

```powershell
$secret = Read-Host 'API key' -AsSecureString
$headers = @{ 'X-API-Key' = [System.Net.NetworkCredential]::new('', $secret).Password }
$response = Invoke-WebRequest -UseBasicParsing -Headers $headers -Uri 'http://127.0.0.1:4711/api/v1/capabilities'
$response.Headers['X-Contract-Version']
($response.Content | ConvertFrom-Json).data
```

These are client-side variables, not daemon configuration. They do not alter
workspace environment variables. Clear them when finished (`unset API_KEY` in
Bash; `Remove-Variable secret,headers,response` in PowerShell). The header value
necessarily exists in client memory; do not log it or include it in screenshots.

Authentication is **`X-API-Key` only** for all `/api/v1` routes. There is no
Basic/Bearer login exchange or query-token substitute. Keep the key out of URLs,
committed scripts and public reports. The daemon serves HTTP; remote TLS is the
reverse proxy's responsibility.

## Contract And Response Handling

Check response header `X-Contract-Version` and
`GET /capabilities` → `data.contractVersion` (currently `2.0.0`). This beta
contract is unstable for third-party consumers; the daemon, console and first-party
tooling evolve together. Version markers do not promise backward compatibility.

Ordinary successful JSON responses contain `data` and `meta`. Errors contain an
`error` object with `code`, `message` and `details`. Streaming and empty responses
have their documented shapes; do not assume every successful request is a JSON
envelope. Unknown/retired request fields are errors, not compatibility aliases.

| Status | Typical meaning |
| --- | --- |
| 401 | Missing or incorrect key |
| 400 | Invalid fields, values or request shape |
| 404 | Requested resource does not exist |
| 409 | State conflict or download conflict |
| 503 | Service unavailable/busy for the requested operation |

Use documented machine-readable error codes and details, rather than parsing
English messages. Respect the exact operation schema and re-read state after a
conflict; do not blindly replay mutating requests.

`GET /healthz` is a separate, unauthenticated readiness probe outside `/api/v1`:
empty 204 while running, 503 while shutting down. It is not API discovery and
does not expose private application state.

## Explore Without Guessing DTOs

Start with authenticated GETs to `/api/v1/app`, `/status`, `/network` and
`/transfers` under the same API prefix. After network connection, a search can use:

```bash
curl --fail-with-body \
  -H "X-API-Key: $API_KEY" -H 'Content-Type: application/json' \
  --data '{"query":"Sample File","method":"automatic"}' \
  http://127.0.0.1:4711/api/v1/searches
```

`automatic` resolves from current network state; offline searches are rejected
as not connected. Read the returned search ID and documented result model.
Download an actual result through
`POST /searches/{searchId}/results/{hash}/operations/download`, or use the
documented `TransferCreateRequest` eD2K-link form. Do not manufacture a transfer
request from a displayed result object.

Shared-folder management uses `/shared-directories` and its documented root and
ignore operations. Roots are recursively scanned and monitored. Settings use
`/app/settings`; bootstrap TOML has a different, minimal responsibility.

For SSE, use a header-capable HTTP/fetch streaming client with `X-API-Key`.
Browser `EventSource` does not provide a custom-header parameter; never solve
that by moving the secret into the URL. Follow `Last-Event-ID` and `sync.reset`
semantics: re-baseline through `GET /transfers` after a reset.

## Report Problems Safely

Include the exact application version/source, contract version, operation and
sanitized request/response when filing an ordinary issue. Diagnostic bundles
contain private credentials and operator state; do not upload them unreviewed.
Use [private vulnerability reporting](https://github.com/emulebb/emulebb-rust/security/advisories/new)
for suspected security defects.

Future Indexer, Torznab and qBittorrent-compatible adapter plans are separate
gated work. They do not add undocumented routes to this current native client
API. For source changes, follow the [contributor guide](../reference/GUIDE-CONTRIBUTING.md).
