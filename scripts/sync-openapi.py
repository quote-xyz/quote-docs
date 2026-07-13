#!/usr/bin/env python3
"""Sync the public Trader API reference spec from quote-backend.

The backend spec (quote-backend/docs/openapi.yaml) documents the full API and
is the source of truth. The public reference is curated:

- Non-trading surfaces are excluded (Quentin/NL-order, the Parallel news
  pipeline, the daily quote).
- The MCP connector endpoints are excluded; the docs site's MCP tab covers
  them.
- The Relay bridge proxy is excluded.
- The reference is API-key only. Privy is a terminal-internal credential, so
  the PrivyBearer scheme, the terminal-session-only endpoints (API-key
  management, invites and referrals), and every mention of Privy are removed.

This script owns those rules so re-syncing never reintroduces anything.

Usage:
    scripts/sync-openapi.py [path-to-backend-spec]
    # default: ../quote-backend/docs/openapi.yaml
"""

import sys
from pathlib import Path

import yaml

EXCLUDED_PATHS = [
    # Non-trading surfaces
    "/api/nl-order",
    "/api/nl-order-dev",
    "/api/news",
    "/api/webhooks/parallel",
    "/api/quotes/daily",
    # MCP connector (documented in the MCP tab)
    "/mcp",
    "/.well-known/oauth-protected-resource",
    "/.well-known/oauth-authorization-server",
    "/oauth/register",
    "/oauth/authorize",
    "/oauth/token",
    "/api/mcp/tools",
    "/api/mcp/guide",
    "/api/mcp/dispatch",
    # Bridge proxy
    "/api/bridge/quote",
    # Terminal-session (Privy) only; not callable with an API key
    "/api/keys",
    "/api/keys/{key_id}",
    "/api/invites",
    "/api/invites/redeem",
    "/api/invites/status",
    "/api/referrals/summary",
]
EXCLUDED_TAGS = [
    "NL Order",
    "News",
    "MCP Connector",
    "Bridge",
    "API Keys",
    "Invites & Referrals",
]
EXCLUDED_SCHEMAS = [
    "NLChatMessage",
    "NLPositionContext",
    "NLOrderContextEntry",
    "NLFillContextEntry",
    "NLOrderHistoryEntry",
    "NLOrderContext",
    "NLOrderRequest",
    "Article",
    "ArticleMarket",
    "WebhookPayload",
    "QuoteInfo",
    "DailyQuoteResponse",
    "MintKeyRequest",
    "MintKeyResponse",
    "ApiKeyRow",
    "ListKeysResponse",
    "InviteCodeView",
    "ListInvitesResponse",
    "IssueInviteResponse",
    "RedeemRequest",
    "RedeemResponse",
    "InviteStatusResponse",
    "ReferralSummaryResponse",
]

# Prose fixups for the top-level description (which otherwise references
# excluded endpoints or the terminal-internal Privy credential).
DESCRIPTION_REPLACEMENTS = [
    (
        "There are two ways to authenticate, both of which converge on the same\n"
        "`wallet_address`:\n"
        "\n"
        "1. **Privy identity token** (`PrivyBearer`), used by the frontend. A Privy\n"
        "   JWT in `Authorization: Bearer <jwt>`, verified offline against Privy's\n"
        "   JWKS endpoint. The embedded EVM wallet is read from the\n"
        "   `linked_accounts` claim. Privy sessions implicitly carry **all** scopes.\n"
        "2. **HMAC API key** (`ApiKeyHmac`), for programmatic clients. See the\n"
        "   `ApiKeyHmac` security scheme for the canonical signing string. API-key\n"
        "   callers carry only the scopes granted at mint time and must satisfy the\n"
        "   per-endpoint scope noted in each operation's description.",
        "Authenticate with an **HMAC API key** (`ApiKeyHmac`); see that security\n"
        "scheme for the canonical signing string. Keys are minted, listed, and\n"
        "revoked in the Quote terminal (**Settings → API Keys**); the secret is\n"
        "shown once at mint time. A key carries only the scopes granted at mint\n"
        "time and must satisfy the per-endpoint scope noted in each operation's\n"
        "description.",
    ),
    (
        "### Privy-only endpoints\n"
        "API-key management (`/api/keys*`) and the invite/referral endpoints\n"
        "(`/api/invites*`, `/api/referrals/summary`) are gated to Privy sessions\n"
        "only: an API key cannot mint, list, or revoke other API keys, nor manage\n"
        "invites. These return `403` for API-key callers.\n"
        "\n",
        "",
    ),
    (
        "Routes under `/api/*` require authentication, except `/api/info`,\n"
        "    `/api/news`, and `/api/webhooks/parallel`. The root probes `/health`,\n"
        "    `/ready`, and `/metrics` are unauthenticated.",
        "Routes under `/api/*` require authentication, except the public\n"
        "    `/api/info`. The root probes `/health`, `/ready`, and `/metrics` are\n"
        "    unauthenticated.",
    ),
]

