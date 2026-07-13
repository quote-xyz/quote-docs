# Quote Docs

Public developer documentation for [Quote](https://quotemarkets.xyz), a trading terminal for Hyperliquid. Built with [Mintlify](https://mintlify.com); `docs.json` defines navigation and theme, pages are MDX.

## Layout

```
├── docs.json                  # Mintlify config: nav, theme, colors
├── introduction.mdx           # Landing page
├── quickstart.mdx             # Key → sign → order in 5 minutes
├── authentication.mdx         # Privy + HMAC, scopes, canonical string
├── concepts/                  # Wallet scoping, agent wallets, order lifecycle, venue constraints
├── strategies/                # Overview + one page per execution strategy
├── guides/                    # API keys, orders, algos, triggers, templates, analytics
├── mcp/                       # MCP server: overview, client setup, tools reference
├── websockets/                # /api/ws/algos telemetry protocol
├── api-reference/
│   ├── introduction.mdx       # Conventions + error envelope
│   └── openapi.yaml           # GENERATED: run scripts/sync-openapi.py, do not hand-edit
└── scripts/
    └── sync-openapi.py        # Curated sync from quote-backend/docs/openapi.yaml
```

## Local preview

```bash
npm i -g mint
mint dev          # http://localhost:3000
```

`mint broken-links` checks internal links before pushing.

## Deploying

The repo is connected to Mintlify, so pushes to `main` deploy automatically. Custom domain (e.g. `docs.quotemarkets.xyz`) is configured in the [Mintlify dashboard](https://dashboard.mintlify.com).

## Keeping the API reference in sync

The endpoint pages are generated from `api-reference/openapi.yaml`, which is produced from the hand-authored spec in the backend repo. The output is **curated to the trading surface**: Quentin/NL-order, the Parallel news pipeline, and the daily quote are deliberately excluded. The exclusion list lives in the sync script. After editing `quote-backend/docs/openapi.yaml`:

```bash
scripts/sync-openapi.py    # default source: ../quote-backend/docs/openapi.yaml
```

Never hand-edit `api-reference/openapi.yaml` or copy the backend spec over it verbatim. The source of truth is `quote-backend/docs/openapi.yaml`, filtered through the script.

## Conventions for new pages

- Add every new page to `docs.json` navigation. Orphaned pages do not render in the sidebar, but they are still publicly served, so never commit internal material here.
- Ground claims in the backend source or the OpenAPI spec; this site documents actual behavior, not intent.
- Follow the platform conventions already documented: decimals as strings, signed-bps benchmarks (positive = worse), async-accept order semantics.
