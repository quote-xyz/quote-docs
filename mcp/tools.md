---
description: Every tool the Quote MCP server exposes, its required scope, and what it returns.
---

# Tools Reference

The authoritative, always-current catalog, including full input schemas, is served by the API itself:

```bash
GET /api/mcp/tools    # catalog with input schemas + required scope per tool
GET /api/mcp/guide    # an operating guide written for agents (markdown)
```

## Market tools (`analytics:read`)

| Tool | What it returns |
|---|---|
| `get_price` | Live price snapshot for a symbol |
| `get_candles` | OHLCV history |
| `get_market_microstructure` | Book depth, spread, imbalance signals |
| `get_funding_history` | Historical funding rates for a market |
| `scan_markets` | Market screener across all listed assets |
| `search_news` | Market-news search |
| `get_earnings` | Earnings calendar/data for equity markets |
| `search_outcome_markets` | HIP-4 prediction-market search |
| `estimate_trade_cost` | Pre-trade cost estimate (spread + impact) for a hypothetical order |
| `stress_test` | Liquidation/PnL stress scenarios against the live book |
| `navigate_symbol` | Resolve a name/ticker to the canonical venue symbol |
| `search_assets` | Find listed markets by what they are: underlying name, sector, or theme |
| `get_fundamentals` | One market's fundamentals: market cap, supply, revenue and valuation ratios |
| `get_contract_terms` | A trade[XYZ] (`xyz:`) market's contract terms and current oracle state |
| `compare_markets` | How up to three perps moved against each other over 7 or 30 days |
| `search_wire` | Quote's breaking-news wire, newest first, filterable by asset, phrase and time |
| `get_catalysts` | Scheduled catalysts: token unlocks, macro events and commodity reports |

## Account tools (`account:read`)

| Tool | What it returns |
|---|---|
| `get_execution_report` | Your execution quality: benchmarks, slippage, savings ([conventions](../api-reference/introduction.md#analytics-conventions)) |
| `get_portfolio_report` | Portfolio analytics: equity, PnL decomposition |
| `get_funding_carry` | Funding economics of your current positions |
| `list_triggers` | Your conditional triggers |
| `get_algo_orders` | Your algo orders, with live progress on the ones still working |
| `get_algo_order` | One algo order in depth: benchmarks, fees and child fills |
| `get_order` | One order of any kind: fills, average price, maker share and fees |
| `get_fee_info` | Your fee tier and builder-fee status |
| `get_referral_summary` | Referral rewards and discount status |

{% hint style="info" %}
Account tools answer only for the wallet the token was issued for. Tool listings are scope-filtered: a token without `account:read` never sees these tools at all.
{% endhint %}

## Example prompts

Once connected, these kinds of questions resolve through the tools above:

- *"What's the cost of buying 50 ETH right now vs. working it over an hour?"* → `estimate_trade_cost`, `get_market_microstructure`
- *"How did my executions perform vs. VWAP this month?"* → `get_execution_report`
- *"Which markets moved most in the last 24h with rising open interest?"* → `scan_markets`
- *"What's my funding carry costing me per day?"* → `get_funding_carry`
