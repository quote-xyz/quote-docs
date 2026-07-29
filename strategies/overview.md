---
description: Five execution algorithms, how to choose between them, and the mechanics they share.
---

# Strategies Overview

Quote's execution engine runs five strategies. You select one by setting `strategy` on [`POST /api/orders`](../guides/algo-orders.md) and tuning it via `params`.

| Strategy | `strategy` value | Best for |
|---|---|---|
| [Passive TWAP](passive-twap.md) | `passive_twap` | Time-sliced execution with guaranteed completion |
| [VWAP](vwap.md) | `vwap` | Tracking the market's volume profile over a window |
| [Iceberg](iceberg.md) | `iceberg` | Hiding large size; pure-passive, no deadline |
| [Participation Rate](participation-rate.md) | `participation_rate` | Staying a fixed % of real-time market volume |
| [Chase Limit](chase-limit.md) | `chase_limit` | A limit order that follows the BBO within a bound |

<figure><img src="../.gitbook/assets/Screenshot 2026-04-06 at 3.29.51 pm.png" alt=""><figcaption><p>The five strategies at a glance.</p></figcaption></figure>

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

Time-sliced strategies share one principle: rest passively first, take liquidity only when the schedule demands it. Passive child orders sit on the book earning the spread and maker fees; if a slice falls behind, the engine takes liquidity to keep the order on schedule.

The `passivePct` parameter sets the balance: higher values wait longer for passive fills before taking liquidity; lower values trade cost for completion certainty.

How and when child orders are placed, repriced, and converted is managed by the engine and adapts to market conditions. Those mechanics are deliberately not documented: publishing them would help others detect and trade against your orders.

### Common parameters

These appear across multiple strategies (all optional; camelCase and snake_case are both accepted):

| Parameter | Type | Meaning |
|---|---|---|
| `durationSecs` | integer | Total execution window |
| `numSlices` | integer | Number of child slices |
| `passivePct` | integer 0–100 | Portion of each slice spent passive before going aggressive |
| `randomize` | boolean | Jitter slice timing and sizing to avoid detectable patterns |
| `reduceOnly` | boolean | Children only reduce an existing position |
| `guaranteedCompletion` | boolean | Sweep any remainder with a wide-tolerance IOC at the end |
| `attachedTpsl` | object | Attach take-profit/stop-loss to the resulting position |

Per-strategy pages document the full parameter set with defaults.

### Execution benchmarks

Every strategy execution is measured against three benchmarks (see [Analytics](../guides/analytics.md)):

- **vs. arrival price**: the mid when your parent order started (implementation shortfall).
- **vs. market VWAP**: all market trades during your execution window.
- **vs. market order**: a simulated aggressive sweep of the book at each fill time. This is the most actionable benchmark: it measures the spread you captured compared with sweeping the book.

All benchmark values are signed basis points with the convention **positive = worse, negative = better**.

{% hint style="info" %}
Strategies are a closed, curated set, and every one runs under the same [execution safeguards](safeguards.md): price bounds, overfill protection, and recovery that survives an engine restart.
{% endhint %}
