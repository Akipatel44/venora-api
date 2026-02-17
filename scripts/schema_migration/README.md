Migration plan and scripts for enforcing foreign keys, uniques and enums

Important: backup your production database before running any of these scripts.

Order of operations (recommended):
1. Take a full DB backup (mysqldump or your backup solution).
2. Run the checks script to detect engine types, orphan rows and duplicates.
3. Resolve any orphan or duplicate rows (manual review or using the provided helper queries).
4. Apply UNIQUE constraints.
5. Re-run checks to confirm no violations.
6. Apply FOREIGN KEY constraints.
7. Optionally convert `role` / `status` columns to ENUM or add CHECK constraints.

Files in this folder:
- 00_checks.sql         — queries to inspect engines, orphan rows and duplicates
- 01_add_uniques.sql    — ADD UNIQUE constraints and guidance to dedupe
- 02_add_foreign_keys.sql — ADD FOREIGN KEY constraints (run after dedupe + engine checks)
- 03_convert_enums.sql  — optional conversions for role/status

How to use
- Run checks first:
  mysql -u <user> -p venora_db < 00_checks.sql

- Inspect results and fix data as needed. Use SELECT queries produced by the checks to manually resolve rows.

- Once clean, run:
  mysql -u <user> -p venora_db < 01_add_uniques.sql
  mysql -u <user> -p venora_db < 02_add_foreign_keys.sql

Notes and safety
- These scripts assume InnoDB. If any table is MyISAM, convert to InnoDB first:
  ALTER TABLE table_name ENGINE=InnoDB;
- Unique and FK additions will fail if violating rows exist — fix them first.
- ENUM conversion can be disruptive; prefer adding CHECK constraints if you need safer rollout.

If you want, I can generate Alembic migrations for these steps instead of raw SQL.
