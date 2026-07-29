---
description: 'Quote''s Model Context Protocol server: read-only market and account analytics
  for AI agents.'
---

# MCP Overview

Quote exposes its analytics as an [MCP](https://modelcontextprotocol.io) server, so AI agents (Claude, coding assistants, or anything that speaks MCP) can query markets and your account in natural language.

```
https://api.quotemarkets.xyz/mcp
```

{% hint style="info" %}
The MCP server is **strictly read-only**. Its tools fetch data (prices, books, analytics, reports) and can never place, modify, or cancel orders. Trading stays behind the [REST API](../api-reference/introduction.md) and its explicit credentials.
{% endhint %}

## What agents can do with it

- **Market research**: live prices, candles, order-book microstructure, funding history, market screeners, earnings, and prediction markets.
- **Pre-trade analysis**: estimate the cost of a trade or stress-test a position against the live book before you commit.
- **Account review**: your execution-quality report, portfolio report, funding carry, triggers, and fee tier.

See the [tools reference](tools.md) for the full catalog.

## Scopes

Access is governed by two scopes, granted during the OAuth consent flow:

| Scope | Grants |
|---|---|
| `analytics:read` | Market-wide data; nothing about your account |
| `account:read` | Your wallet's analytics: execution, portfolio, funding, triggers, fees |

Two properties worth knowing:

- A token only ever sees the account it was issued for, the same [wallet-scoped model](../concepts/wallet-scoped-api.md) as the REST API.
- Tool listings are filtered to the token's scopes: an `analytics:read`-only token doesn't see account tools at all.

## Symbol formats

Symbols are venue-prefixed, and common names are resolved for you (`"oil"` → `xyz:CL`):

- Perps: `BTC`, `ETH`, `HYPE`
- Builder-DEX equities/commodities: `xyz:HOOD`, `xyz:CL`
- Prediction markets: `#2290` (HIP-4 outcome coins)

## Conventions

Execution analytics follow the platform-wide [benchmark convention](../guides/analytics.md#the-benchmark-convention): signed bps, **positive = worse**. Prices are live snapshots at call time and may differ slightly from the terminal's WebSocket-fed views.

<table data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Connect a client</strong></td><td>Claude, Claude Code, Cursor, and any Streamable-HTTP MCP client.</td><td><a href="connect.md">connect.md</a></td></tr><tr><td><strong>Tools reference</strong></td><td>Every tool, its scope, and what it returns.</td><td><a href="tools.md">tools.md</a></td></tr></tbody></table>
