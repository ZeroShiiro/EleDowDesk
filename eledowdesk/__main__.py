"""Entry point for `python -m eledowdesk` and the `eledowdesk` script."""

from __future__ import annotations

import argparse
import asyncio
import logging
import sys


def setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )


async def async_main(args: argparse.Namespace) -> int:
    from eledowdesk.core.config import Config
    from eledowdesk.core.connection import ConnectionManager
    from eledowdesk.features.clipboard import ClipboardService
    from eledowdesk.features.file_transfer import FileTransferService
    from eledowdesk.features.mouse import MouseService

    config = Config.load()
    logging.getLogger("eledowdesk").info(
        "EleDowDesk v%s starting (device=%s)",
        __import__("eledowdesk").__version__,
        config.device_name,
    )

    conn = ConnectionManager(config)
    clipboard = ClipboardService(conn)
    files = FileTransferService(conn)
    mouse = MouseService(conn)

    await conn.start()
    await clipboard.start()
    await files.start()
    await mouse.start()

    logging.info("EleDowDesk is running. Press Ctrl+C to stop.")

    try:
        while True:
            await asyncio.sleep(3600)
    except asyncio.CancelledError:
        pass
    finally:
        await mouse.stop()
        await files.stop()
        await clipboard.stop()
        await conn.stop()

    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="EleDowDesk – clipboard, files & mouse sharing")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    setup_logging(args.verbose)

    try:
        raise SystemExit(asyncio.run(async_main(args)))
    except KeyboardInterrupt:
        print("\nShutting down…")
        raise SystemExit(0)


if __name__ == "__main__":
    main()
