---
description: Permissionless optimal trading execution, and the problem it solves.
---

# Welcome to Quote

Quote is a perpetuals execution layer. Orders submitted through Quote are routed to the Quote Execution Engine before they reach Hyperliquid, where a parent order is optimized down to the child order level, keeping standing orders private until they are placed.

<figure><img src="../.gitbook/assets/Screenshot 2026-02-20 at 6.04.44 pm.png" alt=""><figcaption><p>Figure 1. Quote order flow through the Quote Execution Engine.</p></figcaption></figure>

The engine minimizes implementation shortfall, the cost of completing a trade, by:

* Prioritizing passive execution, to earn the spread and maker fees rather than pay them
* Pacing execution against real-time volume, a target participation rate, or a fixed schedule
* Sizing orders to the depth actually available in the book
* Taking liquidity only when conditions favor it

See the [execution strategies](../strategies/overview.md) for the five algorithms this covers.

## The problem

<figure><img src="../.gitbook/assets/Screenshot 2026-02-20 at 6.09.48 pm.png" alt=""><figcaption><p>Figure 2. Hidden costs of trading perpetual derivatives.</p></figcaption></figure>

Trading perpetuals costs more than the headline fee suggests. Four costs do most of the damage:

* Crossing the spread
* Slippage and adverse selection
* Exchange fees
* No access to professional execution, which on most venues is sold to institutions only

## The solution <a href="#technical-overview" id="technical-overview"></a>

Quote was built from first principles, pairing established algorithmic execution logic with a data engine built specifically for HyperCore's data streams.

An order submitted in the terminal or over the API is routed to the engine, which uses recorded market data to break the parent into child orders and submit them to Hyperliquid through builder codes.

<figure><img src="../.gitbook/assets/Screenshot 2026-02-20 at 6.14.36 pm.png" alt=""><figcaption><p>Figure 3. Quote Execution Engine flow.</p></figcaption></figure>

The result is a permissionless trading desk: institutional execution available to anyone, drawing on Hyperliquid's liquidity.

* Executions are optimized continuously against live market data, to capture the best available price inclusive of fees
* A parent order becomes many optimized child orders rather than one naive order sent to the book
* Routing through builder codes keeps the arrangement non-custodial, so you keep control of your assets throughout

The value that would otherwise leak to market makers, sophisticated traders, and exchanges stays with the trader instead.
