---
description: Explore permissionless optimal trading execution.
cover: .gitbook/assets/gitbook cover.png
coverY: 0
layout:
  width: default
  cover:
    visible: true
    size: hero
    mask: none
  title:
    visible: true
  description:
    visible: true
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
  metadata:
    visible: true
  tags:
    visible: true
  actions:
    visible: true
---

# Welcome to Quote

### Introduction to Quote

Quote is a perpetuals execution layer. Traders' orders submitted via Quote are routed through the Quote Execution Engine (QEE) before being submitted to Hyperliquid, with the parents' orders optimized down to the child order level, guaranteeing privacy for standing orders.

<figure><img src=".gitbook/assets/Screenshot 2026-02-20 at 6.04.44 pm.png" alt=""><figcaption><p>Figure 1. Quote Order Flow through the Quote Execution Engine.</p></figcaption></figure>

The QEE minimizes the Implementation Shortfall (or the cost of completing trades) by:

* Prioritizing passive execution to optimize for fees
* Pacing execution dynamically based on real-time volumes, target participation rates, or pre-defined schedules
* Sizing orders according to real-time orderbook depth
* Turning aggressive fills when liquidity is favorable

More information about the Quote order types can be found in the [Algorithmic Execution Suite](trading/algorithmic-execution-suite/) section.

### The problem

<figure><img src=".gitbook/assets/Screenshot 2026-02-20 at 6.09.48 pm.png" alt=""><figcaption><p>Figure 2. Hidden costs of trading perpetual derivatives</p></figcaption></figure>

Quote aims to solve several problems for traders in the perpetuals market, including:

* Spread crossing
* Slippage and adverse selection
* High exchange fees
* Lack of professional services for pro-retail



### The Solution <a href="#technical-overview" id="technical-overview"></a>

The Beta version of Quote was developed from first principles. The QEE leverages battle-tested algorithmic logic and a HyperCore specialized Data Engine to execute trades. The Data Engine was tailor-built to leverage the rich HyperCore data streams.

Once an order is submitted through the Quote UI or via the Traders API, trader order data is routed through the QEE, which uses recorded market data to optimize the parent order by breaking it into child orders and submitting them to Hyperliquid via Builder Codes.

<figure><img src=".gitbook/assets/Screenshot 2026-02-20 at 6.14.36 pm.png" alt=""><figcaption><p>Figure 3. Quote Execution Engine Flow.</p></figcaption></figure>

Quote addresses the structural inefficiencies of the perpetuals market by introducing a permissionless trading desk. Our platform puts institutional-grade algorithms and trading execution strategies at anyone's fingertips, leveraging liquidity from Hyperliquid.

* Executions are continuously optimized with real-time market data from the Quote Data Engine, to capture the best possible prices, inclusive of exchange fees
* Instead of sending a naive order to the book, the QEE breaks parent trades into multiple optimized child orders
* Orders are routed through Hyperliquid via Builder Codes, maintaining a non-custodial environment that enables us to deliver professional execution while traders retain control of their assets

By using Quote, we expand an institutional service to on-chain traders, internalizing part of the value leakage from Market Makers, Sophisticated Traders, and Exchanges.
