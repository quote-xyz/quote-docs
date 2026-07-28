# Documentation project instructions

## About this project

- Public developer docs for **Quote** (quotemarkets.xyz), a trading terminal for Hyperliquid, published with [GitBook](https://gitbook.com) Git Sync
- Pages are Markdown with YAML frontmatter (`description`); the page title is the first `#` heading. Navigation lives in `SUMMARY.md`, sync configuration in `.gitbook.yaml`
- Site settings (theme, colors, logo, favicon, custom domain, header links) live in the GitBook dashboard, not in this repo. Do not try to configure them from here
- The endpoint pages in `api-reference/endpoints/` are **generated** by `scripts/gen-endpoint-pages.py` from `api-reference/openapi.yaml`, which is itself **generated** from `quote-backend/docs/openapi.yaml` by `scripts/sync-openapi.py` (that spec is the source of truth). The sync script strips non-trading surfaces (Quentin/NL-order, Parallel news, daily quote). Never hand-edit either generated artifact or copy the backend spec over it verbatim; re-run the scripts instead
- Use GitBook block syntax, not MDX components: `{% hint style="info|success|warning|danger" %}` for callouts, `{% tabs %}` / `{% tab title="…" %}` for tabbed code, `{% stepper %}` / `{% step %}` (step titles are `####` headings) for walkthroughs, `{% code title="…" %}` around a fenced block for a titled code block, `<details>` / `<summary>` for collapsible sections, `{% openapi src=… path=… method=… %}` for API operations, and `<table data-view="cards">` for card grids
- Link between pages with relative Markdown paths ending in `.md` (`../concepts/agent-wallets.md`), never absolute site paths. Where a heading's anchor is not obvious from its text, pin it: `## Heading <a href="#slug" id="slug"></a>`

## Terminology

- "Quote" is the product; "the terminal" is the web app at quotemarkets.xyz; "the API" is the backend at api.quotemarkets.xyz
- "Agent wallet" (not "API wallet" or "trading key") for the Hyperliquid agent mechanism
- "Algo order" / "strategy" for parent orders worked by the execution engine; "child order" for the venue orders it places
- Strategy names in code style: `passive_twap`, `vwap`, `iceberg`, `participation_rate`, `chase_limit`. The engine's `adaptive_is` strategy is deliberately undocumented; never add it to these docs
- "Privy session" (terminal auth) vs. "API key" (HMAC auth): see `authentication.md` before writing about auth

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
- Every page must be listed in `SUMMARY.md`, which is the only thing that decides what gets published: a page missing from it does not reach the site. Even so, this repo is public, so never commit internal material here
