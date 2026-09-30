#!/usr/bin/env python3
"""Sync the public Trader API reference spec from quote-backend.

The backend spec (quote-backend/docs/openapi.yaml) documents the full API and
is the source of truth. The public reference is curated:

- Only the operations in PUBLISHED_OPERATIONS are published, so an endpoint the
  backend adds stays out of the reference until someone lists it here. Left
  out: the terminal's own surfaces (Quentin/NL-order, news, the daily quote,
  company and crypto reference data, the journal, its panels, and the
  terminal-session-only endpoints for API keys, invites, referrals, wallets and
  profile), the MCP connector (the docs site's MCP tab covers it), the Relay
  bridge proxy, shadow-only venue routing, the algo diagnostics timeline
  (execution micro-mechanics), and `/metrics`, which the API host does not
  serve.
- The reference is API-key only. Privy is a terminal-internal credential, so
  the PrivyBearer scheme and every mention of Privy are removed.

This script owns those rules so re-syncing never reintroduces anything.

Usage:
    scripts/sync-openapi.py [path-to-backend-spec]
    # default: ../quote-backend/docs/openapi.yaml
"""

import re
import sys
from pathlib import Path

import yaml

METHODS = ("get", "post", "put", "patch", "delete")

PUBLISHED_OPERATIONS = {
    # Orders
    "POST /api/orders",
    "POST /api/orders/cancel",
    "POST /api/orders/cancel-all",
    "POST /api/orders/cancel-batch",
    "POST /api/orders/simulate",
    "GET /api/orders/urgency-preview",
    "GET /api/orders/algo/{order_id}/fills",
    "POST /api/orders/algo/{order_id}/speed-up",
    "POST /api/orders/modify",
    "GET /api/orders/algo",
    "GET /api/orders/algo/{order_id}",
    "GET /api/orders/by-client-id/{client_order_id}",
    # Agents
    "POST /api/agents",
    "GET /api/agents",
    "POST /api/agents/register",
    "POST /api/agents/builder-approval",
    "POST /api/agents/accept-terms",
    # Positions
    "POST /api/account/mode",
    "POST /api/positions/tpsl",
    "POST /api/positions/leverage",
    "POST /api/positions/margin",
    "POST /api/positions/transfer",
    # Templates
    "GET /api/templates",
    "POST /api/templates",
    "GET /api/templates/{template_id}",
    "PUT /api/templates/{template_id}",
    "DELETE /api/templates/{template_id}",
    # Triggers
    "GET /api/triggers",
    "POST /api/triggers",
    "GET /api/triggers/{trigger_id}",
    "DELETE /api/triggers/{trigger_id}",
    "GET /api/triggers/{trigger_id}/history",
    # Quests
    "GET /api/quests",
    "POST /api/quests/quote",
    "POST /api/quests/badges/{key}/seen",
    # Analytics
    "GET /api/trade-intents",
    "GET /api/trade-intents/{id}",
    "GET /api/analytics/execution",
    "GET /api/analytics/execution/timeline",
    "GET /api/analytics/volume",
    "GET /api/analytics/fees",
    "GET /api/fees/summary",
    # Funding
    "GET /api/funding",
    "GET /api/funding/timeline",
    "GET /api/funding/history",
    # Portfolio
    "GET /api/portfolio/equity",
    "GET /api/portfolio/equity/latest",
    # Health
    "GET /api/info",
    "GET /health",
    "GET /ready",
}

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
        "    `/api/info`. The root probes `/health` and `/ready` are\n"
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
    # `/metrics` is served on an internal port, not the API host.
    ("Liveness/readiness probes, info, and Prometheus metrics.",
     "Liveness and readiness probes, and API info."),
]

