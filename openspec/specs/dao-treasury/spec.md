# dao-treasury Specification

## Purpose

Expose a public, eventually-consistent snapshot of the DAO treasury
(on-chain token balances, Aave + Uniswap v4 positions, USD total) plus holder
count. (src: adapters/inbound/api/dao/router.py, domain/dao_treasury)

## Requirements

### Requirement: Treasury overview

The system SHALL expose unauthenticated `GET /api/v1/dao/overview` returning a
snapshot (treasury address, chain id, snapshot time, token balances, Aave
positions, Uniswap positions, and `totalUsdValue`) plus the holder count.
`totalUsdValue` SHALL equal the sum of token USD values, net Aave (supplied −
borrowed), and Uniswap position USD values. A missing treasury-address
configuration SHALL return `503`; an on-chain read failure with no cache SHALL
return `502`.

#### Scenario: Read the overview

- GIVEN the treasury address is configured and chain reads succeed
- WHEN a client GETs `/api/v1/dao/overview`
- THEN a snapshot with `totalUsdValue` and the holder count is returned

#### Scenario: Unconfigured treasury

- GIVEN no treasury address is configured
- WHEN a client GETs `/api/v1/dao/overview`
- THEN the system SHALL respond `503`
