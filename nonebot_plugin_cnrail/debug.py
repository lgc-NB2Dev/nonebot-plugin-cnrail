import json
import time
from pathlib import Path
from typing import Any

ROOT_DEBUG_DIR = Path.cwd() / "debug"
DEBUG_DIR = ROOT_DEBUG_DIR / "cnrail"


def is_debug_mode():
    return ROOT_DEBUG_DIR.exists()


def write_debug_file(filename: str, content: Any, force_write: bool = False):
    if (not force_write) and (not is_debug_mode()):
        return
    if not DEBUG_DIR.exists():
        DEBUG_DIR.mkdir(parents=True)
    filename = filename.format(time=round(time.time() * 1000))
    path = DEBUG_DIR / filename
    if isinstance(content, (bytes, bytearray)):
        path.write_bytes(content)
        return
    if not isinstance(content, str):
        try:
            content = json.dumps(content, ensure_ascii=False)
        except Exception:
            content = str(content)
    path.write_text(content, "u8")
