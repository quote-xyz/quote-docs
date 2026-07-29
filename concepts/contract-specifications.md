---
description: What a Hyperliquid perpetual actually is: collateral, denomination, and the quanto quirk.
---

# Contract Specifications

Quote perpetuals are Hyperliquid perpetuals. They have no expiry date and rely on [funding payments](funding-rate.md) to converge on the underlying spot price over time.

## Collateral and denomination

Hyperliquid runs one main margining style for perpetuals: **USDC collateral, USDT-denominated linear contracts**. The oracle price is denominated in USDT while the collateral you post is USDC.

No USDC/USDT exchange rate conversion is applied. These are therefore technically **quanto** contracts, where profit and loss denominated in USDT is paid out in USDC. In practice the two trade close enough that the distinction rarely shows, but it is the reason the pairing exists rather than an oversight.

The combination is chosen for liquidity and accessibility: USDT is where the deepest oracle sources are, USDC is what people hold on the venue.

## USDC-denominated exceptions

Where an asset's main source of liquidity is itself USDC-denominated, the oracle price is denominated in USDC instead. Currently that applies to **PURR-USD** and **HYPE-USD**, whose most liquid spot source is Hyperliquid's own spot market.

## Simplicity

Hyperliquid's contract specifications are simpler than most venues. There are a handful of contract-specific details and no address-specific restrictions, so what applies to one account applies to all.

The venue rules that do shape your orders are covered in [Hyperliquid Constraints](hyperliquid-constraints.md): minimum notional, price and size precision, post-only rejection, and how market orders actually work.

{% hint style="info" %}
Quote trades everything Hyperliquid lists, not only perpetuals: builder-DEX equities and commodities such as `xyz:HOOD` and `xyz:CL`, and HIP-4 prediction markets. Those follow their own conventions, in particular around trading hours for equities.
{% endhint %}
