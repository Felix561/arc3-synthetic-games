"""Local launcher and data-only checksum verification."""

import argparse
import json
import threading
import webbrowser

from .dataset import catalog, verify_dataset


def main():
    parser = argparse.ArgumentParser(prog="arc3-synthetic-games")
    commands = parser.add_subparsers(dest="command", required=True)
    play = commands.add_parser("play", help="Start the local browser player")
    play.add_argument("--port", type=int, default=8780)
    play.add_argument("--no-browser", action="store_true")
    commands.add_parser("verify", help="Check native file identities without executing games")
    commands.add_parser("list", help="List all native game IDs")
    args = parser.parse_args()
    if args.command == "verify":
        print(json.dumps(verify_dataset(), indent=2))
    elif args.command == "list":
        for game in catalog()["games"]:
            print(f"{game['game_id']}  {game['title']}")
    else:
        if not 1 <= args.port <= 65535:
            parser.error("port must be between 1 and 65535")
        import uvicorn

        from .server import create_app

        app = create_app(args.port)
        print(f"ARC3 Synthetic Games · http://127.0.0.1:{args.port}", flush=True)
        if not args.no_browser:
            timer = threading.Timer(1.5, lambda: webbrowser.open(f"http://127.0.0.1:{args.port}"))
            timer.daemon = True
            timer.start()
        uvicorn.run(app, host="127.0.0.1", port=args.port, access_log=False, log_level="warning")
    return 0
