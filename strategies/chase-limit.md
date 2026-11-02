---
description: >-
  A post-only limit order that follows the best bid or offer, within a bound
  you set.
---

# Chase Limit

<figure><img src="../.gitbook/assets/Chase.gif" alt=""><figcaption></figcaption></figure>

**Chase** is for when you want a maker fill close to the current price and the market is drifting away from you. It rests a post-only limit order at the front of the book and moves it as the best bid moves (the best ask when you sell), so you stay first in line without crossing the spread.

It is a patient version of a marketable limit: it follows price, but only as far as you allow.

<figure><img src="../.gitbook/assets/Quote Docs (5).png" alt=""><figcaption></figcaption></figure>

## Setting it up

Pick **Chase** in the order type selector. You do not type a limit price: the form prices the order off the book. Then set:

| Setting | What it does |
| --- | --- |
| **Stop chasing at** | How far the order may follow the book, as a percentage or a price. Once it gets there it stops and rests, still live, at that price |
| **Fill at market if unfilled** | Off by default. Turn it on and set a time **after** which whatever is left is taken at market, instead of the order expiring |
| **Cancel order at** | Optional. If the market moves this far against you, the whole order is canceled and nothing is left resting |

The summary shows the resting price, the price bound, the placement (**Maker only**, or **Maker, then taker** with the market fill on) and the time in force.

## How long it lasts

By default a chase is **good-til-filled for up to 24 hours**. It keeps following the book until it fills, you cancel it, or the 24 hours run out. With **Fill at market if unfilled** on, the deadline you set replaces the 24 hours, and the remainder is filled at market when it passes.

## Behavior notes

* **It can miss.** A chase fills only if the market comes to you. If price runs away past your **Stop chasing at** level, the order rests there and may never fill. When you need certainty, use a market order, or turn on **Fill at market if unfilled**.
* **Best on liquid books.** On a thin book, each move competes with a sparse, shifting touch.
* **News orders can use it.** Set **News order type** to **Chase** in the [News](../trading-tools/news.md) settings to place headline trades this way.

To submit a chase over the API, see [Algo Orders](../guides/algo-orders.md#chase_limit).

## When to use something else

* Larger size to work over time: [Passive TWAP](passive-twap.md).
* You must fill now whatever the cost: a plain market order.
