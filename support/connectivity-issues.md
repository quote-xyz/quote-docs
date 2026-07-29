# Connectivity Issues

Description: I can’t connect my wallet to Quote / I'm stuck in a loop when trying to sign / My wallet isn’t responding. What should I do?

If you’re experiencing issues connecting your wallet to Quote, such as a recursive "Establish Connection" loop, failed transaction signing, or your wallet extension not loading, try the following troubleshooting steps.

#### Quick fixes <a href="#quick-fixes" id="quick-fixes"></a>

* Update your wallet extension to the latest version and make sure it’s enabled
* Hard refresh your browser (on most browsers: Ctrl+Shift+R or Cmd+Shift+R) and clear cache
* Disconnect and reconnect your wallet
* Switch networks (e.g., to Ethereum) and then switch back to Arbitrum if you’re trying to deposit USDC on Arbitrum or the HyperEVM if you’re trying to use the HyperEVM

#### Wallet specific compatibility issues with Quote <a href="#wallet-specific-issues" id="wallet-specific-issues"></a>

* Coinbase: Users on mobile may face connection problems. Try using the Coinbase Chrome extension instead
* Metamask: Some users face issues with MetaMask on the HyperEVM. If this persists, consider migrating to a more compatible wallet like Rabby
* Trezor forbidden keypath error: This is related to privacy settings within Trezor. In Trezor Suite's Security / Safety Checks change from "Strict" to "Prompt"
* Ledger "Transfer Failed" error on the HyperEVM: Update to the latest Ledger software/firmware
* Reinstall your wallet extension: Make sure you have your seed phrase or private key backed up before doing this

Lastly, you can try switching to Rabby Wallet, which often works more smoothly with Quote. Your trades, history, and address remain the same even if you use a new wallet extension. [https://support.rabby.io/hc/en-us/articles/11477459275279-How-to-migrate-from-other-wallets-to-Rabby-Wallet](https://support.rabby.io/hc/en-us/articles/11477459275279-How-to-migrate-from-other-wallets-to-Rabby-Wallet)