# Applied as regexes to every string, after the literal replacements above.
#
# The public docs never use em dashes (see the docs AGENTS.md style rules), so
# each one the backend spec carries is rewritten into a colon, a comma,
# parentheses or two sentences, depending on what the sentence is doing.
# Whitespace is `\\s+` because these are YAML blocks, where a re-wrapped source
# line puts a line break mid-phrase. If the em dash guard in main() fails, add
# a rule here.
GLOBAL_REGEX_REPLACEMENTS = [
    (r"not\s+two\s+stablecoins\s*—\s*the\s+two\s+schedules\s+Hyperliquid\s+states"
     r"\s+per\s+wallet\s*—\s*with",
     "not two stablecoins (the two schedules Hyperliquid states per wallet), with"),
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

def prune_unreachable_schemas(spec, schemas):
    """Drop every schema nothing left in the spec still points at, and say which.

    This replaces a hand-written list of 47 names, every one of them commented
    "orphaned by excluding X". A list cannot be right for long: by the time it
    was removed it had drifted BOTH ways, carrying two names for schemas the
    backend spec no longer has and missing four that nothing reaches. Worse, it
    cannot see a schema reachable only THROUGH another excluded schema, which is
    how `RoutingVenueSaving` and `AlgoDiagnosticInfo` survived two passes of
    excluding the paths above them.

    Reachability is seeded from everything EXCEPT `components.schemas` (paths,
    responses, parameters), then closed over schema-to-schema references, so a
    `$ref` from a kept response still protects its schema. Over-pruning is not
    silent: the dangling-`$ref` guard in `main` fails the build on it.
    """
    ref = re.compile(r"#/components/schemas/([A-Za-z0-9_]+)")
    seed = dict(spec)
    seed["components"] = {
        k: v for k, v in spec.get("components", {}).items() if k != "schemas"
    }
    reachable = set(ref.findall(yaml.safe_dump(seed)))
    frontier = list(reachable)
    while frontier:
        name = frontier.pop()
        for nested in ref.findall(yaml.safe_dump(schemas.get(name, {}))):
            if nested not in reachable:
                reachable.add(nested)
                frontier.append(nested)
    pruned = sorted(set(schemas) - reachable)
    for name in pruned:
        schemas.pop(name, None)
    return pruned


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    source = Path(
        sys.argv[1]
        if len(sys.argv) > 1
        else repo_root.parent / "quote-backend" / "docs" / "openapi.yaml"
    )
    target = repo_root / "api-reference" / "openapi.yaml"

    spec = yaml.safe_load(source.read_text())

    operations = {
        f"{method.upper()} {path}"
        for path, item in spec["paths"].items()
        for method in item
        if method in METHODS
    }
    missing = sorted(PUBLISHED_OPERATIONS - operations)
    if missing:
        sys.exit(
            "error: PUBLISHED_OPERATIONS lists operations the backend spec does not have:\n"
            + "\n".join(f"    {op}" for op in missing)
        )
    for path, item in list(spec["paths"].items()):
        for method in [m for m in item if m in METHODS]:
            if f"{method.upper()} {path}" not in PUBLISHED_OPERATIONS:
                del item[method]
        if not any(m in METHODS for m in item):
            del spec["paths"][path]
    published_tags = {
        tag
        for item in spec["paths"].values()
        for method, op in item.items()
        if method in METHODS
        for tag in op.get("tags", [])
    }
    spec["tags"] = [t for t in spec.get("tags", []) if t["name"] in published_tags]
    schemas = spec.get("components", {}).get("schemas", {})
    pruned = prune_unreachable_schemas(spec, schemas)

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

    # Fail loudly if a dangling $ref to a pruned schema survives. Pruning is
    # computed, so this is what proves the computation right.
    for name in pruned:
        if f"#/components/schemas/{name}" in text:
            sys.exit(f"error: dangling $ref to pruned schema {name}")
    # The public reference must never mention Privy or use em dashes. If the
    # backend spec grows new mentions, extend the replacement lists above.
    if "Privy" in text or "privy" in text:
        fail("Privy mention survived curation; extend the replacement lists", text, "rivy")
    if "adaptive_is" in text:
        fail("adaptive_is mention survived curation", text, "adaptive_is")
    if "—" in text:
        fail("em dash in generated spec; add a GLOBAL_REGEX_REPLACEMENTS rule", text, "—")
    if "Prometheus" in text:
        fail("Prometheus mention survived curation; /metrics is not on the API host",
             text, "Prometheus")

    # GitBook's own UI duplicated the spec into .gitbook/assets and repointed
    # every endpoint page at that copy (GITBOOK-71). It is the file the site
    # actually serves, and nothing here wrote it, so a sync updated the copy no
    # page reads and published nothing. Both are written together now.
    served = repo_root / ".gitbook" / "assets" / "openapi.yaml"
    target.write_text(text)
    served.write_text(text)

    check_pages_reference_a_written_spec(repo_root, {target, served})

    print(
        f"wrote {target} and {served} ({len(PUBLISHED_OPERATIONS)} of {len(operations)} "
        f"operations, {len(schemas)} schemas)"
    )


if __name__ == "__main__":
    main()
