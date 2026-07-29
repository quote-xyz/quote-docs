# Margin

Margin calculations follow standard practices used by major centralized derivatives exchanges.

***

**Margin Modes**

When opening a position, users must choose a margin mode:

*   Cross Margin (default)

    Collateral is shared across all cross-margin positions, maximizing capital efficiency. Losses or gains from one position can affect others under the same mode.
*   Isolated Margin

    Collateral is confined to a single asset. If the position is liquidated, it does not impact other positions — whether cross or isolated. Likewise, losses from elsewhere won’t affect this position.

***

**Initial Margin & Leverage**

* Users can set leverage anywhere from 1x up to the asset’s maximum.
*   The margin required to open a position is:

    Position Size × Mark Price ÷ Leverage
* In cross margin, the initial margin is locked and cannot be withdrawn.
* In isolated margin, users can adjust the margin (add/remove) even after the position is opened.

For cross positions, unrealized PnL can be reused as margin for new positions. For isolated positions, unrealized PnL adds to that position’s margin.

Once a position is open, leverage is not automatically re-evaluated. Users must monitor their risk and can adjust by:

* Closing part or all of the position
* Adding margin (if isolated)
* Depositing USDC (if cross)

***

**Maintenance Margin & Liquidation**

* Cross positions are liquidated if your total account value (including unrealized PnL) falls below the maintenance margin, which is 50% of the initial margin at max leverage.
* Isolated positions follow the same logic, but the calculation is limited to the margin and notional value of the individual position only.
