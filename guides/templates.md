---
description: Save how an order is worked (strategy, size, time in force, strategy settings) under a name and reuse it across orders.
---

# Order Templates

A template saves how an order is worked, never what it trades. It holds a strategy, a USD size, a time in force and the strategy's settings, but no market, side or price. You pick those each time.

## Save

{% code title="POST /api/templates" %}
```json
{
  "name": "Patient accumulator",
  "ticket": {
    "strategy": "twap",
    "amountUsd": "5000",
    "durationSecs": 3600,
    "priceProtection": true
  }
}
```
{% endcode %}

The ticket uses the terminal's order-ticket names (`twap`, `vwap`, `pov`, `iceberg`, `chase`, and so on), not the order API's strategy names, so map them when you build an order. Every `ticket` field is optional. A field you leave out keeps whatever the order already has when you apply the template. Unknown fields are ignored.

Names are unique per wallet regardless of case, so saving under an existing name replaces that template. A wallet holds at most 12 templates; saving a thirteenth name returns `409`.

## List and delete

```bash
GET    /api/templates                 # list yours, oldest first
DELETE /api/templates/{template_id}
```

Scopes: `templates:read` for the list, `templates:write` to save or delete. Templates are [wallet-scoped](../concepts/wallet-scoped-api.md); another wallet's template UUID is a `404` to you.

## Using a template

Templates are a client-side convenience: read the template, carry its `ticket` settings into the [order submission](algo-orders.md) along with the market, side and price, and send. The order API takes explicit fields (there is no `templateId` on `POST /api/orders`), so a template never constrains what you can submit.
