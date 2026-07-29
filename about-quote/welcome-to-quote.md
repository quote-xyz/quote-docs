---
description: Explore permissionless optimal trading execution.
cover: ../.gitbook/assets/gitbook cover.png
coverY: 0
---

# Welcome to Quote

Quote is a perpetuals execution layer for [Hyperliquid](https://hyperliquid.xyz). Orders submitted through Quote are routed to the Quote Execution Engine before they reach the venue, where a parent order is optimized down to the child order level and standing orders stay private until they are placed.

<figure><img src="../.gitbook/assets/Screenshot 2026-02-20 at 6.04.44 pm.png" alt=""><figcaption><p>Figure 1. Quote order flow through the Quote Execution Engine.</p></figcaption></figure>

The engine minimizes implementation shortfall, the cost of completing a trade, by:

* Prioritizing passive execution, to earn the spread and maker fees rather than pay them
* Pacing execution against real-time volume, a target participation rate, or a fixed schedule
* Sizing orders to the depth actually available in the book
* Taking liquidity only when conditions favor it

<table data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Place your first trade</strong></td><td>From funding your account to choosing an order type in the terminal.</td><td><a href="../guides/first-trade.md">first-trade.md</a></td></tr><tr><td><strong>Deposits and withdrawals</strong></td><td>Fund your account, move between spot and perps, and take money off the venue.</td><td><a href="../account/deposits-and-withdrawals.md">deposits-and-withdrawals.md</a></td></tr><tr><td><strong>Execution strategies</strong></td><td>Five execution algorithms, from passive TWAP to size-hiding Iceberg.</td><td><a href="../strategies/overview.md">overview.md</a></td></tr><tr><td><strong>Build on the API</strong></td><td>Mint a key, sign a request, and submit orders programmatically.</td><td><a href="../quickstart.md">quickstart.md</a></td></tr></tbody></table>

## The problem

Most traders overpay to trade. A market order crosses the spread, pays taker fees, and moves the price against itself. A large one also tells the whole book what you are doing, and the book adjusts before you finish. On most venues the tools that solve this, execution algorithms and transaction-cost analysis, are sold to institutions and denied to everyone else.

<figure><img src="../.gitbook/assets/Screenshot 2026-02-20 at 6.09.48 pm.png" alt=""><figcaption><p>Figure 2. Hidden costs of trading perpetual derivatives.</p></figcaption></figure>

Four costs do most of the damage: crossing the spread, slippage and adverse selection, exchange fees, and having no access to professional execution.

## How it works

Quote was built from first principles, pairing established algorithmic execution logic with a data engine built for HyperCore's data streams. The result is a permissionless trading desk: institutional execution available to anyone, drawing on Hyperliquid's liquidity.

<figure><img src="../.gitbook/assets/Screenshot 2026-02-20 at 6.14.36 pm.png" alt=""><figcaption><p>Figure 3. Quote Execution Engine flow.</p></figcaption></figure>

1. **You keep custody.** Trading happens through an [agent wallet](../concepts/agent-wallets.md), a separate key that can sign orders for your account but can never withdraw funds. You approve it once on Hyperliquid, and Quote stores its key encrypted at rest.
2. **You submit intent, Quote executes.** A plain order goes straight to the venue. An algo order becomes a parent strategy that the engine works over time, slicing it into child orders based on market microstructure. See [Order Lifecycle](../concepts/order-lifecycle.md).
3. **Everything is measured.** Every fill is benchmarked against arrival price, market VWAP, and a simulated naive market order, so you can see in basis points what the engine saved or cost you. See [Analytics](../guides/analytics.md).

Orders are routed to Hyperliquid through builder codes, which is what keeps the arrangement non-custodial. Everything you can do in the [terminal](https://quotemarkets.xyz) you can also do over the API, because the same wallet-scoped backend powers both.

## Core capabilities

| Capability | Description |
|---|---|
| [Execution strategies](../strategies/overview.md) | `passive_twap`, `vwap`, `iceberg`, `participation_rate`, `chase_limit` |
| [Plain orders](../guides/placing-orders.md) | Limit, market (IOC with slippage bound), TP/SL attachment, modify, cancel, cancel-all |
| [Conditional triggers](../guides/triggers.md) | Fire an order on price, funding, open-interest, copy-trade, or time conditions |
| [Order templates](../guides/templates.md) | Save and reuse execution presets with urgency and price-discipline dials |
| [Execution analytics](../guides/analytics.md) | Implementation shortfall, slippage, fees, funding, and portfolio equity time-series |
| [MCP server](../mcp/overview.md) | Read-only analytics for AI agents over the Model Context Protocol |
| [Real-time telemetry](../websockets/algo-status.md) | WebSocket stream of live strategy progress |
| [Funds](../account/deposits-and-withdrawals.md) | Cross-chain deposits and withdrawals, spot-perp transfers, direct sends |
| [Fees and rewards](../account/fees.md) | The full fee stack, the volume-based tier ladder, referrals, and cashback |

## Markets

Quote trades everything listed on Hyperliquid: crypto perpetuals (`BTC`, `ETH`, `HYPE`, …), builder-DEX equities and commodities (`xyz:HOOD`, `xyz:CL`, …), and HIP-4 prediction markets.

## Where to go next

<table data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>The wallet-scoped model</strong></td><td>Why every resource is keyed by your wallet address, and what that means for the API.</td><td><a href="../concepts/wallet-scoped-api.md">wallet-scoped-api.md</a></td></tr><tr><td><strong>Authentication</strong></td><td>Privy sessions for the terminal, HMAC API keys for programmatic access.</td><td><a href="../authentication.md">authentication.md</a></td></tr><tr><td><strong>Fees and rewards</strong></td><td>What a fill costs, and the tier ladder that rebates part of it.</td><td><a href="../account/fees.md">fees.md</a></td></tr><tr><td><strong>Hyperliquid constraints</strong></td><td>Minimum notional, price precision, and other venue rules Quote handles for you.</td><td><a href="../concepts/hyperliquid-constraints.md">hyperliquid-constraints.md</a></td></tr></tbody></table>
