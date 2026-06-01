"""Local-filesystem implementation of ``FileStorage``.

Writes objects under ``<root>/<category>/<stored_filename>``. Every path
is resolved and checked to live within the root before any I/O, so a
crafted category or filename can never escape the storage directory
(defence in depth — the use case already mints a UUID stored name).

Blocking file I/O runs in a thread via ``asyncio.to_thread`` so the event
loop isn't stalled on large writes.
"""

from __future__ import annotations

import asyncio
from pathlib import Path

from cyberdyne_backend.domain.uploads import UploadCategory


class LocalFileStorage:
    def __init__(self, root: str | Path) -> None:
        self._root = Path(root).resolve()
        self._root.mkdir(parents=True, exist_ok=True)

    def _resolve_within_root(self, category: str, stored_filename: str) -> Path:
        candidate = (self._root / category / stored_filename).resolve()
        if not candidate.is_relative_to(self._root):
            raise ValueError(f"resolved path escapes storage root: {candidate}")
        return candidate

    async def save(self, *, category: UploadCategory, stored_filename: str, data: bytes) -> str:
        target = self._resolve_within_root(category.value, stored_filename)

        def _write() -> None:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)

        await asyncio.to_thread(_write)
        return f"{category.value}/{stored_filename}"

    async def delete(self, relative_path: str) -> None:
        # relative_path is "<category>/<stored_filename>".
        parts = relative_path.split("/", 1)
        if len(parts) != 2:
            return
        target = self._resolve_within_root(parts[0], parts[1])

        def _unlink() -> None:
            target.unlink(missing_ok=True)

        await asyncio.to_thread(_unlink)
