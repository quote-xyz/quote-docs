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
{ "success": true, "orderId": "01HZX8…", "status": "accepted", "provider": "hyperliquid" }
```
{% endcode %}

`orderId` is the **parent strategy ID**. Keep it: every status and cancel call uses it.

- `params` accepts both camelCase and snake_case keys, and numeric fields accept strings, integers, or floats.
- Each strategy validates its own params on submission; invalid combinations are rejected with `400` and a message, before anything reaches the venue.

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
      "status": "working",
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

Use the top-level `tpsl` field, exactly as you would on a [plain order](placing-orders.md). There is no per-strategy TP/SL parameter.

```json
{
  "symbol": "ETH",
  "side": "buy",
  "size": "2.5",
  "orderType": "limit",
  "limitPrice": "3150.5",
  "strategy": "passive_twap",
  "params": { "durationSecs": 900 },
  "tpsl": {
    "mode": "market",
    "tp": { "triggerPrice": "3500" },
    "sl": { "triggerPrice": "3000" }
  }
}
```

A strategy works one order as many child orders, so the legs cannot ride along with them: one bracket per clip would be sized to that clip and orphaned as soon as its siblings filled. Instead the legs are placed once, against the position the strategy built, when the run reaches a terminal state. They are sized to that position, including a partial fill left behind by a cancelled or expired run.

{% hint style="warning" %}
The legs do not exist while the strategy is still working, so nothing fires if price crosses your trigger mid-run. To bound execution itself, set a `limitPrice`, or use `maxSlippageBps` on the strategies that accept it.
{% endhint %}

`tpsl` cannot be combined with `reduceOnly` on a strategy. A closing order builds no position to protect, so the request is refused rather than accepted and quietly dropped.

To protect a position you already hold, or to add TP/SL after a run has finished, use [`POST /api/positions/tpsl`](../api-reference/endpoints/positions.md).

## Practical sizing checklist

- **Slices vs. the $10 minimum.** Each child slice must clear ~$10 notional or it is skipped. `size × price / numSlices ≳ $15` is a safe rule of thumb.
- **Duration vs. price risk.** Longer windows capture more spread but carry more price risk. Start with 15–30 minutes on liquid assets and measure the result.
- **Measure it.** After a few executions, check [`/api/analytics/execution`](analytics.md) to see your realized cost vs. benchmarks.
