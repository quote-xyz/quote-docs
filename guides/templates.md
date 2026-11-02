---
description: Save how an order is worked (strategy, size, time in force, strategy settings) under a name and reuse it across orders.
---

# Order Templates

A template saves how an order is worked, never what it trades. It holds a strategy, a USD size, a time in force and the strategy's settings, but no market, side or price. You pick those each time.

## What a template holds

Every setting in a template is optional. A setting the template leaves out keeps whatever the order already has when you apply it.

Names are unique per wallet regardless of case, so saving under an existing name replaces that template. A wallet holds at most 12 templates.

Templates belong to your wallet. Nobody else can see or use yours.

## Using templates

Templates are a convenience for building orders: read a template, combine its settings with the market, side and price, and submit. A template never constrains what you can submit.

Templates are managed over the API. To save, list and delete them, see the [Templates endpoints](../api-reference/endpoints/templates.md), and to turn one into an order, see [Algo Orders](algo-orders.md).
