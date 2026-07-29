# Contract Specifications

Quote perpetuals are powered by Hyperliquid in the backend. Hyperliquid perpetuals are derivative products without an expiration date. Instead, they rely on funding payments to ensure convergence to the underlying spot price over time. See [Funding](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/funding) for more information.

Hyperliquid has one main style of margining for perpetual contracts: USDC margining, USDT denominated linear contracts. That is, the oracle price is denominated in USDT, but the collateral is USDC. This allows for the best combination of liquidity and accessibility. Note that no conversions with the USDC/USDT exchange rate are applied, so these contracts are technically quanto contracts where USDT pnl is denominated in USDC.

When the spot asset's primary source of liquidity is USDC denominated, the oracle price is denominated in USDC. Currently, the only USDC-denominated perpetual contracts are PURR-USD and HYPE-USD, where the most liquid spot oracle source is Hyperliquid spot.

Hyperliquid's contract specifications are simpler than most platforms. There are a few contract-specific details and no address-specific restrictions.
