---
description: What happens when equity falls below maintenance margin, and how to avoid the backstop.
---

# Liquidation

A liquidation happens when your account equity drops below the [maintenance margin](margin.md#maintenance-margin): 50% of the initial margin at the asset's maximum leverage, which ranges from roughly 1.25% on a 40x asset to 16.7% on a 3x one.

## What happens when the threshold breaks

{% stepper %}
{% step %}
#### Market liquidation

The system places market orders to close the full position size.
{% endstep %}

{% step %}
#### Margin restored

If enough capital is recovered to restore the margin requirement, any collateral left over stays yours.
{% endstep %}

{% step %}
#### Backstop liquidation

If closing on the market fails and equity falls below **two thirds of the maintenance margin**, the position is taken over by the Liquidator Vault instead.
{% endstep %}
{% endstepper %}

In a backstop event the outcome depends on your margin mode:

- **Cross**: all cross margin and cross positions transfer to the liquidator. With no isolated positions, your account equity goes to zero.
- **Isolated**: only that position and its margin transfer. Your other assets and cross positions are untouched.

{% hint style="warning" %}
Maintenance margin is not returned in a backstop liquidation. That buffer is what makes liquidations worth performing for the Liquidator Vault, so a backstop always costs more than closing yourself. Use stop losses, or exit manually before the mark price reaches your liquidation level.
{% endhint %}

## Mark price

Liquidation is assessed on the **mark price**, not the last traded price. Hyperliquid builds the mark from external centralized-exchange data as well as its own book state.

This matters in fast markets: a thin book can print a price far from fair value for a moment, and a mark built only from that book would liquidate people who were never actually underwater. Aggregating outside sources makes that much less likely.

## Reducing the risk

- Attach a stop loss when you open the position. Both plain orders and [algo strategies](../guides/algo-orders.md) accept TP/SL at submission time.
- Watch funding on leveraged positions held for a long time. See [Funding Rate](funding-rate.md).
- Use isolated margin to contain the blast radius of a position you are less sure about.
- Prefer adding margin over letting a position drift toward the threshold, since a backstop costs you the buffer as well as the position.

Hyperliquid publishes the full mechanics in its own [liquidation documentation](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/liquidations).
