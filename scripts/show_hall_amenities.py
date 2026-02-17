from sqlalchemy import create_engine, text
DATABASE_URL = "mysql+pymysql://akshay:AKS%402025elite@localhost:3306/venora_db"
engine = create_engine(DATABASE_URL)
with engine.connect() as conn:
    r = conn.execute(text("SELECT * FROM hall_amenities WHERE hall_id = :hid"), {"hid": 5}).fetchall()
    for row in r:
        print(dict(row))
    if not r:
        print('No rows')
