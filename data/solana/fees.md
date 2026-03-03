# Solana fees

## Fee types

Solana has two main fee components:

1. **Base fee** – 5,000 lamports per signature (1 SOL = 1,000,000,000 lamports). Half is burned, half goes to validators. It pays for signature verification.

2. **Prioritization fee** – Optional. Formula: `(compute_unit_price × compute_unit_limit) / 1,000,000` lamports. 100% goes to validators. Higher prioritization fee improves your transaction’s scheduling priority when the network is busy.

## When fees are charged

Fees are charged whether the transaction **succeeds or fails**. If execution runs out of compute units or fails, you still pay.

## Typical cost

A normal transfer is around **0.000005 SOL** (a fraction of a cent). Solana is one of the cheapest major chains for users. During congestion, add a small prioritization fee to get included faster.
