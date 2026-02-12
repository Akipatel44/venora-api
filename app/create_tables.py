"""Utility to create DB tables using the project's models.

This script reads `DATABASE_URL` env var; if not set it'll use the default
from `app.database` (currently MySQL). For a quick local test you can run:

    set DATABASE_URL=sqlite:///./venora_test.db  # PowerShell
    python -m app.create_tables

That will create `venora_test.db` in the repo root and create the `users`
table to verify the model.
"""
import os

if __name__ == "__main__":
    # Ensure any env var override is read by database module
    # (database.py reads DATABASE_URL at import time)
    from app.database import engine, Base

    print("Creating tables using engine:", engine)
    Base.metadata.create_all(bind=engine)
    print("Tables created (if engine reachable).")
