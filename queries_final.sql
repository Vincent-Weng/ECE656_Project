SELECT 
    id, date
FROM
    review
WHERE
    UNIX_TIMESTAMP(date) <= UNIX_TIMESTAMP('2004-10-01')
        OR UNIX_TIMESTAMP(date) >= UNIX_TIMESTAMP('2018-01-01');

SELECT 
    user.id
FROM
    (user
    INNER JOIN review ON user.id = review.user_id)
WHERE
    user.yelping_since > review.date
GROUP BY user.id;

SELECT 
    user.id
FROM
    (user
    INNER JOIN elite_years ON user.id = elite_years.user_id)
WHERE
    YEAR(user.yelping_since) > elite_years.year
GROUP BY user.id;
            
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
        
select count(*) from user join (select count(user_id) as countedReviews, user_id from
           review group by user_id) as a on a.user_id = user.id where a.countedReviews > review_count;
           
SELECT 
    COUNT(*)
FROM
    elite_years
        JOIN
    (SELECT 
        user_id, SUBSTRING_INDEX(date, '-', 1) AS year
    FROM
        review) AS a ON a.user_id = elite_years.user_id
        AND a.year = elite_years.year
GROUP BY elite_years.user_id , elite_years.year;