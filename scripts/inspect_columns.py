from sqlalchemy import create_engine, text
DATABASE_URL = "mysql+pymysql://akshay:AKS%402025elite@localhost:3306/venora_db"
engine = create_engine(DATABASE_URL)
with engine.connect() as conn:
    res = conn.execute(text("SELECT COLUMN_NAME, COLUMN_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='venora_db' AND TABLE_NAME='hall_amenities'"))
    for row in res:
        print(row[0], row[1])
