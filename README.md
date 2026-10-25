# EleDowDesk

**Clipboard, files, and mouse sharing between Windows and Linux.**

EleDowDesk lets you share clipboard contents, transfer files, and move mouse control between a Windows machine and a Linux machine (including elementary OS on Wayland). It uses both **Wi-Fi** and **Bluetooth**, automatically choosing the best available path.

## Features

- **Clipboard sync** — Copy on one machine, paste on the other (text + images)
- **File transfer** — Send files between devices with progress
- **Mouse sharing** — Control the other machine’s cursor when latency is good enough
- **Hybrid transport** — Prefers Wi-Fi (especially 5 GHz), assists/falls back with Bluetooth
- **Auto discovery & reconnect** — Finds the other device and reconnects when it returns

Nothing else. No keyboard sharing, no notifications, no media controls.

## Platforms

| OS | Notes |
|----|--------|
| **Windows 10 / 11** | Fully supported target |
| **Linux (Wayland)** | elementary OS, and other distributions with portal / libei support |
| **Linux (X11)** | Planned / partial |

Works with any combination of the above (desktop + laptop, two desktops, etc.).

## How it works

1. Install and run EleDowDesk on both machines.
2. Devices discover each other via mDNS (Wi-Fi) and Bluetooth LE.
3. First connection requires a short pairing code.
4. After pairing, a secure session is maintained.
5. Traffic is routed automatically:
   - Mouse movement & larger files → Wi-Fi (preferred)
   - Clipboard & small control messages → Wi-Fi or Bluetooth
6. Mouse sharing only activates when measured latency is acceptable.

## Status

**Early development** — Architecture defined, Python implementation in progress.

## Project Structure

```
EleDowDesk/
├── eledowdesk/
│   ├── core/           # Connection manager, protocol, session
│   ├── transport/      # Wi-Fi + Bluetooth
│   ├── features/       # clipboard, file, mouse
│   ├── platform/       # Windows & Linux adapters
│   └── ui/             # Tray application
├── protocol/           # Message definitions
├── tests/
├── README.md
└── pyproject.toml
```

## Requirements (target)

- Python 3.11+
- Windows 10/11 and/or Linux (Wayland preferred)
- Bluetooth adapter recommended on both machines

## License

MIT – see [LICENSE](LICENSE)
