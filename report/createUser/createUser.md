## Part II. 2.1 User control

### 2.1.1 Description of the problem

In real applications, the Yelp database is expected to be visited by
different groups of people, including customers (users), data analyst
(special users), and developers. In this project, this is further
divided into five categories:

1.  A casual user who uses the application to browse search results.
    These users do not need to have an account; hence, they cannot
    submit reviews.

2.  Critiques that use the application to browse results just like the
    casual user, but they also leave reviews for places they visit. A
    logged in user should only be provided enough privileges to write
    the review.

3.  Business analysts can use the application to produce sales reports
    and may want to do special data mining and analysis. They cannot
    perform IUD (Insert/Update/Delete) operations on the database but
    should have access to creating extra views on the database schema.

4.  Developers working with this database are able to create new tables
    and perform data cleaning and indexing. They are allowed to perform
    IUD operations on the database.

5.  The database admin who has full access over the database.

The principle of granting privilege is to guarantee that each group of
people have sufficient permission in order to protect the database.
First, the list of all privileges in MySQL 5.7 are listed in the Table below, from which we can choose levels for each user
group.

<table border=0 cellpadding=0 cellspacing=0 width=1350 style='border-collapse:
 collapse;table-layout:fixed;width:1011pt;box-sizing: inherit;outline: 0px;
 border-spacing: 0px;font-variant-ligatures: normal;font-variant-caps: normal;
 orphans: 2;text-align:start;widows: 2;-webkit-text-stroke-width: 0px;
 text-decoration-style: initial;text-decoration-color: initial'>
 <col width=199 style='mso-width-source:userset;mso-width-alt:6357;width:149pt;
 box-sizing: inherit'>
 <col width=716 style='mso-width-source:userset;mso-width-alt:22912;width:537pt;
 box-sizing: inherit'>
 <col width=87 span=5 style='width:65pt;box-sizing: inherit;outline: 0px'>
 <tr height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'>
  <td height=21 width=199 style='height:16.0pt;width:149pt'>Privilege</td>
  <td width=716 style='width:330pt'>Meaning and Grantable Levels</td>
 </tr>
 <tr height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'>
  <td height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'
  scope=row>ALL [PRIVILEGES]</td>
  <td style='box-sizing: inherit;outline: 0px'>Grant all privileges at
  specified access level except&nbsp;GRANT OPTION&nbsp;and&nbsp;PROXY.</td>
 
 </tr>
 <tr height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'>
  <td height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'
  scope=row>ALTER</td>
  <td style='box-sizing: inherit;outline: 0px'>Enable use of&nbsp;ALTER TABLE.
  Levels: Global, database, table.</td>
 
 </tr>
 <tr height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'>
  <td height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'
  scope=row>ALTER ROUTINE</td>
  <td style='box-sizing: inherit;outline: 0px'>Enable stored routines to be
  altered or dropped. Levels: Global, database, procedure.</td>
 
 </tr>
 <tr height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'>
  <td height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'
  scope=row>CREATE</td>
  <td style='box-sizing: inherit;outline: 0px'>Enable database and table
  creation. Levels: Global, database, table.</td>
 
 </tr>
 <tr height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'>
  <td height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'
  scope=row>CREATE ROUTINE</td>
  <td style='box-sizing: inherit;outline: 0px'>Enable stored routine creation.
  Levels: Global, database.</td>
 
 </tr>
 <tr height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'>
  <td height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'
  scope=row>CREATE TABLESPACE</td>
  <td style='box-sizing: inherit;outline: 0px'>Enable tablespaces and log file
  groups to be created, altered, or dropped. Level: Global.</td>
 
 </tr>
 <tr height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'>
  <td height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'
  scope=row>CREATE TEMPORARY TABLES</td>
  <td style='box-sizing: inherit;outline: 0px'>Enable use of&nbsp;CREATE
  TEMPORARY TABLE. Levels: Global, database.</td>
 
 </tr>
 <tr height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'>
  <td height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'
  scope=row>CREATE USER</td>
  <td style='box-sizing: inherit;outline: 0px'>Enable use of&nbsp;CREATE
  USER,&nbsp;DROP USER,&nbsp;RENAME USER, and&nbsp;REVOKE ALL PRIVILEGES.
  Level: Global.</td>
 
 </tr>
 <tr height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'>
  <td height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'
  scope=row>CREATE VIEW</td>
  <td style='box-sizing: inherit;outline: 0px'>Enable views to be created or
  altered. Levels: Global, database, table.</td>
 
 </tr>
 <tr height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'>
  <td height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'
  scope=row>DELETE</td>
  <td style='box-sizing: inherit;outline: 0px'>Enable use of&nbsp;DELETE.
  Level: Global, database, table.</td>
 
 </tr>
 <tr height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'>
  <td height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'
  scope=row>DROP</td>
  <td style='box-sizing: inherit;outline: 0px'>Enable databases, tables, and
  views to be dropped. Levels: Global, database, table.</td>
 
 </tr>
 <tr height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'>
  <td height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'
  scope=row>EVENT</td>
  <td style='box-sizing: inherit;outline: 0px'>Enable use of events for the
  Event Scheduler. Levels: Global, database.</td>
 
 </tr>
 <tr height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'>
  <td height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'
  scope=row>EXECUTE</td>
  <td style='box-sizing: inherit;outline: 0px'>Enable the user to execute
  stored routines. Levels: Global, database, table.</td>
 
 </tr>
 <tr height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'>
  <td height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'
  scope=row>FILE</td>
  <td style='box-sizing: inherit;outline: 0px'>Enable the user to cause the
  server to read or write files. Level: Global.</td>
 
 </tr>
 <tr height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'>
  <td height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'
  scope=row>GRANT OPTION</td>
  <td style='mso-ignore:colspan;box-sizing: inherit;outline: 0px'>Enable
  privileges to be granted to or removed from other accounts. Levels: Global,
  database, table, procedure, proxy.</td>
  
 </tr>
 <tr height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'>
  <td height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'
  scope=row>INDEX</td>
  <td style='box-sizing: inherit;outline: 0px'>Enable indexes to be created or
  dropped. Levels: Global, database, table.</td>
 
 </tr>
 <tr height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'>
  <td height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'
  scope=row>INSERT</td>
  <td style='box-sizing: inherit;outline: 0px'>Enable use of&nbsp;INSERT.
  Levels: Global, database, table, column.</td>
 
 </tr>
 <tr height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'>
  <td height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'
  scope=row>LOCK TABLES</td>
  <td style='box-sizing: inherit;outline: 0px'>Enable use of&nbsp;LOCK
  TABLES&nbsp;on tables for which you have the&nbsp;SELECT&nbsp;privilege.
  Levels: Global, database.</td>
 
 </tr>
 <tr height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'>
  <td height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'
  scope=row>PROCESS</td>
  <td style='box-sizing: inherit;outline: 0px'>Enable the user to see all
  processes with&nbsp;SHOW PROCESSLIST. Level: Global.</td>
 
 </tr>
 <tr height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'>
  <td height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'
  scope=row>PROXY</td>
  <td style='box-sizing: inherit;outline: 0px'>Enable user proxying. Level:
  From user to user.</td>
 
 </tr>
 <tr height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'>
  <td height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'
  scope=row>REFERENCES</td>
  <td style='box-sizing: inherit;outline: 0px'>Enable foreign key creation.
  Levels: Global, database, table, column.</td>
 
 </tr>
 <tr height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'>
  <td height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'
  scope=row>RELOAD</td>
  <td style='box-sizing: inherit;outline: 0px'>Enable use
  of&nbsp;FLUSH&nbsp;operations. Level: Global.</td>
 
 </tr>
 <tr height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'>
  <td height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'
  scope=row>REPLICATION CLIENT</td>
  <td style='box-sizing: inherit;outline: 0px'>Enable the user to ask where
  master or slave servers are. Level: Global.</td>
 
 </tr>
 <tr height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'>
  <td height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'
  scope=row>REPLICATION SLAVE</td>
  <td style='box-sizing: inherit;outline: 0px'>Enable replication slaves to
  read binary log events from the master. Level: Global.</td>
 
 </tr>
 <tr height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'>
  <td height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'
  scope=row>SELECT</td>
  <td style='box-sizing: inherit;outline: 0px'>Enable use of&nbsp;SELECT.
  Levels: Global, database, table, column.</td>
 
 </tr>
 <tr height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'>
  <td height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'
  scope=row>SHOW DATABASES</td>
  <td style='box-sizing: inherit;outline: 0px'>Enable&nbsp;SHOW
  DATABASES&nbsp;to show all databases. Level: Global.</td>
 
 </tr>
 <tr height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'>
  <td height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'
  scope=row>SHOW VIEW</td>
  <td style='box-sizing: inherit;outline: 0px'>Enable use of&nbsp;SHOW CREATE
  VIEW. Levels: Global, database, table.</td>
 
 </tr>
 <tr height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'>
  <td height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'
  scope=row>SHUTDOWN</td>
  <td style='box-sizing: inherit;outline: 0px'>Enable use of&nbsp;mysqladmin
  shutdown. Level: Global.</td>
 
 </tr>
 <tr height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'>
  <td height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'
  scope=row>SUPER</td>
  <td style='mso-ignore:colspan;box-sizing: inherit;outline: 0px'>Enable
  use of other administrative operations such as&nbsp;CHANGE MASTER
  TO,&nbsp;KILL,&nbsp;PURGE BINARY LOGS,&nbsp;SET GLOBAL, and&nbsp;mysqladmin
  debug&nbsp;command. Level: Global.</td>
 </tr>
 <tr height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'>
  <td height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'
  scope=row>TRIGGER</td>
  <td style='box-sizing: inherit;outline: 0px'>Enable trigger operations.
  Levels: Global, database, table.</td>
 
 </tr>
 <tr height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'>
  <td height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'
  scope=row>UPDATE</td>
  <td style='box-sizing: inherit;outline: 0px'>Enable use of&nbsp;UPDATE.
  Levels: Global, database, table, column.</td>
 
 </tr>
 <tr height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'>
  <td height=21 style='height:16.0pt;box-sizing: inherit;outline: 0px'
  scope=row>USAGE</td>
  <td style='box-sizing: inherit;outline: 0px'>Synonym for&nbsp;"no privileges"</td>
 
 </tr>
