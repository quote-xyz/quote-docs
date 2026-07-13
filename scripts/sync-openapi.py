#!/usr/bin/env python3
"""Sync the public API reference spec from quote-backend, stripped to the
trading-related surface.

The backend spec (quote-backend/docs/openapi.yaml) documents the full API and
is the source of truth. The public docs deliberately exclude non-trading
surfaces (Quentin/NL-order, the Parallel news pipeline, the daily quote);
this script owns that exclusion list so re-syncing never reintroduces them.

Usage:
    scripts/sync-openapi.py [path-to-backend-spec]
    # default: ../quote-backend/docs/openapi.yaml
"""

import sys
from pathlib import Path

import yaml

# Excluded from the Trader API reference: non-trading surfaces, plus the MCP
# connector endpoints (documented in the docs site's own MCP tab instead).
EXCLUDED_PATHS = [
    "/api/nl-order",
    "/api/nl-order-dev",
    "/api/news",
    "/api/webhooks/parallel",
    "/api/quotes/daily",
    "/mcp",
    "/.well-known/oauth-protected-resource",
    "/.well-known/oauth-authorization-server",
    "/oauth/register",
    "/oauth/authorize",
    "/oauth/token",
    "/api/mcp/tools",
    "/api/mcp/guide",
    "/api/mcp/dispatch",
    "/api/bridge/quote",
]
EXCLUDED_TAGS = ["NL Order", "News", "MCP Connector", "Bridge"]
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
]
# Prose fixups for the top-level description (which otherwise references
# excluded endpoints or leads with terminal-internal auth detail).
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
        "Programmatic clients authenticate with an **HMAC API key**\n"
        "(`ApiKeyHmac`); see that security scheme for the canonical signing\n"
        "string. API-key callers carry only the scopes granted at mint time and\n"
        "must satisfy the per-endpoint scope noted in each operation's\n"
        "description.\n"
        "\n"
        "The Quote terminal (web app) authenticates with a **Privy session\n"
        "token** (`PrivyBearer`), which carries all scopes implicitly. There is\n"
        "no way to obtain one programmatically; it appears here because a few\n"
        "endpoints accept only terminal sessions.",
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


class BlockDumper(yaml.SafeDumper):
    pass


def _str_representer(dumper, data):
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


BlockDumper.add_representer(str, _str_representer)


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

    # Public-reference framing: the API key is the credential developers can
    # actually obtain, so it leads. The Privy scheme stays (some endpoints are
    # terminal-session only) but its description is written for readers, not
    # operators; the internal env-var note is dropped.
    spec["security"] = [{"ApiKeyHmac": []}, {"PrivyBearer": []}]
    priv = spec.get("components", {}).get("securitySchemes", {}).get("PrivyBearer")
    if priv:
        priv["description"] = (
            "Privy session token, sent as `Authorization: Bearer <jwt>`. This is\n"
            "the credential the Quote terminal (web app) uses; there is no way to\n"
            "obtain one programmatically. Programmatic clients authenticate with\n"
            "an API key instead (see `ApiKeyHmac`). This scheme is listed because\n"
            "a few endpoints (API-key management, invites and referrals) accept\n"
            "only terminal sessions."
        )

    # The bridge endpoint is excluded, so hide its scope from the mint-key enum.
    mint_scopes = (
        schemas.get("MintKeyRequest", {}).get("properties", {}).get("scopes", {}).get("items", {})
    )
    if "enum" in mint_scopes:
        mint_scopes["enum"] = [s for s in mint_scopes["enum"] if s != "bridge:write"]

    desc = spec["info"]["description"]
    for old, new in DESCRIPTION_REPLACEMENTS:
        # The loaded description has the leading indentation stripped, so
        # normalize the replacement pair the same way.
        old_n = "\n".join(line.strip() for line in old.splitlines())
        new_n = "\n".join(line.strip() for line in new.splitlines())
        desc_n = "\n".join(
            line if line.strip() else "" for line in desc.splitlines()
        )
        # Try both raw and normalized forms.
        if old in desc:
            desc = desc.replace(old, new)
        elif old_n in desc_n:
            desc = desc_n.replace(old_n, new_n)
    spec["info"]["description"] = desc

    # Fail loudly if a dangling $ref to a removed schema survives.
    text = yaml.dump(spec, Dumper=BlockDumper, sort_keys=False, allow_unicode=True, width=100)
    for name in EXCLUDED_SCHEMAS:
        if f"#/components/schemas/{name}" in text:
            sys.exit(f"error: dangling $ref to excluded schema {name}")

    target.write_text(text)
    print(f"wrote {target} ({len(spec['paths'])} paths, {len(schemas)} schemas)")


if __name__ == "__main__":
    main()
