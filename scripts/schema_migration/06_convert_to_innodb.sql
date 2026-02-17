-- 06_convert_to_innodb.sql
-- Convert tables to InnoDB engine if they are MyISAM or different engines. FK constraints require InnoDB.

ALTER TABLE users ENGINE=InnoDB;
ALTER TABLE halls ENGINE=InnoDB;
ALTER TABLE hall_amenities ENGINE=InnoDB;
ALTER TABLE hall_services ENGINE=InnoDB;
ALTER TABLE amenities ENGINE=InnoDB;
ALTER TABLE services ENGINE=InnoDB;

-- Verify engines again after running
SELECT TABLE_NAME, ENGINE FROM information_schema.TABLES WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME IN ('users','halls','hall_amenities','hall_services','amenities','services');
