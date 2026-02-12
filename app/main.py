from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import health, auth, admin

# Ensure model modules are imported so they are registered with SQLAlchemy's metadata
import app.models.user  # noqa: F401


app = FastAPI(title="Venora API - Stage 1")

# Enable CORS for local development (allow Angular dev server)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(admin.router)


@app.on_event("startup")
def on_startup():
    # Create DB tables defined in metadata (safe to call repeatedly)
    Base.metadata.create_all(bind=engine)
