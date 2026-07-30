# Access and Restrictions

Quote is in **private Alpha**. Access is invite-only, and until that changes, you will need an invite wall before you can reach the application. This ensures that we scale infrastructure safely and gradually.

<figure><img src="../.gitbook/assets/video_1.5x_postspark_2026-07-30_12-34-08 (1).gif" alt=""><figcaption></figcaption></figure>

### Invite codes

Every existing user has a referral code, and it doubles as an invite. Ask someone already on Quote for theirs.

Enter it on the landing page. You can do this before connecting a wallet: the code is checked immediately and redeemed once you sign in, so the order of those two steps does not matter.

Codes admit a limited number of people. A code whose seats are used up will tell you so rather than letting you through, and its owner has to earn another seat before it works again. Joining with a code also records you as that person's referral, which starts the [invited-user rebate](referrals.md#the-invited-user-rebate) on your own fees.



### The Telegram whitelist

If your Telegram account was on the waitlist as of the snapshot taken on July 15th, it is your way in.

{% stepper %}
{% step %}
#### Choose the Telegram option at sign-up

Quote generates a one-time link into its bot.
{% endstep %}

{% step %}
#### Open the link in Telegram

The bot checks your account against our waitlist.
{% endstep %}

{% step %}
#### Come back and sign in

If your account is on the list, you are admitted, and the wall carries you into signing in. If it is not, the check tells you so.
{% endstep %}
{% endstepper %}

### A partner program

Quote reserves the right to run campaigns with partner protocols. Each has an eligibility criterion your wallet has to clear, such as a reputation score or a pass level.

Some are automatic. A connected wallet that already meets the bar is admitted silently, with nothing to claim and no separate step. Others have their own page where you connect and check.

{% hint style="info" %}
Coming in through a program can carry a benefit into your account, such as a floor on your [rewards tier](rewards-tiers.md) that holds regardless of your volume.
{% endhint %}



## If you have none of these

Join the waitlist with your email address. No wallet is needed.

The waitlist puts you in the queue for when access opens up. If someone gives you a code in the meantime, use the code.



## Compliance screening

Wallets are screened. Screening is on the wallet, not on you personally, and its result is visible in the application. If your wallet is flagged and you believe it is wrong, raise it in the [Telegram community](https://t.me/quotemarketsxyz).



## Geographic restrictions

Trading is geofenced by the IP address the request comes from. Where a jurisdiction is restricted:

* **Placing orders is blocked.** The backend rejects order submission, and the terminal disables the order form and shows a restriction banner.
* **Canceling still works.** You are never trapped because of a geofence. You can always cancel resting orders.

{% hint style="warning" %}
The geofence is evaluated per request, so it applies to API clients as well as the terminal. If you run a bot, run it from a jurisdiction where trading is permitted, and expect order submission to fail if it moves.
{% endhint %}



## After you are admitted

Trading needs two one-time signatures from your main wallet, both taken in the terminal: registering an [agent wallet](../concepts/agent-wallets.md), and approving Quote's [builder fee](fees.md#the-quote-builder-fee). API keys cannot produce either signature, so complete onboarding in the terminal before integrating. Then [place your first trade](../guides/first-trade.md).
