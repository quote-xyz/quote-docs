---
description: 'Submit a strategy, track its progress, and cancel it: the full lifecycle of
  an execution-engine order.'
---

# Algo Orders

An algo order is a plain `POST /api/orders` with `strategy` set. The engine accepts it as a **parent intent** and works it as child orders on the venue. See [Order Lifecycle](../concepts/order-lifecycle.md) for the model and [Strategies](../strategies/overview.md) for choosing an algorithm.

## Submitting

{% code title="POST /api/orders" %}
```json
{
  "symbol": "ETH",
  "side": "buy",
  "size": "2.0",
  "orderType": "limit",
  "strategy": "passive_twap",
  "params": {
    "durationSecs": 1800,
    "numSlices": 30,
    "guaranteedCompletion": true
  }
}
```
{% endcode %}

{% code title="Response" %}
```json
{ "success": true, "orderId": "01HZX8…", "status": "active", "provider": "quote", "clientOrderId": "…" }
```
{% endcode %}

`orderId` is the **parent strategy ID**. Keep it: every status and cancel call uses it.

- `params` accepts both camelCase and snake_case keys, and numeric fields accept strings, integers, or floats.
- Each strategy validates its own params on submission; invalid combinations are rejected with `400` and a message, before anything reaches the venue.

## Strategy parameters

All parameters are optional, and each strategy uses only its own. Keys accept camelCase or snake_case. Defaults below are what the engine applies when you omit a key.

These work on every strategy:

| Parameter | Type | Description |
| --- | --- | --- |
| `reduceOnly` | boolean | Children only reduce an existing position |
| `hardCancelPct` | decimal string | Abort the whole order if the mid moves this percentage against you from arrival, in (0, 100]. Nothing is left resting |
| `attachedTpsl` | object | Take-profit and stop-loss placed against the position the strategy builds (see the section below) |

### `passive_twap` <a href="#passive_twap" id="passive_twap"></a>

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `durationSecs` | integer | `300` | Total execution window in seconds |
| `urgency` | integer 0–100 | none | The terminal's **Execution** slider. Sets `numSlices` and `passivePct` for you; either one sent explicitly wins |
| `numSlices` | integer | `10` | Number of child slices |
| `passivePct` | integer 0–100 | `80` | Share of each slice interval spent resting passively before crossing |
| `distributionSkew` | integer 0–100 | `50` | How size is weighted across the window: `0` front-loads, `50` is even, `100` back-loads |
| `limitOffsetBps` | decimal | `0` | Offset from the touch for passive placement (0 = at the best bid or offer) |
| `randomizePct` | integer 0–50 | `0` | Jitter on slice size and timing, in percent. `randomize: true` is shorthand for 20 |
| `guaranteedCompletion` | boolean | `false` | Sweep any remainder with one IOC at the end of the window |
| `completionSlippageBps` | decimal | `100` | How far past the best price the completion sweep may reach |

### `vwap` <a href="#vwap" id="vwap"></a>

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `durationSecs` | integer | `300` | Total execution window in seconds |
| `numSlices` | integer | `10` | Number of child slices, sized by the volume profile |
| `passivePct` | integer 0–100 | `80` | Share of each slice interval spent passive before crossing |
| `limitOffsetBps` | decimal | `0` | Offset from the touch for passive placement |
| `dynamic` | boolean | `true` | Refresh the volume forecast during execution rather than fixing it at the start |

### `participation_rate` <a href="#participation_rate" id="participation_rate"></a>

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `participationRate` | decimal string | `"0.10"` | Target fraction of observed market volume (`"0.15"` = 15%) |
| `maxDurationSecs` | integer | `3600` | Time limit. When it expires, the remainder is swept with IOC orders, still bounded by `limitPrice` and `maxSlippageBps` |
| `maxSlippageBps` | decimal string | none | Price band around the arrival mid. No taker order, including the deadline sweep, fills past it, so the order may finish unfilled. Must be greater than 0 |
| `clipSizePct` | decimal | `5` | Largest single clip, as a percentage of total order size |
| `passivePct` | integer 0–100 | `80` | Share of each clip's life spent passive before crossing |
| `limitOffsetBps` | decimal | `0` | Offset from the touch for passive placement |
| `randomizePct` | integer 0–50 | `0` | Jitter on clip size and timing, in percent |

### `iceberg` <a href="#iceberg" id="iceberg"></a>

