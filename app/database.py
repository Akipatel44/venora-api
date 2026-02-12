import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Behavior:
# - If `DATABASE_URL` env var is set, use it (Postgres/MySQL/etc.).
# - Otherwise use a local SQLite file for fast development so the app can start
#   even when Postgres isn't running.

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Default to MySQL for development using the provided credentials.
    # Password contains '@' so it is URL-encoded as '%40'.
    DATABASE_URL = "mysql+pymysql://akshay:AKS%402025elite@localhost:3306/venora_db"
    engine = create_engine(DATABASE_URL, echo=True)
else:
    engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
