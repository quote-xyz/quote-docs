> For Mintlify product knowledge (components, configuration, writing standards),
> install the Mintlify skill: `npx skills add https://mintlify.com/docs`

# Documentation project instructions

## About this project

- Public developer docs for **Quote** (quotemarkets.xyz), a trading terminal for Hyperliquid, built on [Mintlify](https://mintlify.com)
- Pages are MDX files with YAML frontmatter; configuration lives in `docs.json`
- The API Reference tab is auto-generated from `api-reference/openapi.yaml`, which is **generated** from `quote-backend/docs/openapi.yaml` by `scripts/sync-openapi.py` (that spec is the source of truth). The script strips non-trading surfaces (Quentin/NL-order, Parallel news, daily quote). Never hand-edit the generated file or copy the backend spec over it verbatim; re-run the script instead
- Use the Mintlify MCP server, `https://mcp.mintlify.com`, to edit content and settings via MCP
- Use the Mintlify docs MCP server, `https://www.mintlify.com/docs/mcp`, to query information about using Mintlify via MCP

## Terminology

- "Quote" is the product; "the terminal" is the web app at quotemarkets.xyz; "the API" is the backend at api.quotemarkets.xyz
- "Agent wallet" (not "API wallet" or "trading key") for the Hyperliquid agent mechanism
- "Algo order" / "strategy" for parent orders worked by the execution engine; "child order" for the venue orders it places
- Strategy names in code style: `passive_twap`, `vwap`, `iceberg`, `participation_rate`, `chase_limit`. The engine's `adaptive_is` strategy is deliberately undocumented; never add it to these docs
- "Privy session" (terminal auth) vs. "API key" (HMAC auth): see authentication.mdx before writing about auth

## Platform conventions (must hold in every page)

- Decimals are **strings** in all request/response examples; never bare floats for sizes/prices
- Benchmark values are signed bps: **positive = worse**, negative = better
- `POST /api/orders` is async-accept: a 200 means accepted into the engine, not filled; cancel success means durably requested, not terminal
- Wallet-scoped: never show a `walletAddress` field in request bodies; identity comes from the credential

## Style preferences

- Never use em dashes (U+2014) anywhere; use a colon, comma, parentheses, or two sentences instead
- Write plain English in the spirit of The Economist Style Guide: short sentences, active voice, no jargon or marketing adjectives, cut filler words
- Use active voice and second person ("you")
- Keep sentences concise: one idea per sentence
- Use sentence case for headings
- Bold for UI elements: Click **Settings**
- Code formatting for file names, commands, paths, and code references

## Content boundaries

- Never document execution micro-mechanics: state machines, repricing rules or thresholds, timing defaults, randomization or anti-detection details. Describe each strategy by its objective, its user-set parameters, and its completion semantics only. Publishing mechanics helps adversaries detect and trade against user orders
- Document actual backend behavior, grounded in `quote-backend` source or the OpenAPI spec, not roadmap or intent
- Never document internal/admin surfaces (`/api/admin/*`, ops tooling, infrastructure) or reproduce content from `quote-backend/docs/` internal notes
- Every page must be listed in `docs.json` navigation; unlisted pages are still publicly served, so no drafts of sensitive material in this repo
