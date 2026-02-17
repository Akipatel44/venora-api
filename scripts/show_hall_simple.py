from sqlalchemy import create_engine, text
DATABASE_URL = "mysql+pymysql://akshay:AKS%402025elite@localhost:3306/venora_db"
engine = create_engine(DATABASE_URL)
with engine.connect() as conn:
    r = conn.execute(text("SELECT hall_id, subadmin_id, hall_name FROM halls WHERE hall_id = :hid"), {"hid": 5}).fetchone()
    if r:
        print('hall_id=', r[0], 'subadmin_id=', r[1], 'name=', r[2])
    else:
        print('Hall not found')
