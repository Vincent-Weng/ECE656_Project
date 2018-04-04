DROP USER IF EXISTS 'user1'@'%';
CREATE USER user1;
GRANT SELECT ON yelp_db.* TO 'user1'@'%'; <-- This user only need to view data from the database. -->

DROP USER IF EXISTS 'user2'@'%';
CREATE USER user2;
GRANT SELECT, INSERT ON yelp_db.* TO 'user2'@'%'; <-- This user leaves review, therefore needs insert privilege. -->

DROP USER IF EXISTS 'user3'@'%';
CREATE USER user3;
GRANT SELECT, CREATE VIEW, SHOW VIEW ON yelp_db.* TO 'user3'@'%'; <-- This user needs to create and see views to do data analysis. -->

DROP USER IF EXISTS 'user4'@'%';
CREATE USER user4;
GRANT ALTER, ALTER ROUTINE, CREATE, CREATE ROUTINE, CREATE VIEW, DELETE, DROP, EXECUTE, INDEX, INSERT, REFERENCES,
      SELECT, SHOW VIEW, UPDATE ON yelp_db.* TO 'user4'@'%'; 
      <-- This user can do IUD operations, create/execute/see routines including functionsa and procedures, altering table to add keys/indices -->

DROP USER IF EXISTS 'user5'@'%';
CREATE USER user5;
GRANT ALL ON yelp_db.* TO 'user5'@'%'; <-- This is the admin of database. ALL privilege granted. -->
