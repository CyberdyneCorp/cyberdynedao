"""Domain errors for the DAO treasury context."""

from __future__ import annotations


class ChainReadError(RuntimeError):
    """A chain RPC call failed and we have no cached value to fall back on."""


class TreasuryUnconfiguredError(RuntimeError):
    """``DAO_TREASURY_ADDRESS`` isn't configured — caller should 503."""
