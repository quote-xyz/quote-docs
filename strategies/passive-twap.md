---
description: >-
  Time-sliced execution that rests passively at the touch and falls back to
  aggressive orders to stay on schedule. Guaranteed completion.
---

# Passive TWAP

<figure><img src="../.gitbook/assets/Brave Browser.gif" alt=""><figcaption></figcaption></figure>

`passive_twap` splits your order into equal slices over a fixed window. Each slice first rests as a post-only (ALO) order at the best bid/offer, capturing the spread and earning maker fees. If a slice has not filled by its deadline, it converts to an aggressive IOC order. The result is TWAP scheduling at better prices than naive market-order slicing, with completion by end of window when `guaranteedCompletion` is set.

<figure><img src="../.gitbook/assets/Quote Docs (1).png" alt=""><figcaption><p>Passive TWAP: equal slices across the window.</p></figcaption></figure>

## Example

{% code title="POST /api/orders" %}
```json
{
  "symbol": "ETH",
  "side": "buy",
  "size": "2.5",
  "orderType": "limit",
  "strategy": "passive_twap",
  "params": {
    "durationSecs": 1800,
    "numSlices": 30,
    "passivePct": 80,
    "guaranteedCompletion": true
  }
}
```
{% endcode %}

This works 2.5 ETH over 30 minutes in 30 slices, spending 80% of each minute resting passively before taking liquidity.

## Parameters

<table><thead><tr><th width="217.578125">Parameter</th><th>Type</th><th width="139.3515625">Default</th><th>Description</th></tr></thead><tbody><tr><td><code>durationSecs</code></td><td>integer</td><td><code>300</code></td><td>Total execution window in seconds</td></tr><tr><td><code>numSlices</code></td><td>integer</td><td><code>10</code></td><td>Number of equal child slices</td></tr><tr><td><code>passivePct</code></td><td>integer 0–100</td><td><code>80</code></td><td>Percent of each slice interval spent resting passively before the IOC fallback</td></tr><tr><td><code>limitOffsetBps</code></td><td>decimal</td><td><code>0</code></td><td>Offset from the touch for passive placement (0 = at BBO)</td></tr><tr><td><code>randomize</code></td><td>boolean</td><td><code>false</code></td><td>Jitter slice timing/sizing to avoid a detectable cadence</td></tr><tr><td><code>minSpreadBps</code></td><td>decimal</td><td>none</td><td>Skip passive placement when the spread is tighter than this (go straight to schedule)</td></tr><tr><td><code>guaranteedCompletion</code></td><td>boolean</td><td><code>false</code></td><td>Sweep all remaining size with one wide-tolerance IOC at the end of the window</td></tr><tr><td><code>completionSlippageBps</code></td><td>decimal</td><td><code>100</code></td><td>Slippage tolerance for the guaranteed-completion sweep</td></tr><tr><td><code>reduceOnly</code></td><td>boolean</td><td><code>false</code></td><td>Children only reduce an existing position</td></tr><tr><td><code>attachedTpsl</code></td><td>object</td><td>none</td><td>Attach TP/SL to the resulting position</td></tr></tbody></table>

How passive orders are placed, repriced, and converted is managed by the engine and varies with market conditions; those mechanics are deliberately not specified here.

## Behavior notes

* **Slice sizing vs. the $10 minimum.** Slices below Hyperliquid's \~$10 minimum notional are skipped. Choose `numSlices` so each slice clears the minimum comfortably; see [Hyperliquid constraints](../concepts/hyperliquid-constraints.md#minimum-order-notional-10).
* **Behind schedule?** If passive fills lag, the aggressive fallback per slice keeps the schedule. With `guaranteedCompletion`, any final remainder is swept at window end within `completionSlippageBps`.
* **Restart-safe.** Slice state is reconstructed on engine restart; resting children are recovered from the venue rather than duplicated.

## When to use something else

* You're benchmarked to volume, not time → [VWAP](vwap.md).
* No deadline, and hiding size matters most → [Iceberg](iceberg.md).
