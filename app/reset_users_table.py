"""Drop and recreate the `users` table, then seed test users.

Use with caution: this will REMOVE existing `users` table in the configured
database (MySQL or other) and recreate it from the SQLAlchemy model.
"""
from app.database import engine, Base, SessionLocal
from app.models.user import User
from app.seed_users import seed
from sqlalchemy import text


def reset():
    print("Dropping users table if exists...")
    with engine.connect() as conn:
        try:
            conn.execute(text("DROP TABLE IF EXISTS users;"))
            conn.commit()
            print("Dropped users table.")
        except Exception as e:
            print("Error dropping table (continuing):", e)

    print("Creating tables from models...")
    Base.metadata.create_all(bind=engine)
    print("Tables created.")

    print("Seeding users...")
    seed()
    print("Done.")


if __name__ == "__main__":
    reset()
