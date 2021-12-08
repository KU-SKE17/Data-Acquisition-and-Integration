-- ts, lat, lon, sensor, source, value, user

-- ts: every 6 hours
-- sensor: temperature, light, pm25, humidity, rain
-- source: tmd, kidbright, aqi
-- user: 6210545505

create view my_data as

-- temperature: kidbright
SELECT TIMESTAMP(DATE(ts), CONCAT(floor(hour(ts)/6)*6, ':00:00')) as ts, lat, lon,'temperature' as sensor, 'kidbright' as source, avg(temp) as value, '6210545505' as user
FROM kidbright
GROUP BY ts, lat, lon

UNION
-- light
SELECT TIMESTAMP(DATE(ts), CONCAT(floor(hour(ts)/6)*6, ':00:00')) as ts, lat, lon,'light' as sensor, 'kidbright' as source, avg(light) as value, '6210545505' as user
FROM kidbright
GROUP BY ts, lat, lon

UNION
-- pm25
SELECT TIMESTAMP(DATE(ts), CONCAT(floor(hour(ts)/6)*6, ':00:00')) as ts, lat, lon,'pm25' as sensor, 'aqi' as source, avg(pm25) as value, '6210545505' as user
FROM aqi
GROUP BY ts, lat, lon

UNION
-- temperature: tmd
SELECT TIMESTAMP(DATE(ts), CONCAT(floor(hour(ts)/6)*6, ':00:00')) as ts, lat, lon,'temperature' as sensor, 'tmd' as source, avg(temp) as value, '6210545505' as user
FROM tmd
GROUP BY ts, lat, lon

UNION
-- humidity
SELECT TIMESTAMP(DATE(ts), CONCAT(floor(hour(ts)/6)*6, ':00:00')) as ts, lat, lon,'humidity' as sensor, 'tmd' as source, avg(humi) as value, '6210545505' as user
FROM tmd
GROUP BY ts, lat, lon

UNION
-- rain
SELECT TIMESTAMP(DATE(ts), CONCAT(floor(hour(ts)/6)*6, ':00:00')) as ts, lat, lon,'rain' as sensor, 'tmd' as source, sum(rainf) as value, '6210545505' as user
FROM tmd
GROUP BY ts, lat, lon
;


INSERT INTO warehouse.weather (ts, lat, lon, sensor, source, value, user)
SELECT ts, lat, lon, sensor, source, value, user FROM my_data;