Clips are post-only and rest at your `limitPrice`.

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `clipSize` | decimal string | 10% of the order, at least 1 | Visible clip size in the base asset |
| `clipPct` | number | none | Alternative to `clipSize`: the clip as a percentage of total order size |
| `participationRate` | decimal string | `0` (off) | Scale clips to this fraction of recent market volume, falling back to `clipSize` |
| `priceOffsetBps` | decimal | `0` | Rest this far behind the touch (0 = at the best bid or offer) |
| `maxSpreadBps` | decimal | `0` (off) | Pause posting while the spread is wider than this |
| `maxDurationSecs` | integer | `0` (none) | Optional time limit. When it expires, the remainder is swept with an IOC order |
| `randomizePct` | integer 0–50 | `0` | Jitter on clip size and timing, in percent |

### `chase_limit` <a href="#chase_limit" id="chase_limit"></a>

A chase is good-til-filled: it follows the book until it fills, you cancel it, or `maxTotalSecs` runs out.

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `maxTotalSecs` | integer | `86400` | Lifetime of the order in seconds (24 hours) |
| `mustComplete` | boolean | `false` | At the end of `maxTotalSecs`, take the remainder with an IOC order instead of letting it expire unfilled |
| `initialOffsetBps` | decimal | `5` | Starting offset behind the touch |
| `minOffsetBps` | decimal | `0` | Closest the order may come to the touch (0 = allowed to reach it) |
| `maxAttempts` | integer | `8` | How many times the offset tightens towards `minOffsetBps` before the order holds a steady peg |
| `cross` | boolean | `false` | Work the taker side: price at the opposing touch and re-peg there, so every fill pays the spread. `limitPrice` still bounds it |

`limitPrice` bounds how far a chase follows the book: once the market passes it, the order rests there.

## Tracking progress

List all your algo orders:

```bash
GET /api/orders/algo
```

{% code title="Response" %}
```json
{
  "success": true,
  "orders": [
    {
      "orderId": "01HZX8…",
      "symbol": "ETH",
      "side": "Buy",
      "orderQty": "2.0",
      "filledQty": "1.35",
      "status": "active",
      "strategy": "passive_twap",
      "submitTime": "2026-07-13T14:02:11Z"
    }
  ]
}
```
{% endcode %}

Or fetch one by parent ID:

```bash
GET /api/orders/algo/{order_id}
```

For push-based progress (the terminal's live "Placing child order…" telemetry), use the [algo status WebSocket](../websockets/algo-status.md) instead of polling.

## Cancelling

{% code title="POST /api/orders/cancel" %}
```json
{ "symbol": "ETH", "orderId": "01HZX8…" }
```
{% endcode %}

A `200` means the cancel was **durably requested**: the engine stops scheduling new children immediately, cancels open child orders on Hyperliquid, and records terminal `cancelled` only after the venue confirms nothing remains open. Fills that landed before the cancel are yours; check `filledQty` on the final state.

{% hint style="warning" %}
If double-execution matters, do not submit a replacement order the moment the cancel returns `200`. Confirm the parent is terminal first (one poll of `GET /api/orders/algo/{order_id}` or the `parent_completed`/`parent_failed` WebSocket event).
{% endhint %}

## Attaching TP/SL to strategy fills

Strategies accept `attachedTpsl` in `params`: a take-profit/stop-loss placed against the position the strategy builds.

```json
{
  "strategy": "passive_twap",
  "params": {
    "durationSecs": 900,
    "attachedTpsl": {
      "mode": "market",
      "tp": { "triggerPrice": "3500" },
      "sl": { "triggerPrice": "3000" }
    }
  }
}
```

## Building an order from a template

An [order template](templates.md) stores how an order is worked, under the terminal's order-ticket names, not the `strategy` values above:

{% code title="POST /api/templates" %}
```json
{
  "name": "Patient accumulator",
  "ticket": {
    "strategy": "twap",
    "amountUsd": "5000",
    "durationSecs": 3600,
    "priceProtection": true
  }
}
```
{% endcode %}

Map the names when you build the order: `twap` is `passive_twap`, `pov` is `participation_rate` and `chase` is `chase_limit`, while `vwap` and `iceberg` match. Then add the market, side and price, and submit with `POST /api/orders`. There is no `templateId` on the order API, so a template never constrains what you submit. A wallet holds at most 12 templates, and saving a thirteenth name returns `409`. See the [Templates endpoints](../api-reference/endpoints/templates.md).

## Practical sizing checklist

- **Slices vs. the $10 minimum.** Each child slice must clear ~$10 notional or it is skipped. `size × price / numSlices ≳ $15` is a safe rule of thumb.
- **Duration vs. price risk.** Longer windows capture more spread but carry more price risk. Start with 15–30 minutes on liquid assets and measure the result.
- **Measure it.** After a few executions, check `GET /api/analytics/execution` (see the [Analytics endpoints](../api-reference/endpoints/analytics.md)) to see your realized cost against the benchmarks.
