# Smart contracts and Solidity

## What is a smart contract?

A smart contract is code and state stored at an address on the blockchain. It has functions that anyone can call (within the rules of the code). Contracts can hold tokens, enforce logic, and interact with other contracts. They run on the EVM.

## Solidity

Solidity is the main language for writing EVM smart contracts. A contract defines:

- **State variables** – Stored on-chain (e.g. balances, owner)
- **Functions** – Logic that reads or changes state (e.g. transfer, mint)
- **Modifiers and access control** – e.g. only the owner can call a function

Contracts are compiled to bytecode and deployed. Once deployed, the code is immutable unless the contract has upgradeability built in.

## Gas and contracts

Every operation in a contract costs gas. Storage writes are expensive; reads are cheaper. Optimizing gas matters for heavy or popular contracts. Running out of gas reverts the transaction; you still pay for the gas used.

## Resources

- Solidity docs: docs.soliditylang.org  
- Ethereum dev docs: ethereum.org/developers  
- Tooling: Hardhat, Foundry, Remix  
