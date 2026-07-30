---
description: >-
  Venue rules that shape every order: minimum notional, price and size
  precision, ALO crossing, builder fees, and market-order slippage prices.
---

# Hyperliquid Constraints

<figure><img src="../.gitbook/assets/screenshot_1.5x_postspark_2026-07-30_11-28-14.png" alt=""><figcaption></figcaption></figure>

Hyperliquid enforces several non-obvious rules. Quote handles most of them server-side, but they explain behavior you will see: skipped slices, adjusted prices, rejected orders.

## Minimum order notional: \~$10 <a href="#minimum-order-notional-10" id="minimum-order-notional-10"></a>

Hyperliquid rejects any order below roughly **$10 notional**. Consequences:

* A plain order under $10 notional will be rejected by the venue.
* Execution strategies **skip** child slices that would fall under the minimum rather than submit doomed orders. If you split a small order into many slices (e.g. $50 over 20 slices), most slices are sub-minimum and the strategy can stall. Size your `numSlices` so each slice clears \~$10 comfortably.

## Price and size precision

* **Size** is rounded to the asset's `szDecimals`, from Hyperliquid's meta (e.g. ETH: 4, BTC: 5, SOL: 2).
* **Price** allows at most **5 significant figures**, and at most `MAX_DECIMALS − szDecimals` decimal places (`MAX_DECIMALS` = 6 for perps, 8 for spot).

Quote normalizes sizes and prices before signing, so a request with excess precision succeeds. But the working price and size may differ slightly from what you sent.

## ALO orders are rejected if they would cross

ALO (Add Liquidity Only / post-only) orders are rejected by the venue if the price would cross the spread:

* Buy ALO: price must be strictly **below** the best ask.
* Sell ALO: price must be strictly **above** the best bid.

The book can move between your snapshot and your order arriving on-chain, so guard your own ALO prices accordingly. Quote's strategies handle this automatically for their child orders.

## Market orders are IOC limits with a slippage bound

Hyperliquid has no true market order. A "market" order is an **IOC limit** at a slippage-adjusted price, so `orderType: "market"` still requires `limitPrice`, the worst price you'll accept:

* Buy: anchor to the best **ask** (e.g. `bestAsk × 1.05` for 5% max slippage).
* Sell: anchor to the best **bid** (e.g. `bestBid × 0.95`).

{% hint style="warning" %}
Anchor slippage to the best opposing quote, **not** the mid price. On wide-spread books (outcome markets can quote `0.00126 / 0.01013`), `mid × 1.05` sits _below_ the best ask, so the IOC crosses nothing and silently fills zero.
{% endhint %}

## Builder fee

Every order routed through Quote carries Quote's builder code, and the fee is attached server-side.

The constraint this places on you is the approval. **Quote requires builder-fee approval before it will trade for your wallet.** You sign it once with your master wallet during [agent setup](agent-wallets.md); until then every order submission fails, from the terminal and the API alike. Before trading programmatically, confirm that `builderFeeApproved` is `true` on `GET /api/agents`.

For the rate and how it sits against Hyperliquid's own fees, see [Fees](../account/fees.md).

## Resting orders must stay within 1% of the oracle

An order cannot rest further than **1% from the oracle price**. The venue rejects anything priced outside that band, and Hyperliquid's own HLP is exempt so that it can keep quoting.

This bites on strategies that quote well away from the touch, and on resting orders left far out as a cheap limit. Price inside the band, or accept that the order will be rejected rather than sitting where you left it.

The band exists alongside **open interest caps**, set from a combination of liquidity, basis, and leverage. An asset at its cap accepts no new positions at all. See [Risks](../support/risks.md).

## Time in force

| TIF   | Behavior                                                           |
| ----- | ------------------------------------------------------------------ |
| `GTC` | Good till cancelled: rests on the book                             |
| `ALO` | Add liquidity only (post-only): rejected if it would cross         |
| `IOC` | Immediate or cancel: fills what it can instantly, cancels the rest |

Strategies use ALO for passive slices and IOC for aggressive catch-up; plain orders default to `GTC`.
