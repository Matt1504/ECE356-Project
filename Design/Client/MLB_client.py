import mysql.connector
from prettytable import PrettyTable
import datetime
from collections import deque

pitch_legend = {
	'CH': 'Changeup',
	'CU': 'Curveball',
	'EP': 'Eephus',
	'FC': 'Cutter',
	'FF': 'Four-seam Fastball',
	'FO': 'Pitchout',
	'FS': 'Splitter',
	'FT': 'Two-seam Fastball',
	'IN': 'Intentional ball',
	'KC': 'Knuckle curve',
	'KN': 'Knuckeball',
	'PO': 'Pitchout',
	'SC': 'Screwball',
	'SI': 'Sinker',
	'SL': 'Slider',
	'UN': 'Unknown',
}

hit_legend = ['Single', 'Double', 'Triple', 'Home Run']
on_base_legend = ['Single', 'Double', 'Triple', 'Home Run', 'Walk', 'Hit By Pitch']
not_at_bat = ['Walk', 'Intent Walk', 'Hit By Pitch', 'Sac Bunt', 'Sac Fly', 'Sac Fly DP']

class Batter:
	def __init__(self, at_bats = 0, hits = 0, walks = 0, rbi = 0):
		self.at_bats = at_bats
		self.hits = hits
		self.walks = walks
		self.rbi = rbi

class Pitcher:
	def __init__(self, innings = 0.0, hits = 0, walks = 0, strikeouts = 0):
		self.innings = innings
		self.hits = hits
		self.walks = walks
		self.strikeouts = strikeouts

