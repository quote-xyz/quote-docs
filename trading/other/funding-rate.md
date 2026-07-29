# Funding Rate

The funding rate is a periodic payment exchanged between traders holding long and short positions in perpetual contracts. Its primary purpose is to keep the perpetual contract price (mark price) closely aligned with the underlying spot index price.

***

**What It Means:**

*   If the funding rate is positive:

    Traders holding long positions pay traders holding short positions.
*   If the funding rate is negative:

    Traders holding short positions pay traders holding long positions.

This mechanism ensures that if the price of the perpetual diverges from spot (due to demand imbalance), there is a financial incentive for traders to take the opposite side, pulling prices back in line.

***

**How It Works on Hyperliquid:**

*   Funding is calculated and settled every hour.

    This is more frequent than on many other platforms, helping to maintain tighter alignment with the index price.
* You only pay or receive funding if you’re holding a position at the funding timestamp.
* The amount you pay/receive is proportional to your position size and the prevailing funding rate.

***

**Why It Matters:**

Funding rate directly affects your profit and loss (PnL) over time. Even if price doesn’t move, a high funding rate can eat into returns (if you’re paying), or enhance gains (if you’re receiving).
