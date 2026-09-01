# Liquidity Scores

<figure><img src="../.gitbook/assets/image (1).png" alt=""><figcaption></figcaption></figure>

Every perpetual market on Quote carries a liquidity score: a live 0-to-10 measure of current execution conditions. Quote computes a weighted average of liquidity and order flow across all markets, so a score tells you how a market compares with every other market on the venue right now, not in absolute terms.

### Where scores appear

Scores sit in the **Liquidity** column of the market selector, alongside price, funding, volume, and open interest. Each score is shown to one decimal with a color-coded ring around the value: the ring stays green near the top of the scale and shifts as conditions deteriorate, so thin markets stand out before you open the order form.

Scores update continuously as books and flow change. The number you see when you pick a market is the number the engine is working with at that moment.

### What a score tells you

* **10** is the best execution conditions on the venue right now: deep books and steady flow, where size can be worked with minimal impact.
* **0** is the worst: thin, one-sided, or stale conditions where even small orders move the price.
* Because the scale is relative to every other market on the venue, a score is a ranking, not an absolute grade. A 9 means the market is among the most liquid on the venue at this moment; it says nothing about how that compares with last week.

A high score is not a guarantee of a good fill, and a low score is not a reason a strategy will fail. It is a snapshot of the backdrop your order will execute against.

### How scores are computed

Each score blends two inputs across all markets:

* **Liquidity**: the depth and resilience of the order book.
* **Order flow**: the rate and balance of trading activity.

The exact inputs and weights are engine internals and are deliberately not documented, for the same reason child-order mechanics are not: publishing them would make the measure gameable. See Strategies Overview for how the engine uses this kind of microstructure data during execution.

### Using scores

* **Choosing a market.** When two markets would both express your view, the higher-scoring one will usually cost less to trade, especially at size.
* **Sizing an order.** A strategy working a large order in a low-scoring market has less depth to hide in. Consider smaller size, a longer window, or a more passive execution strategy.
* **Timing.** Scores move with conditions. A market that scores poorly mid-session may score well when its main trading hours come around, and a high score can decay fast in stressed markets. Check the score when you trade, not when you plan.

Scores describe conditions; they do not measure what your execution achieved. That is what Analytics is for: implementation shortfall, slippage, and fee benchmarks computed on your own fills.
