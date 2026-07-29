---
description: Move funds in and out of Quote, and between your spot and perp balances.
---

# Deposits and Withdrawals

Quote is non-custodial. Your funds sit in your own Hyperliquid account, and Quote never holds them. Everything below moves value between your wallet, other chains, and the two balances Hyperliquid keeps for you.

There are four flows in the terminal, and they do different jobs:

| Flow | Moves funds | Use it to |
|---|---|---|
| **Deposit** | Another chain → your Hyperliquid perps balance | Fund your account to start trading |
| **Withdraw** | Your Hyperliquid balance → another chain | Take money off the venue |
| **Transfer** | Spot balance ↔ perps balance | Rebalance inside Hyperliquid |
| **Send** | Your Hyperliquid balance → another address | Pay someone directly in USDC |

## Deposit

Deposits are cross-chain. You can fund from Arbitrum, Ethereum, Base, HyperEVM, and BNB Chain, plus the other chains the bridge supports at the time you deposit. Whichever chain you start from, the destination is fixed: **USDC in your Hyperliquid perps balance**. You do not choose it.

Enter an amount and the terminal fetches a live quote before you sign, showing what will arrive. Check that figure rather than assuming you receive what you sent: bridging a small amount can cost a meaningful share of it in route fees.

{% hint style="warning" %}
Send only the token the route asks for, on the chain you selected. Tokens sent outside a quoted route are not credited to your Quote account, and recovering them is a manual wallet operation you have to perform yourself.
{% endhint %}

### Buying with card or bank

If you signed in with email or a social login, Quote gives you an embedded wallet and the deposit flow opens on a choice: **Buy** or **Transfer**. Buy hands off to a hosted onramp that accepts card, Apple Pay, and bank transfer, and delivers USDC to your embedded wallet. Transfer is the ordinary cross-chain deposit above.

If you connected an external wallet such as Rabby or MetaMask, the onramp is not offered and the flow opens straight on the transfer input.

### Where a deposit goes if you are already in a position

A deposit credits your perps balance, but that does not always mean it is available to trade. If you hold cross-margin positions with negative unrealized PnL, incoming funds are absorbed as collateral for those positions first. Your available balance can therefore rise by less than you deposited, or not at all.

This is Hyperliquid margin behavior, not a Quote rule, and it is the single most common reason a deposit looks like it went missing. See [Margin](../concepts/margin.md).

## Withdraw

Withdrawing asks one question the deposit flow does not: **which balance the money comes from**.

- **Perps**: your cross-margin balance. Only the withdrawable portion is available, so collateral backing open positions is excluded.
- **Spot**: your spot USDC balance.

Pick the wrong source and the amount you expect will not be there. If you have positions open, close or reduce them before withdrawing collateral.

## Transfer between spot and perps

Transfer moves USDC between your Hyperliquid spot and perps balances. Nothing leaves the venue and no bridge is involved, so it settles immediately.

You need this whenever a balance is in the wrong place: spot trading draws on the spot balance, perp margin draws on the perps balance.

Over the API this is `POST /api/positions/transfer`, which requires the `positions:write` scope. See the [Trader API reference](../api-reference/endpoints/positions.md).

## Send

Send transfers USDC from your Hyperliquid balance directly to another address on Hyperliquid. It is a payment, not a withdrawal: the funds stay on the venue and arrive in the recipient's account.

{% hint style="warning" %}
Check the destination address before confirming. Sends are irreversible, and an address typo cannot be undone by Quote or by Hyperliquid.
{% endhint %}

{% hint style="info" %}
On a [unified or portfolio-margin account](../concepts/margin.md#unified-accounts), the spot-versus-perps split above stops describing how your collateral actually works. Quote detects the mode and adapts these flows, but treat the balance split as a display convenience rather than the underlying truth.
{% endhint %}

## If a deposit or transfer looks wrong

Usually the funds went to collateral, the amount fell under a route minimum, or the wrong token or chain was used. [Deposit or transfer issues](../support/deposit-or-transfer-issues.md) works through each case.
