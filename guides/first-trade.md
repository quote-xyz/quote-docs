---
description: >-
  Place your first order in the Quote application, and choose the right order
  type.
---

# Placing Your First Trade

<figure><img src="../.gitbook/assets/video_1.5x_postspark_2026-07-30_11-23-02.gif" alt=""><figcaption></figcaption></figure>

This walks through a first trade in the [application](https://quotemarkets.xyz). You need an account with funds in it: see [Access and Restrictions](../account/access-and-restrictions.md) and [Deposits and Withdrawals](../account/deposits-and-withdrawals.md) first.

## Before your first order

Trading needs two one-time signatures from your wallet, both taken in the terminal:

1. **Register an agent wallet.** This is the key Quote signs your orders with. It can trade but can never withdraw. See [Agent Wallets](../concepts/agent-wallets.md).
2. **Approve the builder fee.** Quote will not trade for a wallet that has not approved it. See [Fees](../account/fees.md).

The terminal prompts for both the first time you try to trade. You only do this once.

## The order form

{% stepper %}
{% step %}
#### Pick a market

Use the symbol selector at the top of the form. Quote trades spot, perpetuals like `BTC` and `ETH`, and builder-DEX equities and commodities like `xyz:HOOD`.
{% endstep %}

{% step %}
#### Choose buy or sell

The **Buy / Long** and **Sell / Short** toggle sets the side (on spot it reads **Buy** and **Sell**). On perpetuals, selling with no position opens a short.
{% endstep %}

{% step %}
#### Set your leverage and margin mode

Leverage runs from 1x to the asset's maximum, and you choose **cross** or **isolated** margin. This decides how much collateral the position locks and how a loss propagates. If you are unsure, use isolated: it contains the damage to one position. See [Margin](../concepts/margin.md).
{% endstep %}

{% step %}
#### Enter a size

Enter the size in the asset or in USDC. The form shows your available balance and buying power, so you can see what the position will consume.

Mind the floor: Hyperliquid rejects anything under roughly $10 notional, and for the algorithmic order types each individual slice has to clear it too.
{% endstep %}

{% step %}
#### Choose an order type

This is the decision that matters most, and it is covered in the next section.
{% endstep %}

{% step %}
#### Review and place

The form summarizes the order before you commit. Confirm, and it goes to the engine.

A confirmation means the order was **accepted**, not that it filled. Watch the positions panel for fills, and for the algorithmic types, watch the live progress readout.
{% endstep %}
{% endstepper %}

## Choosing an order type

The selector offers eight, and the first three behave like order types anywhere:

<table><thead><tr><th width="157.421875">Type</th><th>What it does</th></tr></thead><tbody><tr><td><strong>Limit</strong></td><td>Rests on the book at your price</td></tr><tr><td><strong>Market</strong></td><td>Fills right away by sweeping the book</td></tr><tr><td><strong>Scale</strong></td><td>Spreads limit orders across a price range (<a href="#scale-orders">more</a>)</td></tr></tbody></table>

The other five hand the order to the execution engine, which works it over time instead of sending it to the book in one piece. This is what Quote is for, and on any size that would move the market it is usually cheaper.

<table><thead><tr><th width="153.859375">Type</th><th>What it does</th><th>Read more</th></tr></thead><tbody><tr><td><strong>TWAP</strong></td><td>Slices into steady parts over a set time</td><td><a href="../strategies/passive-twap.md">Passive TWAP</a></td></tr><tr><td><strong>VWAP</strong></td><td>Follows market volume to reduce impact</td><td><a href="../strategies/vwap.md">VWAP</a></td></tr><tr><td><strong>POV</strong></td><td>Paces at a target share of market volume</td><td><a href="../strategies/participation-rate.md">Percentage of Volume</a></td></tr><tr><td><strong>Iceberg</strong></td><td>Shows only a small slice of your true size</td><td><a href="../strategies/iceberg.md">Iceberg</a></td></tr><tr><td><strong>Chase</strong></td><td>Follows the best bid/ask toward a fill</td><td><a href="../strategies/chase-limit.md">Chase Limit</a></td></tr></tbody></table>

### A rule of thumb

* **Small order, want it now**: Market. You pay the spread, and on a small size that is fine.
* **Small order, patient**: Limit. Rest at your price and wait.
* **Large order with a deadline**: TWAP.
* **Large order, benchmarked to the market**: VWAP.
* **Large order, no deadline, and you do not want to be seen**: Iceberg.
* **Large order, want to stay a fixed share of activity**: POV.
* **One fill near the touch, soon, without crossing**: Chase.

"Large" here means large relative to the book, not to your account. On a thin market, a few thousand dollars is enough to move the price against you.

## Scale orders

A scale order spreads a set of limit orders across a price range instead of resting the whole size at one price. It is a way to build a position into a move without picking a single level.

In the order form you set four things:

| Field | What it does |
|---|---|
| **Start Price** | One end of the range |
| **End Price** | The other end |
| **Orders** | How many limit orders to spread across it |
| **Size Skew** | Puts more of the size at the start or at the end of the range, rather than splitting it evenly |

Skew is what makes it more than a loop. Weight size towards the far end and you buy more the further price falls, which lowers your average entry if it keeps going and leaves you smaller if it does not.

Two things to watch. Each individual order still has to clear the roughly $10 [minimum notional](../concepts/hyperliquid-constraints.md#minimum-order-notional-10), and the form tells you when the smallest one falls short. And a scale order is a set of resting limits, not a worked strategy: nothing repositions them if the market leaves the range. If you want the engine to adapt, use an [execution strategy](../strategies/overview.md) instead.

## Optional settings

* **Take profit and stop loss**, attached to the order so they are placed against the resulting position.
* **Reduce only**, which stops an order from accidentally opening or increasing a position.
* **Time in force** for plain limit orders: **GTC** rests until filled or canceled, **ALO** is post-only and rejected if it would cross, **IOC** fills what it can and cancels the rest.

## After the order

The positions panel shows what you now hold, with unrealized profit and loss, liquidation price, and funding accrued. Algorithmic orders also show live progress while they work.

Once you have a few executions behind you, [Analytics](analytics.md) tells you what the engine actually saved: every fill is benchmarked against arrival price, market VWAP, and a simulated market order.

## Next

* Understand what you are trading: [Margin](../concepts/margin.md), [Liquidation](../concepts/liquidation.md), and [Funding Rate](../concepts/funding-rate.md).
* Automate an entry: [Conditional Triggers](triggers.md) fire an order when a price, funding, or time condition is met.
