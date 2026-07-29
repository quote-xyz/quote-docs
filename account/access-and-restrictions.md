---
description: How to get into Quote while access is gated, and the checks that can restrict trading.
---

# Access and Restrictions

Quote is not open registration. Access is gated, and two further checks can restrict what an admitted account is allowed to do.

## Getting in

There are three routes, and you need only one.

### An invite code

Someone already on Quote gives you their referral code, which doubles as an invite. Redeem it with your wallet connected and you are admitted, and you are recorded as their referral, which starts the [invited-user rebate](referrals.md#the-invited-user-rebate) on your own fees.

Codes admit a limited number of people. A code whose seats are used up will not let you in, and its owner has to earn another seat before it will.

### A partner access program

Quote runs doors with partner protocols. Each has a bar you have to clear, such as a reputation score or a pass level held by your wallet.

Connect your wallet on the program's page and Quote checks it against the partner. If you clear the bar you are admitted straight away. If you do not, you are told the bar and where you currently stand, so you know what is missing rather than simply being refused.

Coming in through a program can also carry a benefit into your account, such as a floor on your [rewards tier](rewards-tiers.md) that holds regardless of your volume.

{% hint style="info" %}
If a partner is unreachable the check fails with a temporary error rather than a rejection. Try again rather than assuming you were turned down.
{% endhint %}

### The waitlist

With no code and no qualifying program, join the waitlist with your email address. No wallet is needed.

## Linking Telegram

Some access routes and quests ask you to link Telegram. You start the link in the terminal, verify in Telegram, and the terminal confirms once the link lands. It is also how the team reaches you about your account.

## Compliance screening

Wallets are screened. The outcome is one of clear, pending, or flagged, and a flagged wallet carries a reason.

Screening is on the wallet, not on you personally, and its result is visible in the terminal. If your wallet is flagged and you believe it is wrong, raise it in the [Telegram community](https://t.me/quotemarkets).

## Geographic restrictions

Trading is geofenced by the IP address the request comes from. Where a jurisdiction is restricted:

- **Placing orders is blocked.** The backend rejects order submission, and the terminal disables the order form and shows a restriction banner.
- **Cancelling still works.** You are never trapped in a position because of a geofence. You can always cancel resting orders.

{% hint style="warning" %}
The geofence is evaluated per request, so it applies to API clients as well as the terminal. If you run a bot, run it from a jurisdiction where trading is permitted, and expect order submission to fail if it moves.
{% endhint %}

## Onboarding

Once admitted, trading needs two one-time signatures from your main wallet, both taken in the terminal: registering an [agent wallet](../concepts/agent-wallets.md), and approving Quote's [builder fee](fees.md#the-quote-builder-fee). API keys cannot produce either signature, so complete onboarding in the terminal before integrating.
