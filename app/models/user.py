from sqlalchemy import Column, Integer, String, DateTime, func
from app.database import Base


class User(Base):
        """Users table for Venora.

        Fields required by STEP 2:
            - user_id
            - full_name
            - email
            - password (store hashed password here)
            - role
            - status
            - created_at
        """

        __tablename__ = "users"

        user_id = Column(Integer, primary_key=True, index=True)
        full_name = Column(String(255), nullable=False)
        email = Column(String(255), unique=True, nullable=False, index=True)
        password = Column(String(255), nullable=False)
        role = Column(String(50), nullable=False, default="customer")
        status = Column(String(50), nullable=False, default="active")
        created_at = Column(DateTime(timezone=True), server_default=func.now())
