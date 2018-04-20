SELECT id, date FROM review WHERE unix_timestamp(date) <= unix_timestamp('2004-10-01') OR unix_timestamp(date) >= unix_timestamp('2018-01-01');

SELECT 
    SUM(stars = 1) as 1star
    ,SUM(stars = 2) as 2star
    ,SUM(stars = 3) as 3star
    ,SUM(stars = 4) as 4star
    ,SUM(stars = 5) as 5star
FROM
    review
        JOIN
    user ON review.user_id = user.id
WHERE
    date - yelping_since = 0
        AND review_count = 1;
        
SELECT 
    count(*)
FROM
    checkin
        JOIN
    (SELECT 
        id,
            business_id,
            SUBSTRING_INDEX(hours, '|', 1) AS day_of_week,
            SUBSTRING_INDEX(SUBSTRING_INDEX(hours, '|', - 1), '-', 1) AS opening_time,
            SUBSTRING_INDEX(SUBSTRING_INDEX(hours, '|', - 1), '-', - 1) AS closing_time
    FROM
        hours) AS a ON a.business_id = checkin.business_id
        AND a.day_of_week = SUBSTRING_INDEX(checkin.date, '-', 1)
WHERE
    a.opening_time < SUBSTRING_INDEX(checkin.date, '-', - 1)
        AND a.closing_time > SUBSTRING_INDEX(checkin.date, '-', - 1);
        
select count(*) from user join (select count(user_id) as countedReviews, user_id 
from review group by user_id) as a on a.user_id = user.id where a.countedReviews - review_count != 0;

select count(*) from elite_years join
(SELECT user_id, SUBSTRING_INDEX(date, '-', 1) AS year FROM review)
as a on a.user_id=elite_years.user_id and a.year = elite_years.year
group by elite_years.user_id, elite_years.year;

select count(*) from review where substring_index(date, ' ', -1) != '00:00:00';

create table hours_new(
	id int(11) not null auto_increment, primary key (id)
    ,business_id varchar(255)
    ,day_of_week varchar(9)
    ,opening_time time
    ,closing_time time
    );
    
drop procedure if exists dowhile_hours;
delimiter //
create procedure dowhile_hours ()
begin declare v1 int default 821044;
while v1 > 0 do
insert into hours_new(id) values (null);
set v1 = v1 - 1;
end while;
end//
delimiter ;
   
call dowhile_hours();

update hours_new set day_of_week = (
	select SUBSTRING_INDEX(hours, '|', 1) from hours where hours_new.id = hours.id);
update hours_new set opening_time = (
	select SUBSTRING_INDEX(SUBSTRING_INDEX(hours, '|', - 1), '-', 1) from hours where hours_new.id = hours.id);
update hours_new set closing_time = (
	select SUBSTRING_INDEX(SUBSTRING_INDEX(hours, '|', - 1), '-', - 1) from hours where hours_new.id = hours.id);
update hours_new set business_id = (
	select business_id from hours where hours_new.id = hours.id);

create index idx_day_of_week on hours_new(day_of_week);
create index idx_opening_time on hours_new(opening_time);
create index idx_closing_time on hours_new(closing_time);

create table checkin_new(
	id int(11) not null auto_increment, primary key (id)
    ,business_id varchar(255)
    ,day_of_week varchar(9)
    ,checkin_time time
    );

drop procedure if exists dowhile_checkin;
delimiter //
create procedure dowhile_checkin()
begin declare v1 int default 3891600;
while v1 > 0 do
insert into checkin_new(id) values (null);
set v1 = v1 - 1;
end while;
end//
delimiter ;

call dowhile_checkin();

update checkin_new set day_of_week = (
	select SUBSTRING_INDEX(date, '-', 1) from checkin where checkin_new.id = checkin.id);
update checkin_new set checkin_time = (
	select SUBSTRING_INDEX(date, '-', -1) from checkin where checkin_new.id = checkin.id);
update checkin_new set business_id = (
	select business_id from checkin where checkin_new.id = checkin.id);
create index idx_day_of_week on checkin_new(day_of_week);
create index idx_opening_time on checkin_new(checkin_time);