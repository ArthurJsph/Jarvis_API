#!/usr/bin/env python3
"""Entry point for Jarvis Remote Assistant.

By default this script runs the FastAPI server (via uvicorn). You can
override host/port via CLI options or environment variables.
"""

import argparse
import os
import sys

from config import HOST, PORT


def run_server(host: str, port: int, reload: bool = False):
    try:
        import uvicorn
    except Exception:
        print("uvicorn is not installed. Please run: pip install -r requirements.txt")
        sys.exit(1)

    # Import app lazily to avoid heavy imports on non-server flows
    from core.remote_api import app

    uvicorn.run(app, host=host, port=port, reload=reload)


def main():
    parser = argparse.ArgumentParser(description="Jarvis Remote Assistant - server runner")
    parser.add_argument("--host", default=os.getenv("HOST", HOST), help="Host to bind")
    parser.add_argument("--port", type=int, default=int(os.getenv("PORT", PORT)), help="Port")
    parser.add_argument("--reload", action="store_true", help="Enable uvicorn autoreload (dev only)")

    args = parser.parse_args()
    run_server(args.host, args.port, reload=args.reload)


if __name__ == "__main__":
    main()