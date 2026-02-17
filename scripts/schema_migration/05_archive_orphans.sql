-- 05_archive_orphans.sql
-- Move orphan rows (referencing missing parent) into archive tables for manual review.

-- Hall amenities orphans
CREATE TABLE IF NOT EXISTS hall_amenities_orphaned AS SELECT ha.* FROM hall_amenities ha LEFT JOIN halls h ON ha.hall_id = h.hall_id WHERE h.hall_id IS NULL;
CREATE TABLE IF NOT EXISTS hall_amenities_orphaned_amenity AS SELECT ha.* FROM hall_amenities ha LEFT JOIN amenities a ON ha.amenity_id = a.amenity_id WHERE a.amenity_id IS NULL;

-- Remove them from production table after archiving
DELETE ha FROM hall_amenities ha LEFT JOIN halls h ON ha.hall_id = h.hall_id WHERE h.hall_id IS NULL;
DELETE ha FROM hall_amenities ha LEFT JOIN amenities a ON ha.amenity_id = a.amenity_id WHERE a.amenity_id IS NULL;

-- Hall services orphans
CREATE TABLE IF NOT EXISTS hall_services_orphaned AS SELECT hs.* FROM hall_services hs LEFT JOIN halls h ON hs.hall_id = h.hall_id WHERE h.hall_id IS NULL;
CREATE TABLE IF NOT EXISTS hall_services_orphaned_service AS SELECT hs.* FROM hall_services hs LEFT JOIN services s ON hs.service_id = s.service_id WHERE s.service_id IS NULL;

DELETE hs FROM hall_services hs LEFT JOIN halls h ON hs.hall_id = h.hall_id WHERE h.hall_id IS NULL;
DELETE hs FROM hall_services hs LEFT JOIN services s ON hs.service_id = s.service_id WHERE s.service_id IS NULL;

-- Halls referencing missing users
CREATE TABLE IF NOT EXISTS halls_orphaned_subadmin AS SELECT h.* FROM halls h LEFT JOIN users u ON h.subadmin_id = u.user_id WHERE u.user_id IS NULL;
-- You may want to reassign those halls rather than delete them.
