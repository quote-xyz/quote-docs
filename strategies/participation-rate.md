---
description: >-
  Execute at a target percentage of real-time market volume: trade when the
  market trades.
---

# Percentage of Volume

<figure><img src="../.gitbook/assets/POV.gif" alt=""><figcaption></figcaption></figure>

**POV** (percentage of volume) keys your execution to **live** market activity. It watches the volume that actually trades and places orders sized to keep you at a target share of it. When the tape is busy you trade more; when it is quiet you slow down. This bounds your footprint as a share of the market rather than as a schedule.

<figure><img src="../.gitbook/assets/Quote Docs (3).png" alt=""><figcaption></figcaption></figure>

## Setting it up

Pick **POV** in the order type selector, then set:

| Setting | What it does |
| --- | --- |
| **Percent of volume** | Your target share of traded volume, from 1% to 50%. The default is 10% |
| **Time limit** | How long the order may run. When it expires, any remainder is swept at market |
| Randomization | Click to cycle between **no**, **light** and **strong** randomization of each order's size and timing |

The form estimates how long the order will take **to fill** at the rate you chose. If that runs past your time limit, it warns you that the remainder will be swept at market, so you can raise the rate or the limit and stay passive.

## Behavior notes

* **Completion depends on volume.** If the market goes quiet, so do you. A low rate in a dead market can reach its time limit with much of the order left, and that remainder is then swept at market.
* **Rate against footprint.** A higher rate finishes faster but moves the market more. Above roughly 25%, your own flow starts to dominate the tape you are measuring.
* **No volume, no pacing.** If a market has no volume data, the order paces on time alone and its page tells you so.
* Orders still run the standard [passive to aggressive cycle](overview.md#the-passive-aggressive-cycle), so you capture spread within the volume budget.
* **You can speed it up.** While it runs, **Speed up 2×** on the **Algos** tab raises the participation rate.

To submit a POV order over the API, see [Algo Orders](../guides/algo-orders.md#participation_rate).

## When to use something else

* You must finish by a time regardless of volume: [Passive TWAP](passive-twap.md) with **Guarantee completion**.
* You want the historical volume curve, not the live tape: [VWAP](vwap.md).
* Stealth matters more than pace: [Iceberg](iceberg.md).
