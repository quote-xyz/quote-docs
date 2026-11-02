---
description: Clip-based, passive execution that hides your size.
---

# Iceberg

<figure><img src="../.gitbook/assets/iceberg.gif" alt=""><figcaption></figcaption></figure>

**Iceberg** shows the market only a small clip of your order at a time. When a clip fills, the next one takes its place at your limit price, so the market never sees your full size on the book. Clips are post-only orders that rest on the book and never cross the spread. In the terminal it has no time limit: it works until it fills or you cancel it.

A naive iceberg is easy to spot, because the same size reappearing at the same level is a pattern anyone can trade against. Quote's iceberg avoids presenting that pattern. How it does so is not published, because publishing it would help others detect it.

<figure><img src="../.gitbook/assets/Quote Docs (4).png" alt=""><figcaption></figcaption></figure>

## Setting it up

Pick **Iceberg** in the order type selector, then set:

| Setting | What it does |
| --- | --- |
| Limit price | The price the clips rest at |
| **Display size** | The visible clip. The rest of the order stays hidden. You can also drag the split on the iceberg graphic |
| Randomization | Click to cycle between **no**, **light** and **strong** randomization |

The summary shows the visible clip, the hidden size, the number of clips, and **Time limit: None**.

## Behavior notes

* **No completion guarantee.** Iceberg never takes liquidity. If price runs away from your level, it does not fill. That is the point. Pair it with a [trigger](../guides/triggers.md), or watch its progress, if you need a plan B.
* **Sizing the clip.** Each clip has to clear Hyperliquid's roughly $10 [minimum notional](../concepts/hyperliquid-constraints.md#minimum-order-notional-10), and the form will not submit a smaller one. Too large a clip defeats the hiding. A good starting point is the typical size at the top of the book for the asset.
* **Restart-safe.** A resting clip is recovered after an engine restart, not duplicated.

To submit an iceberg over the API, see [Algo Orders](../guides/algo-orders.md#iceberg).

## When to use something else

* You have a deadline: [Passive TWAP](passive-twap.md).
* You want to scale with volume without the concealment: [Percentage of Volume](participation-rate.md).
