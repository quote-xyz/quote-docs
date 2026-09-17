---
description: 'Counterfactual multi-venue routing: what each venue would have been
  worth, and which venues you allow.'
---

# Routing

## What connecting each venue would have been worth

{% openapi src="../../.gitbook/assets/openapi.yaml" path="/api/routing/savings" method="get" %}
[openapi.yaml](../../.gitbook/assets/openapi.yaml)
{% endopenapi %}

## Which venues you allow routing to

{% openapi src="../../.gitbook/assets/openapi.yaml" path="/api/routing/venues" method="get" %}
[openapi.yaml](../../.gitbook/assets/openapi.yaml)
{% endopenapi %}

## Turn one venue on or off

{% openapi src="../../.gitbook/assets/openapi.yaml" path="/api/routing/venues/{venue}" method="put" %}
[openapi.yaml](../../.gitbook/assets/openapi.yaml)
{% endopenapi %}
