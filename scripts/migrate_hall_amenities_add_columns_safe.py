from sqlalchemy import create_engine, text
DATABASE_URL = "mysql+pymysql://akshay:AKS%402025elite@localhost:3306/venora_db"
engine = create_engine(DATABASE_URL)
with engine.connect() as conn:
    def has_column(col):
        res = conn.execute(text("SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='venora_db' AND TABLE_NAME='hall_amenities' AND COLUMN_NAME=:col"), {"col": col})
        return res.scalar() > 0

    print('Checking columns...')
    if not has_column('id'):
        print('Adding id column...')
        conn.execute(text('ALTER TABLE hall_amenities ADD COLUMN id INT NOT NULL AUTO_INCREMENT PRIMARY KEY'))
    else:
        print('id exists')
    if not has_column('custom_price'):
        print('Adding custom_price...')
        conn.execute(text("ALTER TABLE hall_amenities ADD COLUMN custom_price DECIMAL(10,2) NULL"))
    else:
        print('custom_price exists')
    if not has_column('is_active'):
        print('Adding is_active...')
        conn.execute(text("ALTER TABLE hall_amenities ADD COLUMN is_active TINYINT(1) NOT NULL DEFAULT 1"))
    else:
        print('is_active exists')
    print('Migration complete')
