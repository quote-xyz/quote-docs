---
description: Place your first order in the Quote terminal, and choose the right order type.
---

# Placing Your First Trade

This walks through a first trade in the [terminal](https://quotemarkets.xyz). You need an account with funds in it: see [Access and Restrictions](../account/access-and-restrictions.md) and [Deposits and Withdrawals](../account/deposits-and-withdrawals.md) first.

## Before your first order

Trading needs two one-time signatures from your wallet, both taken in the terminal:

1. **Register an agent wallet.** This is the key Quote signs your orders with. It can trade but can never withdraw. See [Agent Wallets](../concepts/agent-wallets.md).
2. **Approve the builder fee.** Quote will not trade for a wallet that has not approved it. See [Fees](../account/fees.md).

The terminal prompts for both the first time you try to trade. You only do this once.

## The order form

{% stepper %}
{% step %}
#### Pick a market

Use the symbol selector at the top of the form. Quote trades everything Hyperliquid lists: perpetuals like `BTC` and `ETH`, builder-DEX equities and commodities like `xyz:HOOD`, and prediction markets.
{% endstep %}

{% step %}
#### Choose buy or sell

The **Buy** and **Sell** toggle sets the side. On perpetuals, selling with no position opens a short.
{% endstep %}

{% step %}
#### Set your leverage and margin mode

Leverage runs from 1x to the asset's maximum, and you choose **cross** or **isolated** margin. This decides how much collateral the position locks and how a loss propagates. If you are unsure, use isolated: it contains the damage to one position. See [Margin](../concepts/margin.md).
{% endstep %}

{% step %}
#### Enter a size

Size is in the base asset. The form shows your available balance and buying power, so you can see what the position will consume.

Mind the floor: Hyperliquid rejects anything under roughly $10 notional, and for the algorithmic order types each individual slice has to clear it too.
{% endstep %}

{% step %}
#### Choose an order type

This is the decision that matters most, and it is covered in the next section.
{% endstep %}

{% step %}
#### Review and place

The form summarizes the order before you commit. Confirm, and it goes to the engine.

A confirmation means the order was **accepted**, not that it filled. Watch the positions panel for fills, and for the algorithmic types watch the live progress readout.
{% endstep %}
{% endstepper %}

## Choosing an order type

The selector offers eight, and the first three behave like order types anywhere:

| Type | What it does |
|---|---|
| **Limit** | Rests on the book at your price |
| **Market** | Fills right away by sweeping the book |
| **Scale** | Spreads limit orders across a price range |

The other five hand the order to the execution engine, which works it over time instead of sending it to the book in one piece. This is what Quote is for, and on any size that would move the market it is usually cheaper.

| Type | What it does | Read more |
|---|---|---|
| **TWAP** | Slices into steady parts over a set time | [Passive TWAP](../strategies/passive-twap.md) |
| **VWAP** | Follows market volume to reduce impact | [VWAP](../strategies/vwap.md) |
| **POV** | Paces at a target share of market volume | [Participation Rate](../strategies/participation-rate.md) |
| **Iceberg** | Shows only a small slice of your true size | [Iceberg](../strategies/iceberg.md) |
| **Chase** | Follows the best bid/ask toward a fill | [Chase Limit](../strategies/chase-limit.md) |

{% hint style="info" %}
The terminal and the API use different names for the same strategies. **TWAP** is `passive_twap`, **POV** is `participation_rate`, and **Chase** is `chase_limit`. VWAP and Iceberg match. See [Strategies Overview](../strategies/overview.md).
{% endhint %}

### A rule of thumb

- **Small order, want it now**: Market. You pay the spread, and on a small size that is fine.
- **Small order, patient**: Limit. Rest at your price and wait.
- **Large order with a deadline**: TWAP.
- **Large order, benchmarked to the market**: VWAP.
- **Large order, no deadline, and you do not want to be seen**: Iceberg.
- **Large order, want to stay a fixed share of activity**: POV.
- **One fill near the touch, soon, without crossing**: Chase.

"Large" here means large relative to the book, not to your account. On a thin market a few thousand dollars is enough to move the price against you.

## Optional settings

- **Take profit and stop loss**, attached to the order so they are placed against the resulting position.
- **Reduce only**, which stops an order from accidentally opening or increasing a position.
- **Time in force** for plain limit orders: `GTC` rests, `ALO` is post-only and rejected if it would cross, `IOC` fills what it can and cancels the rest.

## After the order

The positions panel shows what you now hold, with unrealized profit and loss, liquidation price, and funding accrued. Algorithmic orders also show live progress while they work.

Once you have a few executions behind you, [Analytics](analytics.md) tells you what the engine actually saved: every fill is benchmarked against arrival price, market VWAP, and a simulated market order.

## Next

* Understand what you are trading: [Margin](../concepts/margin.md), [Liquidation](../concepts/liquidation.md), and [Funding Rate](../concepts/funding-rate.md).
* Automate an entry: [Conditional Triggers](triggers.md) fire an order when a price, funding, or time condition is met.
* Save an execution style you like as an [Order Template](templates.md).
