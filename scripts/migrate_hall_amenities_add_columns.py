from sqlalchemy import create_engine, text
DATABASE_URL = "mysql+pymysql://akshay:AKS%402025elite@localhost:3306/venora_db"
engine = create_engine(DATABASE_URL)
with engine.connect() as conn:
    print('Altering table hall_amenities...')
    # Add id primary key if not exists
    conn.execute(text("ALTER TABLE hall_amenities ADD COLUMN IF NOT EXISTS id INT NOT NULL AUTO_INCREMENT PRIMARY KEY"))
    conn.execute(text("ALTER TABLE hall_amenities ADD COLUMN IF NOT EXISTS custom_price DECIMAL(10,2) NULL"))
    conn.execute(text("ALTER TABLE hall_amenities ADD COLUMN IF NOT EXISTS is_active TINYINT(1) NOT NULL DEFAULT 1"))
    print('Done')
