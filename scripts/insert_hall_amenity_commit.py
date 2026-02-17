from sqlalchemy import create_engine, text
DATABASE_URL = "mysql+pymysql://akshay:AKS%402025elite@localhost:3306/venora_db"
engine = create_engine(DATABASE_URL)
with engine.begin() as conn:
    conn.execute(text("INSERT IGNORE INTO hall_amenities (amenity_id, hall_id, custom_price, is_active) VALUES (:a,:h,:c,:ia)"), {"a":1, "h":5, "c": None, "ia":1})
    print('Inserted with commit')
    r = conn.execute(text('SELECT COUNT(*) FROM hall_amenities WHERE hall_id=5')).scalar()
    print('count=', r)
