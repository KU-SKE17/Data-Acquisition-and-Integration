SELECT b.ename, s.ename, lat, lon
FROM station s
    INNER JOIN basin b on ST_Contains(b.geometry, POINT(s.lon, s.lat));


SELECT b.ename, s.station_id, s.ename, r.year, r.month, r.amount
FROM rainfall r
    INNER JOIN station s ON r.station_id = s.station_id
    INNER JOIN basin b ON ST_Contains(b.geometry, Point(s.lon, s.lat))
WHERE b.basin_id = 3 AND r.year = 2011;


SELECT SUM(daily_avg)
FROM (
    SELECT b.ename, s.station_id, s.ename, r.year, r.month, r.day, AVG(r.amount) as daily_avg
    FROM rainfall r
        INNER JOIN station s ON r.station_id = s.station_id
        INNER JOIN basin b ON ST_Contains(b.geometry, Point(s.lon, s.lat))
    WHERE b.basin_id = 3 AND r.year = 2021
    GROUP BY b.basin_id, r.year, r.month, r.day
) daily;
