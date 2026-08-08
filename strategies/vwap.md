---
description: >-
  Volume-proportional execution: slice sizes follow the asset's intraday volume
  profile instead of the clock.
---

# VWAP

<figure><img src="../.gitbook/assets/VWAP (1).gif" alt=""><figcaption></figcaption></figure>

`vwap` executes your order in proportion to how the market actually trades through the day. Instead of equal time slices, each slice's size follows a volume profile built from historical candle data for the asset: larger slices when the market is typically busy, smaller when it is quiet. Use it when your benchmark is the market VWAP over your window.

#### Participation and volume caps

* The "% of volume" figure shown is the _target_ participation rate — the average share of expected market volume the order needs to consume, given its size and duration, to finish on schedule against the forecasted volume curve.
* The volume cap is a separate, harder ceiling: the max participation allowed in any interval. It isn't set directly by size or duration alone — it also depends on the execution setting (below) and shrinks for tighter windows. In the observed UI, the same passive setting showed a 9% cap on a 30-minute order and a 5% cap on a 1-minute order.
* If hitting the requested duration would require exceeding the cap, the engine does not raise the cap to compensate. It fills as much as the cap allows inside the window and surfaces the shortfall directly: expected % filled in-window, plus the extra time needed to complete the remainder (e.g. "\~84% fills in-window, \~1m 11s to complete" for a 1-minute order needing 5.9% of volume against a 5% cap).

#### Impact vs fills speed

<figure><img src="../.gitbook/assets/Screenshot 2026-08-08 at 3.37.31 pm.png" alt=""><figcaption></figcaption></figure>

The "Execution" slider trades off market impact against certainty of finishing on time by moving both the cap and the crossing behavior together:

* _Lower impact_ (left end): lowest volume cap, passive placement only. The order never crosses the spread — if the cap binds, it under-fills within the window and finishes late rather than taking liquidity.
* _Faster fill_ (right end): highest volume cap, crosses to hold schedule. The order is willing to cross the spread to stay on the forecasted curve, trading impact for a higher chance of completing within the requested duration.



Each slice still runs the standard [passive → aggressive cycle](overview.md#the-passive-aggressive-cycle), so you're capturing spread within the volume schedule.

<figure><img src="../.gitbook/assets/Quote Docs (2).png" alt=""><figcaption></figcaption></figure>

## Example

{% code title="POST /api/orders" %}
```json
{
  "symbol": "BTC",
  "side": "buy",
  "size": "0.75",
  "orderType": "limit",
  "strategy": "vwap",
  "params": {
    "durationSecs": 7200,
    "numSlices": 24
  }
}
```
{% endcode %}

## Parameters

| Parameter        | Type          | Default | Description                                                                   |
| ---------------- | ------------- | ------- | ----------------------------------------------------------------------------- |
| `durationSecs`   | integer       | `300`   | Total execution window in seconds                                             |
| `numSlices`      | integer       | `10`    | Number of child slices (sized by the volume profile)                          |
| `passivePct`     | integer 0–100 | `80`    | Percent of each slice interval spent passive before the IOC fallback          |
| `limitOffsetBps` | decimal       | `0`     | Offset from the touch for passive placement                                   |
| `dynamic`        | boolean       | `true`  | Refresh the volume forecast during execution rather than freezing it at start |
| `reduceOnly`     | boolean       | `false` | Children only reduce an existing position                                     |

## Behavior notes

* **The profile is per-asset and horizon-aware.** Volume curves differ sharply between crypto majors, builder-DEX equities (which follow underlying market hours), and prediction markets; the engine builds each profile from the asset's own history. How the forecast is built and rebalanced is deliberately not specified here.
* **Falls back gracefully.** If no usable profile exists for the asset/window, slicing degrades to uniform TWAP behavior rather than stalling.
* The engine's VWAP forecasting has been verified by walk-forward testing on real Hyperliquid data across all product classes.

## When to use something else

* Deadline matters more than tracking volume → [Passive TWAP](passive-twap.md) with `guaranteedCompletion`.
* You want to scale with _live_ volume rather than the historical curve → [Participation Rate](participation-rate.md).
