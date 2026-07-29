---
description: 'Limit and market orders, TP/SL attachment, modify, and cancel: the plain-order
  surface.'
---

# Placing Orders

This guide covers plain (non-algo) orders. For execution strategies, see [Algo Orders](algo-orders.md).

## Limit orders

{% code title="POST /api/orders" %}
```json
{
  "symbol": "ETH",
  "side": "buy",
  "size": "0.5",
  "orderType": "limit",
  "limitPrice": "3150.5",
  "timeInForce": "GTC"
}
```
{% endcode %}

- `size` and `limitPrice` are decimal **strings**, never floats. Quote normalizes them to the asset's [precision rules](../concepts/hyperliquid-constraints.md#price-and-size-precision).
- `timeInForce`: `GTC` (default), `ALO` (post-only), or `IOC`.
- `clientOrderId` (optional) lets you tag the order with your own identifier.
- `reduceOnly: true` restricts the order to reducing an existing position.

The response returns the venue `orderId`:

{% code title="Response" %}
```json
{ "success": true, "orderId": "1234567890", "status": "resting", "provider": "hyperliquid" }
```
{% endcode %}

## Market orders

Hyperliquid market orders are IOC limits with a slippage bound, so **`limitPrice` is required**. It is the worst price you will accept:

{% code title="POST /api/orders" %}
```json
{
  "symbol": "ETH",
  "side": "buy",
  "size": "0.5",
  "orderType": "market",
  "limitPrice": "3320.0"
}
```
{% endcode %}

Compute the bound from the best opposing quote. Buy: `bestAsk × (1 + slippage)`. Sell: `bestBid × (1 − slippage)`.

{% hint style="warning" %}
Anchor to the best **opposing quote**, not mid. On wide-spread books (prediction markets especially), a mid-anchored bound can sit inside the spread, so the IOC crosses nothing and silently fills zero. See [Hyperliquid constraints](../concepts/hyperliquid-constraints.md#market-orders-are-ioc-limits-with-a-slippage-bound).
{% endhint %}

## Scale orders

A scale order spreads a set of limit orders evenly across a price range instead of resting the whole size at one price. It is a way to build a position into a move without picking a single level.

In the terminal you set four things:

| Field | What it does |
|---|---|
| **Start price** | One end of the range |
| **End price** | The other end |
| **Total orders** | How many limit orders to spread across it |
| **Size skew** | How size is weighted across the range, rather than split evenly |

Skew is what makes it more than a loop. Weight size toward the far end and you buy more the further price falls, which lowers your average entry if it keeps going and leaves you smaller if it does not.

Two things to watch. Each individual order still has to clear the roughly $10 [minimum notional](../concepts/hyperliquid-constraints.md), so a small order split many ways will have levels skipped. And a scale order is a set of resting limits, not a worked strategy: nothing repositions them if the market leaves the range. If you want the engine to adapt, use an [execution strategy](../strategies/overview.md) instead.

## Attaching TP/SL

Attach take-profit / stop-loss to any order with `tpsl`:

```json
{
  "symbol": "ETH",
  "side": "buy",
  "size": "0.5",
  "orderType": "limit",
  "limitPrice": "3150.5",
  "tpsl": {
    "mode": "market",
    "tp": { "triggerPrice": "3500" },
    "sl": { "triggerPrice": "3000" }
  }
}
```

- `mode: "market"` exits at market when triggered; `mode: "limit"` places a limit at `limitPrice` per side.
- Either `tp` or `sl` may be omitted.

## Modifying an order

{% code title="POST /api/orders/modify" %}
```json
{
  "symbol": "ETH",
  "orderId": 1234567890,
  "side": "buy",
  "limitPrice": "3160.0",
  "size": "0.5"
}
```
{% endcode %}

This uses Hyperliquid's native modify: the order keeps working, and price and/or size change atomically. `orderId` here is the numeric exchange order ID.

## Cancelling

Single order:

{% code title="POST /api/orders/cancel" %}
```json
{ "symbol": "ETH", "orderId": "1234567890" }
```
{% endcode %}

All open orders (optionally per symbol):

{% code title="POST /api/orders/cancel-all" %}
```json
{ "symbol": "ETH" }
```
{% endcode %}

Omit `symbol` to cancel everything. The response reports how many orders were cancelled.

{% hint style="info" %}
Plain-order cancels are synchronous. Cancelling an **algo parent** via the same endpoint is a request with reconciliation semantics; see [Order Lifecycle](../concepts/order-lifecycle.md#cancellation-semantics).
{% endhint %}

## Common rejections

| Error | Cause | Fix |
|---|---|---|
| Sub-minimum notional | `size × price` under ~$10 | Increase size |
| ALO would cross | Post-only price at or through the opposing touch | Reprice inside the spread |
| Market order without `limitPrice` | Missing slippage bound | Compute from best opposing quote |
| `403` | Missing `orders:write` scope | Re-mint key with the right scopes |
