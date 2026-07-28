---
description: Quote is a trading terminal for Hyperliquid with execution algorithms, a wallet-scoped REST API, and real-time strategy telemetry.
---

# Introduction

<figure><img src="images/docs-banner.jpg" alt="Quote: the execution layer on Hyperliquid"><figcaption></figcaption></figure>

## Why Quote exists

Most traders overpay to trade. A market order crosses the spread, pays taker fees, and moves the price against itself; a large one also tells the whole book what you are doing, and the book adjusts before you finish. On most venues, the tools that solve this (execution algorithms, transaction-cost analysis) are sold to institutions and denied to everyone else.

Quote is an execution layer for [Hyperliquid](https://hyperliquid.xyz) that closes that gap. Instead of sending your order straight to the book, the Quote execution engine works it: splitting the parent order into child orders, resting them passively to capture the spread and maker fees rather than pay them, pacing them with real-time market data, and taking liquidity only when the schedule demands it. Every execution is then measured against arrival price, market VWAP, and a simulated market order, so you can see, in basis points, what working the order saved you.

It is non-custodial: you keep your funds, and everything settles directly on Hyperliquid. And everything you can do in the [terminal](https://quotemarkets.xyz) you can also do over the API; the same wallet-scoped backend powers both.

<table data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Quickstart</strong></td><td>Mint an API key and submit your first order in five minutes.</td><td><a href="quickstart.md">quickstart.md</a></td></tr><tr><td><strong>Execution strategies</strong></td><td>Five execution algorithms, from passive TWAP to size-hiding Iceberg.</td><td><a href="strategies/overview.md">overview.md</a></td></tr><tr><td><strong>Authentication</strong></td><td>Privy sessions for the terminal, HMAC API keys for programmatic access.</td><td><a href="authentication.md">authentication.md</a></td></tr><tr><td><strong>Trader API reference</strong></td><td>Every endpoint, request schema, and response shape.</td><td><a href="api-reference/introduction.md">introduction.md</a></td></tr></tbody></table>

## How it works

Quote sits between you and Hyperliquid as an execution layer:

1. **You keep custody.** Trading happens through an [agent wallet](concepts/agent-wallets.md): a separate key that can sign orders for your account but can never withdraw funds. You approve it once on Hyperliquid; Quote stores its key encrypted at rest.
2. **You submit intent, Quote executes.** A plain order goes straight to the venue. An algo order becomes a parent strategy that the execution engine works over time, slicing it into child orders based on market microstructure. See [Order Lifecycle](concepts/order-lifecycle.md).
3. **Everything is measured.** Every fill is benchmarked against arrival price, market VWAP, and a simulated naive market order, so you can see exactly what the execution engine saved (or cost) you. See [Analytics](guides/analytics.md).

## Core capabilities

| Capability | Description |
|---|---|
| [Execution strategies](strategies/overview.md) | `passive_twap`, `vwap`, `iceberg`, `participation_rate`, `chase_limit` |
| [Plain orders](guides/placing-orders.md) | Limit, market (IOC with slippage bound), TP/SL attachment, modify, cancel, cancel-all |
| [Conditional triggers](guides/triggers.md) | Fire an order on price, funding, open-interest, copy-trade, or time conditions |
| [Order templates](guides/templates.md) | Save and reuse execution presets with urgency and price-discipline dials |
| [Execution analytics](guides/analytics.md) | Implementation shortfall, slippage, fees, funding, and portfolio equity time-series |
| [MCP server](mcp/overview.md) | Read-only analytics for AI agents over the Model Context Protocol |
| [Real-time telemetry](websockets/algo-status.md) | WebSocket stream of live strategy progress |

## Markets

Quote trades everything listed on Hyperliquid: crypto perpetuals (`BTC`, `ETH`, `HYPE`, …), builder-DEX equities and commodities (`xyz:HOOD`, `xyz:CL`, …), and HIP-4 prediction markets.

## Where to go next

<table data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>The wallet-scoped model</strong></td><td>Why every resource is keyed by your wallet address, and what that means for the API.</td><td><a href="concepts/wallet-scoped-api.md">wallet-scoped-api.md</a></td></tr><tr><td><strong>Hyperliquid constraints</strong></td><td>Minimum notional, price precision, and other venue rules Quote handles for you.</td><td><a href="concepts/hyperliquid-constraints.md">hyperliquid-constraints.md</a></td></tr></tbody></table>
