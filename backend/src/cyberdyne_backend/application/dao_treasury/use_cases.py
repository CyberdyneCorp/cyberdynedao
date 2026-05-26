"""DAO treasury use cases — bundled overview for the DaoView."""

from __future__ import annotations

from dataclasses import dataclass

from cyberdyne_backend.domain.dao_treasury import (
    ChainReaderPort,
    DaoOverview,
    TreasuryUnconfiguredError,
)


@dataclass(slots=True)
class GetDaoOverview:
    """Returns the bundled treasury snapshot + governance metadata."""

    reader: ChainReaderPort
    treasury_address: str | None
    holders: int = 0

    async def execute(self) -> DaoOverview:
        if not self.treasury_address:
            raise TreasuryUnconfiguredError(
                "DAO_TREASURY_ADDRESS is not configured — cannot read snapshot"
            )
        snapshot = await self.reader.read_snapshot(self.treasury_address)
        return DaoOverview(snapshot=snapshot, holders=self.holders)
