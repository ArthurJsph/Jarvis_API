import os
from typing import List
import time

# Simple in-memory cache for directory listings: { (path, recursive, max_depth) : (timestamp, results) }
_LIST_CACHE = {}
_CACHE_TTL = 5.0  # seconds

# Base directory that file operations are allowed to use
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


def _safe_path(path: str) -> str:
    # prevent directory traversal
    target = os.path.abspath(os.path.join(BASE_DIR, path))
    if not target.startswith(BASE_DIR):
        raise ValueError("Path outside of allowed directory")
    return target


def list_dir(path: str = "") -> List[str]:
    """Return immediate entries (files and dirs) in the given directory (non-recursive)."""
    p = _safe_path(path)
    if not os.path.exists(p):
        return []
    try:
        return os.listdir(p)
    except Exception:
        return []


def list_files(path: str = "", recursive: bool = False, max_depth: int = 3, refresh: bool = False) -> List[str]:
    """List files under `path` relative to project base.

    - If recursive is False, behaves like `list_dir`.
    - If recursive is True, walks directories up to `max_depth` levels using os.scandir for speed.
    - Results are relative paths from BASE_DIR.
    - A very small in-memory cache speeds up repeated calls; set `refresh=True` to bypass cache.
    """
    key = (os.path.normpath(path), bool(recursive), int(max_depth))
    now = time.time()
    if not refresh:
        cached = _LIST_CACHE.get(key)
        if cached and now - cached[0] < _CACHE_TTL:
            return list(cached[1])

    base = _safe_path(path)
    results = []
    if not os.path.exists(base):
        _LIST_CACHE[key] = (now, results)
        return results

    if not recursive:
        try:
            entries = os.listdir(base)
            _LIST_CACHE[key] = (now, entries)
            return entries
        except Exception:
            _LIST_CACHE[key] = (now, [])
            return []

    # iterative stack-based scandir for speed and low memory
    stack = [(base, 0)]
    base_len = len(base.rstrip(os.sep)) + 1
    while stack:
        current, depth = stack.pop()
        try:
            with os.scandir(current) as it:
                for entry in it:
                    try:
                        rel = entry.path[base_len:]
                    except Exception:
                        rel = entry.name
                    if entry.is_file(follow_symlinks=False):
                        results.append(rel)
                    elif entry.is_dir(follow_symlinks=False) and depth < max_depth:
                        stack.append((entry.path, depth + 1))
        except Exception:
            # ignore permission errors and continue
            continue

    _LIST_CACHE[key] = (now, list(results))
    return results


def read_file(path: str) -> str:
    p = _safe_path(path)
    if not os.path.exists(p):
        raise FileNotFoundError(path)
    with open(p, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def write_file(path: str, content: str, overwrite: bool = True) -> None:
    p = _safe_path(path)
    d = os.path.dirname(p)
    os.makedirs(d, exist_ok=True)
    if os.path.exists(p) and not overwrite:
        raise FileExistsError(path)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)


def delete_file(path: str) -> None:
    p = _safe_path(path)
    if os.path.isdir(p):
        # do not allow recursive delete for safety
        raise IsADirectoryError(path)
    if os.path.exists(p):
        os.remove(p)
