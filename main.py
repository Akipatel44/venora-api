"""Top-level entrypoint for uvicorn compatibility.

Allows running `uvicorn main:app` from the repo root. Delegates to `app.main.app`.
"""

from app.main import app  # re-export FastAPI `app`

__all__ = ["app"]
