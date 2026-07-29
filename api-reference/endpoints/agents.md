---
description: Agent wallet lifecycle (create, register, builder-fee approval, terms).
---

# Agents

## Create an agent wallet

{% openapi src="../openapi.yaml" path="/api/agents" method="post" %}
[openapi.yaml](../openapi.yaml)
{% endopenapi %}

## Get the caller's agent wallet

{% openapi src="../openapi.yaml" path="/api/agents" method="get" %}
[openapi.yaml](../openapi.yaml)
{% endopenapi %}

## Register an agent wallet with Hyperliquid

{% openapi src="../openapi.yaml" path="/api/agents/register" method="post" %}
[openapi.yaml](../openapi.yaml)
{% endopenapi %}

## Record builder-fee approval

{% openapi src="../openapi.yaml" path="/api/agents/builder-approval" method="post" %}
[openapi.yaml](../openapi.yaml)
{% endopenapi %}

## Accept terms of service

{% openapi src="../openapi.yaml" path="/api/agents/accept-terms" method="post" %}
[openapi.yaml](../openapi.yaml)
{% endopenapi %}
