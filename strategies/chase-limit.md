---
description: >-
  A limit order that follows the best bid/offer within a hard time and attempt
  budget.
---

# Chase Limit

<figure><img src="../.gitbook/assets/Chase.gif" alt=""><figcaption></figcaption></figure>

`chase_limit` is for when you want **to fill near the touch soon**, without paying the full spread of a market order. It places a limit order near the BBO and follows the market as it moves, converging toward the touch until the order fills or the attempt/time budget runs out.

It is a patient version of a marketable limit: it chases price moves, but only within bounds you set.

<figure><img src="../.gitbook/assets/Quote Docs (5).png" alt=""><figcaption></figcaption></figure>

## Example

{% code title="POST /api/orders" %}
```json
{
  "symbol": "BTC",
  "side": "buy",
  "size": "0.1",
  "orderType": "limit",
  "strategy": "chase_limit",
  "params": {
    "maxAttempts": 8,
    "maxTotalSecs": 30
  }
}
```
{% endcode %}

This chases for at most 8 attempts or 30 seconds, whichever comes first.

## Parameters

| Parameter          | Type    | Default        | Description                                           |
| ------------------ | ------- | -------------- | ----------------------------------------------------- |
| `maxAttempts`      | integer | `8`            | Maximum number of placements/re-pegs                  |
| `maxTotalSecs`     | integer | `30`           | Hard wall-clock budget for the whole chase            |
| `initialOffsetBps` | decimal | server default | Starting offset behind the touch                      |
| `minOffsetBps`     | decimal | `0`            | Floor for the offset (0 = allowed to reach the touch) |
| `reduceOnly`       | boolean | `false`        | Only reduce an existing position                      |

The re-peg cadence and how quickly the chase converges toward the touch are managed by the engine and vary with market conditions; they are deliberately not specified here.

## Behavior notes

* **It can miss.** If price runs away faster than the chase converges, the strategy ends `completed`-with-partial or unfilled at the budget limit. Check `filledQty`. If you need certainty, use a market order with a slippage bound (see [placing orders](../guides/placing-orders.md#market-orders)); chase limit is the _cheaper but not guaranteed_ alternative.
* **Best on liquid books.** On thin books, each re-peg competes with a moving, sparse touch. Consider a wider `initialOffsetBps` or a different strategy.
* Good default for "get me in around here" order entry from a bot: bounded latency, bounded slippage, no spread crossing unless the chase converges to the touch.

## When to use something else

* Larger size to work over time → [Passive TWAP](passive-twap.md).
* Must fill _now_ whatever the cost → plain market order with a slippage-bounded `limitPrice`.
