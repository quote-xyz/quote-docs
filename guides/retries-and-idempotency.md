---
description: >-
  How to retry a submit safely: what clientOrderId guarantees on each order path,
  and how to tell whether a timed-out order landed.
---

# Retries and Idempotency

`POST /api/orders` is [async-accept](../concepts/order-lifecycle.md): a `200` means the engine accepted the order, not that it filled. So a timeout or a dropped connection leaves you in the worst state. The order may be live on Hyperliquid, or it may never have reached the engine, and the response that would have told you never arrived.

Retrying blind doubles your position. Send your own `clientOrderId` on every order instead. It is the only thing that makes a retry safe.

{% hint style="warning" %}
Without a `clientOrderId`, retries are **not** idempotent. Quote assigns an id internally so fills can be attributed, but each retry gets a fresh one, so each retry is a new order.
{% endhint %}

## What clientOrderId guarantees

The guarantee differs by order path, so read the one you use.

### Algo orders

Before the parent intent becomes durable, Quote reserves `(wallet, clientOrderId)`. A retry carrying the same id places nothing and returns `200` with the **original** `orderId`:

{% code title="Response to a duplicate submit" %}
```json
{
  "success": true,
  "orderId": "01HZX8QK7M4T2V9WB3YCEN6RPD",
  "status": "active",
  "provider": "quote",
  "warnings": ["duplicate clientOrderId: returning the existing order"]
}
```
{% endcode %}

Submission is at-most-once. The `warnings` entry is how you tell a replay from a first submit.

The reservation covers non-terminal orders only. Once an order reaches `completed`, `cancelled` or `failed`, the id is released and you may reuse it for a new order. Do not treat an id as claimed forever.

### Plain orders

Your id travels to Hyperliquid as the order's `cloid`. Hyperliquid rejects a second order carrying a cloid it has already seen, so a retry cannot double-fill.

The difference from the algo path matters: the retry **fails** rather than returning the original order. Quote does not special-case the venue's rejection, so it reaches you as an ordinary failed submission. Today you have to read the message to tell "this already landed" from "this was rejected on its merits".

## Choosing an id

Hyperliquid needs a 16-byte hex cloid, so Quote converts whatever you send:

| What you send | What reaches the venue |
| --- | --- |
| A UUID, such as `f81d4fae-7dec-11d0-a765-00a0c91e6bf6` | Dashes stripped, used exactly |
| `0x` followed by 32 hex characters | Used exactly |
| Any other string | Hashed down to 16 bytes |

Send a UUID or a `0x` hex string. Both map to the venue exactly, so the same id always produces the same cloid, which is what the whole guarantee rests on. An arbitrary string is hashed instead, and a hash is not a promise: two different ids can collide, and the mapping is not part of the contract.

Ids are stored up to 128 characters.

## Which failures to retry

Cross-reference the [error envelope](../api-reference/introduction.md#error-envelope) for the full status table. For retry decisions:

| Status | Did it take effect? | What to do |
| --- | --- | --- |
| `429` | No. A rate limit refused the request before it took effect | Pause, then resend with the same `clientOrderId` |
| `502`, `503`, or a client-side timeout | Unknown | Resend with the same `clientOrderId`, with backoff |
| `400`, `401`, `403`, `404` | No. Rejected before the venue saw it | Fix the request. Do not retry it unchanged |

## Confirming what happened

Two limits to plan around:

- The submit response does not echo `clientOrderId` back. Keep your own map from your id to the `orderId` you get.
- No endpoint looks an order up by `clientOrderId`. Lookups take the `orderId`.

So the retry itself is your most reliable probe. Resend with the same id and read the response: on an algo order you get the original `orderId` back, and on a plain order a rejection tells you the first one landed.

Once you hold an `orderId`, [`GET /api/orders/algo/{order_id}`](algo-orders.md) reports an algo order's status and filled quantity. For a plain order, Hyperliquid remains the source of truth for its resting state and fills.

## Putting it together

{% stepper %}
{% step %}
#### Mint an id before you submit

Generate a UUID and store it against whatever your system calls this order. Do this before the request, not after: an id you generate on the retry path is useless.
{% endstep %}

{% step %}
#### Submit with it

Send it as `clientOrderId` on `POST /api/orders`.
{% endstep %}

{% step %}
#### On an ambiguous failure, resend the same id

Timeouts, `502` and `503` are ambiguous. Resend the identical body, including the identical `clientOrderId`, after a backoff.
{% endstep %}

{% step %}
#### Read the response, do not poll

An algo order returns its original `orderId` with a `duplicate clientOrderId` warning. A plain order fails because the venue already holds that cloid. Either answer tells you the first attempt landed, without waiting on a reconciliation window.
{% endstep %}
{% endstepper %}
