---
description: Execution-quality, volume, and fee analytics.
---

# Analytics

## List trade intents

{% openapi src="../openapi.yaml" path="/api/trade-intents" method="get" %}
[openapi.yaml](../openapi.yaml)
{% endopenapi %}

## Get a trade intent's execution report

{% openapi src="../openapi.yaml" path="/api/trade-intents/{id}" method="get" %}
[openapi.yaml](../openapi.yaml)
{% endopenapi %}

## Execution-quality metrics

{% openapi src="../openapi.yaml" path="/api/analytics/execution" method="get" %}
[openapi.yaml](../openapi.yaml)
{% endopenapi %}

## Execution-quality timeline

{% openapi src="../openapi.yaml" path="/api/analytics/execution/timeline" method="get" %}
[openapi.yaml](../openapi.yaml)
{% endopenapi %}

## Quote-routed volume

{% openapi src="../openapi.yaml" path="/api/analytics/volume" method="get" %}
[openapi.yaml](../openapi.yaml)
{% endopenapi %}

## Quote-routed fees

{% openapi src="../openapi.yaml" path="/api/analytics/fees" method="get" %}
[openapi.yaml](../openapi.yaml)
{% endopenapi %}

## Fee stack

{% openapi src="../openapi.yaml" path="/api/fees/summary" method="get" %}
[openapi.yaml](../openapi.yaml)
{% endopenapi %}
