# Solana core concepts

## Account model

All data on Solana is stored in "accounts," like a key-value store. Each database entry is an account. Accounts hold SOL, token balances, or program code and data.

## Transactions and instructions

Users interact with the network by sending **transactions** that contain one or more **instructions**. Each instruction is a specific operation. Execution logic lives in **programs** (smart contracts) deployed on the network.

## Programs

Programs are Solana’s smart contracts. They are stored in on-chain accounts and define instructions that can be invoked via transactions. Programs are usually written in Rust.

## Program Derived Addresses (PDAs)

PDAs are addresses derived deterministically from optional "seeds" and a program ID. They act like hashmap keys on-chain and let programs sign for those addresses. They have no private key.

## Cross Program Invocation (CPI)

CPI lets one program call another program’s instructions. This enables composability: programs can build on top of each other (e.g. a DEX calling the token program).

## Consensus

Solana uses **Proof of History (PoH)** together with **Proof of Stake (PoS)**. Validators order transactions and produce blocks. Rewards come from inflation and transaction fees and are distributed by stake and commission.
