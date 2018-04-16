DROP USER IF EXISTS 'user1'@'%';
CREATE USER user1;
GRANT SELECT ON yelp_db.* TO 'user1'@'%';

DROP USER IF EXISTS 'user2'@'%';
CREATE USER user2;
GRANT SELECT ON yelp_db.* TO 'user2'@'%';
GRANT INSERT ON yelp_db.review TO 'user2'@'%';
GRANT INSERT ON yelp_db.tip TO 'user2'@'%';
GRANT UPDATE (stars) ON yelp_db.business TO 'user2'@'%';
GRANT UPDATE (review_count) ON yelp_db.business TO 'user2'@'%';
GRANT UPDATE ON yelp_db.user TO 'user2'@'%';

DROP USER IF EXISTS 'user3'@'%';
CREATE USER user3;
GRANT SELECT, CREATE VIEW, SHOW VIEW ON yelp_db.* TO 'user3'@'%';

DROP USER IF EXISTS 'user4'@'%';
CREATE USER user4;
GRANT ALTER ROUTINE, CREATE ROUTINE, EXECUTE, # routine related
CREATE VIEW, SHOW VIEW, # view related
CREATE, ALTER, INDEX, REFERENCES, # tables, indexes and keys
DELETE, DROP, INSERT, SELECT, UPDATE # basic operations including IUD
ON yelp_db.* TO 'user4'@'%';

DROP USER IF EXISTS 'user5'@'%';
CREATE USER user5;
GRANT ALL ON yelp_db.* TO 'user5'@'%';