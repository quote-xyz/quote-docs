---
description: Liveness and readiness probes, and API info.
---

# Health

## API/network info

{% openapi src="../../.gitbook/assets/openapi.yaml" path="/api/info" method="get" %}
[openapi.yaml](../../.gitbook/assets/openapi.yaml)
{% endopenapi %}

## Liveness probe

{% openapi src="../../.gitbook/assets/openapi.yaml" path="/health" method="get" %}
[openapi.yaml](../../.gitbook/assets/openapi.yaml)
{% endopenapi %}

## Readiness probe

{% openapi src="../../.gitbook/assets/openapi.yaml" path="/ready" method="get" %}
[openapi.yaml](../../.gitbook/assets/openapi.yaml)
{% endopenapi %}
