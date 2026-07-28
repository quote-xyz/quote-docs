# Quote Docs

Public developer documentation for [Quote](https://quotemarkets.xyz), a trading terminal for Hyperliquid. Built with [GitBook](https://gitbook.com) Git Sync; `SUMMARY.md` defines navigation, pages are Markdown.

## Layout

```
├── .gitbook.yaml              # GitBook Git Sync config: root, structure, redirects
├── SUMMARY.md                 # Navigation (table of contents)
├── introduction.md            # Landing page (structure.readme in .gitbook.yaml)
├── quickstart.md              # Key → sign → order in 5 minutes
├── authentication.md          # Privy + HMAC, scopes, canonical string
├── concepts/                  # Wallet scoping, agent wallets, order lifecycle, venue constraints
├── strategies/                # Overview + one page per execution strategy
├── guides/                    # API keys, orders, algos, triggers, templates, analytics
├── mcp/                       # MCP server: overview, client setup, tools reference
├── websockets/                # /api/ws/algos telemetry protocol
├── api-reference/
│   ├── introduction.md        # Conventions + error envelope
│   ├── openapi.yaml           # GENERATED: run scripts/sync-openapi.py, do not hand-edit
│   └── endpoints/             # GENERATED: run scripts/gen-endpoint-pages.py
└── scripts/
    ├── sync-openapi.py        # Curated sync from quote-backend/docs/openapi.yaml
    └── gen-endpoint-pages.py  # OpenAPI spec → one endpoint page per tag
```

## How Git Sync works

The repo is connected to a GitBook space with bi-directional Git Sync: pushes to `main` publish, and edits made in the GitBook editor come back as commits. `.gitbook.yaml` tells GitBook how to read the repo:

- `structure.readme: introduction.md` makes `introduction.md` the site's landing page, so this file stays a contributor README rather than becoming a docs page.
- `structure.summary: SUMMARY.md` is the navigation. **A page that is not listed in `SUMMARY.md` is not published**, which is also how drafts stay out of the site.
- `redirects` maps old paths to pages. A redirect only fires if no page already exists at that path.

Site-level settings live in the [GitBook dashboard](https://app.gitbook.com), not in this repo: theme and colors, logo, favicon, the custom domain (e.g. `docs.quotemarkets.xyz`), and header links. The brand assets to upload are in `logo/` and `favicon-*.ico`.

## Local preview

GitBook has no local dev server. Preview a change by opening a pull request: GitBook builds a preview for the PR and comments with the link. Any Markdown previewer is good enough for prose, but GitBook block syntax (`{% hint %}`, `{% tabs %}`, `{% stepper %}`, `{% openapi %}`) only renders in GitBook.

## Keeping the API reference in sync

The endpoint pages are generated from `api-reference/openapi.yaml`, which is produced from the hand-authored spec in the backend repo. The output is **curated to the trading surface**: Quentin/NL-order, the Parallel news pipeline, and the daily quote are deliberately excluded. The exclusion list lives in the sync script. After editing `quote-backend/docs/openapi.yaml`:

```bash
scripts/sync-openapi.py         # default source: ../quote-backend/docs/openapi.yaml
scripts/gen-endpoint-pages.py   # rewrite api-reference/endpoints/ from the spec
```

Then add any new page to `SUMMARY.md` (the second script prints the entries).

Never hand-edit `api-reference/openapi.yaml`, the files in `api-reference/endpoints/`, or copy the backend spec over the curated one verbatim. The source of truth is `quote-backend/docs/openapi.yaml`, filtered through the script.

## Conventions for new pages

- Add every new page to `SUMMARY.md`. Unlisted pages are not published at all, so `SUMMARY.md` is the only thing that decides what is public.
- Pages are Markdown with YAML frontmatter carrying `description`; the page title is the first `#` heading.
- Use GitBook block syntax for callouts (`{% hint %}`), tabbed code (`{% tabs %}`), numbered walkthroughs (`{% stepper %}`), titled code blocks (`{% code title="…" %}`), and collapsible sections (`<details>`).
- Link between pages with relative Markdown paths ending in `.md` (`../concepts/agent-wallets.md`), not absolute site paths.
- Ground claims in the backend source or the OpenAPI spec; this site documents actual behavior, not intent.
- Follow the platform conventions already documented: decimals as strings, signed-bps benchmarks (positive = worse), async-accept order semantics.
