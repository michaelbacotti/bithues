# Bithues NFT Collection — "Reader's Edition"

## Concept

Limited NFT collection celebrating reading culture. Each NFT is a unique, generative "reading scene" that early Bithues supporters can mint for free (gas only).

## Collection Details

| | |
|---|---|
| **Name** | Bithues Reader's Edition |
| **Size** | 100 unique NFTs |
| **Network** | Base (Coinbase L2) |
| **Contract Standard** | ERC-721 |
| **Mint Price** | Free (pay gas only, ~$0.01-0.05 each) |
| **Max per wallet** | 5 |

## Trait Categories

| Category | Options |
|---|---|
| **Scene** | Cozy corner, Library, Café, Beach, Forest, Study |
| **Book Style** | Classic hardcover, Modern paperback, Ancient tome, Modern tablet |
| **Time of Day** | Dawn, Day, Dusk, Night |
| **Mood** | Serene, Focused, Adventurous, Romantic |
| **Accent** | Coffee cup, Candle, Plant, Globe, Typewriter |
| **Rarity** | Common, Uncommon, Rare, Legendary |

## Roadmap

- [x] Design NFT collection concept
- [ ] Generate 100 unique trait combinations
- [ ] Write Solidity smart contract
- [ ] Build minting page (integrates into Bithues)
- [ ] Deploy contract to Base
- [ ] Test mint flow
- [ ] Launch

## Technical Stack

- **Images**: Generated via AI, stored on IPFS
- **Contract**: OpenZeppelin ERC-721 on Base
- **Minting Site**: Subdomain `nft.bithues.com`
- **Wallet Connect**: RainbowKit + wagmi
- **Storage**: Pinata for IPFS

## Estimated Cost

| Item | Cost |
|---|---|
| IPFS storage (100 imgs + metadata) | ~$0 |
| Smart contract deployment | ~$5-10 (Base gas) |
| Minting gas (100 NFTs) | ~$1-5 |
| **Total** | **~$10-15** |
