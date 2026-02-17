-- 03_convert_enums.sql
-- Optional: convert `role` and `status` to ENUM types.
-- Review current values before applying.

-- 1) Inspect distinct values
SELECT DISTINCT role FROM users;
SELECT DISTINCT status FROM users;

-- 2) If values are safe, alter the columns. Example (adjust allowed values accordingly):
-- ALTER TABLE users MODIFY COLUMN role ENUM('admin','subadmin','customer') NOT NULL;
-- ALTER TABLE users MODIFY COLUMN status ENUM('active','inactive','pending') NOT NULL;

-- Alternative (safer): add CHECK constraints (MySQL 8+)
-- ALTER TABLE users ADD CONSTRAINT chk_role CHECK (role IN ('admin','subadmin','customer'));
-- ALTER TABLE users ADD CONSTRAINT chk_status CHECK (status IN ('active','inactive','pending'));
