# Security and Advanced Features

Quote operates to the highest standard of Security, and the core logic of the Quote's Execution Engine (QEE) algorithms includes advanced security features.

#### Order Price Protection

For specific algorithmic strategies, child orders sent to markets are governed by a Fair Price Model. This model computes aggressive and fair price benchmarks to ensure that orders crossing beyond fair value are restricted. These price limits are applied to both aggressive and resting orders to maintain execution quality.

#### Volatility Protection

To mitigate risk during extreme market swings, the Quote Execution Engine (QEE) converts Market orders into Limit orders. These orders are sent to HyperCore with a reasonable, configurable price leniency, providing a critical layer of protection against slippage.

#### Overfill Protection

The system actively monitors the relationship between parent and child orders to prevent excess exposure.

* **Safety Checks**\
  The QEE ensures child order exposure never exceeds the total requested size of the parent order.
* **Pending Request Logic**\
  If a child order remains pending past a timeout or a mid-execution disconnection occurs, the engine halts new activity until the pending status is resolved, effectively preventing overfill scenarios.

#### Order State Recovery

The QEE enters recovery mode following network errors, disconnects, or the detection of long-pending order states. Gateways automatically reconnect to target destinations to query for the latest fills and order statuses, synchronizing the parent and child order records.

> Note: This mechanism ensures all fills are booked to reduce overfill or mishedge risks. Any fill that cannot be mapped to a specific order is still recorded in the system for reconciliation and out-trade detection.

#### Runaway Algo & Duplicate Order Detection

The system employs high-frequency safeguards to maintain market and system stability:

* **Rate Limiting**\
  Both incoming and outgoing order rates are monitored. If a configured threshold is breached, new orders are blocked until the rate limit window resets.
* **Duplicate Detection**\
  The system checks for identical orders (Symbol, Side, Price, and Size). If the frequency of these identical orders exceeds the allowed rate within a specific window, they are blocked to prevent accidental order loops.

More information around the [security-and-advanced-features.md](security-and-advanced-features.md "mention") of the QEE can be found in the section below.
