---
description: Hold up to five wallets under one login, each with its own balance, positions and agent wallet, and switch between them in the terminal.
---

# Subaccounts

One login can hold up to five accounts: your **Main Account** and up to four more. Each account is its own wallet, with its own balance, positions and [agent wallet](../concepts/agent-wallets.md). Use them to keep strategies, books or risk apart without signing in again.

## Create an account

Open the account switcher in the footer and choose **New account**. You can:

* **Create a new wallet**: an embedded wallet that Privy creates and secures. No browser extension or recovery phrase is needed.
* **Connect an existing wallet**: a self-custody wallet such as MetaMask or Rabby. You keep custody of the keys, and you sign a message to prove you own it. It is not a transaction and costs no gas.

A wallet can belong to only one Quote login. A wallet that is already on another login is refused.

{% hint style="info" %}
A new account trades like any new wallet. Before it can place orders it needs its own one-time setup in the terminal: registering an [agent wallet](../concepts/agent-wallets.md) and approving Quote's [builder fee](fees.md#the-quote-builder-fee).
{% endhint %}

## Switch accounts

Pick an account in the footer switcher. Orders, positions and history then show the active account. Algo orders running on the account you leave keep running, and their updates arrive as notifications.

## Rename and archive

Under **Manage accounts** you can rename any account, the Main Account included, and archive the others.

* **Archive** hides an account from the switcher and stops the terminal trading as it. You can archive an account only when nothing is open on it: no positions, resting orders, active triggers or running algos.
* An archived account keeps its history and still counts toward your [rewards tier](rewards-tiers.md). Its API keys, linked phones and Telegram link keep working.
* **Restore** brings an archived account back, as long as you are under the five-account limit.

The Main Account cannot be archived.

## Accounts and the API

An [API key](../guides/api-keys.md) belongs to the account that was active when you minted it, and it always trades as that account. To automate several accounts, mint a key on each. Creating, renaming and archiving accounts is done in the terminal only; API keys cannot manage accounts.
