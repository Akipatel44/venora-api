-- 01_add_uniques.sql
-- Add UNIQUE constraints to prevent duplicates. Run this only after resolving duplicates.

-- Users: ensure email unique
ALTER TABLE users
  ADD UNIQUE KEY ux_users_email (email);

-- Hall amenities: unique per hall + amenity
ALTER TABLE hall_amenities
  ADD UNIQUE KEY ux_hall_amenity (hall_id, amenity_id);

-- Hall services: unique per hall + service
ALTER TABLE hall_services
  ADD UNIQUE KEY ux_hall_service (hall_id, service_id);

-- Note: If any of the above ALTER TABLE statements fail due to duplicates, run the checks
-- from 00_checks.sql and dedupe accordingly. A safe dedupe pattern:
-- 1) Create a new table with desired unique constraint and copy aggregated rows
-- 2) Move data with care (preserve custom_price/is_active according to business rules)
