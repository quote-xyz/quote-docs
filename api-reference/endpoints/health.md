---
description: Liveness/readiness probes, info, and Prometheus metrics.
---

# Health

## API/network info

{% openapi src="../openapi.yaml" path="/api/info" method="get" %}
[openapi.yaml](../openapi.yaml)
{% endopenapi %}

## Liveness probe

{% openapi src="../openapi.yaml" path="/health" method="get" %}
[openapi.yaml](../openapi.yaml)
{% endopenapi %}

## Readiness probe

{% openapi src="../openapi.yaml" path="/ready" method="get" %}
[openapi.yaml](../openapi.yaml)
{% endopenapi %}

## Prometheus metrics

{% openapi src="../openapi.yaml" path="/metrics" method="get" %}
[openapi.yaml](../openapi.yaml)
{% endopenapi %}
