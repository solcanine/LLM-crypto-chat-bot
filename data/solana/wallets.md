# Solana wallets and keypairs

## Keypairs

A Solana keypair has a **secret key** (private key) and a **public key** (wallet address). The private key controls the wallet; never share it or commit it to git. The public key is safe to share (it’s your address).

## Solana CLI

- Create a keypair: `solana-keygen new` (optionally `--outfile my-wallet.json`)
- Set default keypair: `solana config set --keypair ~/my-wallet.json`
- Check balance: `solana balance`
- Use a different cluster: `solana config set --url devnet` or `mainnet-beta`

## Phantom and other wallets

**Phantom** is a popular browser and mobile wallet for Solana. You can:

- Import a CLI keypair: in Phantom choose "Import Private Key" and paste the JSON array from your keypair file
- Export for CLI: use your seed phrase with `solana-keygen recover` and the correct BIP44 path (e.g. m/44'/501'/0'/0')

Other wallets (Solflare, Backpack, etc.) also support the same keypair/seed format.

## Security

- Dev/test: file-based wallet, no passphrase is common
- Mainnet with real funds: use a passphrase, encrypted disk, or a hardware wallet
- Never expose your seed phrase or private key
