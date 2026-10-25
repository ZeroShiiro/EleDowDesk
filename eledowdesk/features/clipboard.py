"""Clipboard synchronization feature."""

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING

from eledowdesk.core.protocol import MsgType

if TYPE_CHECKING:
    from eledowdesk.core.connection import ConnectionManager

logger = logging.getLogger("eledowdesk.clipboard")


class ClipboardService:
    """Watches local clipboard and syncs with remote peer."""

    def __init__(self, conn: ConnectionManager) -> None:
        self.conn = conn
        self._last_local_text: str | None = None
        self._ignore_until: float = 0.0
        self._task: asyncio.Task | None = None

        # Register handlers
        conn.on(MsgType.CLIPBOARD_TEXT, self._on_remote_text)
        conn.on(MsgType.CLIPBOARD_IMAGE, self._on_remote_image)

    async def start(self) -> None:
        if not self.conn.config.clipboard_enabled:
            logger.info("Clipboard feature disabled")
            return
        self._task = asyncio.create_task(self._watch_loop())
        logger.info("Clipboard service started")

    async def stop(self) -> None:
        if self._task:
            self._task.cancel()
            self._task = None

    async def _watch_loop(self) -> None:
        """Poll local clipboard for changes (platform adapter will replace this)."""
        while True:
            try:
                # Placeholder – real implementation uses platform-specific watchers
                await asyncio.sleep(0.5)
            except asyncio.CancelledError:
                break
            except Exception:
                logger.exception("Clipboard watch error")
                await asyncio.sleep(1.0)

    async def send_text(self, text: str) -> None:
        if text == self._last_local_text:
            return
        self._last_local_text = text
        await self.conn.send(MsgType.CLIPBOARD_TEXT, {"text": text})
        logger.debug("Sent clipboard text (%d chars)", len(text))

    async def _on_remote_text(self, msg_type: MsgType, payload: dict) -> None:
        text = payload.get("text", "")
        logger.info("Received remote clipboard text (%d chars)", len(text))
        # Platform adapter will set the local clipboard
        # Temporary ignore window to avoid echo loops
        import time
        self._ignore_until = time.monotonic() + 0.8
        self._last_local_text = text

    async def _on_remote_image(self, msg_type: MsgType, payload: dict) -> None:
        logger.info("Received remote clipboard image (stub)")
