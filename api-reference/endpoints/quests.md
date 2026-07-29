---
description: Tiered new-user quest progress and the favorite-quote submission.
---

# Quests

## Quest and badge progress

{% openapi src="../openapi.yaml" path="/api/quests" method="get" %}
[openapi.yaml](../openapi.yaml)
{% endopenapi %}

## Submit a favorite quote

{% openapi src="../openapi.yaml" path="/api/quests/quote" method="post" %}
[openapi.yaml](../openapi.yaml)
{% endopenapi %}

## Acknowledge a badge unlock

{% openapi src="../openapi.yaml" path="/api/quests/badges/{key}/seen" method="post" %}
[openapi.yaml](../openapi.yaml)
{% endopenapi %}
