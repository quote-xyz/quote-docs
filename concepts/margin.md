---
description: Cross and isolated margin, how much a position locks up, and when it becomes at risk.
---

# Margin

Margin on Quote is Hyperliquid's margin. Quote routes your orders to the venue and does not add a margin layer of its own, so the rules below are the venue's and apply identically whether you trade from the terminal or the API.

## Margin modes

You choose a mode when you open a position.

| Mode | Collateral | Consequence |
|---|---|---|
| **Cross** (default) | Shared across all your cross positions | Best capital efficiency. A loss on one position can pull down the others |
| **Isolated** | Confined to the one position | A liquidation there does not touch anything else, and losses elsewhere do not touch it |

## Initial margin and leverage

Leverage runs from 1x up to the asset's maximum. The margin a position requires is:

```
position size × mark price ÷ leverage
```

In cross margin that amount is locked and cannot be withdrawn. In isolated margin you can add or remove margin after the position is open.

Unrealized profit is usable: on cross positions it can back new positions, and on isolated positions it adds to that position's own margin.

{% hint style="warning" %}
Leverage is not re-evaluated once a position is open. Nothing raises your margin for you as the price moves, so watch the position yourself and act by closing part of it, adding margin if it is isolated, or depositing USDC if it is cross.
{% endhint %}

## Maintenance margin

Maintenance margin is the floor your equity has to stay above. It is **50% of the initial margin at maximum leverage** for the asset, which works out between roughly 1.25% for a 40x asset and 16.7% for a 3x one.

- **Cross**: measured against your total account value, including unrealized profit and loss, across all cross positions.
- **Isolated**: measured against that position's own margin and notional only.

Fall below it and the position is liquidated. See [Liquidation](liquidation.md).

## Margin over the API

`POST /api/positions/leverage` sets leverage and `POST /api/positions/margin` adjusts isolated margin. Both need the `positions:write` scope. See the [Positions endpoints](../api-reference/endpoints/positions.md).

## Unified accounts

Hyperliquid offers account modes that unify spot and perp collateral. Under those, the cross-versus-isolated split above still exists but your collateral pool is wider than the perp balance alone, so perp-only equity figures understate what is actually backing your positions.
