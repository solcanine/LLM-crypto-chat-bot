# EVM and Ethereum basics

## Ethereum Virtual Machine (EVM)

The EVM is a virtual machine that runs the same code on every Ethereum node. Ethereum is a **distributed state machine**: it keeps track of accounts, balances, and smart contract state. The EVM runs contract code step by step using opcodes (e.g. ADD, SSTORE). Each operation costs **gas**.

## Gas

Gas measures how much work a transaction or contract call does. Each opcode has a gas cost. You set:

- **gasLimit** – Max gas you allow; execution stops if it’s exceeded (changes revert, but gas is still used)
- **maxFeePerGas** / **maxPriorityFeePerGas** – How much you pay per gas (in gwei; 1 gwei = 0.000000001 ETH)

Fee paid = gas used × effective gas price. High demand on mainnet means higher gas prices.

## Accounts

- **Externally Owned Accounts (EOAs)** – Controlled by a private key. Can send transactions and hold ETH.
- **Contract accounts** – Controlled by code (smart contract). Have an address but no private key; they run when someone calls them.

## Transactions

A transaction is a signed message that changes state. It includes sender, recipient, value (ETH), optional calldata for contract calls, nonce, and gas parameters. Transactions are broadcast to the network and included in blocks by validators.
