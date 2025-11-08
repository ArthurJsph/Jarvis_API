#!/usr/bin/env python3
"""Minimal setup helper for Jarvis Remote Assistant.

This script performs lightweight project setup tasks. It is intentionally
small because `install.py` handles the main installation flow.
"""

from pathlib import Path
import os


def ensure_dirs():
    base = Path(__file__).parent
    for d in (base / "data", base / "logs", base / "web" / "static"):
        d.mkdir(parents=True, exist_ok=True)
        print(f"✅ {d} OK")


def print_run_instructions():
    print("Setup minimal concluído.")
    print("Para rodar o servidor localmente:")
    print("  python main.py")
    print("Ou use o launcher: jarvis_server(.bat) gerado pelo install.py")


def main():
    ensure_dirs()
    print_run_instructions()


if __name__ == '__main__':
    main()