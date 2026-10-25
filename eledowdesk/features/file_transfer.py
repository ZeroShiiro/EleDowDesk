"""File transfer feature."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING

from eledowdesk.core.protocol import MsgType

if TYPE_CHECKING:
    from eledowdesk.core.connection import ConnectionManager

logger = logging.getLogger("eledowdesk.file")


class FileTransferService:
    """Handles sending and receiving files."""

    def __init__(self, conn: ConnectionManager) -> None:
        self.conn = conn
        self._active_transfers: dict[str, dict] = {}

        conn.on(MsgType.FILE_OFFER, self._on_offer)
        conn.on(MsgType.FILE_ACCEPT, self._on_accept)
        conn.on(MsgType.FILE_REJECT, self._on_reject)
        conn.on(MsgType.FILE_CHUNK, self._on_chunk)
        conn.on(MsgType.FILE_COMPLETE, self._on_complete)
        conn.on(MsgType.FILE_ERROR, self._on_error)

    async def start(self) -> None:
        if not self.conn.config.file_transfer_enabled:
            logger.info("File transfer disabled")
            return
        logger.info("File transfer service started")

    async def stop(self) -> None:
        self._active_transfers.clear()

    async def send_file(self, path: Path) -> None:
        if not path.is_file():
            logger.error("Not a file: %s", path)
            return
        transfer_id = path.name  # simple for now
        size = path.stat().st_size
        await self.conn.send(
            MsgType.FILE_OFFER,
            {
                "id": transfer_id,
                "name": path.name,
                "size": size,
            },
        )
        logger.info("Offered file %s (%d bytes)", path.name, size)

    async def _on_offer(self, msg_type: MsgType, payload: dict) -> None:
        name = payload.get("name", "unknown")
        size = payload.get("size", 0)
        transfer_id = payload.get("id", name)
        logger.info("Incoming file offer: %s (%d bytes)", name, size)

        if self.conn.config.auto_accept_files:
            await self.conn.send(MsgType.FILE_ACCEPT, {"id": transfer_id})
        else:
            # UI will decide later
            logger.info("Waiting for user accept/reject for %s", name)

    async def _on_accept(self, msg_type: MsgType, payload: dict) -> None:
        logger.info("File accepted: %s", payload.get("id"))

    async def _on_reject(self, msg_type: MsgType, payload: dict) -> None:
        logger.info("File rejected: %s", payload.get("id"))

    async def _on_chunk(self, msg_type: MsgType, payload: dict) -> None:
        # Real implementation will write chunks to disk
        pass

    async def _on_complete(self, msg_type: MsgType, payload: dict) -> None:
        logger.info("File transfer complete: %s", payload.get("id"))

    async def _on_error(self, msg_type: MsgType, payload: dict) -> None:
        logger.error("File transfer error: %s", payload.get("error"))
