"""Domain errors for the access-tier context."""

from __future__ import annotations


class InvalidWalletAddressError(ValueError):
    """The supplied wallet address isn't a valid EVM address — caller 400s."""


class AccessReadError(RuntimeError):
    """Reading the access NFT failed (RPC error) with no fallback — 502."""
