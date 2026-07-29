---
description: >-
  Quote is in private Alpha and invite-only. How to get in, and the checks that
  can restrict trading afterwards.
---

# Access and Restrictions

Quote is in **private Alpha**. Access is invite-only, and until that changes you have to clear the invite wall before you can reach the terminal.

The wall is a full-screen gate. You never see the trading interface before you are both admitted and signed in.

## Ways in

There are three doors. You need only one.

### An invite code

Every existing user has a referral code, and it doubles as an invite. Ask someone already on Quote for theirs.

Enter it on the wall. You can do this before connecting a wallet: the code is checked immediately and redeemed once you sign in, so the order of those two steps does not matter.

Codes admit a limited number of people. A code whose seats are used up will tell you so rather than letting you through, and its owner has to earn another seat before it works again. Joining with a code also records you as that person's referral, which starts the [invited-user rebate](referrals.md#the-invited-user-rebate) on your own fees.

### The Telegram whitelist

If your Telegram account is on the alpha whitelist, it is your way in.

{% stepper %}
{% step %}
#### Start the flow on the wall

Choose the Telegram option. Quote generates a one-time link into its bot.
{% endstep %}

{% step %}
#### Open the link in Telegram

The bot checks your account against the whitelist. The link expires, so finish this promptly rather than leaving it open.
{% endstep %}

{% step %}
#### Come back and sign in

If your account is on the list you are admitted, and the wall carries you into signing in. If it is not, the check tells you so.
{% endstep %}
{% endstepper %}

### A partner program

Quote runs doors with partner protocols. Each has a bar your wallet has to clear, such as a reputation score or a pass level.

Some are automatic. A connected wallet that already meets the bar is admitted silently, with nothing to claim and no separate step. Others have their own page where you connect and check.

If you do not clear the bar, you are told what it is and where you currently stand, so you know what is missing rather than simply being refused.

{% hint style="info" %}
Coming in through a program can carry a benefit into your account, such as a floor on your [rewards tier](rewards-tiers.md) that holds regardless of your volume.
{% endhint %}

If a partner is unreachable the check fails with a temporary error rather than a rejection. Try again rather than assuming you were turned down.

## If you have none of these

Join the waitlist with your email address. No wallet is needed.

The waitlist is not a door: it does not admit you, it puts you in the queue for when access opens up. If someone gives you a code in the meantime, use the code.

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

## After you are admitted

Trading needs two one-time signatures from your main wallet, both taken in the terminal: registering an [agent wallet](../concepts/agent-wallets.md), and approving Quote's [builder fee](fees.md#the-quote-builder-fee). API keys cannot produce either signature, so complete onboarding in the terminal before integrating.

Then [place your first trade](../guides/first-trade.md).
