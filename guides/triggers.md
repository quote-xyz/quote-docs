---
description: >-
  Fire an order automatically when a price, funding, copy-trade or time
  condition is met.
---

# Conditional Triggers

<figure><img src="../.gitbook/assets/conditional.gif" alt=""><figcaption></figcaption></figure>

Triggers are conditions Quote watches for you. When one is met, Quote places your order. Unlike the venue's own trigger orders, Quote triggers can watch things Hyperliquid cannot express: funding rates, another wallet's trades, or the clock. The order a trigger places can be anything the order form can place, including a full [algo strategy](../strategies/overview.md).

## Creating a trigger

1. Set up the order in the order form as usual: market, side, size, and order type.
2. Turn on **Trigger** and pick a trigger type.
3. Configure the condition, then click **Create Trigger** and confirm.

Triggers are not available with **Scale** orders.

## Trigger types

| Type | Places the order when |
| --- | --- |
| **Price** | A market's price is above or below a level you set |
| **Funding** | A market's funding rate is above or below a level you set |
| **Wallet** | A wallet you name trades |
| **Time** | A date and time you set arrives, once or on a schedule |

#### Price

Pick the market to watch, **Above** or **Below**, and the price. The market you watch can be a different one from the market you trade. The form tells you if the condition would fire now.

Turn on **Require the level to hold** to fire only once the price has stayed past your level for a period you set, from 2 minutes to 24 hours in whole minutes. The hold is measured on traded prices from the moment you arm the trigger, and the fire is still confirmed on the live mark.

#### Funding

Pick the market, **Above** or **Below**, and the rate. The form shows what the rate would come to over a year if it held.

Turn on **Require the rate to hold** to fire only once the rate has stayed past your level for a number of hours. Funding is published hourly, so the window is a whole number of hours, from 2 to 500.

#### Wallet

Enter the wallet address to copy. You can limit it to the wallet's buys or its sells, and set a **Minimum size** so small trades are ignored.

#### Time

Pick a **Date** and **Time**, and a timezone. **Repeats** sets a schedule: hourly, daily, weekly, monthly or a custom cadence. A repeating trigger needs an end: after a number of executions (up to 365), or on a date.

Turn on **Only while a market condition holds** to attach a price or funding condition to a schedule, for example "buy $500 every hour while BTC is below 80,000". A period in which the condition is false is skipped, and does not use up an execution.

## Managing triggers

Your triggers appear in the **Triggers** tab of the positions panel, with their condition and status. Cancel one there.

A trigger is in one of these states:

| State | Meaning |
| --- | --- |
| Active | Watching its condition |
| Triggered | It fired and placed its order |
| Canceled | You canceled it |
| Expired | It reached its expiry without firing |
| Failed | It could not place its order |

To create and manage triggers over the API, see the [Triggers endpoints](../api-reference/endpoints/triggers.md).

## Semantics worth knowing

* **One-off triggers fire once.** A price, funding or wallet trigger fires once, places its order, and becomes **Triggered**. Create it again if you want it re-armed. A repeating time trigger stays active until it has used its executions or reached its end date.
* **The order still has to pass.** When a trigger fires, its order goes through the normal order path: agent signing, venue constraints, minimum notional. A failed order is recorded in the trigger's history.
* **Triggers survive restarts.** They are stored server-side, not in your browser, so they keep watching while you are away.
* **Ownership.** Triggers belong to your wallet, and only you can see and manage them.
