drop procedure dowhile_checkin;
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