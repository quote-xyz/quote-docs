---
description: Base URLs, conventions, and the error envelope. Read this before the endpoint pages.
---

# Trader API Reference

This reference covers the trading surface: orders, agents, positions, templates, triggers, alerts, analytics, funding, portfolio, and the [algo status WebSocket](../websockets/algo-status.md). The [MCP server](../mcp/overview.md) is documented in its own section.

## Base URL

```
https://api.quotemarkets.xyz
```

The active network (Hyperliquid mainnet vs. testnet) is reported by the public `GET /api/info` endpoint.

## Authentication

Every request carries an HMAC API key in three headers: `X-Quote-Key`, `X-Quote-Timestamp` (milliseconds), and `X-Quote-Signature`. A key holds only the scopes granted at mint time, and each endpoint page notes the scope it requires. Mint, list, and revoke keys in the [terminal](https://quotemarkets.xyz) on the **Connections** page, under **API keys**.

A few endpoints are **public** and need no key: `/api/info` and the health probes.

Full details, the canonical signing string, and code samples: [Authentication](../authentication.md).

## Prerequisites for trading

Order, position, and strategy endpoints require two one-time setup steps on the wallet, both performed in the [terminal](https://quotemarkets.xyz):

1. A **registered [agent wallet](../concepts/agent-wallets.md)**. Quote signs venue actions with it.
2. **Builder-fee approval**. Every Quote-routed order carries Quote's builder code, and Quote requires the approval before it will trade for your wallet. Without it, order submission fails.

Verify both with `GET /api/agents`: you need an `agentAddress` with `expired: false` and `builderFeeApproved: true`.

## Conventions

- **Decimals are strings.** Sizes and prices are decimal strings (`"0.05"`, `"3150.5"`), never floats. Precision matters when a venue rejects a fifth significant figure.
- **Request/response keys are camelCase**, with a handful of documented snake_case exceptions (noted per schema).
- **Timestamps** are epoch milliseconds in analytics payloads and RFC 3339 strings on resource records; each field documents its shape.
- **IDs**: templates and triggers use UUIDs; algo parents use engine-issued IDs; plain orders use the venue's numeric order ID.

## Analytics conventions

The analytics, funding and portfolio endpoints take a common `range` query parameter: `1d`, `7d`, `30d`, or `all`. API-key callers need `orders:read`.

- **Benchmarks are signed basis points: positive = worse**, negative = better. `isBps` on `GET /api/analytics/execution` is notional-weighted implementation shortfall against arrival (negative = you beat arrival); `isSavingsDollars` is dollars saved against naive market orders (positive = saved).
- **Fees.** `totalFee` on `GET /api/analytics/fees` is the whole cost of Quote-routed fills, inclusive of the builder fee; `builderFee` is the part of it that went to Quote, never an addition to it.
- **Funding.** On `GET /api/funding`, `net = totalReceived − totalPaid`, and both totals are positive magnitudes. `GET /api/funding/timeline` buckets hourly for `1d` and daily otherwise; `GET /api/funding/history` is the raw per-payment log, newest first.
- **Equity gaps are null, never zero.** On `GET /api/portfolio/equity`, `accountValue` may be `null`: a gap in sampling. Skip the point rather than drawing it to the axis.
- **PnL excludes transfers.** PnL over a window is `Δ accountValue − Σ netFlow`, where `netFlow` is each hour's external net flow (+ in, − out), so deposits and withdrawals do not read as performance.

{% code title="GET /api/portfolio/equity?range=30d (one sample)" %}
```json
{
  "timestamp": 1752402000000,
  "accountValue": 25431.2,
  "perpEquity": 21200.5,
  "spotEquity": 4230.7,
  "unrealizedPnl": 312.4,
  "netFlow": 0.0
}
```
{% endcode %}

## The async-accept model

`POST /api/orders` returns `200` when the order or strategy is **accepted into the execution engine**, not when it fills. Parent cancel success means the cancel was durably accepted; the terminal state is recorded only after venue reconciliation. Internalize this before integrating: see [Order Lifecycle](../concepts/order-lifecycle.md).

## Error envelope

All `4xx`/`5xx` responses (except `413` and bodyless `204`) share one shape:

{% code title="Response" %}
```json
{ "success": false, "error": "human-readable message" }
```
{% endcode %}

| Status | Meaning |
|---|---|
| `400` | Validation error: malformed body, bad UUID, out-of-range parameter |
| `401` | Missing or invalid credentials (bad signature, stale timestamp) |
| `403` | Authenticated but not permitted: the API key lacks the required scope |
| `404` | Resource not found **or not owned by your wallet** |
| `429` | Rate limit exceeded |
| `502` | Upstream venue (Hyperliquid/Relay) returned an error |
| `503` | A required dependency is unavailable, or a circuit breaker to Hyperliquid is open |

{% hint style="info" %}
`503` responses are usually transient. Quote wraps its Hyperliquid clients in circuit breakers that recover automatically within ~30 seconds. Retry with backoff.
{% endhint %}

## Request size limit

Request bodies are capped at **4 MiB**; larger payloads receive `413` (without the JSON envelope).
