---
description: Why a deposit or a spot-to-perps transfer can look smaller than the amount you sent.
---

# Deposit or Transfer Issues

Almost every "my funds are missing" report resolves to one of the cases below. Work through them before raising it.

## The balance is smaller than what I sent

This is the most common case by a wide margin, and the funds are not lost.

**What you see.** You transfer 1,000 USDC from spot to perps, or deposit 1,000 USDC, the transaction succeeds, and your available balance rises by less than 1,000, or not at all.

**Why.** If you hold cross-margin positions with negative unrealized profit and loss, incoming funds are applied as collateral against those positions first. The money is in your account. It is backing your open risk rather than sitting available to trade.

Close or reduce the losing positions and the collateral is released back to your available balance. See [Margin](../concepts/margin.md) for how cross collateral is pooled.

## I sent the wrong token, or used the wrong chain

Only the token and chain in the route you quoted are credited. Anything else does not arrive in your Quote account.

Quote deposits are cross-chain and support several networks, so check what the deposit screen actually quoted rather than assuming a particular chain. If you sent something outside that route, the funds are still in your own wallet on the sending chain and recovering them is a wallet operation you perform yourself.

## The amount was too small

Bridge routes have minimums, and a small transfer can fall under one and not be credited. The quote shown before you sign is what tells you the amount that will arrive, so check it rather than assuming you receive what you sent.

Bridging small amounts is poor value in any case, because the route fee is a fixed-ish cost against a small principal.

## I withdrew and the amount was not available

Withdrawals draw from one balance, and you pick which: your perps (cross-margin) balance or your spot balance. Only the **withdrawable** portion of the perps balance is available, so collateral backing open positions is excluded from it.

If the figure looks short, check you selected the right source and that your positions are not holding the collateral. See [Deposits and Withdrawals](../account/deposits-and-withdrawals.md).

## Still stuck

If none of the above explains it, bring the transaction hash and the approximate time to the [Telegram community](https://t.me/quotemarkets). See [Contact Us](contact-us.md).
