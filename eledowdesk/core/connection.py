"""Connection manager – owns discovery, pairing, and active sessions."""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Callable, Awaitable

from eledowdesk.core.config import Config
from eledowdesk.core.protocol import MsgType, pack, unpack

logger = logging.getLogger("eledowdesk.connection")


class TransportKind(Enum):
    WIFI = auto()
    BLUETOOTH = auto()


class ConnectionState(Enum):
    DISCONNECTED = auto()
    DISCOVERING = auto()
    PAIRING = auto()
    CONNECTED = auto()


@dataclass
class Peer:
    device_id: str
    name: str
    transport: TransportKind
    address: str  # IP or BT address
    latency_ms: float = 999.0
    last_seen: float = 0.0


@dataclass
class Session:
    peer: Peer
    reader: asyncio.StreamReader | None = None
    writer: asyncio.StreamWriter | None = None
    state: ConnectionState = ConnectionState.CONNECTED
    mouse_active: bool = False


MessageHandler = Callable[[MsgType, dict], Awaitable[None]]


class ConnectionManager:
    """Central connection + session manager."""

    def __init__(self, config: Config) -> None:
        self.config = config
        self.state = ConnectionState.DISCONNECTED
        self.session: Session | None = None
        self._handlers: dict[MsgType, list[MessageHandler]] = {}
        self._tasks: list[asyncio.Task] = []
        self._running = False

    def on(self, msg_type: MsgType, handler: MessageHandler) -> None:
        self._handlers.setdefault(msg_type, []).append(handler)

    async def start(self) -> None:
        if self._running:
            return
        self._running = True
        self.state = ConnectionState.DISCOVERING
        logger.info("ConnectionManager started (device_id=%s)", self.config.device_id)
        # Discovery and transport loops will be added next
        self._tasks.append(asyncio.create_task(self._heartbeat_loop()))

    async def stop(self) -> None:
        self._running = False
        for t in self._tasks:
            t.cancel()
        self._tasks.clear()
        if self.session and self.session.writer:
            try:
                await self.send(MsgType.GOODBYE, {})
                self.session.writer.close()
                await self.session.writer.wait_closed()
            except Exception:
                pass
        self.session = None
        self.state = ConnectionState.DISCONNECTED
        logger.info("ConnectionManager stopped")

    async def send(self, msg_type: MsgType, payload: dict | None = None) -> None:
        if not self.session or not self.session.writer:
            logger.warning("Cannot send %s – no active session", msg_type.name)
            return
        data = pack(msg_type, payload)
        # Simple length-prefixed framing
        header = len(data).to_bytes(4, "big")
        self.session.writer.write(header + data)
        await self.session.writer.drain()

    async def _dispatch(self, msg_type: MsgType, payload: dict) -> None:
        for handler in self._handlers.get(msg_type, []):
            try:
                await handler(msg_type, payload)
            except Exception:
                logger.exception("Handler error for %s", msg_type.name)

    async def _heartbeat_loop(self) -> None:
        while self._running:
            if self.session and self.session.state == ConnectionState.CONNECTED:
                try:
                    await self.send(MsgType.PING, {})
                except Exception:
                    logger.warning("Ping failed – connection may be lost")
            await asyncio.sleep(5.0)

    # --- Placeholder methods (to be implemented with transports) ---

    async def start_discovery(self) -> None:
        """Begin Wi-Fi mDNS + Bluetooth LE discovery."""
        logger.info("Discovery started (stub)")

    async def connect_to(self, peer: Peer) -> None:
        """Establish session with a discovered peer."""
        logger.info("Connecting to %s via %s (stub)", peer.name, peer.transport.name)

    async def accept_incoming(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        """Handle an incoming Wi-Fi connection."""
        logger.info("Incoming connection (stub)")
