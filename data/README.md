# RAG data per field

- **solana/** – Add Solana-related docs here (e.g. from [Solana Cookbook](https://solanacookbook.com/) or official docs). Supported: `.md`, `.txt`, `.pdf`.
- **evm/** – Add EVM/Ethereum-related docs here (e.g. Ethereum docs, Solidity guides). Same formats.

After adding files, run: `python -m app.rag.ingest`

If these folders are empty, the chatbot still runs but retrieval will be empty until you add and ingest docs.
