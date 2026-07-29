# Algorithmic Execution Suite

The Quote Execution Engine (QEE) offers five order types, representing the first order types introduced by the Quote team. All trading processed through the QEE benefits from [security-and-advanced-features.md](../security-and-advanced-features.md "mention") and [execution-parameters-and-backend-intelligence.md](../execution-parameters-and-backend-intelligence.md "mention"), which enhances and protects users' trades flowing through Quote.&#x20;

***

## Strategies

<div data-full-width="true"><figure><img src="../../.gitbook/assets/Screenshot 2026-04-06 at 3.29.51 pm.png" alt=""><figcaption></figcaption></figure></div>

### Chase

<div data-full-width="true"><figure><img src="../../.gitbook/assets/Screenshot 2026-04-06 at 3.39.24 pm.png" alt="" width="375"><figcaption></figcaption></figure></div>

<details>

<summary>Strategy</summary>

Chase is a passive limit order that reprices progressively tighter toward the market on each attempt, with an optional escalation to cross the spread via IOC if it doesn't fill within the time/attempt limit. With escalation toggled off, it behaves as a pegged order that tracks the BBO.

</details>

<details>

<summary>Objectives</summary>

* Minimize market impact
* Track the market average
* Minimize fees

</details>

<details>

<summary>Order placement strategy</summary>

Places orders at the BBO and adjusts based on market movements.

</details>



### Quote TWAP

<figure><img src="../../.gitbook/assets/Screenshot 2026-04-06 at 3.42.47 pm.png" alt="" width="375"><figcaption></figcaption></figure>

<details>

<summary>Strategy</summary>

Splits the order into equally-timed slices across a defined window, executing each slice\
passively before falling back to aggressive if the passive window expires unfilled. Slice\
distribution can be shaped (even, front-loaded, back-loaded, or measured) and timing optionally randomized to reduce detectability.

</details>

<details>

<summary>Objectives</summary>

* Minimize market impact
* Minimize paying spread
* Minimize fees

</details>

<details>

<summary>Order placement strategy</summary>

Posts passive ALO per slice at best bid/ask. If unfilled within the passive window, crosses the spread via IOC. Slice timing can be shaped (even, early, late, measured).

</details>



### VWAP

<figure><img src="../../.gitbook/assets/Screenshot 2026-04-06 at 3.45.15 pm.png" alt="" width="375"><figcaption></figcaption></figure>

<details>

<summary>Strategy</summary>

Distributes execution proportionally to a predicted intraday volume curve, concentrating slices in high-volume periods and thinning them in low-volume ones to converge on the volume-weighted average price. Volume prediction is model-driven with slice sizes rebalanced as actual volume deviates from\
forecast.

</details>

<details>

<summary>Objectives</summary>

* Minimize market impact
* Follow the market benchmark
* Minimize fees

</details>

<details>

<summary>Order placement strategy</summary>

Uses a volume prediction model to size and time each slice. Passive-first per slice with aggressive fallback. Slice sizes adapt to predicted vs actual volume.

</details>



### Percent of Volume (Participation Rate)

<figure><img src="../../.gitbook/assets/Screenshot 2026-04-06 at 3.50.04 pm.png" alt="" width="375"><figcaption></figcaption></figure>

<details>

<summary>Strategy</summary>

Paces execution to maintain a fixed target percentage of real-time market volume,\
emitting clips only when filled quantity falls below the target ratio. Increases size when volume surges/pauses when volume dries up, keeping a consistent/low-profile market footprint throughout the window.

</details>

<details>

<summary>Objectives</summary>

* Minimize market impact with proportional execution
* Track market average with dynamic pacing and adaptiveness
* Minimize information leakage by maintaining a low-profile footprint
* Manage execution risk

</details>

<details>

<summary>Order placement strategy</summary>

Monitors cumulative market volume and emits clips only when filled quantity falls below target participation rate. Passive-first with optional aggressive fallback per clip.

</details>



### Iceberg

<figure><img src="../../.gitbook/assets/Screenshot 2026-04-06 at 3.53.49 pm.png" alt="" width="375"><figcaption></figcaption></figure>

<details>

<summary>Strategy</summary>

Hides total order size by exposing only a fractional display quantity in the order book, automatically replacing each filled clip until the full order is executed. Clip sizes, replenishment timing, and repost delays can be randomized to prevent pattern detection by other market participants.

</details>

<details>

<summary>Objective</summary>

* Minimize market impact preventing slippage
* Avoid front-running by hiding the full order size
* Maintain price stability
* Minimize fees

</details>

<details>

<summary>Order placement strategy</summary>

Posts a single limit order at the display size. Reposts next clip after\
randomized delay on fill. Reprices if market drifts beyond threshold.

</details>

***

### General design principles

The algorithmic strategies in the QEE have been designed to help traders achieve specific goals:

* Minimizing market impact by breaking down large orders into smaller orders over time, adapting to volume
* Maximizing liquidity capture by utilizing multi-level passive limit orders and sweeping available orders at best prices (fee inclusive)
* Executing trades at specific times or prices, and adapting to changing market conditions
* Protecting standing orders from public view on HyperCore
