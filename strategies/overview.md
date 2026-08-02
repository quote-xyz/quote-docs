---
description: >-
  Execution algorithms, how to choose between them, and the mechanics they
  share.
---

# Strategies Overview

<figure><img src="../.gitbook/assets/SC .gif" alt=""><figcaption></figcaption></figure>

Quote's execution engine runs five strategies. In the terminal, you pick one from the order type selector; over the API you set `strategy` on [`POST /api/orders`](../guides/algo-orders.md) and tune it via `params`.

| Strategy                                    | In the terminal | `strategy` value     | Best for                                           |
| ------------------------------------------- | --------------- | -------------------- | -------------------------------------------------- |
| [Passive TWAP](passive-twap.md)             | TWAP            | `passive_twap`       | Time-sliced execution with guaranteed completion   |
| [VWAP](vwap.md)                             | VWAP            | `vwap`               | Tracking the market's volume profile over a window |
| [Iceberg](iceberg.md)                       | Iceberg         | `iceberg`            | Hiding large size; pure-passive, no deadline       |
| [Participation Rate](participation-rate.md) | POV             | `participation_rate` | Staying a fixed % of real-time market volume       |
| [Chase Limit](chase-limit.md)               | Chase           | `chase_limit`        | A limit order that follows the BBO within a bound  |

The terminal's names are shorter than the API's. Where they differ, the middle column is what you will see in the order form.

<figure><img src="../.gitbook/assets/Screenshot 2026-08-02 at 3.41.35 pm.png" alt=""><figcaption></figcaption></figure>

## Choosing a strategy

<details>

<summary>I need it done by a deadline</summary>

**Passive TWAP** with `guaranteedCompletion: true`. It slices your order evenly over `durationSecs` and falls back to aggressive IOC orders when passive fills lag.

</details>

<details>

<summary>I'm benchmarked against VWAP</summary>

**VWAP**. Slices proportionally to the asset's historical intraday volume profile instead of uniformly in time.

</details>

<details>

<summary>I don't want the market to see my size</summary>

**Iceberg**. Shows only one small clip at a time, repositions with randomized timing and sizing to defeat order-book pattern detection, and never crosses the spread. It has no time limit: it works until filled or cancelled.

</details>

<details>

<summary>I want to scale with market activity</summary>

**Participation Rate**. Targets a fixed percentage of observed market volume: it trades more when the market is busy, less when it is quiet.

</details>

<details>

<summary>I want one fill near the touch, soon</summary>

**Chase Limit**. Places a limit near the BBO and re-pegs as the market moves, tightening each attempt, for a bounded number of attempts/seconds.

</details>

## Shared mechanics

### The passive → aggressive cycle <a href="#the-passive-aggressive-cycle" id="the-passive-aggressive-cycle"></a>

Time-sliced strategies share one principle: rest passively first, take liquidity only when the schedule demands it. Passive child orders sit on the book, earning the spread and maker fees; if a slice falls behind, the engine takes liquidity to keep the order on schedule.

The `passivePct` parameter sets the balance: higher values wait longer for passive fills before taking liquidity; lower values trade cost for completion certainty.

How and when child orders are placed, repriced, and converted is managed by the engine and adapts to market conditions. Those mechanics are deliberately not documented: publishing them would help others detect and trade against your orders.

### Urgency and price discipline

The terminal does not make you set slice counts and passive percentages by hand. Two dials, each 0 to 100, express the trade-off instead:

* **Urgency**: how aggressively to interact with market liquidity. Higher urgency means larger orders posted to the book and less waiting for a fill.
* **Price discipline**: how much price matters against completion. Higher discipline means resting more passively and accepting a greater chance of not finishing.

Urgency resolves into concrete parameters for whichever strategy you picked: how many intervals the order is split into, how much of each interval is spent passively, and the target participation rate. The terminal previews those values as you move the dial, so you can see what a setting will actually do before submitting.

The two dials are what an [order template](../guides/templates.md) stores. Over the API you skip them and set the underlying parameters directly.

### Common parameters

These appear across multiple strategies (all optional; camelCase and snake\_case are both accepted):

<table><thead><tr><th width="230.04296875">Parameter</th><th>Meaning</th></tr></thead><tbody><tr><td><code>durationSecs</code></td><td>Total execution window</td></tr><tr><td><code>numSlices</code></td><td>Number of child slices</td></tr><tr><td><code>passivePct</code></td><td>Portion of each slice spent passive before going aggressive</td></tr><tr><td><code>randomize</code></td><td>Jitter slice timing and sizing to avoid detectable patterns</td></tr><tr><td><code>reduceOnly</code></td><td>Children only reduce an existing position</td></tr><tr><td><code>guaranteedCompletion</code></td><td>Sweep any remainder with a wide-tolerance IOC at the end</td></tr><tr><td><code>attachedTpsl</code></td><td>Attach take-profit/stop-loss to the resulting position</td></tr></tbody></table>

Per-strategy pages document the full parameter set with defaults.

### Execution benchmarks

Every strategy execution is measured against three benchmarks (see [Analytics](../guides/analytics.md)):

* **vs. arrival price**: the mid when your parent order started (implementation shortfall).
* **vs. market VWAP**: all market trades during your execution window.
* **vs. market order**: a simulated aggressive sweep of the book at each fill time. This is the most actionable benchmark: it measures the spread you captured compared with sweeping the book.

All benchmark values are signed basis points with the convention **positive = worse, negative = better**.

{% hint style="info" %}
Strategies are a closed, curated set, and every one runs under the same [execution safeguards](safeguards.md): price bounds, overfill protection, and recovery that survives an engine restart.
{% endhint %}
