import os
import logging
from fastapi import FastAPI, HTTPException, Body, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, PlainTextResponse, RedirectResponse
from collections import deque
from config import LOG_FILE, LOG_LEVEL, API_KEY
from pydantic import BaseModel
from dotenv import load_dotenv

from .security import APIKeyAndRateLimitMiddleware
from .file_manager import list_dir, list_files, read_file, write_file, delete_file

load_dotenv()

app = FastAPI(title="Jarvis Remote Assistant API")

# Configure file logging so runtime logs are available to the UI / /logs endpoint.
# This attaches a FileHandler to the root logger and common uvicorn loggers.
try:
    LOG_LEVEL_NAME = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
except Exception:
    LOG_LEVEL_NAME = logging.INFO

formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s - %(message)s")
file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_handler.setFormatter(formatter)
file_handler.setLevel(LOG_LEVEL_NAME)

root_logger = logging.getLogger()
root_logger.setLevel(LOG_LEVEL_NAME)
# Avoid adding duplicate file handlers
if not any(isinstance(h, logging.FileHandler) and getattr(h, 'baseFilename', None) == os.path.abspath(LOG_FILE) for h in root_logger.handlers):
    root_logger.addHandler(file_handler)

for logger_name in ("uvicorn.error", "uvicorn.access", "fastapi"):
    lg = logging.getLogger(logger_name)
    lg.setLevel(LOG_LEVEL_NAME)
    if not any(isinstance(h, logging.FileHandler) and getattr(h, 'baseFilename', None) == os.path.abspath(LOG_FILE) for h in lg.handlers):
        lg.addHandler(file_handler)

# Attach middleware
app.add_middleware(APIKeyAndRateLimitMiddleware)

# Serve static UI
static_dir = os.path.join(os.path.dirname(__file__), os.pardir, "web")
static_dir = os.path.abspath(static_dir)
if os.path.isdir(static_dir):
    # mount /static to web/static and serve ui.html at /ui
    app.mount("/static", StaticFiles(directory=os.path.join(static_dir, "static")), name="static")

@app.get("/ui")
async def ui():
    ui_path = os.path.join(static_dir, "ui.html")
    if os.path.exists(ui_path):
        return FileResponse(ui_path)
    raise HTTPException(status_code=404, detail="UI not found")


@app.get("/")
async def root_redirect():
    """Redirect root to the UI page for convenience."""
    return RedirectResponse(url="/ui")


@app.get("/ui/authed")
async def ui_authed(api_key: str = None):
    """Return the UI HTML with a small script injected that stores the provided api_key in localStorage.

    For convenience only: the server will accept the api_key query parameter and inject it into the
    returned HTML so the browser UI is pre-authenticated. For safety this endpoint will only inject
    the key if it matches the configured server `API_KEY` environment value.
    """
    ui_path = os.path.join(static_dir, "ui.html")
    if not os.path.exists(ui_path):
        raise HTTPException(status_code=404, detail="UI not found")

    # If no api_key provided, just serve the UI normally
    if not api_key:
        return FileResponse(ui_path)

    # Only allow injection when the provided key matches the server's API_KEY
    if API_KEY is None or api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key for UI injection")

    # Read UI and inject a small script before </body> to set localStorage
    try:
        with open(ui_path, "r", encoding="utf-8") as f:
            html = f.read()

        injection = f"<script>try{{localStorage.setItem('jarvis_api_key_v1', '{api_key.replace("'","\\'")}');}}catch(e){{console.error(e);}}</script>"
        if "</body>" in html:
            html = html.replace("</body>", injection + "</body>")
        else:
            html = html + injection

        return PlainTextResponse(html, media_type="text/html")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/logs")
async def get_logs(lines: int = 200):
    """Return the last `lines` lines from the log file as plain text.

    Protected by API key middleware.
    """
    log_path = LOG_FILE
    if not os.path.exists(log_path):
        raise HTTPException(status_code=404, detail="Log file not found")
    try:
        # Read last N lines efficiently
        with open(log_path, "r", encoding="utf-8", errors="replace") as f:
            dq = deque(f, maxlen=lines)
        text = "".join(dq)
        return PlainTextResponse(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("CORS_ORIGINS", "*")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class FileWriteRequest(BaseModel):
    path: str
    content: str
    overwrite: bool = True


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/capabilities")
async def capabilities():
    """Return a small JSON describing available server capabilities.

    This is useful for the UI to enable/disable features dynamically.
    """
    return {
        "ui": True,
        "files": True,
        "execute": True,
        "logs": True,
        "llm": False,
    }


# LLM/chat functionality removed: this server now exposes task-based endpoints only.


@app.get("/files/list")
async def api_list(path: str = "", recursive: bool = False, max_depth: int = 3, refresh: bool = False):
    """List files or directory entries.

    Query params:
    - recursive: if true, traverse directories up to `max_depth`.
    - max_depth: recursion depth when recursive=true.
    - refresh: bypass small in-memory cache (boolean).
    """
    try:
        # run the potentially IO-heavy listing in a thread to avoid blocking the event loop
        items = await __import__("asyncio").to_thread(list_files, path, recursive, max_depth, refresh)
        return {"path": path, "items": items}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/files/read")
async def api_read(path: str):
    try:
        content = read_file(path)
        return {"path": path, "content": content}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/files/write")
async def api_write(req: FileWriteRequest):
    try:
        write_file(req.path, req.content, req.overwrite)
        return {"ok": True}
    except FileExistsError:
        raise HTTPException(status_code=409, detail="File exists and overwrite=false")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/files/delete")
async def api_delete(path: str):
    try:
        delete_file(path)
        return {"ok": True}
    except IsADirectoryError:
        raise HTTPException(status_code=400, detail="Path is a directory; deletion not allowed")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/execute")
async def execute_command(command: str = Body(None), q_command: str = Query(None)):
    """Execute a small set of allowed command tokens.

    The endpoint accepts the command either as JSON body {"command": "..."}
    or as a query parameter `?command=...` (useful for quick testing). If no
    command is provided a clear 400 error is returned.
    """
    cmd = command or q_command
    if not cmd:
        # Match FastAPI's validation style but give a clear message
        raise HTTPException(status_code=400, detail="Missing required field: command")

    # For safety only allow a minimal set of built-in actions via command tokens.
    # The preferred way to extend behavior is to add endpoints or use file ops.
    if cmd == "list_root":
        return {"items": list_dir("")}
    return {"ok": False, "error": "Unsupported command: %s" % cmd}
