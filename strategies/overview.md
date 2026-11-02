---
description: >-
  Execution algorithms, how to choose between them, and the mechanics they
  share.
---

# Strategies Overview

<figure><img src="../.gitbook/assets/SC .gif" alt=""><figcaption></figcaption></figure>

Quote's execution engine runs five strategies. You pick one from the order type selector in the order form.

| Strategy                                    | In the terminal | Best for                                           |
| ------------------------------------------- | --------------- | -------------------------------------------------- |
| [Passive TWAP](passive-twap.md)             | **TWAP**        | Time-sliced execution over a window you set        |
| [VWAP](vwap.md)                             | **VWAP**        | Tracking the market's volume profile over a window |
| [Iceberg](iceberg.md)                       | **Iceberg**     | Hiding large size; passive, no deadline            |
| [Percentage of Volume](participation-rate.md) | **POV**       | Staying a fixed share of real-time market volume   |
| [Chase Limit](chase-limit.md)               | **Chase**       | A limit order that follows the best bid or offer   |

To submit strategies over the API, see [Algo Orders](../guides/algo-orders.md).

<figure><img src="../.gitbook/assets/Screenshot 2026-08-02 at 3.41.35 pm.png" alt=""><figcaption></figcaption></figure>

## Choosing a strategy

<details>

<summary>I need it done by a deadline</summary>

**TWAP** with **Guarantee completion** on. It slices your order over the duration you set, crosses the spread when a slice falls behind, and takes any final remainder in one cross at the end.

</details>

<details>

<summary>I'm benchmarked against VWAP</summary>

**VWAP**. It sizes slices in proportion to the asset's historical intraday volume profile instead of evenly in time.

</details>

<details>

<summary>I don't want the market to see my size</summary>

**Iceberg**. It shows only one small clip at a time and never crosses the spread. It has no time limit: it works until filled or canceled.

</details>

<details>

<summary>I want to scale with market activity</summary>

**POV**. It targets a fixed share of the volume that actually trades: more when the market is busy, less when it is quiet.

</details>

<details>

<summary>I want one fill near the touch, soon</summary>

**Chase**. It rests a post-only limit at the front of the book and follows the best bid or offer, up to a bound you set.

</details>

## Shared mechanics

### The passive to aggressive cycle <a href="#the-passive-aggressive-cycle" id="the-passive-aggressive-cycle"></a>

Time-sliced strategies share one principle: rest passively first, take liquidity only when the schedule demands it. Passive child orders sit on the book, earning the spread and paying the maker fee. If a slice falls behind, the engine takes liquidity to keep the order on schedule.

How and when child orders are placed, repriced and converted is managed by the engine and adapts to market conditions. Those mechanics are not documented, because publishing them would help others detect and trade against your orders.

### The Execution slider

The terminal does not make you set slice counts and passive percentages by hand. **TWAP** and **VWAP** have one **Execution** slider, from 0 to 100, that expresses the trade-off between patience and speed:

* Lower settings rest more of the order on the book and cross the spread less. Cost is lower, and the chance of finishing on time is lower too.
* Higher settings cross the spread more readily to hold the schedule.

On **TWAP** the slider resolves into the number of intervals and the share of each one spent resting passively. On **VWAP** it sets your volume cap. The form previews the resolved values as you move it, so you can see what a setting will do before you submit.

### Guardrails and running orders

Every algo order has a **Guardrails** section. **Cancel order at** cancels the whole order if the market moves that far against you, and leaves nothing resting. **Reduce only** stops the order from opening or adding to a position.

Running orders appear in the **Algos** tab of the positions panel. From there you can cancel an order, or use **Finish now** to sweep the remainder at market. **TWAP** and **POV** orders can also be sped up once with **Speed up 2×**. Open an order to see its own page: progress against plan, fills, fees and benchmarks.

### Execution benchmarks

Every strategy execution is measured against three benchmarks (see [Analytics](../guides/analytics.md)):

* **vs. arrival price**: the mid when your parent order started (implementation shortfall).
* **vs. market VWAP**: all market trades during your execution window.
* **vs. market order**: a simulated sweep of the book at each fill time. This is the most actionable benchmark: it measures the spread you captured compared with sweeping the book.

All benchmark values are signed basis points with the convention **positive = worse, negative = better**.

{% hint style="info" %}
Strategies are a closed, curated set, and every one runs under the same [execution safeguards](safeguards.md): price bounds, overfill protection, and recovery that survives an engine restart.
{% endhint %}
