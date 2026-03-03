# Solana development

## Anchor

Anchor is a Rust framework for building Solana programs. It gives you:

- A clear structure for programs (instructions, state, errors)
- Built-in SPL token support (original Token Program and Token-2022)
- Client libraries in TypeScript and Rust
- Testing and deployment helpers

Many Solana programs are written with Anchor.

## SPL tokens

Solana has two main token standards:

- **Token Program (original)** – Basic mint, transfer, burn. Immutable and widely used.
- **Token-2022 (Token Extensions)** – Extends the original with extra features (e.g. transfer hooks, metadata). Use for new tokens when you need more than basics.

Both work with Anchor via `anchor-spl` and `spl-token`.

## Rust and tooling

Programs are written in **Rust**. Common crates: `solana-program`, `anchor-lang`, `anchor-spl`. You can develop in Solana Playground (browser) or locally with the Solana CLI and Anchor CLI.

## Resources

- Solana docs: solana.com/docs  
- Anchor book: book.anchor-lang.com  
- Solana Cookbook: solanacookbook.com  
- Program examples: solana.com/docs/programs/examples  
