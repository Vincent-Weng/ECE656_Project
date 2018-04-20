drop table if exists hours_new;
create table hours_new(
id int(11) not null auto_increment, primary key (id)
,business_id varchar(255)
,day_of_week varchar(9)
,opening_time time
,closing_time time
);
drop procedure dowhile;
delimiter //
create procedure dowhile ()
begin declare v1 int default 821044;
while v1 > 0 do
insert into hours_new(id) values (null);
set v1 = v1 - 1;
end while;
end//
delimiter ;
call dowhile();
update hours_new set day_of_week = (select SUBSTRING_INDEX(hours, '|', 1) from 
hours where hours_new.id = hours.id);
update hours_new set opening_time = (select SUBSTRING_INDEX(SUBSTRING_INDEX(hours, '|', - 1), '-', 1) from 
hours where hours_new.id = hours.id);
update hours_new set closing_time = (select SUBSTRING_INDEX(SUBSTRING_INDEX(hours, '|', - 1), '-', - 1) from 
hours where hours_new.id = hours.id);
update hours_new set business_id = (select business_id from hours where hours_new.id = hours.id);