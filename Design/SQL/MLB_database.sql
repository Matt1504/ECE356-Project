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

create table PlayerNames (id decimal(6),
  firstName char(15),
  lastName char(20),
  primary key (id)
);

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
  foreign key (homeTeam) references TeamNames(abbreviation),
  foreign key (awayTeam) references TeamNames(abbreviation),
  check(left(gID,4) = year(gameDate))
);

create table AtBats (abID decimal(10),
  gID decimal(9),
  inning int check(inning > 0 and inning < 10),
  topInning char(5) check(topInning in ('TRUE', 'FALSE')),
  pScore int not null check(pScore >= 0),
  bScore int not null check(bScore >= 0),
  batterID decimal(6),
  batDir char(1) not null check(batDir in ('TRUE', 'FALSE')),
  pitcherID decimal(6),
  pitchDir char(1) not null check(pitchDir in ('L', 'R')),
  event char(15) not null,
  outsAfter decimal(1) not null check (outsAfter >= 0 and outsAfter <= 3),
  primary key (abID),
  foreign key (gID) references Games(gID),
  foreign key (batterID) references PlayerNames(id),
  foreign key (pitcherID) references PlayerNames(id),
  check(left(abID,4) = left(gID,4))
);

create table Pitches (abID decimal(10),
  pitchNum int not null check(pitchNum > 0),
  pitchType char(2) not null check (pitchType in ('CH', 'CU', 'EP', 'FC', 'FF', 'FO', 'FS', 'IN', 'KC', 'KN', 'PO', 'SC', 'SI', 'SL', 'UN')),
  startSpeed float(1) not null,
  endSpeed float(1) not null,
  spinRate float(3),
  code char(2) not null check (code in ('B', '*B', 'S', 'C', 'F', 'T', 'L', 'I', 'W', 'M', 'P', 'Q', 'R', 'X', 'D', 'E', 'H')),
  ballCount int not null check (ballCount >= 0 and ballCount <= 4),
  strikeCount int not null check (strikeCount >= 0 and strikeCount <= 2),
  outs int not null check (outs <= 0 and outs >= 3),
  on1B char(5) check(on1B in ('TRUE', 'FALSE')),
  on2B char(5) check(on2B in ('TRUE', 'FALSE')),
  on3B char(5) check(on3B in ('TRUE', 'FALSE')),
  primary key (abID, pitchNum),
  foreign key (abID) references AtBats(abID),
  check(startSpeed > 0.0 and startSpeed > endSpeed),
  check(endSpeed > 0.0 and endSpeed < startSpeed)
);

create table Ejections (abID decimal(10),
  playerID decimal(6),
  team char(3),
  description char(100),
  argueBallsStrikes char(5) check(argueBallsStrikes in ('TRUE', 'FALSE')),
  correctEjection char(5) check(correctEjection in ('TRUE', 'FALSE')),
  primary key (abID, playerID),
  foreign key (abID) references AtBats(abID),
  foreign key (playerID) references PlayerNames(id)
);
