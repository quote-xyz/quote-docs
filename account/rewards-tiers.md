---
description: The volume-based loyalty ladder, and the three rates each tier sets.
---

# Rewards Tiers

Your tier answers one question: how much do you trade? It is set by your **rolling 30-day volume** of Quote-routed activity, and it decides three rates.

| Rate | What it does |
|---|---|
| Referral rate | Your cut of the fees paid by people you referred directly |
| L2 rate | Your override on the fees paid by their referrals |
| Cashback | The rebate on your own fees |

## The ladder

| Tier | 30-day volume | Referral rate | L2 rate | Cashback |
|---|---|---|---|---|
| Wood | $0 | 10% | 1% | 5% |
| Bronze | $100,000 | 12.5% | 1% | 10% |
| Silver | $2,500,000 | 15% | 1% | 12.5% |
| Gold | $10,000,000 | 17.5% | 1.5% | 15% |
| Platinum | $100,000,000 | 20% | 1.5% | 17.5% |
| Diamond | $250,000,000 | 22.5% | 2% | 20% |
| Obsidian | $500,000,000 | 25% | 2% | 22.5% |

{% hint style="info" %}
Rates and volume floors are served live by the API and can change. The table above is the ladder as it currently stands; the profile surface in the terminal always shows your own current rates, and those are the ones accrual uses.
{% endhint %}

Volume is measured on a rolling 30-day window, so the ladder works in both directions. Stop trading and your 30-day figure decays, and your tier follows it down.

## Your effective tier

Volume is the usual route to a tier, but it is not the only one. Quote can grant a tier floor, for instance through a partner [access program](access-and-restrictions.md), which holds you at that tier regardless of what your volume alone would give you.

Your **effective tier** is the higher of the two, and it is what the system accrues at. If you were granted a floor, working out your tier from your volume will under-report your real rates. Trust the tier shown on your profile.

## What tiers do not affect

A tier changes what Quote rebates you. It does not change what Hyperliquid charges you: the venue runs its own volume ladder and its own staking discounts, which are separate and share some names. See [Fees](fees.md) for how the layers fit together.

{% hint style="warning" %}
Tiers are not [badges](quests-and-badges.md). Tiers measure how much you trade and set your rates. Badges record what you have done and set nothing. The two are deliberately separate systems.
{% endhint %}

## Where the rates apply

Cashback lands on your own fees and accrues as claimable USDC rather than reducing the fee at fill time. The referral and L2 rates apply to other people's fees and pay out through the same claim. Both are covered in [Referrals](referrals.md).
