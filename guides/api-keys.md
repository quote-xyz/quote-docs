---
description: Mint, scope, rotate, and revoke HMAC API keys for programmatic trading.
---

# API Keys

API keys give bots and scripts scoped access to your account. They authenticate with HMAC-SHA256 request signing; see [Authentication](../authentication.md#hmac-api-keys) for the signing mechanics.

{% hint style="info" %}
Key management is **Privy-session only**: you mint, list, and revoke keys from a logged-in terminal session. An API key can never mint another API key, so a leaked key cannot escalate itself.
{% endhint %}

## Minting a key

In the terminal, open **Connections** from the account menu and click **Create API key** under **API keys**. Over the API, mint with a Privy session token:

```bash
POST /api/keys
Authorization: Bearer <privy-jwt>

{
  "name": "execution-bot",
  "scopes": ["orders:read", "orders:write", "agents:read"],
  "expiresInDays": 90
}
```

{% code title="Response" %}
```json
{
  "keyId": "qk_a1b2c3…",
  "secret": "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"
}
```
{% endcode %}

{% hint style="warning" %}
The `secret` (a 32-byte hex value used directly as your HMAC-SHA256 signing key) is returned **once**. It is not stored recoverably and cannot be retrieved again. If you lose it, revoke the key and mint a new one.
{% endhint %}

### Choosing scopes

Grant the minimum the client needs (see the [scope table](../authentication.md#scopes)). Typical setups:

| Use case | Scopes |
|---|---|
| Read-only dashboard / monitoring | `orders:read` |
| Trading bot | `orders:read`, `orders:write`, `agents:read` |
| Full account automation | add `positions:write`, `templates:read`, `templates:write` |

`expiresInDays` is optional, from 1 to 365. Omit it for a non-expiring key (you can still revoke it anytime).

`ipAllowlist` optionally restricts the key to up to 32 IP addresses or CIDR blocks (IPv4 or IPv6). A request signed with the key from any other IP is rejected with `403`. Omit it, or send an empty array, to allow any IP.

Minting requires the terms of service to have been accepted in the terminal (`403` otherwise). A wallet holds at most 10 unrevoked, unexpired keys; past that, minting returns `422` with `code` `api_key_limit`, so revoke one first.

## Listing keys

```bash
GET /api/keys
```

Returns each key's `key_id`, `name`, a `secret_preview` (never the full secret), `scopes`, `created_at`, `last_used_at`, `expires_at`, and `revoked_at`. Use `last_used_at` to find dead keys worth revoking.

## Revoking a key

```bash
DELETE /api/keys/{key_id}
```

Returns `204`. Revocation is immediate: in-flight requests signed with the key will fail.

## Operational tips

- **Rotate by overlap.** Mint the replacement key, deploy it, then revoke the old one. No downtime.
- **One key per deployment.** Separate keys per bot/environment make `last_used_at` meaningful and blast radius small.
- **Clock discipline.** Signatures embed a millisecond timestamp with a 30-second tolerance; run NTP on anything that signs requests.
- **What a leaked key can't do:** withdraw funds (the [agent wallet](../concepts/agent-wallets.md) can't withdraw), manage keys or invites (Privy-only), or act beyond its scopes. It can still trade within its scopes, so revoke a leaked key immediately.
