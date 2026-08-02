---
description: >-
  Execute at a target percentage of real-time market volume: trade when the
  market trades.
---

# Percentage of Volume

<figure><img src="../.gitbook/assets/POV.gif" alt=""><figcaption></figcaption></figure>

`participation_rate` (POV, percentage of volume) keys your execution to **live** market activity. It observes traded volume in real time and submits clips sized to keep you at a target fraction of it. Busy tape → you trade more; quiet tape → you slow down. This bounds your footprint as a share of the market rather than as a schedule.

<figure><img src="../.gitbook/assets/Quote Docs (3).png" alt=""><figcaption><p>Participation rate: pacing against live market volume.</p></figcaption></figure>

## Example

{% code title="POST /api/orders" %}
```json
{
  "symbol": "ETH",
  "side": "sell",
  "size": "12",
  "orderType": "limit",
  "strategy": "participation_rate",
  "params": {
    "participationRate": "0.15",
    "maxDurationSecs": 7200
  }
}
```
{% endcode %}

This targets 15% of observed ETH volume until 12 ETH is done or two hours elapse.

## Parameters

| Parameter           | Type           | Default        | Description                                                              |
| ------------------- | -------------- | -------------- | ------------------------------------------------------------------------ |
| `participationRate` | decimal string | `0.10`         | Target fraction of observed market volume (e.g. `"0.15"` = 15%)          |
| `maxDurationSecs`   | integer        | `3600`         | Hard stop; remaining size is left unexecuted after this                  |
| `clipSizePct`       | decimal        | `5`            | Max single-clip size as a percent of total order size                    |
| `passivePct`        | integer 0–100  | `80`           | Percent of each clip's life spent passive before the aggressive fallback |
| `limitOffsetBps`    | decimal        | `0`            | Offset from the touch for passive placement                              |
| `minIntervalMs`     | integer        | server default | Minimum spacing between clips                                            |
| `reduceOnly`        | boolean        | `false`        | Clips only reduce an existing position                                   |

## Behavior notes

* **Completion is volume-dependent.** If the market goes quiet, so do you. A strategy at 10% participation in a dead market may not finish inside `maxDurationSecs`. Check `filledQty` at terminal state.
* **Rate vs. footprint.** Higher participation finishes faster but moves the market more. A common institutional range is 10–20%; above \~25% your own flow starts dominating the tape you're measuring.
* Clips run the standard [passive → aggressive cycle](overview.md#the-passive-aggressive-cycle), so you're still capturing spread within the volume budget.

## When to use something else

* You must finish by a time regardless of volume → [Passive TWAP](passive-twap.md) with `guaranteedCompletion`.
* You want the historical volume curve, not live tape → [VWAP](vwap.md).
* Stealth matters more than pace → [Iceberg](iceberg.md) (which also supports a participation cap).
