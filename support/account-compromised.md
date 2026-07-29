---
description: What to do if you see activity you did not authorize, and how to avoid it happening again.
---

# Account Compromised

If you see transactions you did not make, funds missing, or a multi-sig on your account that you did not set up, treat your wallet as compromised.

Quote and Hyperliquid are both non-custodial. Only someone holding your private key or seed phrase can sign on your address's behalf. Activity you did not initiate therefore means your key is in someone else's hands, not that a service was breached.

{% hint style="danger" %}
Act immediately. An attacker with your key keeps it, and anything you leave in that address stays reachable by them indefinitely.
{% endhint %}

## What to do now

{% stepper %}
{% step %}
#### Stop using the address

Treat it as permanently unsafe. Do not deposit to it again, however small the amount.
{% endstep %}

{% step %}
#### Create a new wallet

Use a trusted wallet provider and generate a fresh address.
{% endstep %}

{% step %}
#### Move what remains

Transfer any remaining funds to the new address, across every application, not only Quote. Include anything on HyperEVM, which also applies if your HyperCore address has been converted into a multi-sig you do not control.
{% endstep %}

{% step %}
#### Revoke contract permissions

Use [revoke.cash](https://revoke.cash) to withdraw approvals you granted from the old address, limiting what an attacker can still reach.
{% endstep %}

{% step %}
#### Clean up and find the cause

Clear your browser cache and cookies, then work out how the key leaked and whether the device has malware. Without this step you will repeat the mistake on the new address.
{% endstep %}
{% endstepper %}

## Staying safe afterwards

Self-custody means the safeguards are yours to run. The habits that matter most:

- **Never share your seed phrase or private key.** Never type it into a website, and never give it to anyone claiming to be support. No legitimate support person will ask.
- **Use a hardware wallet** for anything meaningful (Ledger, Trezor, Keystone). Pair one with a browser wallet such as Rabby to keep the key off the browser entirely.
- **Never rush a signature.** Read every transaction before signing, and heed your wallet's warnings. If it does not tell you enough to be sure, do not sign.
- **Verify links.** Beware sponsored search results, cross-check against official accounts, and bookmark the sites you use. Quote's canonical addresses are listed in [Official Links](official-links.md).
- **Do not install unverified software**, and do not open PDFs from unknown senders.
- **Assume unsolicited direct messages are scams**, particularly any that ask you to install something or follow a link out of context.
- **Keep browsers and extensions updated**, and remove extensions that are no longer maintained.

## Reporting it

Quote cannot reverse a signed transaction or freeze an address, because neither Quote nor Hyperliquid holds custody. Telling the team is still worth doing, since it helps warn others if an attack is spreading through a shared route such as a fake site. See [Contact Us](contact-us.md).
