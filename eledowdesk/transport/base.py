"""Base transport interface."""

from __future__ import annotations

import abc
import asyncio
from typing import Callable, Awaitable


class Transport(abc.ABC):
    """Abstract transport (Wi-Fi or Bluetooth)."""

    @abc.abstractmethod
    async def start(self) -> None:
        ...

    @abc.abstractmethod
    async def stop(self) -> None:
        ...

    @abc.abstractmethod
    async def send(self, data: bytes) -> None:
        ...

    def on_data(self, callback: Callable[[bytes], Awaitable[None]]) -> None:
        self._on_data = callback

    def on_peer_found(self, callback: Callable[[str, str], Awaitable[None]]) -> None:
        """callback(device_id, address)"""
        self._on_peer_found = callback
