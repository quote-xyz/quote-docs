---
description: The material risks of trading on Quote and the Hyperliquid L1 underneath it.
---

# Risks

Trading perpetuals on-chain carries risks beyond being wrong about the price. This is not an exhaustive list.

## Smart contract risk

The on-chain perpetual DEX depends on the correctness and security of its contracts. A bug or vulnerability could result in loss of user funds.

## L1 risk

Quote is built on Hyperliquid, which runs its own L1. That chain has not been through the testing and scrutiny that older networks such as Ethereum have, and it may experience downtime from consensus or other faults.

## Market liquidity risk

Liquidity can be thin, particularly on newer markets. Thin books mean significant price slippage and a worse execution experience, and in the worst case substantial losses on entry or exit.

Quote's [execution strategies](../strategies/overview.md) are designed to reduce this cost, but they cannot manufacture liquidity that is not there. A [passive strategy](../strategies/iceberg.md) on an illiquid book may simply not fill.

## Oracle manipulation risk

Quote and Hyperliquid rely on price oracles maintained by validators. An oracle that is compromised or manipulated for a sustained period could move the mark price and trigger [liquidations](../concepts/liquidation.md) before the price returns to fair value.

Two venue rules limit the damage on less liquid assets: open interest caps, and a band that stops orders resting far from the oracle price. Both are documented as the constraints they are in [Hyperliquid Constraints](../concepts/hyperliquid-constraints.md), because both will reject your orders in normal trading, not only during an attack.

## Execution risk

Working an order over time trades one risk for another. Passive execution captures spread but takes time, and price can move against you while it runs. Strategies without a completion guarantee, such as [Iceberg](../strategies/iceberg.md), may end unfilled or partly filled. Check `filledQty` at terminal state rather than assuming a strategy completed.

## Custody

Quote is non-custodial and never holds your funds. That removes the risk of the operator losing them, and puts the security of your keys entirely on you. See [Account Compromised](account-compromised.md).
