# EleDowDesk

**Clipboard, files, and mouse sharing between elementary OS and Windows.**

EleDowDesk connects a Windows PC and an elementary OS laptop using both **Wi-Fi** and **Bluetooth**. It automatically chooses the best available path.

## Features

- **Clipboard sync** — Copy on one machine, paste on the other (text + images)
- **File transfer** — Send files between devices with progress
- **Mouse sharing** — Control the other machine’s cursor when latency is good enough
- **Hybrid transport** — Prefers Wi-Fi (especially 5 GHz), assists/falls back with Bluetooth
- **Auto discovery & reconnect** — Finds the other device and reconnects when it returns

Nothing else. No keyboard sharing, no notifications, no media controls.

## Platforms

| Side         | OS                        | Role                            |
|--------------|---------------------------|---------------------------------|
| Primary host | Windows 10 / 11           | PC (Preferrably Ethernet)       |
| Mobile       | elementary OS (Wayland)   | Laptop                          |

## How it works

1. Both machines run the EleDowDesk daemon + tray.
2. They discover each other via mDNS (Wi-Fi) and Bluetooth LE.
3. First connection requires a short pairing code.
4. After pairing, a secure session is maintained.
5. Traffic is routed automatically:
   - Mouse movement & larger files → Wi-Fi (preferred)
   - Clipboard & small control messages → Wi-Fi or Bluetooth
6. Mouse sharing only activates when measured latency is acceptable.

## Status

**Early development** — Architecture defined, Python implementation starting.

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
- Windows 10/11
- elementary OS 7/8 (Wayland)
- Bluetooth adapter on both machines (recommended)

## License

MIT – see [LICENSE](LICENSE)
