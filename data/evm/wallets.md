# EVM wallets and addresses

## Address format

Ethereum addresses start with **0x** followed by 40 hexadecimal characters (0–9, A–F), 42 characters total. They are not case-sensitive. Example: 0x742d35Cc6634C0532925a3b844Bc454e4438f44e.

## One address, many chains

The same address works on **all EVM-compatible networks**: Ethereum, Base, Arbitrum, Polygon, BSC, etc. You don’t need a new wallet per chain. Always confirm you’re on the right network before sending or approving transactions.

## MetaMask and EOAs

**MetaMask** is a common wallet for EVM. It creates **Externally Owned Accounts (EOAs)**: accounts controlled by a private key. You can view and copy your address in the app. Never share your seed phrase or private key.

## Contract accounts vs EOAs

- **EOA** – You control it with a key; it can send txs and hold ETH/tokens.
- **Contract account** – Controlled by code (smart contract); no private key. Some wallets let you “upgrade” an EOA to a smart account for extra features (e.g. batched txs).

## Sending and receiving

To receive: share your 0x address. To send: enter the recipient’s 0x address and choose amount and network. Wrong network = funds can be lost, so double-check.
