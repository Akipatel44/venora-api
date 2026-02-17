from sqlalchemy import create_engine, text
DATABASE_URL = "mysql+pymysql://akshay:AKS%402025elite@localhost:3306/venora_db"
engine = create_engine(DATABASE_URL)
with engine.connect() as conn:
    r = conn.execute(text("SELECT * FROM halls WHERE hall_id = :hid"), {"hid": 5}).fetchone()
    if r:
        print(dict(r))
    else:
        print('Hall not found')
