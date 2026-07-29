# Agent Wallet

The Quote platform utilizes an Agentic (API) Wallet system to facilitate interactions with self-custodial wallets. This architecture separates signing authority from asset custody, allowing for seamless, "one-click" trading. An Agent Wallet must be pre-approved by the user and has a limited set of actions that can be performed without requiring an additional user signature.&#x20;

* Users maintain ownership while granting limited permissions to the Agent Wallet
* Agent operates as an additional signer with scoped policies
* Users retain ultimate control and can revoke agent access at any time



In particular, the Quote Agent Wallet **has the following limited permissions**

* Trade perps (with perps balance)
* Trade spot (with spot balance)
* Swap spot tokens

While the Quote Agent wallet **cannot**:

* Withdraw funds
* Transfer funds
* Deposit (via Arbitrum or HyperEVM)
* Transact on the HyperEVM

### Resources

{% columns %}
{% column width="41.66666666666667%" %}
{% embed url="https://hyperliquid.gitbook.io/hyperliquid-docs/" %}
{% endcolumn %}

{% column width="16.666666666666668%" %}

{% endcolumn %}

{% column width="41.66666666666664%" %}
{% embed url="https://hyperliquid.gitbook.io/hyperliquid-docs/hyperevm" %}
{% endcolumn %}
{% endcolumns %}
