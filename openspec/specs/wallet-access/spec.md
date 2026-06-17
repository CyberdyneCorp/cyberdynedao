# wallet-access Specification

## Purpose

Server-side mirror of the CyberdyneAccessNFT capability set: a public
lookup of the aggregated access traits a wallet holds, so the chat agent's
`get_user_tier` tool and any future NFT-gated endpoint share one
aggregation instead of each re-reading the chain. (src:
adapters/inbound/api/wallet/router.py, domain/access, application/access)

## Requirements

### Requirement: Public wallet access-tier lookup

The system SHALL expose `GET /api/v1/wallet/{address}/access-tier`
returning the wallet's aggregated CyberdyneAccessNFT profile:
`hasAccessNft`, `tokenCount`, and a `traits` object of six booleans
(`learning`, `frontend`, `backend`, `blogCreator`, `admin`,
`marketplace`) ORed across every token the address holds. A malformed
address (not a `0x`-prefixed 40-hex string) SHALL return `400`. A read
failure SHALL return `502`.

#### Scenario: Malformed address is rejected

- GIVEN a path address that is not a valid EVM address
- WHEN the endpoint is called
- THEN the system SHALL respond `400` without reading the chain

#### Scenario: Known holder's traits are surfaced

- GIVEN a wallet whose access NFT grants the learning + blog-creator traits
- WHEN the endpoint is called
- THEN `hasAccessNft` is `true` and `traits.learning` / `traits.blogCreator`
  are `true` while ungranted traits are `false`

### Requirement: Conservative stub until the on-chain reader is wired

The system SHALL report "no access NFT" (`hasAccessNft: false`, all traits
`false`) for every address until a real on-chain reader is configured
(`BASE_RPC_URL` plus the access-NFT contract address), rather than
fabricating capabilities — an access/permissions lookup MUST never hand
out a grant that wasn't read from the chain.

#### Scenario: Unprovisioned environment denies by default

- GIVEN no access-NFT reader is configured
- WHEN any address is looked up
- THEN every trait is `false` and `hasAccessNft` is `false`
