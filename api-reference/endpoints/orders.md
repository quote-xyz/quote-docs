---
description: Order submission, cancellation, modification, and algo-order status.
---

# Orders

## Submit an order or algo strategy

{% openapi src="../openapi.yaml" path="/api/orders" method="post" %}
[openapi.yaml](../openapi.yaml)
{% endopenapi %}

## Cancel a single order

{% openapi src="../openapi.yaml" path="/api/orders/cancel" method="post" %}
[openapi.yaml](../openapi.yaml)
{% endopenapi %}

## Cancel all open orders

{% openapi src="../openapi.yaml" path="/api/orders/cancel-all" method="post" %}
[openapi.yaml](../openapi.yaml)
{% endopenapi %}

## Modify an existing order

{% openapi src="../openapi.yaml" path="/api/orders/modify" method="post" %}
[openapi.yaml](../openapi.yaml)
{% endopenapi %}

## List algo (strategy) orders

{% openapi src="../openapi.yaml" path="/api/orders/algo" method="get" %}
[openapi.yaml](../openapi.yaml)
{% endopenapi %}

## Get a single algo order

{% openapi src="../openapi.yaml" path="/api/orders/algo/{order_id}" method="get" %}
[openapi.yaml](../openapi.yaml)
{% endopenapi %}

## List an algo order's fills

{% openapi src="../openapi.yaml" path="/api/orders/algo/{order_id}/fills" method="get" %}
[openapi.yaml](../openapi.yaml)
{% endopenapi %}

## Speed up a running algo order

{% openapi src="../openapi.yaml" path="/api/orders/algo/{order_id}/speed-up" method="post" %}
[openapi.yaml](../openapi.yaml)
{% endopenapi %}

## Cancel a list of orders

{% openapi src="../openapi.yaml" path="/api/orders/cancel-batch" method="post" %}
[openapi.yaml](../openapi.yaml)
{% endopenapi %}

## Estimate what an order would cost

{% openapi src="../openapi.yaml" path="/api/orders/simulate" method="post" %}
[openapi.yaml](../openapi.yaml)
{% endopenapi %}

## Preview what an urgency setting will do

{% openapi src="../openapi.yaml" path="/api/orders/urgency-preview" method="get" %}
[openapi.yaml](../openapi.yaml)
{% endopenapi %}

## List executable strategies

{% openapi src="../openapi.yaml" path="/api/strategies" method="get" %}
[openapi.yaml](../openapi.yaml)
{% endopenapi %}
