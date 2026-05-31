# eMuleBB REST API Quickstart

This quickstart is for trusted local controllers and scripts. The formal
contract remains [REST-API-CONTRACT](REST-API-CONTRACT.md) and the machine
source of truth is [REST-API-OPENAPI.yaml](REST-API-OPENAPI.yaml).

## Enable The Listener

1. Finish normal desktop setup first.
2. Open `Preferences > Web Server`.
3. Enable the WebServer/REST listener.
4. Bind to `127.0.0.1` for same-machine automation, or a deliberate LAN/VPN
   address for controlled-network automation.
5. Set a strong API key.
6. Keep firewall exposure limited to the intended controller machines.

The examples below use HTTP on port `4711`. Use HTTPS only when the listener is
configured for it and the controller trusts the certificate.

## First Status Call

```powershell
$base = 'http://127.0.0.1:4711'
$key = '<emulebb-api-key>'
$headers = @{ 'X-API-Key' = $key }

Invoke-RestMethod -Uri "$base/api/v1/app" -Headers $headers
```

Expected result: a JSON success envelope with app identity, API version, and
capabilities.

## Read Current State

```powershell
Invoke-RestMethod -Uri "$base/api/v1/status" -Headers $headers
Invoke-RestMethod -Uri "$base/api/v1/transfers" -Headers $headers
Invoke-RestMethod -Uri "$base/api/v1/shared-files" -Headers $headers
```

Read routes should work before any controller performs mutations. If these
fail, fix bind, port, firewall, API key, or app lifecycle first.

## Start A Search

```powershell
$body = @{
  query = 'ubuntu iso'
  method = 'global'
  type = ''
} | ConvertTo-Json

Invoke-RestMethod `
  -Method Post `
  -Uri "$base/api/v1/searches" `
  -Headers $headers `
  -ContentType 'application/json' `
  -Body $body
```

Store the returned `searchId`, then poll:

```powershell
Invoke-RestMethod -Uri "$base/api/v1/searches/<searchId>" -Headers $headers
```

## Add A Transfer Deliberately

Use a known safe `ed2k://` or magnet link:

```powershell
$body = @{
  link = '<ed2k-or-magnet-link>'
  categoryName = 'manual-test'
  paused = $true
} | ConvertTo-Json

Invoke-RestMethod `
  -Method Post `
  -Uri "$base/api/v1/transfers" `
  -Headers $headers `
  -ContentType 'application/json' `
  -Body $body
```

Start with `paused = $true` when testing a new controller path so the native UI
can confirm category, filename, and destination behavior before network
activity begins.

## Common Failures

| Status | Meaning | First Check |
|---|---|---|
| `401` | Missing or wrong API key | Confirm `X-API-Key` and WebServer preferences |
| `404` | Route or id not found | Compare the full `/api/v1/...` path with OpenAPI |
| `405` | Wrong HTTP method | Check whether the route is `GET`, `POST`, `PATCH`, or `DELETE` |
| `409` | Lifecycle or state conflict | Check whether the app is starting, stopping, or the object changed |
| `503` | API temporarily unavailable | Check startup/shutdown state, listener readiness, and busy search bridge |

For deeper triage, capture method, full route, status code, request body,
response body, controller logs, and app logs. Use
[Controllers and REST](../reference/GUIDE-CONTROLLERS-REST.md) for operating
rules and [Troubleshooting](../reference/GUIDE-TROUBLESHOOTING.md) for evidence.
