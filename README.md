# Quote Docs

Public developer documentation for [Quote](https://quotemarkets.xyz) — a professional trading terminal for Hyperliquid. Built with [Mintlify](https://mintlify.com); `docs.json` defines navigation and theme, pages are MDX.

## Layout

```
├── docs.json                  # Mintlify config: nav, theme, colors
├── introduction.mdx           # Landing page
├── quickstart.mdx             # Key → sign → order in 5 minutes
├── authentication.mdx         # Privy + HMAC, scopes, canonical string
├── concepts/                  # Wallet scoping, agent wallets, order lifecycle, venue constraints
├── strategies/                # Overview + one page per execution strategy
├── guides/                    # API keys, orders, algos, triggers, templates, analytics, MCP
├── websockets/                # /api/ws/algos telemetry protocol
└── api-reference/
    ├── introduction.mdx       # Conventions + error envelope
    └── openapi.yaml           # Synced from quote-backend/docs/openapi.yaml (endpoint pages are auto-generated)
```

## Local preview

```bash
npm i -g mint
mint dev          # http://localhost:3000
```

`mint broken-links` checks internal links before pushing.

## Deploying

The repo is connected to Mintlify — pushes to `main` deploy automatically. Custom domain (e.g. `docs.quotemarkets.xyz`) is configured in the [Mintlify dashboard](https://dashboard.mintlify.com).

## Keeping the API reference in sync

The endpoint pages are generated from `api-reference/openapi.yaml`, which is a **copy** of the hand-authored spec in the backend repo. After editing `quote-backend/docs/openapi.yaml`:

```bash
cp ../quote-backend/docs/openapi.yaml api-reference/openapi.yaml
```

The source of truth is `quote-backend/docs/openapi.yaml`.

## Conventions for new pages

- Add every new page to `docs.json` navigation — orphaned pages don't render in the sidebar (but are still publicly served, so never commit internal material here).
- Ground claims in the backend source or the OpenAPI spec; this site documents actual behavior, not intent.
- Follow the platform conventions already documented: decimals as strings, signed-bps benchmarks (positive = worse), async-accept order semantics.
