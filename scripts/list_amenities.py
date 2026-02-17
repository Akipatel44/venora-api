from sqlalchemy import create_engine, text
DATABASE_URL = "mysql+pymysql://akshay:AKS%402025elite@localhost:3306/venora_db"
engine = create_engine(DATABASE_URL)
with engine.connect() as conn:
    rows = conn.execute(text("SELECT amenity_id, amenity_name FROM amenities ORDER BY amenity_id")).fetchall()
    for r in rows:
        print(r[0], r[1])
