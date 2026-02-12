from fastapi import FastAPI
from app.database import engine, Base
from app.routers import health

# Ensure model modules are imported so they are registered with SQLAlchemy's metadata
import app.models.user  # noqa: F401


app = FastAPI(title="Venora API - Stage 1")

app.include_router(health.router)


@app.on_event("startup")
def on_startup():
    # Create DB tables defined in metadata (safe to call repeatedly)
    Base.metadata.create_all(bind=engine)
