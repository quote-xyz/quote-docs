---
description: >-
  Venue rules that shape every order: minimum notional, price and size
  precision, ALO crossing, builder fees, and market-order slippage prices.
---

# Hyperliquid Constraints

<figure><img src="../.gitbook/assets/screenshot_1.5x_postspark_2026-07-30_11-28-14.png" alt=""><figcaption></figcaption></figure>

Hyperliquid enforces several non-obvious rules. Quote handles most of them for you, but they explain behavior you will see: capped slice counts, adjusted prices, rejected orders.

## Minimum order notional: \~$10 <a href="#minimum-order-notional-10" id="minimum-order-notional-10"></a>

Hyperliquid rejects any order below roughly **$10 notional**. Consequences:

* A plain order under $10 is rejected by the venue, and the order form stops you before you submit one.
* Every child order an execution strategy places has to clear the minimum too. Split a small order into many slices (say $50 over 20 slices) and most slices fall below it. The form caps a **TWAP** at the number of slices that each clear $10, and an **Iceberg** clip has to clear it on its own.

## Price and size precision

* **Size** is rounded to the asset's size step, which Hyperliquid sets per asset (ETH trades in steps of 0.0001, BTC in 0.00001).
* **Price** allows at most **5 significant figures**, and a limited number of decimal places that depends on the asset's size step (more for spot than for perpetuals).

Quote normalizes sizes and prices before signing, so an order with excess precision still goes through. But the working price and size may differ slightly from what you typed.

## Post-only orders are rejected if they would cross

A post-only order (**ALO**, add liquidity only) is rejected by the venue if its price would cross the spread:

* A buy must sit strictly **below** the best ask.
* A sell must sit strictly **above** the best bid.

The book can move between the moment you price an order and the moment it arrives on-chain. Quote's strategies guard their own post-only child orders against this automatically.

## Market orders are limits with a slippage bound <a href="#market-orders-are-ioc-limits-with-a-slippage-bound" id="market-orders-are-ioc-limits-with-a-slippage-bound"></a>

Hyperliquid has no true market order. A market order is an immediate-or-cancel limit at a slippage-adjusted price, the worst price you will accept. The terminal sets that price for you from the best opposing quote: the best ask when you buy, the best bid when you sell.

{% hint style="warning" %}
The bound is anchored to the best opposing quote, **not** the mid price. On wide-spread books, a bound computed from the mid can sit inside the spread, so the order crosses nothing and fills zero.
{% endhint %}

To place market orders over the API, see [Placing Orders](../guides/placing-orders.md#market-orders).

## Builder fee

Every order routed through Quote carries Quote's builder code, and the fee is attached server-side.

The constraint this places on you is the approval. **Quote requires builder-fee approval before it will trade for your wallet.** You sign it once with your main wallet when you [enable trading](agent-wallets.md#setting-it-up). Until then every order fails, whether placed from the terminal or the API.

For the rate and how it sits against Hyperliquid's own fees, see [Fees](../account/fees.md).

## Resting orders and open interest caps

Hyperliquid caps open interest on each asset, using a combination of liquidity, basis and leverage. An asset at its cap accepts no orders that would add to positions. The venue also rejects resting orders priced too far from the oracle price, which an algo order's activity timeline reports as **Too far from oracle**.

Both limits bite hardest on less liquid assets, and both can reject your orders in normal trading. See [Risks](../support/risks.md).

## Time in force

| Time in force | Behavior |
| --- | --- |
| **GTC** | Good til canceled: rests on the book until filled or canceled |
| **ALO** | Add liquidity only (post-only): rejected if it would cross |
| **IOC** | Immediate or cancel: fills what it can at once and cancels the rest |

Strategies use post-only orders for passive slices and immediate-or-cancel orders to catch up. Plain limit orders default to **GTC**.
