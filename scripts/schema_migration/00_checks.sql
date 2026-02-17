-- 00_checks.sql
-- Run these queries to inspect engines, orphan rows and duplicates

-- 1) Check storage engines for critical tables
SELECT TABLE_NAME, ENGINE
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = DATABASE()
  AND TABLE_NAME IN ('users','halls','hall_amenities','hall_services','amenities','services');

-- 2) Find orphan hall_amenities referencing missing halls or amenities
SELECT ha.* FROM hall_amenities ha LEFT JOIN halls h ON ha.hall_id = h.hall_id WHERE h.hall_id IS NULL;
SELECT ha.* FROM hall_amenities ha LEFT JOIN amenities a ON ha.amenity_id = a.amenity_id WHERE a.amenity_id IS NULL;

-- 3) Find orphan hall_services referencing missing halls or services
SELECT hs.* FROM hall_services hs LEFT JOIN halls h ON hs.hall_id = h.hall_id WHERE h.hall_id IS NULL;
SELECT hs.* FROM hall_services hs LEFT JOIN services s ON hs.service_id = s.service_id WHERE s.service_id IS NULL;

-- 4) Find halls referencing non-existing users
SELECT h.* FROM halls h LEFT JOIN users u ON h.subadmin_id = u.user_id WHERE u.user_id IS NULL;

-- 5) Find duplicate mappings
SELECT hall_id, amenity_id, COUNT(*) c FROM hall_amenities GROUP BY hall_id, amenity_id HAVING c > 1;
SELECT hall_id, service_id, COUNT(*) c FROM hall_services GROUP BY hall_id, service_id HAVING c > 1;

-- 6) Check if unique index already exists
SELECT INDEX_NAME, GROUP_CONCAT(COLUMN_NAME ORDER BY SEQ_IN_INDEX) cols FROM INFORMATION_SCHEMA.STATISTICS
 WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'hall_amenities' GROUP BY INDEX_NAME;