</table>

### 2.1.2 Group 1


For the first group of users, they only browse information about the
business, including their opening hours, stars, reviews, without signing
in so they do not need to write information into the database. In some
cases, if the app allows some specific types of anonymous
communications, such as marking a review as “cool" or “useful” by a
visitor, then the permission should be extended to allow for
modification of the count of these tags. However, in this project we
assume that the user are not allowed to perform any operations except
exploring. Hereby we only grant `SELECT` privilege to the first group of
user, which we call `user1`:

          DROP USER IF EXISTS 'user1'@'%';
          CREATE USER user1;
          GRANT SELECT ON yelp_db.* TO 'user1'@'%';
        

### 2.1.3 Group 2

For the second type of user, they are different from casual users in
that they may leave reviews or tips on a business. They are logged-in
users, so they can interact with other reviews or tips. Therefore, they
are granted global `SELECT` privilege, `INSERT` on the review and tip
table, `UPDATE` on certain columns in the business table, and table-wise
`UPDATE` on user table. The SQL query is shown as follows, similarly we
call this `user2`:

          DROP USER IF EXISTS 'user2'@'%';
          CREATE USER user2;
          GRANT SELECT ON yelp_db.* TO 'user2'@'%';
          GRANT INSERT ON yelp_db.review TO 'user2'@'%';
          GRANT INSERT ON yelp_db.tip TO 'user2'@'%';
          GRANT UPDATE (stars) ON yelp_db.business TO 'user2'@'%';
          GRANT UPDATE (review_count) ON yelp_db.business TO 'user2'@'%';
          GRANT UPDATE ON yelp_db.user TO 'user2'@'%';
        

