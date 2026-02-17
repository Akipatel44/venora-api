from sqlalchemy import create_engine, text
DATABASE_URL = "mysql+pymysql://akshay:AKS%402025elite@localhost:3306/venora_db"
engine = create_engine(DATABASE_URL)
with engine.connect() as conn:
    try:
        conn.execute(text("INSERT INTO hall_amenities (amenity_id, hall_id, custom_price, is_active) VALUES (:a,:h,:c,:ia)"), {"a":1, "h":5, "c": None, "ia":1})
        print('Inserted')
    except Exception as e:
        print('Error:', e)
    r = conn.execute(text('SELECT * FROM hall_amenities WHERE hall_id=:h'), {"h":5}).fetchall()
    for row in r:
        print(dict(row))
    if not r:
        print('No rows')
