------------------------------------------------------------
--
-- MLB Statistics 2015 - 2019
-- ECE 356 Project
--
-- Code used to create the MLB database for testing
--
-- History: initial creation 3 April 2021: MH

-- Clean out the old teefile
\! rm -f mlb-origin-outfile.txt
tee mlb-origin-outfile.txt

-- Show warnings after every statement
warnings;

drop table if exists PlayerNames_Origin;
drop table if exists Ejections_Origin;
drop table if exists AtBats_Origin;
drop table if exists Pitches_Origin;
drop table if exists TeamNames_Origin;
drop table if exists Games_Origin;

select '------------------------------------------------' as '';
select 'Create Teams_Origin' as '';

create table TeamNames_Origin (abbreviation char(3),
  city char(15),
  shortName char(15)
);

-- don't actually have a csv for teams, so have to make it ourselves

create table PlayerNames_Origin (id decimal(6),
  firstName char(15),
  lastName char(20)
);

-- load in the data
load data infile '/var/lib/mysql-files/17-MLB/player_names.csv'
ignore into table PlayerNames_Origin
  fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
  ignore 1 lines
  (id, firstName, lastName);

create table Games_Origin (gID decimal(9),
  homeTeam char(3),
  homeFinalScore int,
  awayTeam char(3),
  awayFinalScore int,
  gameDate date,
  venueName varchar(64),
  attendance int,
  startTime time,
  delay int,
  elapsedTime int,
  weatherDegrees int,
  windSpeedMpH int,
  windDirection char(15)
);

load data infile '/var/lib/mysql-files/17-MLB/games.csv'
ignore into table Games_Origin
  fields terminated by ','
  lines terminated by '\n'
  ignore 1 lines
  (@attendance, @awayFinalScore, @awayTeam, @gameDate, @elapsedTime, @gID, @homeFinalScore, @homeTeam, @startTime, @umpire1b, @umpire2b, @umpire3b, @umpireHp, @venue, @weatherDegrees, @weather, @windSpeed, @windDirection, @delay)
  set gID = @gID,
      homeTeam = upper(@homeTeam),
      homeFinalScore = @homeFinalScore,
      awayTeam = upper(@awayTeam),
      awayFinalScore = @awayFinalScore,
      gameDate = @gameDate,
      venueName = @venue,
      attendance = @attendance,
      startTime = time(str_to_date(@startTime, '%h:%i %p')),
      delay = @delay,
      elapsedTime = @elapsedTime,
      weatherDegrees = substring(@weatherDegrees, 2, 2),
      windSpeedMpH = if(substring(@windSpeed,3,1) = ' ', substring(@windSpeed,2,1), substring(@windSpeed,2,2)),
      windDirection = left(@windDirection, length(@windDirection) -1);

insert into TeamNames_Origin select distinct homeTeam, '', '' from Games_Origin;

update TeamNames_Origin set city = 'Los Angeles', shortName = 'Angels' where abbreviation = 'ANA';
update TeamNames_Origin set city = 'Arizona', shortName = 'Diamondbacks' where abbreviation = 'ARI';
update TeamNames_Origin set city = 'Atlanta', shortName = 'Braves' where abbreviation = 'ATL';
update TeamNames_Origin set city = 'Baltimore', shortName = 'Orioles' where abbreviation = 'BAL';
update TeamNames_Origin set city = 'Boston', shortName = 'Red Sox' where abbreviation = 'BOS';
update TeamNames_Origin set city = 'Chicago', shortName = 'White Sox' where abbreviation = 'CHA';
update TeamNames_Origin set city = 'Chicago', shortName = 'Cubs' where abbreviation = 'CHN';
update TeamNames_Origin set city = 'Cincinnati', shortName = 'Reds' where abbreviation = 'CIN';
update TeamNames_Origin set city = 'Cleveland', shortName = 'Indians' where abbreviation = 'CLE';
update TeamNames_Origin set city = 'Colorado', shortName = 'Rockies' where abbreviation = 'COL';
update TeamNames_Origin set city = 'Detroit', shortName = 'Tigers' where abbreviation = 'DET';
update TeamNames_Origin set city = 'Houston', shortName = 'Astros' where abbreviation = 'HOU';
update TeamNames_Origin set city = 'Kansas City', shortName = 'Royals' where abbreviation = 'KCA';
update TeamNames_Origin set city = 'Los Angeles', shortName = 'Dodgers' where abbreviation = 'LAN';
update TeamNames_Origin set city = 'Miami', shortName = 'Marlins' where abbreviation = 'MIA';
update TeamNames_Origin set city = 'Milwaukee', shortName = 'Brewers' where abbreviation = 'MIL';
update TeamNames_Origin set city = 'Minnesota', shortName = 'Twins' where abbreviation = 'MIN';
update TeamNames_Origin set city = 'New York', shortName = 'Yankees' where abbreviation = 'NYA';
update TeamNames_Origin set city = 'New York', shortName = 'Mets' where abbreviation = 'NYN';
update TeamNames_Origin set city = 'Oakland', shortName = 'Athletics' where abbreviation = 'OAK';
update TeamNames_Origin set city = 'Philadelphia', shortName = 'Phillies' where abbreviation = 'PHI';
update TeamNames_Origin set city = 'Pittsburgh', shortName = 'Pirates' where abbreviation = 'PIT';
update TeamNames_Origin set city = 'San Diego', shortName = 'Padres' where abbreviation = 'SDN';
update TeamNames_Origin set city = 'Seattle', shortName = 'Mariners' where abbreviation = 'SEA';
update TeamNames_Origin set city = 'San Francisco', shortName = 'Giants' where abbreviation = 'SFN';
update TeamNames_Origin set city = 'St. Louis', shortName = 'Cardinals' where abbreviation = 'SLN';
update TeamNames_Origin set city = 'Tampa Bay', shortName = 'Rays' where abbreviation = 'TBA';
update TeamNames_Origin set city = 'Texas', shortName = 'Rangers' where abbreviation = 'TEX';
update TeamNames_Origin set city = 'Toronto', shortName = 'Blue Jays' where abbreviation = 'TOR';
update TeamNames_Origin set city = 'Washington', shortName = 'Nationals' where abbreviation = 'WAS';

