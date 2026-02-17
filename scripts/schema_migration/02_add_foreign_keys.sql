-- 02_add_foreign_keys.sql
-- Add foreign keys after data has been cleaned and tables are InnoDB.

-- 1) Ensure halls.subadmin_id references users.user_id
ALTER TABLE halls
  ADD CONSTRAINT fk_halls_subadmin FOREIGN KEY (subadmin_id) REFERENCES users(user_id);

-- 2) hall_amenities -> halls, amenities
ALTER TABLE hall_amenities
  ADD CONSTRAINT fk_ha_hall FOREIGN KEY (hall_id) REFERENCES halls(hall_id),
  ADD CONSTRAINT fk_ha_amenity FOREIGN KEY (amenity_id) REFERENCES amenities(amenity_id);

-- 3) hall_services -> halls, services
ALTER TABLE hall_services
  ADD CONSTRAINT fk_hs_hall FOREIGN KEY (hall_id) REFERENCES halls(hall_id),
  ADD CONSTRAINT fk_hs_service FOREIGN KEY (service_id) REFERENCES services(service_id);

-- If any of these fail, re-run 00_checks.sql and resolve orphan rows.
