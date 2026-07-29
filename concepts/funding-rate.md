---
description: The hourly payment between longs and shorts that keeps the perpetual price near spot.
---

# Funding Rate

A perpetual contract has no expiry, so nothing forces its price back to the underlying. Funding does that job: a periodic payment exchanged directly between traders holding long and short positions.

## Who pays whom

| Funding rate | Direction |
|---|---|
| Positive | Longs pay shorts |
| Negative | Shorts pay longs |

When the perpetual trades above spot, demand is skewed long, funding turns positive, and holding a long costs you something. That cost is the incentive for someone to take the other side, which pulls the price back toward the index.

## How it works on Hyperliquid

- Funding is calculated and settled **every hour**, more often than most venues, which keeps the perpetual tracking the index more tightly.
- You pay or receive only if you hold the position **at the funding timestamp**. A position opened and closed between timestamps pays nothing.
- The amount scales with your position size and the prevailing rate.

## Why it matters

Funding is a real component of your profit and loss, and it accrues whether or not the price moves. Hold a large position through a sustained high funding rate and it will erode returns on its own. Held on the receiving side, it adds to them.

This is why funding is worth tracking as its own line rather than being folded into price performance.

## Tracking your funding

Quote keeps a per-wallet funding ledger synced from Hyperliquid, with totals, a timeline, and the raw per-payment log. See [Analytics](../guides/analytics.md#funding) for the endpoints and the sign convention.
