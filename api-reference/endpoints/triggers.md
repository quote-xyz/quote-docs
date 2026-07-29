---
description: Conditional triggers (CRUD + history).
---

# Triggers

## List conditional triggers

{% openapi src="../openapi.yaml" path="/api/triggers" method="get" %}
[openapi.yaml](../openapi.yaml)
{% endopenapi %}

## Create a conditional trigger

{% openapi src="../openapi.yaml" path="/api/triggers" method="post" %}
[openapi.yaml](../openapi.yaml)
{% endopenapi %}

## Get a trigger

{% openapi src="../openapi.yaml" path="/api/triggers/{trigger_id}" method="get" %}
[openapi.yaml](../openapi.yaml)
{% endopenapi %}

## Cancel a trigger

{% openapi src="../openapi.yaml" path="/api/triggers/{trigger_id}" method="delete" %}
[openapi.yaml](../openapi.yaml)
{% endopenapi %}

## Get trigger history

{% openapi src="../openapi.yaml" path="/api/triggers/{trigger_id}/history" method="get" %}
[openapi.yaml](../openapi.yaml)
{% endopenapi %}
