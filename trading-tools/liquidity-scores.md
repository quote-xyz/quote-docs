# Liquidity Scores

<figure><img src="../.gitbook/assets/image (1).png" alt=""><figcaption></figcaption></figure>

Every perpetual market on Quote carries a liquidity score: a live 1-to-10 measure of what it costs to trade that market right now, ranked against every other perpetual on the venue. 10 is the cheapest tier to trade. The score tells you how a market compares with the rest of the venue at this moment, not how it compares with its own past.

### Where scores appear

* **The market selector**, in the **Liquidity** column alongside price, funding, volume and open interest.
* **The market header**, under **Liquidity**. Hover it to see the market's rank among all ranked assets, and whether it is cheaper or more expensive to trade than usual for this time of day.
* **The Discover page**, whose **Liquidity** widget offers three views: **Movers** (how far each book sits from its own normal), **Ladder** (cheapest to cross, ranked across the venue) and **Mismatch** (where trading flow and book depth disagree).

The color around a score encodes absolute cost, not rank, so two markets with the same score can still differ.

### What a score tells you

* **10** is the cheapest tier to trade on the venue right now: deep books where size can be worked with little impact.
* **1** is the most expensive: thin books where even small orders move the price.
* Because the scale ranks every market against every other, a score is a ranking, not an absolute grade. A 9 means the market is among the cheapest to trade on the venue at this moment; it says nothing about how that compares with last week.

A high score is not a guarantee of a good fill, and a low score is not a reason a strategy will fail. It is a snapshot of the backdrop your order will execute against.

### How scores are computed

A score measures the cost of crossing the book: the round-trip spread you would pay to buy and sell a fixed amount at once, as Hyperliquid reports it for each perpetual. Scores cover perpetuals only. A market that trades in sessions, such as an equity or commodity, is scored only while its session is open.

The "usual" a market is compared with in the header is its own history at the same hour of day, so a market that is always quieter overnight is not flagged for it.

### Using scores

* **Choosing a market.** When two markets would both express your view, the higher-scoring one will usually cost less to trade, especially at size.
* **Sizing an order.** A strategy working a large order in a low-scoring market has less depth to hide in. Consider smaller size, a longer window, or a more passive [execution strategy](../strategies/overview.md).
* **Timing.** Scores move with conditions. A market that scores poorly at a quiet hour may score well when its main trading hours come round, and a high score can decay fast in stressed markets. Check the score when you trade, not when you plan.

Scores describe conditions; they do not measure what your execution achieved. That is what [Analytics](../guides/analytics.md) is for: benchmarks, slippage and fees computed on your own fills.
