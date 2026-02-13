from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import health, auth, admin, hall

# Ensure model modules are imported so they are registered with SQLAlchemy's metadata
import app.models.user  # noqa: F401
import app.models.hall  # noqa: F401


app = FastAPI(title="Venora API - Stage 1")

# Enable CORS for local development (allow Angular dev server)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200", "http://localhost:4201"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(hall.router)


@app.on_event("startup")
def on_startup():
    # Create DB tables defined in metadata (safe to call repeatedly)
    Base.metadata.create_all(bind=engine)
