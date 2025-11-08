#!/usr/bin/env python3
"""Lightweight installer for Jarvis Remote Assistant (API-focused).

This simplified installer creates basic folders, copies `.env.example` to
`.env` (if missing), installs Python requirements and creates simple launcher
scripts to run the FastAPI server with uvicorn.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


def ensure_dirs():
    base = Path(__file__).parent
    for d in (base / "data", base / "logs", base / "web" / "static"):
        d.mkdir(parents=True, exist_ok=True)
        print(f"✅ {d} OK")


def ensure_env():
    base = Path(__file__).parent
    ex = base / ".env.example"
    dst = base / ".env"
    if not ex.exists():
        print("⚠️ .env.example not found; please create one from the repository or provide environment variables.")
        return
    if not dst.exists():
        shutil.copy(ex, dst)
        print("✅ .env created from .env.example — edit it with real secrets before running")
    else:
        print("✅ .env already exists (skipping)")


def install_requirements():
    req = Path(__file__).parent / "requirements.txt"
    if not req.exists():
        print("⚠️ requirements.txt not found — install dependencies manually")
        return
    print("� Installing requirements (this may take a while)...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(req)])


def create_launchers():
    base = Path(__file__).parent
    if os.name == "nt":
        bat = base / "jarvis_server.bat"
        bat.write_text(f"@echo off\ncd /d \"{base}\"\npython -m uvicorn core.remote_api:app --host 0.0.0.0 --port 8000\n")
        print(f"✅ {bat} created")
    else:
        sh = base / "jarvis_server"
        sh.write_text(f"#!/bin/sh\ncd \"{base}\"\npython3 -m uvicorn core.remote_api:app --host 0.0.0.0 --port 8000\n")
        sh.chmod(0o755)
        print(f"✅ {sh} created")


def main():
    print("Jarvis Remote Assistant - installer")
    ensure_dirs()
    ensure_env()
    try:
        install_requirements()
    except subprocess.CalledProcessError:
        print("⚠️ Failed to install requirements; please run 'pip install -r requirements.txt' manually")
    create_launchers()
    print("\nInstalação básica concluída. Edite .env e rode o servidor com: python main.py")


if __name__ == "__main__":
    main()