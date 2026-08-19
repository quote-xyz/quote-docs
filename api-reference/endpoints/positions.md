---
description: Leverage, margin, and spot/perp transfer actions.
---

# Positions

## Set the account margin mode

{% openapi src="../../.gitbook/assets/openapi.yaml" path="/api/account/mode" method="post" %}
[openapi.yaml](../../.gitbook/assets/openapi.yaml)
{% endopenapi %}

## Attach take-profit and stop-loss to a position

{% openapi src="../../.gitbook/assets/openapi.yaml" path="/api/positions/tpsl" method="post" %}
[openapi.yaml](../../.gitbook/assets/openapi.yaml)
{% endopenapi %}

## Update leverage

{% openapi src="../../.gitbook/assets/openapi.yaml" path="/api/positions/leverage" method="post" %}
[openapi.yaml](../../.gitbook/assets/openapi.yaml)
{% endopenapi %}

## Update isolated margin

{% openapi src="../../.gitbook/assets/openapi.yaml" path="/api/positions/margin" method="post" %}
[openapi.yaml](../../.gitbook/assets/openapi.yaml)
{% endopenapi %}

## Transfer between spot and perp

{% openapi src="../../.gitbook/assets/openapi.yaml" path="/api/positions/transfer" method="post" %}
[openapi.yaml](../../.gitbook/assets/openapi.yaml)
{% endopenapi %}
