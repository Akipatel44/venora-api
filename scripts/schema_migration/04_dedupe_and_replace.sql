-- 04_dedupe_and_replace.sql
-- Safely dedupe hall_amenities and hall_services by creating a new table, copying aggregated rows,
-- then atomically renaming tables. This preserves original data in *_old tables.

-- WARNING: Run only after reviewing results from 00_checks.sql and taking a backup.

-- 1) Create new deduped hall_amenities table with same structure
CREATE TABLE IF NOT EXISTS hall_amenities_new LIKE hall_amenities;

-- 2) Ensure new table has a unique constraint to prevent duplicates
ALTER TABLE hall_amenities_new DROP INDEX IF EXISTS ux_hall_amenity;
ALTER TABLE hall_amenities_new ADD UNIQUE KEY ux_hall_amenity (hall_id, amenity_id);

-- 3) Copy aggregated rows into new table. Strategy: pick MAX(custom_price) and MAX(is_active).
INSERT INTO hall_amenities_new (hall_id, amenity_id, custom_price, is_active)
SELECT hall_id, amenity_id, MAX(custom_price) AS custom_price, MAX(is_active) AS is_active
FROM hall_amenities
GROUP BY hall_id, amenity_id;

-- 4) Swap tables atomically
RENAME TABLE hall_amenities TO hall_amenities_old, hall_amenities_new TO hall_amenities;

-- 5) Repeat same for hall_services
CREATE TABLE IF NOT EXISTS hall_services_new LIKE hall_services;
ALTER TABLE hall_services_new DROP INDEX IF EXISTS ux_hall_service;
ALTER TABLE hall_services_new ADD UNIQUE KEY ux_hall_service (hall_id, service_id);
INSERT INTO hall_services_new (hall_id, service_id, custom_price, is_active)
SELECT hall_id, service_id, MAX(custom_price) AS custom_price, MAX(is_active) AS is_active
FROM hall_services
GROUP BY hall_id, service_id;
RENAME TABLE hall_services TO hall_services_old, hall_services_new TO hall_services;

-- After verification, you can drop the _old tables or keep them for audit.
-- DROP TABLE hall_amenities_old;
-- DROP TABLE hall_services_old;
