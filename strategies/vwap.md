---
description: >-
  Volume-proportional execution: slice sizes follow the asset's intraday volume
  profile instead of the clock.
---

# VWAP

<figure><img src="../.gitbook/assets/VWAP (1).gif" alt=""><figcaption></figcaption></figure>

**VWAP** works your order in step with how the market actually trades. Instead of equal time slices, each slice's size follows a volume profile built from the asset's own trading history: larger slices when the market is usually busy, smaller when it is quiet. Use it when your benchmark is the market VWAP over your window.

## Setting it up

Pick **VWAP** in the order type selector, then set:

| Setting | What it does |
| --- | --- |
| **Duration** | The window the order is scheduled across |
| **Execution** | One slider from **Lower impact** to **Faster fill**. It sets your volume cap and how willing the order is to cross the spread |
| Randomization | Click to cycle between **no**, **light** and **strong** randomization of slice size and timing |
| **Sweep any remainder at the end** | Off by default. When on, whatever is still unfilled when the window closes is filled by crossing the spread, instead of expiring |

#### Participation and the volume cap

The form shows two figures beside the slider:

* The **of volume** figure is the share of expected market volume your order needs, given its size and duration, to finish on schedule.
* The **cap** figure is the ceiling on your share of volume in any interval. The **Execution** slider sets it.

The engine does not raise the cap to make the deadline. If finishing in your window would need more than the cap allows, the form tells you before you submit: roughly what share fills in the window, and how much longer the rest would take. Give the order a longer duration, or move the slider towards **Faster fill**.

#### Impact against fill speed

<figure><img src="../.gitbook/assets/Screenshot 2026-08-08 at 3.37.31 pm.png" alt=""><figcaption></figcaption></figure>

The **Execution** slider moves the cap and the crossing behavior together:

* **Lower impact** (left end): the lowest volume cap and passive placement only. The order never crosses the spread. If the cap binds, it finishes late rather than taking liquidity.
* **Faster fill** (right end): the highest volume cap, and the order crosses the spread to hold its schedule.

Each slice still runs the standard [passive to aggressive cycle](overview.md#the-passive-aggressive-cycle), so you capture spread within the volume schedule.

<figure><img src="../.gitbook/assets/Quote Docs (2).png" alt=""><figcaption></figcaption></figure>

## Behavior notes

* **The profile is per asset.** Volume curves differ sharply between crypto majors, builder-DEX equities (which follow their home market's hours) and other markets. The engine builds each profile from the asset's own history.
* **It falls back gracefully.** If no usable profile exists for the asset, the order is scheduled evenly through the window rather than stalling. The order's page then shows its plan as uniform.
* **The sweep covers only the tail.** **Sweep any remainder at the end** fills what is left at the close. If the volume cap is what holds the order back, a longer duration or a higher setting is the fix.

To submit a VWAP over the API, see [Algo Orders](../guides/algo-orders.md#vwap).

## When to use something else

* The deadline matters more than tracking volume: [Passive TWAP](passive-twap.md) with **Guarantee completion**.
* You want to scale with live volume rather than the historical curve: [Percentage of Volume](participation-rate.md).
