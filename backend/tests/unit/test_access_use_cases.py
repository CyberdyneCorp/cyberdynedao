"""Unit tests for the access-tier domain + use case (issue #7)."""

from __future__ import annotations

import pytest

from cyberdyne_backend.application.access import GetWalletAccess
from cyberdyne_backend.domain.access import (
    AccessTraits,
    InvalidWalletAddressError,
    WalletAccess,
    normalize_wallet_address,
)

pytestmark = pytest.mark.unit

_ADDR = "0x1111111111111111111111111111111111111111"


class _SpyReader:
    def __init__(self, result: WalletAccess) -> None:
        self.result = result
        self.seen: list[str] = []

    async def read_access(self, address: str) -> WalletAccess:
        self.seen.append(address)
        return self.result


class TestNormalizeWalletAddress:
    def test_lowercases_valid_address(self) -> None:
        assert normalize_wallet_address("0xABCDef" + "0" * 34) == "0xabcdef" + "0" * 34

    @pytest.mark.parametrize(
        "bad",
        [
            "",
            "0x123",  # too short
            "1" * 40,  # no 0x prefix
            "0x" + "z" * 40,  # non-hex
            "0x" + "1" * 41,  # too long
        ],
    )
    def test_rejects_malformed(self, bad: str) -> None:
        with pytest.raises(InvalidWalletAddressError):
            normalize_wallet_address(bad)


class TestAccessTraits:
    def test_any_false_when_empty(self) -> None:
        assert AccessTraits().any is False

    def test_any_true_with_one_grant(self) -> None:
        assert AccessTraits(blog_creator=True).any is True


class TestGetWalletAccess:
    async def test_passes_normalized_address_to_reader(self) -> None:
        reader = _SpyReader(WalletAccess.none(_ADDR))
        result = await GetWalletAccess(reader=reader).execute("0x" + "1" * 40)
        assert reader.seen == [_ADDR]
        assert result.has_access_nft is False

    async def test_rejects_bad_address_before_reading(self) -> None:
        reader = _SpyReader(WalletAccess.none(_ADDR))
        with pytest.raises(InvalidWalletAddressError):
            await GetWalletAccess(reader=reader).execute("not-an-address")
        assert reader.seen == []  # never hit the reader
