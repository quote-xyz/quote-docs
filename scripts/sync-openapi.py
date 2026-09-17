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

import re
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
    # Stored fundamentals for an underlying: reference data, not a trading
    # operation, and unauthenticated. Same reason news and the daily quote are
    # excluded.
    "/api/companies/{ticker}",
    # Terminal surfaces. These are documented in the backend spec because the
    # app calls them and the frontend's conformance check pins against it, but
    # they are not an integration surface: the journal is the coaching layer's
    # own store, and the rest back panels the terminal renders.
    "/api/journal",
    "/api/journal/consent",
    "/api/journal/trades",
    "/api/analytics/fills",
    "/api/compliance/status",
    "/api/geo/status",
    "/api/markets/depth-compare",
    "/api/markets/liquidity",
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
    "/api/referrals/invites",
    "/api/referrals/summary",
    # Routing is SHADOW ONLY. `RoutingMode::Off` is the default and there is no
    # `Live` variant at all, so nothing is routed anywhere and `route_decisions`
    # is empty unless an environment opts in. The savings endpoint says as much
    # itself ("nothing is acted on: the order goes where it always went"), and
    # the two prefs endpoints set an opt-out for execution that cannot happen.
    # Publishing them would document a surface that answers nothing.
    "/api/routing/savings",
    "/api/routing/venues",
    "/api/routing/venues/{venue}",
    # The redacted `wake`-frame timeline. AGENTS.md: execution micro-mechanics
    # (state machines, repricing thresholds, timing, anti-detection) are never
    # published, and this is that projection by definition. It also documents
    # itself as best-effort research data.
    "/api/orders/algo/{order_id}/diagnostics",
    # MCP has its own tab, and the un-suffixed `/.well-known/oauth-protected-
    # resource` is already excluded below; the list simply never matched this
    # one.
    "/.well-known/oauth-protected-resource/mcp",
    # Unauthenticated reference data rather than a trading operation, which is
    # the reason `/api/companies/{ticker}` is excluded above. The tokenomics
    # snapshot is explicitly the same contract one asset class over, and
    # `/summary` is the companies endpoint's lighter twin.
    "/api/crypto/{symbol}/tokenomics",
    "/api/companies/{ticker}/summary",
    # The asset page's order-book block, a terminal surface like the
    # `depth-compare` and `liquidity` panels excluded above.
    "/api/markets/book-depth",
    # Both answer `403` to every API-key caller, so an API-key-only reference
    # documenting them would describe a surface no reader of it can reach.
    # They are also the two paths that broke this script: their `PrivyBearer`
    # security entries and their "Privy identity" / "Privy token" prose are not
    # what the replacement lists above rewrite, so the curation guard in main()
    # failed and NOTHING was written. Excluding the path removes all of it at
    # once, which is why the other terminal-only endpoints are excluded rather
    # than reworded.
    "/api/account/wallets",
    "/api/account/profile",
]
EXCLUDED_TAGS = [
    # Every path carrying these is excluded above, so the tag itself would
    # publish a section header and a description for a surface with nothing
    # under it. "Routing" is the one that matters: its description advertises
    # "counterfactual multi-venue routing" as a feature of the API.
    "Routing",
    "Account",
    "Crypto",
    "NL Order",
    "News",
    "Companies",
    "MCP Connector",
    "Bridge",
    "API Keys",
    "Invites & Referrals",
]
EXCLUDED_SCHEMAS = [
    # Orphaned by the shadow-routing, diagnostics, reference-data and
    # terminal-surface exclusions above.
    "RoutingSavingsResponse",
    "RoutingVenuePref",
    # Nested one level down, and missed on the first pass because the orphan
    # check followed only the paths' DIRECT references. A schema reachable only
    # through an excluded schema is just as orphaned.
    "RoutingVenueSaving",
    "AlgoDiagnosticsResponse",
    "AlgoDiagnosticInfo",
    "TokenomicsResponse",
    "CompanySummaryResponse",
    "BookDepth",
    # Orphaned by excluding /api/account/wallets and /api/account/profile.
    # `RegisterWalletRequest` is the one that matters: its description names a
    # "Privy token", which no replacement rule rewrites, so leaving the schema
    # behind kept the curation guard failing even after its path was excluded.
    "AccountProfileResponse",
    "ListAccountWalletsResponse",
    "RegisterWalletRequest",
    "RegisterWalletResponse",
    "SetAccountProfileRequest",
    # Orphaned by excluding /api/companies/{ticker}.
    "CompanyResponse",
    # Orphaned by excluding the terminal surfaces above.
    "JournalStatus",
    "JournalTrade",
    "JournalTradesResponse",
    "JournalConsentRequest",
    "ComplianceStatusResponse",
    "GeoStatusResponse",
    "UserFill",
    "DepthComparison",
    "LiquidityManifest",
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
    # Privy is a terminal-internal credential and is never named publicly. Some
    # operations legitimately need to say an action is terminal-only, so rename
    # the credential rather than dropping the sentence. Kept generic (not tied
    # to one operation's wording) so a re-worded or re-wrapped source line does
    # not silently stop matching.
    ("Privy session", "terminal session"),
    ("Privy-session only", "terminal-session only"),
]

