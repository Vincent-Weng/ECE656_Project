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

select *
from
elite_years join
(SELECT 
    user_id, SUBSTRING_INDEX(date, '-', 1) AS year
FROM
    review) as a using(user_id, year)
;

select count(*) from review where substring_index(date, ' ', -1) != '00:00:00';