# Applied to every string in the spec (operation descriptions and the like).
GLOBAL_TEXT_REPLACEMENTS = [
    ("**Auth:** authenticated (Privy or API key). API-key scope:", "**Auth:** API-key scope:"),
    ("**Auth:** authenticated. API-key scope:", "**Auth:** API-key scope:"),
]

APIKEY_SCHEME_DESCRIPTION = """\
HMAC API-key authentication. Three headers are sent on every request:

- `X-Quote-Key`: the public key id (this scheme's header).
- `X-Quote-Timestamp`: request time in **milliseconds** since epoch.
  Must be within 30 seconds of server time.
- `X-Quote-Signature`: hex HMAC-SHA256 over the canonical string.

**Canonical signing string** (literal `\\n` separators):

```
<timestamp>\\n<METHOD>\\n<path_with_query>\\n<body>
```

where `<timestamp>` is the `X-Quote-Timestamp` value, `<METHOD>` is the
uppercase HTTP method, `<path_with_query>` is the request path including
any query string, and `<body>` is the raw request body (empty string if
none). The 32-byte secret returned at mint time is used **directly** as
the HMAC-SHA256 key.

Keys are minted, listed, and revoked in the Quote terminal
(**Settings → API Keys**). A key carries only the scopes granted at mint
time.
"""

FORBIDDEN_DESCRIPTION = "Authenticated but not permitted: the API key lacks the required scope."


class BlockDumper(yaml.SafeDumper):
    pass


def _str_representer(dumper, data):
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


BlockDumper.add_representer(str, _str_representer)


def replace_everywhere(node, pairs):
    if isinstance(node, dict):
        return {k: replace_everywhere(v, pairs) for k, v in node.items()}
    if isinstance(node, list):
        return [replace_everywhere(v, pairs) for v in node]
    if isinstance(node, str):
        for old, new in pairs:
            node = node.replace(old, new)
        return node
    return node


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    source = Path(
        sys.argv[1]
        if len(sys.argv) > 1
        else repo_root.parent / "quote-backend" / "docs" / "openapi.yaml"
    )
    target = repo_root / "api-reference" / "openapi.yaml"

    spec = yaml.safe_load(source.read_text())

    for path in EXCLUDED_PATHS:
        spec["paths"].pop(path, None)
    spec["tags"] = [t for t in spec.get("tags", []) if t["name"] not in EXCLUDED_TAGS]
    schemas = spec.get("components", {}).get("schemas", {})
    for name in EXCLUDED_SCHEMAS:
        schemas.pop(name, None)

    # API-key only: drop the Privy scheme entirely.
    spec["security"] = [{"ApiKeyHmac": []}]
    scheme = spec.get("components", {}).get("securitySchemes", {})
    scheme.pop("PrivyBearer", None)
    if "ApiKeyHmac" in scheme:
        scheme["ApiKeyHmac"]["description"] = APIKEY_SCHEME_DESCRIPTION

    responses = spec.get("components", {}).get("responses", {})
    if "Forbidden" in responses:
        responses["Forbidden"]["description"] = FORBIDDEN_DESCRIPTION

    desc = spec["info"]["description"]
    for old, new in DESCRIPTION_REPLACEMENTS:
        # The loaded description has the leading indentation stripped, so
        # normalize the replacement pair the same way.
        old_n = "\n".join(line.strip() for line in old.splitlines())
        new_n = "\n".join(line.strip() for line in new.splitlines())
        desc_n = "\n".join(line if line.strip() else "" for line in desc.splitlines())
        if old in desc:
            desc = desc.replace(old, new)
        elif old_n in desc_n:
            desc = desc_n.replace(old_n, new_n)
    spec["info"]["description"] = desc

    spec = replace_everywhere(spec, GLOBAL_TEXT_REPLACEMENTS)

    text = yaml.dump(spec, Dumper=BlockDumper, sort_keys=False, allow_unicode=True, width=100)

    # Fail loudly if a dangling $ref to a removed schema survives.
    for name in EXCLUDED_SCHEMAS:
        if f"#/components/schemas/{name}" in text:
            sys.exit(f"error: dangling $ref to excluded schema {name}")
    # The public reference must never mention Privy or use em dashes. If the
    # backend spec grows new mentions, extend the replacement lists above.
    if "Privy" in text or "privy" in text:
        line = next(l for l in text.splitlines() if "rivy" in l)
        sys.exit(f"error: Privy mention survived curation: {line.strip()!r}")
    if "—" in text:
        sys.exit("error: em dash in generated spec")

    target.write_text(text)
    print(f"wrote {target} ({len(spec['paths'])} paths, {len(schemas)} schemas)")


if __name__ == "__main__":
    main()