### 2.1.4 Group 3

Business analysts are special casual users. Here we assume they are not
logged in so they are not expected to change any contents in the
database. Therefore, we only add some view-related privileges to this
group of users besides those granted to group 1:

          DROP USER IF EXISTS 'user3'@'%';
          CREATE USER user3;
          GRANT SELECT, CREATE VIEW, SHOW VIEW ON yelp_db.* TO 'user3'@'%';
        

### 2.1.5 Group 4

Group 4 corresponds to normal developers. These people are in charge of
the visiting, development and maintenance of database. Therefore we
grant them full IUD privileges on the whole database. Also, in case they
need to perform automated operations, query optimization or concurrency
control, we also grant them with view, routine(function, procedure),
index and lock permissions. The SQL queries are as follows:

          DROP USER IF EXISTS 'user4'@'%';
          CREATE USER user4;
          GRANT ALTER ROUTINE, CREATE ROUTINE, EXECUTE, # routine related
          CREATE VIEW, SHOW VIEW, # view related
          CREATE, ALTER, INDEX, REFERENCES, # tables, indexes and keys
          DELETE, DROP, INSERT, SELECT, UPDATE # basic operations including IUD
          ON yelp_db.* TO 'user4'@'%';
        

### 2.1.6 Group 5


Group 5 is the database administrator, so its privilege is all but
`GRANT` and `PROXY` options, which should only be done using the root
user. In practical use only these two operations should be done using
root user in order to prevent abuse or unexpected threats to the
database. The SQL queries are as follows:

          DROP USER IF EXISTS 'user5'@'%';
          CREATE USER user5;
          GRANT ALL ON yelp_db.* TO 'user5'@'%';
        

