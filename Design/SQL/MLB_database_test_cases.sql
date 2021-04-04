------------------------------------------------------------
--
-- MLB Statistics 2015 - 2019
-- ECE 356 Project
--
-- Code used to create the MLB database for testing
--
-- History: initial creation 3 April 2021: MH

-- Clean out the old teefile
\! rm -f mlb-test-outfile.txt
tee mlb-test-outfile.txt

-- Show warnings after every statement
warnings;

select 'Chack if data is lost by adding constraints' as '';
With GamesDataLost as
(
    select 'Games' as 'TablesThatLostData', (count(*) - (select count(*) from Games)) as DataLost
    from (select distinct * from Games_Origin where gID IN (select gID from Games)) as mlb
),
TeamNamesDataLost as
(
    select 'TeamNames' as 'TablesThatLostData', (count(*) - (select count(*) from TeamNames)) as DataLost 
    from (select distinct * from TeamNames_Origin where abbreviation IN (select abbreviation from TeamNames)) as mlb
),
PitchesDataLost as
(
    select 'Pitches' as 'TablesThatLostData', (count(*) - (select count(*) from Pitches)) as DataLost 
    from (select distinct * from Pitches_Origin where abID IN (select abID from Pitches)) as mlb
),
PlayerNamesDataLost as
(
    select 'PlayerNames' as 'TablesThatLostData', (count(*) - (select count(*) from PlayerNames)) as DataLost 
    from (select distinct * from PlayerNames_Origin where id IN (select id from PlayerNames)) as mlb
),
AtBatsDataLost as
(
    select 'AtBats' as 'TablesThatLostData', (count(*) - (select count(*) from AtBats)) as DataLost 
    from (select distinct * from AtBats_Origin where abID IN (select abID from AtBats)) as mlb
),
EjectionsDataLost as
(
    select 'Ejections' as 'TablesThatLostData', (count(*) - (select count(*) from Ejections)) as DataLost
    from (select distinct * from Ejections_Origin where abID IN (select abID from Ejections)) as mlb
),
-- union them
TotalDataLost as
(
    select TablesThatLostData from GamesDataLost where DataLost > 0
    UNION 
    select TablesThatLostData from TeamNamesDataLost where DataLost > 0
    UNION 
    select TablesThatLostData from PitchesDataLost where DataLost > 0
    UNION
    select TablesThatLostData from PlayerNamesDataLost where DataLost > 0
    UNION
    select TablesThatLostData from AtBatsDataLost where DataLost > 0
    UNION
    select TablesThatLostData from EjectionsDataLost where DataLost > 0
)
select count(*) as TotalCountTablesLostData from TotalDataLost;
-- should be empty, count = 0

-- Finish
nowarning
notee;