# Applied as regexes to every string, after the literal replacements above.
#
# The public docs never use em dashes (see the docs AGENTS.md style rules), but
# the backend spec is written without that constraint, so each one has to be
# rewritten into a colon, a comma, or two sentences depending on what the
# sentence is doing. Patterns are anchored on a few distinctive words either
# side and treat whitespace as `\\s+`, so re-wrapping the source line does not
# stop them matching. If the em dash guard in main() fails, add a rule here.
GLOBAL_REGEX_REPLACEMENTS = [
    (r"`code: HL_NOT_FUNDED`\s*—\s*deposit", "`code: HL_NOT_FUNDED`. Deposit"),
    (r"badges/\{key\}/seen`\s*—\s*use it", "badges/{key}/seen`. Use it"),
    (r"published ladder\s*—\s*treat", "published ladder. Treat"),
    (r"published ladder\s*—\s*unknown", "published ladder: unknown"),
    (r"Attribution only\s*—\s*never", "Attribution only, never"),
    (r"still accrues\s*—\s*referred", "still accrues: referred"),
    (r"Present once earned\s*—\s*the completion", "Present once earned: the completion"),
    (r"taker rate\s*—\s*tier, staking", "taker rate, with tier, staking"),
    (r"\*\*sell\*\* rate\s*—\s*see", "**sell** rate: see"),
    (r"Other strategies ignore it\s*—\s*use", "Other strategies ignore it: use"),
    # Whitespace is `\\s+`: these are YAML folded blocks, so a line break lands
    # mid-phrase and a literal space silently stops matching.
    (r"unmodelled\s+here\s*—\s*modelling", "unmodelled here, since modelling"),
    (r"asked\s+and\s+answered\s*—\s*outside", "asked and answered: outside"),
    # These five were already in the source spec and had no rules, so this
    # script exited 1 and wrote nothing. A sync that fails writes no partial
    # output, which is the safe direction, but it also means the published
    # reference silently stopped tracking the spec: the trigger `condition`
    # schema it serves is one nobody can successfully POST (QUO-40).
    (r"socket\s+streams\s+live\s*—\s*the same projection\s*—\s*so",
     "socket streams live, the same projection, so"),
    (r"before\s+rendering\s+the\s+totals\*\*\s*—\s*see the field",
     "before rendering the totals**. See the field"),
    (r"`metrics`\s+and\s+`calendar`\s*—\s*who the company",
     "`metrics` and `calendar`: who the company"),
    (r"often\s*—\s*the trade page's About panel\s*—\s*and it is",
     "often, on the trade page's About panel, and it is"),
    (r"No\s+snapshot\s+for\s+this\s+ticker\s*—\s*the sweep",
     "No snapshot for this ticker: the sweep"),
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


def replace_everywhere(node, pairs, regex_pairs=()):
    if isinstance(node, dict):
        return {k: replace_everywhere(v, pairs, regex_pairs) for k, v in node.items()}
    if isinstance(node, list):
        return [replace_everywhere(v, pairs, regex_pairs) for v in node]
    if isinstance(node, str):
        for old, new in pairs:
            node = node.replace(old, new)
        for pattern, new in regex_pairs:
            node = re.sub(pattern, new, node)
        return node
    return node


def fail(message: str, text: str, needle: str) -> None:
    """Exit with the offending lines, so the fix is obvious from the error."""
    lines = [l.strip() for l in text.splitlines() if needle in l]
    detail = "\n".join(f"    {l}" for l in lines[:5])
    sys.exit(f"error: {message}\n{detail}")



def check_pages_reference_a_written_spec(repo_root, written):
    """Refuse a page pointing at a spec this script does not write.

    The failure this catches is silent: the page renders fine from a file that
    simply stops being updated, so the published reference goes stale while the
    repo, the diff and this script's exit code all look correct.
    """
    pages = sorted((repo_root / "api-reference" / "endpoints").glob("*.md"))
    stale = {}
    for page in pages:
        for ref in re.findall(r'src="([^"]+)"', page.read_text()):
            resolved = (page.parent / ref).resolve()
            if resolved not in {w.resolve() for w in written}:
                stale.setdefault(str(resolved), []).append(page.name)
    if stale:
        lines = "\n".join(
            f"  {path}\n    referenced by: {', '.join(sorted(names))}"
            for path, names in sorted(stale.items())
        )
        sys.exit(
            "error: endpoint pages reference a spec this script does not write.\n"
            "Those pages would render from a file that never updates.\n"
            f"{lines}\n"
            "Fix: write that path here, or point SRC in gen-endpoint-pages.py at one we do."
        )

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

    # Hide strategy knobs whose names hint at undocumented engine mechanics
    # (and at the undocumented adaptive_is strategy).
    strategy_props = schemas.get("StrategyParamsInput", {}).get("properties", {})
    for prop in ("observationMode", "queueImproveThreshold", "distributionSkew"):
        strategy_props.pop(prop, None)

    # The backend spec lists a localhost server for its own development. A
    # public reference has no use for it, and GitBook renders the server list
    # in the "test it" selector, where it is an invitation to call a machine
    # the reader does not have.
    spec["servers"] = [s for s in spec.get("servers", []) if "localhost" not in s.get("url", "")]

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

    spec = replace_everywhere(spec, GLOBAL_TEXT_REPLACEMENTS, GLOBAL_REGEX_REPLACEMENTS)

    text = yaml.dump(spec, Dumper=BlockDumper, sort_keys=False, allow_unicode=True, width=100)

    # Fail loudly if a dangling $ref to a removed schema survives.
    for name in EXCLUDED_SCHEMAS:
        if f"#/components/schemas/{name}" in text:
            sys.exit(f"error: dangling $ref to excluded schema {name}")
    # The public reference must never mention Privy or use em dashes. If the
    # backend spec grows new mentions, extend the replacement lists above.
    if "Privy" in text or "privy" in text:
        fail("Privy mention survived curation; extend the replacement lists", text, "rivy")
    if "adaptive_is" in text:
        fail("adaptive_is mention survived curation", text, "adaptive_is")
    if "—" in text:
        fail("em dash in generated spec; add a GLOBAL_REGEX_REPLACEMENTS rule", text, "—")

    # GitBook's own UI duplicated the spec into .gitbook/assets and repointed
    # every endpoint page at that copy (GITBOOK-71). It is the file the site
    # actually serves, and nothing here wrote it, so a sync updated the copy no
    # page reads and published nothing. Both are written together now.
    served = repo_root / ".gitbook" / "assets" / "openapi.yaml"
    target.write_text(text)
    served.write_text(text)

    check_pages_reference_a_written_spec(repo_root, {target, served})

    print(f"wrote {target} and {served} ({len(spec['paths'])} paths, {len(schemas)} schemas)")


if __name__ == "__main__":
    main()
