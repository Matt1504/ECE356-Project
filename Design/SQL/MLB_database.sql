------------------------------------------------------------
--
-- MLB Statistics 2015 - 2019
-- ECE 356 Project
--
-- Code used to create the MLB database for the project
--
-- History: initial creation 21 March 2021: ML

-- Clean out the old teefile
\! rm -f mlb-outfile.txt
tee mlb-outfile.txt

-- Show warnings after every statement
warnings;

drop table if exists PlayerNames;
drop table if exists Ejections;
drop table if exists AtBats;
drop table if exists Pitches;
drop table if exists TeamNames;
drop table if exists Games;

select '------------------------------------------------' as '';
select 'Create Teams' as '';

create table TeamNames (abbreviation char(3),
  city char(15) not null,
  shortName char(15) not null,
  primary key (abbreviation)
);

-- don't actually have a csv for teams, so have to make it ourselves

create table PlayerNames (id decimal(6),
  firstName char(15),
  lastName char(20),
  primary key (id)
);

-- load in the data
load data infile '/var/lib/mysql-files/17-MLB/player_names.csv'
ignore into table PlayerNames
  fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
  ignore 1 lines
  (id, firstName, lastName);

create table Games (gID decimal(9),
  homeTeam char(3) not null,
  homeFinalScore int check(homeFinalScore >= 0),
  awayTeam char(3) not null,
  awayFinalScore int check(awayFinalScore >= 0),
  gameDate date not null,
  venueName varchar(64) not null,
  attendance int,
  startTime time,
  delay int,
  elapsedTime int,
  weatherDegrees int,
  windSpeedMpH int,
  windDirection char(15),
  primary key (gID),
  check(left(gID,4) = year(gameDate))
);

load data infile '/var/lib/mysql-files/17-MLB/games.csv'
ignore into table Games
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

insert into TeamNames select distinct homeTeam, '', '' from Games;

update TeamNames set city = 'Los Angeles', shortName = 'Angels' where abbreviation = 'ANA';
update TeamNames set city = 'Arizona', shortName = 'Diamondbacks' where abbreviation = 'ARI';
update TeamNames set city = 'Atlanta', shortName = 'Braves' where abbreviation = 'ATL';
update TeamNames set city = 'Baltimore', shortName = 'Orioles' where abbreviation = 'BAL';
update TeamNames set city = 'Boston', shortName = 'Red Sox' where abbreviation = 'BOS';
update TeamNames set city = 'Chicago', shortName = 'White Sox' where abbreviation = 'CHA';
update TeamNames set city = 'Chicago', shortName = 'Cubs' where abbreviation = 'CHN';
update TeamNames set city = 'Cincinnati', shortName = 'Reds' where abbreviation = 'CIN';
update TeamNames set city = 'Cleveland', shortName = 'Indians' where abbreviation = 'CLE';
update TeamNames set city = 'Colorado', shortName = 'Rockies' where abbreviation = 'COL';
update TeamNames set city = 'Detroit', shortName = 'Tigers' where abbreviation = 'DET';
update TeamNames set city = 'Houston', shortName = 'Astros' where abbreviation = 'HOU';
update TeamNames set city = 'Kansas City', shortName = 'Royals' where abbreviation = 'KCA';
update TeamNames set city = 'Los Angeles', shortName = 'Dodgers' where abbreviation = 'LAN';
update TeamNames set city = 'Miami', shortName = 'Marlins' where abbreviation = 'MIA';
update TeamNames set city = 'Milwaukee', shortName = 'Brewers' where abbreviation = 'MIL';
update TeamNames set city = 'Minnesota', shortName = 'Twins' where abbreviation = 'MIN';
update TeamNames set city = 'New York', shortName = 'Yankees' where abbreviation = 'NYA';
update TeamNames set city = 'New York', shortName = 'Mets' where abbreviation = 'NYN';
update TeamNames set city = 'Oakland', shortName = 'Athletics' where abbreviation = 'OAK';
update TeamNames set city = 'Philadelphia', shortName = 'Phillies' where abbreviation = 'PHI';
update TeamNames set city = 'Pittsburgh', shortName = 'Pirates' where abbreviation = 'PIT';
update TeamNames set city = 'San Diego', shortName = 'Padres' where abbreviation = 'SDN';
update TeamNames set city = 'Seattle', shortName = 'Mariners' where abbreviation = 'SEA';
update TeamNames set city = 'San Francisco', shortName = 'Giants' where abbreviation = 'SFN';
update TeamNames set city = 'St. Louis', shortName = 'Cardinals' where abbreviation = 'SLN';
update TeamNames set city = 'Tampa Bay', shortName = 'Rays' where abbreviation = 'TBA';
update TeamNames set city = 'Texas', shortName = 'Rangers' where abbreviation = 'TEX';
update TeamNames set city = 'Toronto', shortName = 'Blue Jays' where abbreviation = 'TOR';
update TeamNames set city = 'Washington', shortName = 'Nationals' where abbreviation = 'WAS';

