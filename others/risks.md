# Risks

#### Smart contract risk <a href="#smart-contract-risk" id="smart-contract-risk"></a>

The on-chain perp DEX depends on the correctness and security of smart contracts. Bugs or vulnerabilities in the smart contracts could result in the loss of user funds.

#### L1 risk <a href="#l1-risk" id="l1-risk"></a>

Quote is built on top of Hyperliquid, which runs on its own L1, and has not undergone as extensive testing and scrutiny as other established L1s like Ethereum. The network may experience downtime due to consensus or other issues.

#### Market liquidity risk <a href="#market-liquidity-risk" id="market-liquidity-risk"></a>

As a relatively new protocol, there could be a potential risk of low liquidity, especially in the early stages. This can lead to significant price slippage for traders, negatively affecting the overall trading experience and possibly leading to substantial losses.

#### Oracle manipulation risk <a href="#oracle-manipulation-risk" id="oracle-manipulation-risk"></a>

Quote and Hyperliquid rely on price oracles maintained by the validators to supply market data. If an oracle is compromised or manipulated for an extended period of time, the mark price could be affected and liquidations could occur before the price reverts to its fair value.

#### Risk mitigation <a href="#risk-mitigation" id="risk-mitigation"></a>

There are additional measures in place to prevent oracle manipulation attacks on less liquid assets. One such restriction is open interest caps, which are based on a combination of liquidity, basis, and leverage in the system.

When an asset hits the open interest cap, no new positions can be opened. Furthermore, orders cannot rest further than 1% from the oracle price. HLP is exempt from these rules in order to continue quoting liquidity.

Note that this is not an exhaustive list of potential risks.
