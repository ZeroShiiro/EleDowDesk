"""Message protocol definitions for EleDowDesk."""

from __future__ import annotations

from enum import IntEnum
from typing import Any

import msgpack


class MsgType(IntEnum):
    """Message types used on the wire."""

    # Control
    HELLO = 1
    PAIR_REQUEST = 2
    PAIR_ACCEPT = 3
    PAIR_REJECT = 4
    PING = 5
    PONG = 6
    GOODBYE = 7

    # Clipboard
    CLIPBOARD_TEXT = 20
    CLIPBOARD_IMAGE = 21

    # Files
    FILE_OFFER = 30
    FILE_ACCEPT = 31
    FILE_REJECT = 32
    FILE_CHUNK = 33
    FILE_COMPLETE = 34
    FILE_ERROR = 35

    # Mouse
    MOUSE_MOVE = 40
    MOUSE_BUTTON = 41
    MOUSE_SCROLL = 42
    MOUSE_ENABLE = 43
    MOUSE_DISABLE = 44


def pack(msg_type: MsgType, payload: dict[str, Any] | None = None) -> bytes:
    """Serialize a message to bytes."""
    data = {
        "t": int(msg_type),
        "p": payload or {},
    }
    return msgpack.packb(data, use_bin_type=True)


def unpack(raw: bytes) -> tuple[MsgType, dict[str, Any]]:
    """Deserialize bytes into (message type, payload)."""
    data = msgpack.unpackb(raw, raw=False)
    msg_type = MsgType(data["t"])
    payload = data.get("p") or {}
    return msg_type, payload