class MLB:
	def __init__(self):
		self.nav = ''
		self.playerID = 0
		self.home = ''
		self.away = ''
		self.gameID = 0
		self.cnx = mysql.connector.connect(user='kh37lee', password='Zaqwsx@1021102', host='marmoset04.shoshin.uwaterloo.ca', database='project_36');
		self.cursor = self.cnx.cursor()
		self.years = ['2015', '2016', '2017', '2018']
		self.team_names = {}
		self.team_abbrev = {}
		self.team_cities = {}

	def print_teams(self, show_all = True):
		if show_all:
			query = "select concat(city, ' ', shortName) from TeamNames;"
		else:
			query = "select shortName from TeamNames;"
		# run the query
		# print the results
		self.cursor.execute(query)
		results = self.cursor.fetchall()
		print('Below is all MLB Teams')
		for x in results:
			print(''.join(x))

	def print_players(self, pitchers=True):
		if pitchers:
			query = "select concat(lastName, ', ', firstName) from PlayerNames where id in (select distinct pitcherID from AtBats);"
		else:
			query = "select concat(lastName, ', ', firstName) from PlayerNames where id in (select distinct batterID from AtBats)"
		# run the query
		# print the results
		self.cursor.execute(query)
		results = self.cursor.fetchall()
		for x in results:
			print(x[0])

	def home_page(self):
		print('\nWelcome to the MLB Stats Database for the 2015-2018 Regular Seasons')
		print('Input \"back\" to go to previous page, or \"home\" to go back to this page at any point, or \"exit\" to close the application')
		print('Do you want to view:')
		print('\t1. Game Data')
		print('\t2. Player Data')
		self.nav = input('Enter where you want to go: ')
		if self.nav == '1':
			self.game_page()
		elif self.nav == '2':
			self.player_page()
		elif self.nav == 'home':
			self.home_page()
		elif self.nav == 'back':
			self.home_page()
		elif self.nav == 'exit':
			self.cleanup()
		else:
			print('Invalid Input')
			self.home_page()

	def game_page(self):
		print('\nGame Data')
		print('Do you want to view:')
		print('\t1. A Single Game')
		print('\t2. Combined Team Data')
		self.nav = input('Enter where you want to go: ')
		if self.nav == '1':
			self.game_info()
		elif self.nav == '2':
			self.team_info()
		elif self.nav == 'home':
			self.home_page()
		elif self.nav == 'back':
			self.home_page()
		elif self.nav == 'exit':
			self.cleanup()
		else:
			print('Invalid Input')
			self.game_page()

	def player_page(self):
		print('\nPlayer Data')
		print('Do you want to view:')
		print('\t1. Pitcher\'s Data')
		print('\t2. Batter\'s Data')
		self.nav = input('Enter where you want to go: ')
		if self.nav == '1':
			self.pitcher_info()
		elif self.nav == '2':
			self.batter_info()
		elif self.nav == 'home':
			self.home_page()
		elif self.nav == 'back':
			self.home_page()
		elif self.nav == 'exit':
			self.cleanup()
		else:
			print('Invalid Input')
			self.player_page()

	def game_info(self):
		print('\nGame Data: Single Game')
		print('Type \"year\" to filter games by year, or \"team\" to filter games by team')
		print('Input format: \"<home_team>, <away_team>, <yyyy-mm-dd>\". (Example: Cubs, Cardinals, 2015-04-05)')
		self.nav = input('Enter the home team, away team, and teh date of the game you are looking for : ')
		if self.nav == 'back':
			self.game_page()
		elif self.nav == 'home':
			self.home_page()
		elif self.nav == 'exit':
			self.cleanup()
		elif self.nav == 'year' or self.nav == 'team':
			if self.nav == 'year':
				self.nav = input('Enter the desired year to display all games by that year (Ex: 2015): ')
				print('showing games from ', self.nav)
				# run query to get all games from that year
				if self.nav not in self.years:
					print('Not a valid year!')
					self.game_info()
				else:
					query = "select concat(a.shortName, ', ', b.shortName, ', ', c.gameDate) from Games c left join TeamNames a on c.homeTeam = a.abbreviation left join TeamNames b on c.awayTeam = b.abbreviation where year(c.gameDate) = '" + self.nav + "';"
					self.cursor.execute(query)
					results = self.cursor.fetchall()
					for x in results:
						print(''.join(x))
					self.game_info()
			else:
				# run query to get all team names
				# print teams
				self.print_teams(False)
				self.nav = input('Enter the number of the games you want to see from the desired team (Ex: Blue Jays): ')
				# run query to get all games from that team
				if self.nav not in self.team_abbrev:
					print('Not a valid team name!')
					self.game_info()
				else:
					query = "select concat(a.shortName, ', ', b.shortName, ', ', c.gameDate) from Games c left join TeamNames a on c.homeTeam = a.abbreviation left join TeamNames b on c.awayTeam = b.abbreviation where a.shortName = '" + self.nav + "' or b.shortName = '" + self.nav + "';"
					self.cursor.execute(query)
					results = self.cursor.fetchall()
					for x in results:
						print(''.join(x))
					self.game_info()
		else:
			self.print_game_info()

	def team_info(self):
		print('\nGame Data: Combined Team Data')
		print('Type \"show teams\" to display all active teams')
		print('Input format: \"<team_name>\". Do not include the city. (Example: Blue Jays)')
		self.nav = input('Enter the team\'s name of the team you are looking for: ')
		if self.nav == 'back':
			self.game_page()
		elif self.nav == 'home':
			self.home_page()
		elif self.nav == 'exit':
			self.cleanup()
		elif self.nav == 'show teams':
			self.print_teams(False)
			self.team_info()
		else:
			# get the info for that team
			self.print_team_info()
			self.team_info()

	def print_game_info(self):
		# run query to get the game data
		inputs = self.nav.split(', ')
		# make sure the inputs are valid
		if inputs[0] in self.team_abbrev and inputs[1] in self.team_abbrev:
			home_team = inputs[0]
			away_team = inputs[1]
			game_date = inputs[2]
			# run the query
			self.home = self.team_abbrev[inputs[0]]
			self.away = self.team_abbrev[inputs[1]]
			query = "select a.city ,a.shortName, b.city, b.shortName, c.* from Games c left join TeamNames a on c.homeTeam = a.abbreviation left join TeamNames b on c.awayTeam = b.abbreviation where homeTeam = '" + self.team_abbrev[inputs[0]] + "' and awayTeam = '"+ self.team_abbrev[inputs[1]] +"' and gameDate='" + game_date + "';"
			self.cursor.execute(query)
			# get the number of rows
			results = self.cursor.fetchone()
			if not results:
				print('Game Does Not Exist!')
			else:
				self.gameID = results[4]
				t = PrettyTable()
				t.field_names=['Label', 'Value']
				t.align='l'
				t.add_row(['Final Score', '(' + str(results[8]) + ') ' + results[1] + ' vs. (' + str(results[6]) + ') ' + results[3]])
				t.add_row(['Venue', results[10]])
				t.add_row(['Attendance', results[11]])
				t.add_row(['Start Time', results[12]])
				t.add_row(['Delay', str(results[13]) + ' mins'])
				t.add_row(['Game Length', str(results[14]) + ' mins'])
				t.add_row(['Weather', str(results[15]) + ' degrees'])
				t.add_row(['Wind', str(results[16]) + ' mph,' + results[17]])
				table_title = results[2] + ' ' + results[3] + ' at ' + results[0] + ' ' + results[1] + ' on ' + results[9].strftime("%Y-%m-%d")
				print(t.get_string(title=table_title))
				self.print_game_details()
		else:
			print('Invalid Input Format')

	def print_game_details(self):
		print('\n1. (Home)', self.team_names[self.home])
		print('2. (Away)', self.team_names[self.away])
		self.nav = input('Enter the number of the team you want to view the Batter and Pitcher Stats for:')
		if self.nav == '1' or self.nav == '2':
			query = " select distinct inning, topInning, concat(b.firstName,' ', b.lastName) as batter, pt.bScore, concat(p.firstName, ' ', p.lastName) as pitcher, a.event, pt.on1B, pt.on2B, pt.on3B, pt.outs from AtBats a left join PlayerNames b on a.batterID = b.id left join PlayerNames p on a.pitcherID = p.id left join Pitches pt using (abID) where gID = " + str(self.gameID) + ";"
			self.cursor.execute(query)
			results = self.cursor.fetchall()

			# batters and pitchers set where the key will be the player name and the value will be the the Batter or Pitcher class
			batters = {}
			pitchers = {}

			tb = PrettyTable()
			tb.field_names = ['Batter', 'At Bats', 'Hits', 'Walks', 'RBI']
			tb.align = 'l'

			tp = PrettyTable()
			tp.field_names = ['Pitcher', 'Innings Played', 'Hits', 'Walks', 'Strikeouts']
			tp.align = 'l'

			if self.nav == '1':
				# show home Stats
				# get the batting stats
				# home will bat at the bottom of the inning, so topInning = 'FALSE'
				curr_score = 0
				prev_batter = ''

				for x in results:
					if x[1] == 'TRUE':
						continue
					# batting stats include Player, At Bats, Runs, Hits, Walks, RBI
					if x[2] not in batters:
						# add the player to the set
						batters[x[2]] = Batter()

					if curr_score != x[3]:
						# at least 1 run has been made in the previous play
						# increase the previous player's rbi by the score difference
						batters[prev_batter].rbi += x[3] - curr_score
						curr_score = x[3]

					if x[5] in not_at_bat:
						if x[5] == 'Walk' or x[5] == 'Intent Walk':
							batters[x[2]].walks += 1
					else:
						batters[x[2]].at_bats += 1
						if x[5] in hit_legend:
							batters[x[2]].hits += 1

					prev_batter = x[2]

				# add the rows using the batters dictionary
				for key in batters:
					tb.add_row([key, batters[key].at_bats, batters[key].hits, batters[key].walks, batters[key].rbi])

				# print the table
				batting_title = self.team_cities[self.home] + ' ' +  self.team_names[self.home] + ' Batting'
				print(tb.get_string(title=batting_title))

				# pitching stats
				# home team will be pitching at the top of the inning, so topInning = 'TRUE'
				curr_inning = 0
				inning_pitcher = ''
				full_pitch = True
				inning_outs = 0
				for x in results:
					# pitching stats include Pitcher, Innings, Hits, Walks, Strikeouts
					if x[1] == 'FALSE':
						continue

					# innings are in terms of outs
					# 3 outs made = 1 inning pitched
					# 1 out = 1/3 or 0.1, 2 outs = 2/3 or 0.2
					if x[4] not in pitchers:
						pitchers[x[4]] = Pitcher()

					if curr_inning == 0:
						curr_inning = x[0]
						inning_pitcher = x[4]

					if curr_inning != x[0]:
						if full_pitch == False:
							pitchers[inning_pitcher].innings += (float(3.0 - inning_outs) * 0.1)
						else:
							pitchers[inning_pitcher].innings += 1.0
						curr_inning = x[0]
						inning_pitcher = x[4]
						full_pitch = True
						inning_outs = 0

					if inning_pitcher != x[4]:
						# pitcher changed during the inning
						full_pitch = False
						o = x[9] - inning_outs
						pitchers[inning_pitcher].innings += float(o) * 0.1
						inning_outs = x[9]
						inning_pitcher = x[4]

					if x[5] in hit_legend:
						pitchers[x[4]].hits += 1
					else:
						if x[5] == 'Walk' or x[5] == 'Intent Walk':
							pitchers[x[4]].walks += 1
						elif x[5] == 'Strikeout':
							pitchers[x[4]].strikeouts += 1

				# calculate innings played for last pitcher
				if full_pitch == False:
					pitchers[inning_pitcher].innings += (float(3.0 - inning_outs) * 0.1)
				else:
					pitchers[inning_pitcher].innings += 1.0

				for key in pitchers:
					tp.add_row([key, pitchers[key].innings, pitchers[key].hits, pitchers[key].walks, pitchers[key].strikeouts])

				pitching_title = self.team_cities[self.home] + ' ' + self.team_names[self.home] + ' Pitching'
				print(tp.get_string(title=pitching_title))

			else:
				# show away stats
				# batting stas
				# away team bats at the top of the inning
				curr_score = 0
				prev_batter = ''
				for x in results:
					if x[1] == 'FALSE':
						continue
					# batting stats include Player, At Bats, Runs, Hits, Walks, RBI
					if x[2] not in batters:
						# add the player to the set
						batters[x[2]] = Batter()

					if curr_score != x[3]:
						# at least 1 run has been made in the previous play
						# increase the previous player's rbi by the score difference
						batters[prev_batter].rbi += x[3] - curr_score
						curr_score = x[3]

					if x[5] in not_at_bat:
						if x[5] == 'Walk' or x[5] == 'Intent Walk':
							batters[x[2]].walks += 1
					else:
						batters[x[2]].at_bats += 1
						if x[5] in hit_legend:
							batters[x[2]].hits += 1

					prev_batter = x[2]

				# add the rows using the batters dictionary
				for key in batters:
					tb.add_row([key, batters[key].at_bats, batters[key].hits, batters[key].walks, batters[key].rbi])

				# print the table
				batting_title = self.team_cities[self.away] + ' ' +  self.team_names[self.away] + ' Batting'
				print(tb.get_string(title=batting_title))

				# pitching stats
				# away team will be pitching at the bottom of the inning, so topInning = 'FALSE'
				inning_pitcher = ''
				curr_inning = 0
				full_pitch = True
				inning_outs = 0
				for x in results:
					if x[1] == 'TRUE':
						continue
					# pitching stats include Pitcher, Innings, Hits, Walks, Strikeouts
					if x[4] not in pitchers:
						pitchers[x[4]] = Pitcher()

					if curr_inning == 0:
						curr_inning = x[0]
						inning_pitcher = x[4]

					if curr_inning != x[0]:
						if full_pitch == False:
							pitchers[inning_pitcher].innings += (float(3.0 - inning_outs) * 0.1)
						else:
							pitchers[inning_pitcher].innings += 1.0
						curr_inning = x[0]
						inning_pitcher = x[4]
						full_pitch = True
						inning_outs = 0

					if inning_pitcher != x[4]:
						# pitcher changed during the inning
						full_pitch = False
						o = x[9] - inning_outs
						pitchers[inning_pitcher].innings += float(o) * 0.1
						inning_outs = x[9]
						inning_pitcher = x[4]

					if x[5] in hit_legend:
						pitchers[x[4]].hits += 1
					else:
						if x[5] == 'Walk' or x[5] == 'Intent Walk':
							pitchers[x[4]].walks += 1
						elif x[5] == 'Strikeout':
							pitchers[x[4]].strikeouts += 1

				# calculate the innings pitched for the last pitcher
				if full_pitch == False:
					pitchers[inning_pitcher].innings += (float(3.0 - inning_outs) * 0.1)
				else:
					pitchers[inning_pitcher].innings += 1.0

				for key in pitchers:
					tp.add_row([key, pitchers[key].innings, pitchers[key].hits, pitchers[key].walks, pitchers[key].strikeouts])

				pitching_title = self.team_cities[self.away] + ' ' + self.team_names[self.away] + ' Pitching'
				print(tp.get_string(title=pitching_title))
			self.print_game_details()
		elif self.nav == 'back':
			self.game_info()
		elif self.nav == 'home':
			self.home_page()
		elif self.nav == 'exit':
			self.cleanup()
		else:
			print('Invalid Input')
			self.print_game_details()

	def print_team_info(self):
		# check that the input is valid
		if self.nav not in self.team_abbrev:
			print('Team does not exist')
			self.team_info()
		else:
			query = """
				select gameYear, sum(runs), sum(runsAllowed), sum(games), sum(wins), sum(attendance) from
				  (
				    (select year(gameDate) as gameYear, sum(homeFinalScore) as runs, sum(awayFinalScore) as runsAllowed, count(gID) as games, count(case when winningTeam = 'TOR' then 1 else null end) as wins, sum(attendance) as attendance from Games
				      where homeTeam='TOR' group by year(gameDate))
				    union all
				    (select year(gameDate) as gameYear, sum(awayFinalScore) as runs, sum(awayFinalScore) as runsAllowed, count(gID) as games, count(case when winningTeam = 'TOR' then 1 else null end) as wins, 0 as attendance from Games where awayTeam = 'TOR' group by year(gameDate)
				  )) teamGames group by gameYear;
			"""
			self.cursor.execute(query)
			results = self.cursor.fetchall()
			full_team = self.team_cities[self.team_abbrev[self.nav]] + ' ' + self.nav + ' 2015-2018'
			t = PrettyTable()
			t.field_names = ['Season', 'Record', 'Total Runs', 'Avg Runs/Game', 'Total Runs Allowed', 'Avg Runs Allowed/Game', 'Total Attendance']
			t.align='l'
			for x in results:
				t.add_row([x[0], str(x[4]) + '-' + str(int(x[3])-int(x[4])), x[1], round(float(x[1])/float(x[4]),2), x[2], round(float(x[2])/float(x[4]),2), x[5]])
			print(t.get_string(title=full_team))

	def pitcher_info(self):
		print('\nPlayer Data: Pitchers')
		print('Input format: <last name>, <first name>')
		print('Type \"show pitchers\" to display all pitchers')
		self.nav = input('Enter the name of the pitcher you are looking for: ')
		if self.nav == 'back':
			self.player_page()
		elif self.nav == 'home':
			self.home_page()
		elif self.nav == 'show pitchers':
			self.print_players(True)
			self.pitcher_info()
		elif self.nav == 'exit':
			self.cleanup()
		else:
			# split the string
			inputs = self.nav.split(', ')
			if len(inputs) != 2:
				print('Invalid Input!')
				self.pitcher_info()
			else:
				last_name = inputs[0]
				first_name = inputs[1]
				# get and print the basic player info
				self.print_pitcher_info()
				self.pitcher_info()

	def batter_info(self):
		print('\nPlayer Data: Batters')
		print('Input format: <last name>, <first name>')
		print('Type \"show batters\" to display all batters')
		self.nav = input('Enter the name of the batter you are looking for: ')
		if self.nav == 'back':
			self.player_page()
		elif self.nav == 'home':
			self.home_page()
		elif self.nav == 'show batters':
			self.print_players(False)
			self.batter_info()
		elif self.nav == 'exit':
			self.cleanup()
		else:
			# get the player info
			# split the string
			inputs = self.nav.split(', ')
			if len(inputs) != 2:
				print('Invalid Input!')
				self.batter_info()
			else:
				last_name = inputs[0]
				first_name = inputs[1]
				# get and print the basic player info
				self.print_batter_info()
				self.batter_info()

	def print_pitcher_info(self):
		# first check that the player exists
		# split the string
		inputs = self.nav.split(', ')
		last_name = inputs[0]
		first_name = inputs[1]

		query = "select id from PlayerNames where firstName = '" + first_name + "' and lastName = '" + last_name + "';"
		self.cursor.execute(query)
		# get the number of rows
		results = self.cursor.fetchone()
		if not results:
			print('Player Does Not Exist!')
			self.pitcher_info()
		else:
			# have the id, so now can get the rest of the player data
			self.playerID = results[0]
			# note that the visiting team always bats at the top of the inning
			# earned run average = earned runs / innings pitched  * 9
			query = "select distinct a.gID, g.homeTeam, a.inning, g.awayTeam, p.bScore, g.winningTeam, a.topInning, a.pitchDir from AtBats a left join Games g using(gID) left join Pitches p using (abID) where pitcherID = " + str(self.playerID) + ";"

			# print the data
			self.cursor.execute(query)
			results = self.cursor.fetchall()
			hand = []
			teams = []
			win_count = 0
			loss_count = 0
			games_started = 0
			inning_count = 0
			earned_runs = 0

			curr_inning = 0
			gId = 0
			prev_bscore = 0
			# Earned Run Average (ERA) = Earned Runs / Innings Pitched * 9, where Earned Runs is just the bScore
			for x in results:
				# tally the earns runed in Total
				if gId != x[0] and gId != 0:
					earned_runs += prev_bscore

				# check the game counter
				if gId != x[0]:
					gId = x[0]
					# if he started the game, the first record for that game should be inning 1
					if x[2] == 1:
						games_started += 1
					# check who wins and loses and increment accordingly
					# if he pitches on top inning, then he plays for the home team
					if (x[5] == x[1] and x[6] == 'TRUE') or (x[5] == x[3] and x[6] == 'FALSE'):
						win_count += 1
					else:
						loss_count += 1

				# need to count innings played
				if curr_inning != x[2]:
					curr_inning = x[2]
					inning_count += 1

				# check the pitchDir
				hand_dir = 'Left-Handed' if x[7] == 'L' else 'Right-Handed'
				if hand_dir not in hand:
					hand.append(hand_dir)
				# if topInning is true, then that means the visiting team is batting, so player is on the home team
				if x[6] == 'TRUE':
					team = self.team_cities[x[1]] + ' ' + self.team_names[x[1]]
					if team not in teams:
						teams.append(team)
				else:
					team = self.team_cities[x[3]] + ' ' + self.team_names[x[3]]
					if team not in teams:
						teams.append(team)

				prev_bscore = x[4]

			# print the calulcated stats
			print('\n' + first_name + ' ' + last_name)
			if len(hand) == 2:
				print('Ambidexterous')
			else:
				print(hand[0])
			print('\nPast and Current Teams:')
			print(*teams, sep = "\n")
			tb = PrettyTable()
			tb.field_names = ['Stat', 'Value']
			tb.align = 'l'

			era = earned_runs / inning_count * 9.0
			tb.add_row(['Total Games', win_count + loss_count])
			tb.add_row(['Games Started', games_started])
			tb.add_row(['Record', str(win_count) + '-' + str(loss_count)])
			tb.add_row(['Earned Run Average', round(era,2)])

			print(tb.get_string(title='Overall Pitching Stats'))

			# grab and print pitch stats
			query = "select pitchType, count(pitchType), avg(p.startSpeed), avg(p.endSpeed), avg(p.spinRate) from Pitches p left join AtBats a using (abID) where a.pitcherID = " + str(self.playerID) + " group by p.pitchType;"
			self.cursor.execute(query)
			results = self.cursor.fetchall()

			t = PrettyTable()
			t.field_names = ['Pitch Type', 'Total Thrown', 'Average Start Speed (MPH)', 'Average End Speed (MPH)', 'Average Spin Rate']
			t.align = 'l'
			for x in results:
				if x[0] in pitch_legend:
					t.add_row([pitch_legend[x[0]], x[1], round(x[2],2), round(x[3],2), round(x[4],2)])
			print(t.get_string(title='Pitch Breakdown'))

	def print_batter_info(self):
		# first check that the player exists
		# split the string
		inputs = self.nav.split(', ')
		last_name = inputs[0]
		first_name = inputs[1]

		query = "select id from PlayerNames where firstName = '" + first_name + "' and lastName = '" + last_name + "';"
		self.cursor.execute(query)
		# get the number of rows
		results = self.cursor.fetchone()
		if not results:
			print('Player Does Not Exist!')
			self.batter_info()
		else:
			# have the id, so now can get the rest of the player data
			self.playerID = results[0]

			query = "select a.gID, g.homeTeam, g.awayTeam, g.winningTeam, a.inning, a.topInning, a.batDir, a.event from AtBats a left join Games g using (gID)  where batterID = " + str(self.playerID) + ";"
			self.cursor.execute(query)
			results = self.cursor.fetchall()

			# now gotta parse through all the data
			bat_dir = []
			teams = []

			win_count = [0,0,0,0]
			loss_count = [0,0,0,0]
			at_bats = [0,0,0,0]
			plate_appearance = [0,0,0,0]
			singles = [0,0,0,0]
			doubles = [0,0,0,0]
			triples = [0,0,0,0]
			home_runs = [0,0,0,0]
			hits = [0,0,0,0]
			gId = 0
			times_on_base = [0,0,0,0]

			# batting average = hits / at bats
			# a hit = single, double, triple, homerun
			for x in results:
				# separate the stats based on year (from the first 4 digits of the gID)
				yr = int(str(x[0])[:4])

				# year can be from 2015 - 2018
				yr = yr - 2015

				plate_appearance[yr] += 1
				# at bat does not include walks, hits by pitch, sacrifices
				if x[7] not in not_at_bat:
					at_bats[yr] += 1
				if x[7] in hit_legend:
					hits[yr] += 1
				if x[7] in on_base_legend:
					times_on_base[yr] += 1

				if x[7] == 'Single':
					singles[yr] += 1
				elif x[7] == 'Double':
					doubles[yr] += 1
				elif x[7] == 'Triple':
					triples[yr] += 1
				elif x[7] == 'Home Run':
					home_runs[yr] += 1

				# check the game counter
				if gId != x[0]:
					gId = x[0]
					# check who wins and loses and increment accordingly
					# batting at the top of the inning = playing for away team
					if (x[3] == x[2] and x[5] == 'TRUE') or (x[3] == x[1] and x[5] == 'FALSE'):
						win_count[yr] += 1
					else:
						loss_count[yr] += 1

					# check the batDir
					dir = 'Left-Handed' if x[6] == 'L' else 'Right-Handed'
					if dir not in bat_dir:
						bat_dir.append(dir)
					# if topInning is true, then that means the visiting team is batting, so player is on the away team
					if x[5] == 'TRUE':
						team = self.team_cities[x[2]] + ' ' + self.team_names[x[2]]
						if team not in teams:
							teams.append(team)
					else:
						team = self.team_cities[x[1]] + ' ' + self.team_names[x[1]]
						if team not in teams:
							teams.append(team)

			# print the calulcated stats
			print('\n' + first_name + ' ' + last_name)
			if len(bat_dir) == 2:
				print('Ambidexterous')
			else:
				print(bat_dir[0])
			print('\nPast and Current Teams:')
			print(*teams, sep = "\n")

			t = PrettyTable()
			t.field_names = ['Stat', 'Value']
			t.align='l'

			t.add_row(['Total Games', sum(win_count) + sum(loss_count)])
			t.add_row(['Record', str(sum(win_count)) + '-' + str(sum(loss_count))])
			t.add_row(['At Bats', sum(at_bats)])
			t.add_row(['Hits', sum(hits)])
			t.add_row(['Home Runs', sum(home_runs)])
			t.add_row(['On Base Percentage', round(float(sum(times_on_base)/sum(at_bats)),3)])
			t.add_row(['Batting Average', round(float(sum(hits)/sum(at_bats)),3)])
			t.add_row(['Slugging Percentage', round((sum(singles) + 2 * sum(doubles) + 3 * sum(triples) + 4 * sum(home_runs))/sum(at_bats),4)])
			print(t.get_string(title='Overall Batting Stats'))

			tb = PrettyTable()
			tb.field_names = ['Year', 'Games Played', 'Record', 'At Bats', 'Hits', 'Singles', 'Doubles', 'Triples', 'Home Runs', 'OBP', 'BA', 'SLG']
			tb.align = 'l'

			for i in range(0, 4):
				if at_bats[i] > 0:
					tb.add_row([self.years[i], win_count[i] + loss_count[i], str(win_count[i]) + '-' + str(loss_count[i]), at_bats[i], hits[i], singles[i], doubles[i], triples[i], home_runs[i], round(float(times_on_base[i]/at_bats[i]),3), round(float(hits[i]/at_bats[i]),3), round((singles[i] + 2 * doubles[i] + 3 * triples[i] + 4 * home_runs[i])/at_bats[i],4)])

			print(tb.get_string(title='Yearly Batting Stats'))


	def first_load(self):
		# have to first load the team dictionary
		query = "select * from TeamNames"
		self.cursor.execute(query)
		results = self.cursor.fetchall()
		# first column = abbreviation
		# second column = City
		# third column = shortName
		for x in results:
			# load first into team_abbrev
			# Ex: team_abbrev[Blue Jays] = TOR
			self.team_abbrev[x[2]] = x[0]
			# Load into team_cities
			# Ex: team_cities[TOR] = Toronto
			self.team_cities[x[0]] = x[1]
			# Load into team_names
			# Ex: team_names[TOR] = Blue Jays
			self.team_names[x[0]] = x[2]
		# load home page
		self.home_page()

	def cleanup(self):
		self.cursor.close()
		self.cnx.close()
		print('Thank you for using our MLB client')
		print('Exiting...')

MLB_client = MLB()
MLB_client.first_load()
