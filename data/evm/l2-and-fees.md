# EVM Layer 2s and fees

## Why L2s exist

Ethereum mainnet (L1) can be slow and expensive when busy. Layer 2s (L2s) run on top of Ethereum and move computation off L1 while still settling on it. That gives **much lower fees** (often 10–100x cheaper) and often faster confirmation.

## Types of L2s

- **Optimistic rollups** (Arbitrum, Base, Optimism) – Assume transactions are valid and use a challenge period for fraud proofs. EVM-compatible; withdrawals to L1 often take ~7 days.
- **ZK rollups** (zkSync, Starknet, Polygon zkEVM) – Use zero-knowledge proofs. Withdrawals can be faster (hours). Ecosystem and tooling vary by chain.

## Fee comparison (typical)

- **Ethereum L1** – Can be $1–10+ per simple tx when busy; swaps and contracts cost more.
- **Base** – Often under $0.01; some flows (e.g. USDC with Coinbase) can be free.
- **Arbitrum, Optimism** – Often a few cents per tx.
- **Polygon** – Very low (fractions of a cent); often treated like an L2 though it’s a sidechain.
- **zkSync Era, others** – Often in the cents range.

L2s batch many transactions and post compressed data to L1, so the cost is split across users—hence the big fee drop.

## Same address everywhere

Your Ethereum address (0x...) works on all EVM chains. You can use the same wallet on mainnet, Base, Arbitrum, Polygon, etc. Always send assets only on the correct network (e.g. don’t send Base ETH to an Arbitrum-only app).
