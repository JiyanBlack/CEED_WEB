DROP DATABASE IF EXISTS ceed;
CREATE DATABASE ceed;
USE ceed;

DROP TABLE IF EXISTS journey;
CREATE TABLE journey
(
Count INT,
CardId INT,
OnTran INT,
OnRef INT,
OnDate VARCHAR(100),
OnType INT,
OnMode INT,
Jrny INT,
EtimCode INT,
OnZone INT,
OnLocation INT,
OnLandmark INT,
OffTran INT,
OffDate VARCHAR(100),
OffZone INT,
OffLocation INT,
OffLandmark INT,
FareType INT,
Origin INT,
TransferFrom INT,
Token VARCHAR(100),
Distance DECIMAL(6,2),
OnDay TEXT,
OnTime TIME,
OffDay TEXT,
OffTime TIME
);


LOAD DATA LOCAL INFILE "/home/rglsm/Codes/UWA_CEED_Web/csv/20090228_with_date.csv" INTO TABLE journey
 FIELDS TERMINATED BY ','
 LINES TERMINATED BY '\r'
;


#STR_TO_DATE(OnDay,'%d/%m/%Y')

UPDATE journey SET OnDay=STR_TO_DATE(OnDay,'%d/%m/%Y');
UPDATE journey SET OffDay=STR_TO_DATE(OffDay,'%d/%m/%Y');

ALTER TABLE journey MODIFY OnDay DATE;
ALTER TABLE journey MODIFY OffDay DATE;

#finds trips of < 0km or faretype of 1 (indicates an error)
-- SELECT CardId FROM journey WHERE distance <= 0 OR faretype = 1;

#finds tuples with an excessive one-stage journey length (greater than 80 km)
-- SELECT CardId, distance FROM journey WHERE distance > 80 AND UNIX_TIMESTAMP(CONCAT(OnDay, " ", OnTime)) < UNIX_TIMESTAMP(CONCAT(OffDay, " ", OffTime));

#finds tuples with an impossible speed (greater than 90 km/h)
--  SELECT CardId, (3600 * distance) / (UNIX_TIMESTAMP(CONCAT(OffDay, " ", OffTime)) - UNIX_TIMESTAMP(CONCAT(OnDay, " ", OnTime))) AS "Speed" FROM journey
--   WHERE (3600 * distance) / (UNIX_TIMESTAMP(CONCAT(OffDay, " ", OffTime)) - UNIX_TIMESTAMP(CONCAT(OnDay, " ", OnTime))) > 90
--   AND UNIX_TIMESTAMP(CONCAT(OnDay, " ", OnTime)) < UNIX_TIMESTAMP(CONCAT(OffDay, " ", OffTime));

#speed
  -- SELECT CardId, (3600 * distance) / (UNIX_TIMESTAMP(CONCAT(OffDay, " ", OffTime)) - UNIX_TIMESTAMP(CONCAT(OnDay, " ", OnTime))) AS "Speed" FROM journey
  --  WHERE UNIX_TIMESTAMP(CONCAT(OnDay, " ", OnTime)) < UNIX_TIMESTAMP(CONCAT(OffDay, " ", OffTime));

#finds single stage trips of an implausible length (greater than 4 hours) or less than zero hours.
-- SELECT CardId, CONCAT(OnDay, " ", OnTime) AS "OnTime", CONCAT(OffDay, " ", OffTime) AS "OffTime" FROM journey
--  WHERE UNIX_TIMESTAMP(CONCAT(OnDay, " ", OnTime)) > UNIX_TIMESTAMP(CONCAT(OffDay, " ", OffTime)) OR
--  UNIX_TIMESTAMP(CONCAT(OffDay, " ", OffTime)) - UNIX_TIMESTAMP(CONCAT(OnDay, " ", OnTime)) > 3600 * 4;

DROP TABLE IF EXISTS stops;
CREATE TABLE stops
(
STOPNUMBER INT,
ROAD VARCHAR(50),
SUFFIX VARCHAR(5),
STOPNAME VARCHAR(50),
SUBURB VARCHAR(50),
Stop_Status TEXT,
POSITIONX_MGA DECIMAL(9,2),
POSITIONY_MGA DECIMAL(9,2)
);

LOAD DATA LOCAL INFILE "/home/rglsm/Codes/UWA_CEED_Web/csv/stops20090101 - 20090228.csv" INTO TABLE stops
 FIELDS TERMINATED BY ','
 LINES TERMINATED BY '\r\n'
;
