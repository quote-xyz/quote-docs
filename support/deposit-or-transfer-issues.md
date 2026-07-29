# Deposit or Transfer Issues

## Deposited via Arbitrum network (USDC)

Description: You deposited via the Arbitrum network

#### Important note <a href="#important-note" id="important-note"></a>

* Only USDC deposits from the Arbitrum network are supported. If you transferred USDT, ETH, ARB or any other token, your funds will not have been deposited.

#### What to do (for email accounts only) <a href="#what-to-do-for-email-accounts-only" id="what-to-do-for-email-accounts-only"></a>

* Wrong deposit: If you deposited anything other than USDC on the Arbitrum network, you can retrieve the funds yourself by following the steps here: [https://hyperliquid.gitbook.io/hyperliquid-docs/onboarding/export-your-email-wallet](https://hyperliquid.gitbook.io/hyperliquid-docs/onboarding/export-your-email-wallet)
* Deposited <5 USDC, which is the minimum: If your deposit was less than 5 USDC, then it will not be credited. If you logged in with an email, you can send more USDC and the whole amount will be credited. If you are not an email wallet user, your funds are lost.



## Transfer or deposit to USDC (Perps) missing

Description: You transferred USDC from your Spot to Perps balance or deposited USDC via Arbitrum and can’t figure out where it went or why you are not able to use the USDC in your Perps balance.

Situation 1: Transferred 1,000 from USDC (Spot) to USDC (Perps). When I checked, I see <1,000 USDC in my Available Balance. Where did it go?

Situation 2: Deposited 1,000 USDC from Arbitrum, and the deposit was successful. When I checked, I see <1,000 USDC in my Available Balance. Where did it go?

#### Reasoning <a href="#reasoning" id="reasoning"></a>

* If you have open positions on cross margin with negative unrealized P\&L, your deposits and Spot to Perp transfers will go toward collateral for those open positions. Please refer to the Docs to understand how margining works: [https://hyperliquid.gitbook.io/hyperliquid-docs/trading/margining#unrealized-pnl-and-transfer-margin-requirements](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/margining#unrealized-pnl-and-transfer-margin-requirements)[<br>](https://hyperliquid.gitbook.io/hyperliquid-docs/support/faq/withdrawal-issues)
