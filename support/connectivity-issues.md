---
description: Wallet connection loops, failed signing, and wallet-specific fixes.
---

# Connectivity Issues

Symptoms this page covers: you cannot connect your wallet, you are stuck in a repeating "establish connection" loop, signing fails silently, or the wallet extension does not respond.

## Quick fixes

Try these in order. They resolve most cases.

1. **Update your wallet extension** to the latest version, and check it is enabled.
2. **Hard refresh** the page (`Ctrl+Shift+R`, or `Cmd+Shift+R` on macOS) and clear your cache.
3. **Disconnect and reconnect** your wallet.
4. **Switch networks and switch back.** Move to another network in your wallet, then back to the one you need.

## Wallet-specific issues

| Wallet | Symptom | Fix |
|---|---|---|
| Coinbase Wallet | Connection problems on mobile | Use the Coinbase browser extension instead |
| MetaMask | Problems on HyperEVM | Migrate to a wallet with better HyperEVM support, such as Rabby |
| Trezor | "Forbidden keypath" error | In Trezor Suite, under **Security** and **Safety checks**, change **Strict** to **Prompt** |
| Ledger | "Transfer failed" on HyperEVM | Update to the latest Ledger firmware and software |

## Reinstalling the extension

Reinstalling clears a surprising number of stuck states.

{% hint style="danger" %}
Back up your seed phrase or private key **before** you uninstall anything. Removing a wallet extension without a backup means losing access to the account permanently, and nobody can recover it for you.
{% endhint %}

## Switching wallets

Rabby tends to work most smoothly with Quote. Switching costs you nothing: your address, positions, and history live on-chain and on Hyperliquid, not in the extension, so they are unchanged when you connect with a different wallet to the same address.

Rabby documents [how to migrate from another wallet](https://support.rabby.io/hc/en-us/articles/11477459275279-How-to-migrate-from-other-wallets-to-Rabby-Wallet).

## If trading is blocked rather than connection

If your wallet connects but the order form is disabled with a restriction banner, that is not a connectivity fault. See [Access and Restrictions](../account/access-and-restrictions.md), which covers the geographic restrictions and compliance screening that can block order placement.
