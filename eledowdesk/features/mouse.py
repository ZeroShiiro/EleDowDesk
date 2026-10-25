"""Mouse sharing feature."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from eledowdesk.core.protocol import MsgType

if TYPE_CHECKING:
    from eledowdesk.core.connection import ConnectionManager

logger = logging.getLogger("eledowdesk.mouse")


class MouseService:
    """Captures local mouse or injects remote mouse events."""

    def __init__(self, conn: ConnectionManager) -> None:
        self.conn = conn
        self.active = False

        conn.on(MsgType.MOUSE_MOVE, self._on_move)
        conn.on(MsgType.MOUSE_BUTTON, self._on_button)
        conn.on(MsgType.MOUSE_SCROLL, self._on_scroll)
        conn.on(MsgType.MOUSE_ENABLE, self._on_enable)
        conn.on(MsgType.MOUSE_DISABLE, self._on_disable)

    async def start(self) -> None:
        if not self.conn.config.mouse_enabled:
            logger.info("Mouse sharing disabled")
            return
        logger.info("Mouse service started (inactive until latency is good)")

    async def stop(self) -> None:
        self.active = False

    async def enable(self) -> None:
        """Activate mouse sharing if latency allows."""
        if self.conn.session and self.conn.session.peer.latency_ms <= self.conn.config.mouse_latency_threshold_ms:
            self.active = True
            await self.conn.send(MsgType.MOUSE_ENABLE, {})
            logger.info("Mouse sharing enabled")
        else:
            logger.warning("Latency too high – mouse sharing not enabled")

    async def disable(self) -> None:
        self.active = False
        await self.conn.send(MsgType.MOUSE_DISABLE, {})
        logger.info("Mouse sharing disabled")

    async def send_move(self, dx: int, dy: int) -> None:
        if not self.active:
            return
        await self.conn.send(MsgType.MOUSE_MOVE, {"dx": dx, "dy": dy})

    async def send_button(self, button: int, pressed: bool) -> None:
        if not self.active:
            return
        await self.conn.send(MsgType.MOUSE_BUTTON, {"button": button, "pressed": pressed})

    async def send_scroll(self, dx: int, dy: int) -> None:
        if not self.active:
            return
        await self.conn.send(MsgType.MOUSE_SCROLL, {"dx": dx, "dy": dy})

    async def _on_move(self, msg_type: MsgType, payload: dict) -> None:
        # Platform adapter will inject relative movement
        dx = payload.get("dx", 0)
        dy = payload.get("dy", 0)
        logger.debug("Remote mouse move: %d, %d", dx, dy)

    async def _on_button(self, msg_type: MsgType, payload: dict) -> None:
        logger.debug("Remote mouse button: %s", payload)

    async def _on_scroll(self, msg_type: MsgType, payload: dict) -> None:
        logger.debug("Remote mouse scroll: %s", payload)

    async def _on_enable(self, msg_type: MsgType, payload: dict) -> None:
        self.active = True
        logger.info("Remote enabled mouse sharing")

    async def _on_disable(self, msg_type: MsgType, payload: dict) -> None:
        self.active = False
        logger.info("Remote disabled mouse sharing")
