---
description: Order submission, cancellation, modification, and algo-order status.
---

# Orders

## Submit an order or algo strategy

{% openapi src="../../.gitbook/assets/openapi.yaml" path="/api/orders" method="post" %}
[openapi.yaml](../../.gitbook/assets/openapi.yaml)
{% endopenapi %}

## Cancel a single order

{% openapi src="../../.gitbook/assets/openapi.yaml" path="/api/orders/cancel" method="post" %}
[openapi.yaml](../../.gitbook/assets/openapi.yaml)
{% endopenapi %}

## Cancel all open orders

{% openapi src="../../.gitbook/assets/openapi.yaml" path="/api/orders/cancel-all" method="post" %}
[openapi.yaml](../../.gitbook/assets/openapi.yaml)
{% endopenapi %}

## Cancel a specific list of resting orders

{% openapi src="../../.gitbook/assets/openapi.yaml" path="/api/orders/cancel-batch" method="post" %}
[openapi.yaml](../../.gitbook/assets/openapi.yaml)
{% endopenapi %}

## Estimate what an order would cost

{% openapi src="../../.gitbook/assets/openapi.yaml" path="/api/orders/simulate" method="post" %}
[openapi.yaml](../../.gitbook/assets/openapi.yaml)
{% endopenapi %}

## Preview the parameters an urgency setting implies

{% openapi src="../../.gitbook/assets/openapi.yaml" path="/api/orders/urgency-preview" method="get" %}
[openapi.yaml](../../.gitbook/assets/openapi.yaml)
{% endopenapi %}

## List an algo order's child fills

{% openapi src="../../.gitbook/assets/openapi.yaml" path="/api/orders/algo/{order_id}/fills" method="get" %}
[openapi.yaml](../../.gitbook/assets/openapi.yaml)
{% endopenapi %}

## Replay an algo order's diagnostics

{% openapi src="../../.gitbook/assets/openapi.yaml" path="/api/orders/algo/{order_id}/diagnostics" method="get" %}
[openapi.yaml](../../.gitbook/assets/openapi.yaml)
{% endopenapi %}

## Speed up a running algo order

{% openapi src="../../.gitbook/assets/openapi.yaml" path="/api/orders/algo/{order_id}/speed-up" method="post" %}
[openapi.yaml](../../.gitbook/assets/openapi.yaml)
{% endopenapi %}

## Modify an existing order

{% openapi src="../../.gitbook/assets/openapi.yaml" path="/api/orders/modify" method="post" %}
[openapi.yaml](../../.gitbook/assets/openapi.yaml)
{% endopenapi %}

## List algo (strategy) orders

{% openapi src="../../.gitbook/assets/openapi.yaml" path="/api/orders/algo" method="get" %}
[openapi.yaml](../../.gitbook/assets/openapi.yaml)
{% endopenapi %}

## Get a single algo order

{% openapi src="../../.gitbook/assets/openapi.yaml" path="/api/orders/algo/{order_id}" method="get" %}
[openapi.yaml](../../.gitbook/assets/openapi.yaml)
{% endopenapi %}

## Resolve an order by its client order id

{% openapi src="../../.gitbook/assets/openapi.yaml" path="/api/orders/by-client-id/{client_order_id}" method="get" %}
[openapi.yaml](../../.gitbook/assets/openapi.yaml)
{% endopenapi %}