-- add back the foreign keys to the Games table after we have fully populated the TeamNames table
alter table Games
  add foreign key (homeTeam) references TeamNames(abbreviation),
  add foreign key (awayTeam) references TeamNames(abbreviation);

create table AtBats (abID decimal(10),
  gID decimal(9),
  inning int check(inning > 0),
  topInning char(5) check(topInning in ('TRUE', 'FALSE')),
  pScore int not null check(pScore >= 0),
  batterID decimal(6),
  batDir char(1) not null check(batDir in ('L', 'R')),
  pitcherID decimal(6),
  pitchDir char(1) not null check(pitchDir in ('L', 'R')),
  event char(25) not null,
  outsAfter decimal(1) not null check (outsAfter >= 0 and outsAfter <= 3),
  primary key (abID),
  foreign key (gID) references Games(gID),
  foreign key (batterID) references PlayerNames(id),
  foreign key (pitcherID) references PlayerNames(id),
  check(left(abID,4) = left(gID,4))
);

load data infile '/var/lib/mysql-files/17-MLB/atbats.csv'
ignore into table AtBats
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

create table Pitches (abID decimal(10),
  pitchNum int not null check(pitchNum > 0),
  pitchType char(2),
  startSpeed float(1),
  endSpeed float(1),
  spinRate float(3),
  code char(2),
  ballCount int not null check(ballCount >= 0 and ballCount <= 4),
  strikeCount int not null check(strikeCount >= 0 and strikeCount < 3),
  bScore int not null check(bScore >= 0),
  outs int not null check (outs >= 0 and outs < 3),
  on1B char(5) check(on1B in ('TRUE', 'FALSE')),
  on2B char(5) check(on2B in ('TRUE', 'FALSE')),
  on3B char(5) check(on3B in ('TRUE', 'FALSE')),
  primary key (abID, pitchNum),
  foreign key (abID) references AtBats(abID),
  check(pitchType is null or pitchType in ('CH', 'CU', 'EP', 'FA', 'AB', 'FC', 'FF', 'FO', 'FS', 'FT', 'IN', 'KC', 'KN', 'PO', 'SC', 'SI', 'SL', 'UN')),
  check(startSpeed is null or startSpeed > 0.0),
  check(endSpeed is null or endSpeed > 0.0),
  check(code is null or code in ('B', '*B', 'S', 'C', 'F', 'T', 'L', 'I', 'W', 'M', 'P', 'Q', 'R', 'X', 'D', 'E', 'H', 'V', 'Z'))
);

-- load the data
load data infile '/var/lib/mysql-files/17-MLB/pitches.csv'
ignore into table Pitches
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

create table Ejections (abID decimal(10),
  playerID decimal(6),
  team char(3),
  description char(100),
  argueBallsStrikes char(5) check(argueBallsStrikes in ('TRUE', 'FALSE')),
  correctEjection char(5) check(correctEjection in ('TRUE', 'FALSE')),
  primary key (abID, playerID),
  foreign key (abID) references AtBats(abID));
);

-- load the data
-- some of the data has to be fixed
load data infile '/var/lib/mysql-files/17-MLB/ejections.csv'
ignore into table Ejections
  fields terminated by ','
  lines terminated by '\n'
  ignore 1 lines
  (@abID, @des, @eventNumber, @gID, @playerID, @gameDate, @bs, @correct, @team, @isHomeTeam)
  set abID = @abID,
      playerID = @playerID,
      team = upper(@team),
      description = @des,
      argueBallsStrikes = if(@argueBallsStrikes = 'Y', 'TRUE', 'FALSE'),
      correctEjection = if(@correct = 'C', 'TRUE', if(@correct = 'I', 'FALSE', null));

update Ejections
  set team = 'ANA' where team = 'LAA';
update Ejections
  set team = 'SLN' where team = 'STL';
update Ejections
  set team = 'ARI' where team = 'AZN';

-- in this database, we only care about the players (pitchers and hitters, etc.)
-- we don't care about managers, coaches, etc.
-- many of the ejections are related to coaches and managers, so we can remove those from the table

delete from Ejections where playerID not in (select id from PlayerNames);

alter table Ejections
  add foreign key (team) references TeamNames(abbreviation),
  add foreign key (playerID) references PlayerNames(id);

-- Finish
nowarning
notee;
