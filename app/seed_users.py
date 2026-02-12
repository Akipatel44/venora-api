"""Seed script to create three users: SuperAdmin, SubAdmin, Customer."""
from app.database import SessionLocal, Base, engine
from app.services.security import get_password_hash
from app.models.user import User


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing = db.query(User).first()
        if existing:
            print("Users already exist; skipping seeding")
            return

        users = [
            {"full_name": "Super Admin", "email": "super@venora.local", "password": "superpass", "role": "superadmin"},
            {"full_name": "Sub Admin", "email": "sub@venora.local", "password": "subpass", "role": "subadmin"},
            {"full_name": "Customer User", "email": "cust@venora.local", "password": "custpass", "role": "customer"},
        ]

        for u in users:
            db_user = User(full_name=u["full_name"], email=u["email"], password=get_password_hash(u["password"]), role=u["role"])
            db.add(db_user)
        db.commit()
        print("Seeded users")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
