# Execution Parameters and Backend Intelligence

The Quote Execution Engine is designed for trading optimization by managing market impact, capturing passive liquidity, and providing protection against predatory market participants.

When trading on the Quote UI or Traders API, traders submit an order similar to a traditional perp-dex, with some differences around additional data points.

#### Urgency

The Urgency parameter determines how aggressively the system interacts with market liquidity. It dictates the size of orders posted to the book and the speed at which the system seeks a fill.



## Backend intelligence

#### Adaptive Volume Tracking

The system monitors real-time market volume and historical moving averages to blend orders into the book. This minimizes information leakage by ensuring the execution footprint remains consistent with organic market activity.

#### Dynamic Order Placement

A passive-only strategy that monitors and tracks bids (for buy orders) or offers (for sell orders) across multiple venues. It dynamically adjusts placement across various price levels within the order books to optimize capture.

#### Enhanced Fill Probability

By distributing orders across several price layers simultaneously, this strategy increases the likelihood of execution. The distribution is calibrated based on specific urgency requirements and available liquidity.

#### Segmented Execution

Large parent orders are partitioned into smaller "clips." These clips are then executed at precise, recurring time intervals to maintain a steady market presence without triggering volatility.

#### Anti-Gaming Protection

All executions have an option to utilize logic models to randomize order schedules and sizes. This protects from front-running.

#### Smart Overfill Protection

The system monitors all child orders in real-time to prevent over-execution. This safeguard remains active even during venue disconnections or technical timeouts, ensuring the total filled quantity never exceeds the parent order limit.

#### Automated Error Handling

To ensure execution consistency, the algorithms automatically regenerate child orders if a clip encounters errors or fails to fill within its allotted interval, maintaining the integrity of the execution schedule.

#### Non-Accelerated Pacing Optionality

If market conditions move outside your limit price, the strategy remains disciplined. It will not increase aggressiveness to "catch up" on lost time, ensuring you trade only at your desired levels and avoid price chasing.

#### Order Randomization

Users can apply a Variance setting to randomize clip sizes. This further helps blend execution activity into overall market volume, making it harder for external observers to detect a large parent order in progress.

More information around the [security-and-advanced-features.md](security-and-advanced-features.md "mention") of the QEE can be found in the section above.