-- add back the foreign keys to the Games table after we have fully populated the TeamNames table
-- alter table Games
--   add foreign key (homeTeam) references TeamNames(abbreviation),
--   add foreign key (awayTeam) references TeamNames(abbreviation);

create table AtBats_Origin (abID decimal(10),
  gID decimal(9),
  inning int,
  topInning char(5),
  pScore int,
  batterID decimal(6),
  batDir char(1),
  pitcherID decimal(6),
  pitchDir char(1),
  event char(25),
  outsAfter decimal(1)
);

load data infile '/var/lib/mysql-files/17-MLB/atbats.csv'
ignore into table AtBats_Origin
  fields terminated by ','
  lines terminated by '\n'
  ignore 1 lines
  (@abID, @batterID, @event, @gID, @inning, @o, @pScore, @pThrows, @pitcherID, @stand, @top)
  set abID = @abID,
      gID = @gID,
      inning = @inning,
      topInning = upper(@top),
      pScore = @pScore,
      batterID = @batterID,
      batDir = @stand,
      pitcherID = @pitcherID,
      pitchDir = @pThrows,
      event = @event,
      outsAfter = @o;

create table Pitches_Origin (abID decimal(10),
  pitchNum int,
  pitchType char(2),
  startSpeed float(1),
  endSpeed float(1),
  spinRate float(3),
  code char(2),
  ballCount int,
  strikeCount int,
  bScore int,
  outs int,
  on1B char(5),
  on2B char(5),
  on3B char(5)
);

-- load the data
load data infile '/var/lib/mysql-files/17-MLB/pitches.csv'
ignore into table Pitches_Origin
  fields terminated by ','
  lines terminated by '\n'
  ignore 1 lines
  (@px, @pz, @startSpeed, @endSpeed, @spinRate, @spinDir, @breakAngle, @breakLen, @breakY, @ax, @ay, @az, @szBot, @szTop, @typeConfidence, @vx0, @vy0, @vz0, @x, @x0, @y, @y0, @z0, @pfxX, @pfxZ, @nasty, @zone, @code, @type, @pitchType, @eventNumber, @bScore, @abID, @bCount, @sCount, @outs, @pitchNumber, @on1b, @on2b, @on3b)
  set abID = @abID,
      pitchNum = @pitchNumber,
      pitchType = if(@pitchType= '', null, @pitchType),
      startSpeed = if(@startSpeed = '', null, round(@startSpeed, 1)),
      endSpeed = if(@endSpeed = '', null, round(@endSpeed, 1)),
      spinRate = if(@spinRate = '', null, round(@spinRate, 3)),
      code = if(@code = '', null, @code),
      ballCount = @bCount,
      strikeCount = @sCount,
      bScore = @bScore,
      outs = @outs,
      on1B = if(@on1b = 0, 'FALSE', 'TRUE'),
      on2B = if(@on2b = 0, 'FALSE', 'TRUE'),
      on3B = if(@on3b = 0, 'FALSE', 'TRUE');

create table Ejections_Origin (abID decimal(10),
  playerID decimal(6),
  team char(3),
  description char(100),
  argueBallsStrikes char(5),
  correctEjection char(5)
);

-- load the data
-- some of the data has to be fixed
load data infile '/var/lib/mysql-files/17-MLB/ejections.csv'
ignore into table Ejections_Origin
  fields terminated by ','
  lines terminated by '\n'
  ignore 1 lines
  (@abID, @des, @eventNumber, @gID, @playerID, @gameDate, @bs, @correct, @team, @isHomeTeam)
  set abID = @abID,
      playerID = @playerID,
      team = upper(@team),
      description = @des,
      argueBallsStrikes = if(@bs = 'Y', 'TRUE', 'FALSE'),
      correctEjection = if(@correct = 'C', 'TRUE', if(@correct = 'I', 'FALSE', null));

update Ejections_Origin
  set team = 'ANA' where team = 'LAA';
update Ejections_Origin
  set team = 'SLN' where team = 'STL';
update Ejections_Origin
  set team = 'ARI' where team = 'AZN';

-- in this database, we only care about the players (pitchers and hitters, etc.)
-- we don't care about managers, coaches, etc.
-- many of the ejections are related to coaches and managers, so we can remove those from the table

delete from Ejections_Origin where playerID not in (select id from PlayerNames);

-- alter table Ejections_Origin
--   add foreign key (team) references TeamNames(abbreviation),
--   add foreign key (playerID) references PlayerNames(id);

-- Finish
nowarning
notee;
