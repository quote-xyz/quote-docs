---
description: What a fill actually costs you, from the venue fee through Quote's builder fee to the rebates that come back.
---

# Fees

Every fill you make carries three layers of cost. The terminal shows the assembled figure, but it is worth understanding what goes into it, because two of the three layers move with your own activity.

| Layer | Who charges it | Direction |
|---|---|---|
| Hyperliquid fee | The venue | You pay |
| Quote builder fee | Quote | You pay |
| Rewards rebates | Quote | You get back |

## Hyperliquid fees

Hyperliquid charges separate taker and maker rates for perps and for spot. Your rate is not fixed. It moves with:

- **Your volume tier.** Hyperliquid steps your rate down as your traded volume rises. The ladder is the venue's, not Quote's.
- **A HYPE staking discount**, expressed as a percentage off your Hyperliquid fees.
- **A referral discount**, if a Hyperliquid referral applies to your account.

Quote reads your net rate after all three, so what you see is the rate you actually pay rather than the published base rate.

{% hint style="warning" %}
Hyperliquid's staking levels share names with Quote's [rewards tiers](rewards-tiers.md), and they are unrelated. A staking level changes what the venue charges you. A Quote tier changes what Quote rebates you. Quote deliberately never names the staking level for this reason.
{% endhint %}

## The Quote builder fee

Quote earns through Hyperliquid's builder-code mechanism rather than through subscriptions or spread markup. Every Quote-routed order carries Quote's builder code, and the fee is attached server-side.

The rate is **2 bps (0.02%) on perpetuals and 4 bps (0.04%) on spot**. There are no fixed subscriptions and no monthly minimums: if you do not trade, you pay Quote nothing. The rate sits on top of [Hyperliquid's own fees](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/fees), as the builder-code design intends.

Two conditions decide whether it is actually charged on a given fill: fee collection has to be switched on for the deployment, and your wallet has to have approved the builder fee on Hyperliquid. Approval is a one-time signature during [agent setup](../concepts/agent-wallets.md), and Quote will not trade for a wallet that has not given it.

The builder fee is never hidden. [Execution analytics](../guides/analytics.md) report it separately from exchange fees, so you can always see Quote's share of what a fill cost.

## Rebates

Two rebates act on your own fees, both from the rewards program:

- **Cashback**, a percentage of your own fees returned to you, set by your [rewards tier](rewards-tiers.md).
- **The invited-user rebate**, a flat rate that applies while you were referred by a real referrer and your volume is under the program cap.

{% hint style="info" %}
Rebates accrue as claimable USDC. They do not reduce the fee charged on-chain. A fill still costs the Hyperliquid fee plus the builder fee at the moment it happens, and the rebate arrives separately, to be claimed. See [Referrals](referrals.md) for claiming.
{% endhint %}

Anything you earn from other people's trading, as a referrer, is not part of this. That lives in the referral program.

## Your effective rate

The all-in rate is the Hyperliquid fee plus the builder fee, minus what rewards hand back. The terminal computes this server-side so that every surface showing you a fee number is showing the same number.

Look for the fee schedule in the terminal to see your current stack: your net Hyperliquid taker and maker rates for perps and spot, your volume tier and the volume that would reach the next one, your staking and referral discounts, the builder fee and whether it is being charged, and your tier's cashback.

{% hint style="info" %}
[`GET /api/analytics/fees`](../api-reference/endpoints/analytics.md) reports fees you have **already paid** over a range, split into total and builder. It does not return your rate card. The assembled rate stack is a separate surface and is not yet in the Trader API reference.
{% endhint %}
