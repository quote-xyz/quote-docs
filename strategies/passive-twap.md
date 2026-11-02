---
description: >-
  Time-sliced execution that rests passively at the touch and crosses the
  spread when a slice falls behind.
---

# Passive TWAP

<figure><img src="../.gitbook/assets/Brave Browser.gif" alt=""><figcaption></figcaption></figure>

**TWAP** splits your order into slices and works them at a steady pace over a window you set. Each slice first rests passively at the best bid or offer, capturing the spread and paying the maker fee. A slice that has not filled in its time crosses the spread to keep the order on schedule. The result is TWAP scheduling at better prices than slicing with market orders.

<figure><img src="../.gitbook/assets/Quote Docs (1).png" alt=""><figcaption></figcaption></figure>

## Setting it up

Pick **TWAP** in the order type selector, then set:

| Setting | What it does |
| --- | --- |
| **Duration** | The window the order is worked over |
| **Execution** | One slider from patient to fast. Lower settings rest more of each slice on the book; higher settings cross the spread more often to stay on schedule |
| Execution shape | Click to cycle between **front** load, **even** load and **back** load: how size is weighted across the window |
| Randomization | Click to cycle between **no**, **light** and **strong** randomization of each slice's size and timing |
| **Guarantee completion** | Off by default. When on, any size still unfilled at the end is taken in one final cross, up to 1% past the best price |

As you move the **Execution** slider, the form shows the number of intervals and the passive share it resolves to, and a summary of the runtime, the number of slices and the size of each.

## Behavior notes

* **Slices and the $10 minimum.** Every slice has to clear Hyperliquid's roughly $10 [minimum notional](../concepts/hyperliquid-constraints.md#minimum-order-notional-10). On a small order the form caps the number of slices so each one clears it, and says so above the submit button.
* **Without a guarantee, it can end short.** If the market moves beyond your limit price, the order stays at your levels and finishes with what it filled. Turn on **Guarantee completion** when finishing matters more than price.
* **You can speed it up.** While it runs, **Speed up 2×** on the **Algos** tab compresses the remaining schedule. **Finish now** sweeps the remainder at market.
* **Restart-safe.** The engine recovers a running TWAP after a restart rather than duplicating its child orders. See [Execution Safeguards](safeguards.md).

To submit a TWAP over the API, see [Algo Orders](../guides/algo-orders.md#passive_twap).

## When to use something else

* You are benchmarked to volume, not time: [VWAP](vwap.md).
* No deadline, and hiding size matters most: [Iceberg](iceberg.md).
