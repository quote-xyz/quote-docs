---
description: The guarantees the execution engine holds while it works your order.
---

# Execution Safeguards

Every strategy runs under the same set of protections. This page states what they guarantee, not how they are implemented: the mechanics are deliberately undocumented, because publishing them would help others detect and trade against your orders.

## Price protection

Child orders are bounded by a fair-price benchmark, so the engine will not cross far beyond fair value to fill you. The bound applies to aggressive and resting orders alike.

Market orders get a second layer. In fast markets they are converted to limit orders carrying a price allowance, so a violent move cannot fill you at an arbitrary price. This is also why `orderType: "market"` still requires a `limitPrice`, as described in [Hyperliquid Constraints](../concepts/hyperliquid-constraints.md#market-orders-are-ioc-limits-with-a-slippage-bound).

## Overfill protection

Total child exposure never exceeds the size of the parent order.

The guarantee holds through failure, which is the part that matters. If a child order's status is unresolved, because it is pending past a timeout or the connection dropped mid-execution, the engine stops opening new exposure until it knows the outcome. It will finish late rather than fill you twice.

## Recovery

The engine reconciles against the venue after a disconnect or restart, retrieving the true fill and order state rather than trusting its own last-known view. Fills that cannot be matched to a known order are still recorded, so nothing is silently dropped.

[Order Lifecycle](../concepts/order-lifecycle.md) covers what this means for you: the venue is the source of truth, and a strategy reaches a terminal state only when its own logic and the venue agree.

## Runaway and duplicate protection

Order rates are monitored in both directions. If a configured threshold is breached, new orders are blocked until the window resets. Identical orders repeated at high frequency, matching on symbol, side, price, and size, are blocked in the same way.

These exist to stop a client bug or an accidental loop from turning into real exposure.

## Privacy

Resting orders stay inside the engine until the moment they are placed on HyperCore, so a parent order is never displayed in full. Strategies vary their schedule and sizing to avoid presenting a repeating pattern.

The [Iceberg](iceberg.md) strategy makes concealment its primary objective. The specifics of how any of it varies are not published, for the reason given at the top of this page.
