"""Configuration handling for EleDowDesk."""

from __future__ import annotations

import json
import os
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path


def _default_config_dir() -> Path:
    if os.name == "nt":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    return base / "eledowdesk"


@dataclass
class Config:
    """Persistent application configuration."""

    device_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    device_name: str = field(default_factory=lambda: os.uname().nodename if hasattr(os, "uname") else "EleDowDesk")
    paired_devices: dict[str, dict] = field(default_factory=dict)

    # Network
    wifi_port: int = 47832
    enable_wifi: bool = True
    enable_bluetooth: bool = True

    # Features
    clipboard_enabled: bool = True
    file_transfer_enabled: bool = True
    mouse_enabled: bool = True
    mouse_latency_threshold_ms: float = 40.0

    # Behavior
    auto_accept_files: bool = False
    start_minimized: bool = True

    def save(self, path: Path | None = None) -> None:
        path = path or (_default_config_dir() / "config.json")
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            json.dump(asdict(self), f, indent=2)

    @classmethod
    def load(cls, path: Path | None = None) -> "Config":
        path = path or (_default_config_dir() / "config.json")
        if not path.exists():
            cfg = cls()
            cfg.save(path)
            return cfg
        with path.open(encoding="utf-8") as f:
            data = json.load(f)
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
