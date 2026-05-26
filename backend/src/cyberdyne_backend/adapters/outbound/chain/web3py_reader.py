"""Web3Py-backed chain reader (Phase 5 — scaffolded, not yet active).

Lands in a follow-up PR once ``DAO_TREASURY_ADDRESS`` is registered on
Base and ``BASE_RPC_URL`` is wired into settings. The container won't
construct this reader until ``CHAIN_READER_PROVIDER=web3py``.

Why scaffolded rather than implemented now:
- The DAO multisig isn't deployed yet — there's nothing on-chain to read
- Pulling in ``web3.py`` (+ eth-account, eth-abi) is a meaningful dep
  bump we'd rather defer until it's load-bearing
- The fake reader covers every frontend code path

When this lands, it'll wrap:
- ``eth_call`` against the AAVE v3 PoolDataProvider (``getUserReserveData``)
- ``eth_call`` against the Uniswap v4 PositionManager (``positions``)
- Multicall to batch ERC-20 ``balanceOf`` + ``decimals`` lookups
- A Coingecko / Chainlink oracle for USD pricing

The shape returned matches ``FakeChainReader.read_snapshot`` exactly.
"""

from __future__ import annotations

from cyberdyne_backend.domain.dao_treasury import ChainReadError, TreasurySnapshot


class Web3PyChainReader:
    def __init__(
        self,
        *,
        rpc_url: str,
        aave_pool_data_provider: str,
        uniswap_position_manager: str,
        token_allowlist: tuple[str, ...] = (),
        timeout_s: float = 10.0,
    ) -> None:
        if not rpc_url:
            raise ValueError("rpc_url is required for Web3PyChainReader")
        self._rpc_url = rpc_url
        self._aave_pool_data_provider = aave_pool_data_provider
        self._uniswap_position_manager = uniswap_position_manager
        self._token_allowlist = token_allowlist
        self._timeout_s = timeout_s

    async def read_snapshot(self, treasury_address: str) -> TreasurySnapshot:  # pragma: no cover
        # Real implementation lands in a follow-up PR — see module docstring.
        raise ChainReadError(
            "Web3PyChainReader is scaffolded but not implemented yet — "
            "set CHAIN_READER_PROVIDER=fake until the real DAO multisig is registered"
        )
