# Liquidation

A liquidation occurs when a trader’s account equity drops below the required maintenance margin, which is set at 50% of the initial margin at maximum leverage. Depending on the asset, this margin can range from 1.25% (for 40x leverage) to 16.7% (for 3x leverage).

When this threshold is breached:

1. The system attempts to close positions by placing market orders for the full position size.
2. If sufficient capital is recovered and margin requirements are restored, any leftover collateral stays with the trader.
3. If liquidation through the market fails and account equity falls below two-thirds of the maintenance margin, a backstop liquidation occurs through the Liquidator Vault.

* Cross Margin: In backstop events, all cross margin and positions are transferred to the liquidator. If no isolated positions exist, the trader’s account equity becomes zero.
* Isolated Margin: Only the isolated position and its margin are transferred. Other assets and cross positions remain unaffected.

In backstop scenarios, maintenance margin is not returned to the trader — this buffer ensures liquidations remain profitable for the Liquidator Vault.

To avoid backstop liquidation, traders are advised to use stop loss orders or manually exit before their mark price hits the liquidation threshold.

***

**Mark Price & Robust Liquidation**

Hyperliquid (Quote uses HL systems) uses a mark price—an aggregated value based on both external CEX data and internal book state—making it more reliable than relying solely on a volatile order book price. This improves fairness and helps prevent unnecessary liquidations during market spikes.

To learn more, please look at Hyperliquid liquidation Docs: https://hyperliquid.gitbook.io/hyperliquid-docs/trading/liquidations
