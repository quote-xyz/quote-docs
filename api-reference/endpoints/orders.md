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
