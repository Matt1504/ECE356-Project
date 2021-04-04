import mysql.connector

years = ['2015', '2016', '2017', '2018']
team_names = {
	'Angels': 'ANA',
	'Diamondbacks': 'ARI',
	'Braves': 'ATL',
	'Orioles': 'BAL',
	'Red Sox': 'BOS',
	'White Sox': 'CHA',
	'Cubs': 'CHN',
	'Reds': 'CIN',
	'Indians': 'CLE',
	'Rockies': 'COL',
	'Tigers': 'DET',
	'Astros': 'HOU',
	'Royals': 'KCA',
	'Dodgers': 'LAN',
	'Marilins': 'MIA',
	'Brewers': 'MIL',
	'Twins': 'MIN',
	'Yankees': 'NYA',
	'Mets': 'NYN',
	'Athletics': 'OAK',
	'Phillies': 'PHI',
	'Pirates': 'PHT',
	'Padres': 'SDN',
	'Mariners': 'SEA',
	'Giants': 'SFN',
	'Cardinals': 'SLN',
	'Rays': 'TBA',
	'Rangers': 'TEX',
	'Blue Jays': 'TOR',
	'Nationals': 'WAS'
}

class MLB:
	def __init__(self):
		self.nav = ''
		self.cnx = mysql.connector.connect(user='kh37lee', password='Zaqwsx@1021102', host='marmoset04.shoshin.uwaterloo.ca', database='project_36');
		self.cursor = self.cnx.cursor()

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

	def print_players(self):
		query = "select concat(lastName, ', ', firstName) from PlayerNames;"
		# run the query
		# print the results
		self.cursor.execute(query)
		results = self.cursor.fetchall()
		print('Below is all active MLB Players')
		for x in results:
			print(''.join(x))

	def home_page(self):
		print('Welcome to the MLB Stats Database for the 2015-2018 Regular Seasons')
		print('Input \"back\" to go to previous page, or \"home\" to go back to this page at any point.')
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

	def game_page(self):
		print('Game Data')
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

	def player_page(self):
		print('Player Data')
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

	def game_info(self):
		print('Game Data: Single Game')
		print('Type \"year\" to filter games by year, or \"team\" to filter games by team')
		print('Input format: \"<home_team>, <away_team>, <yyyy-mm-dd>\". Example: Cubs, Cardinals, 2015-04-05')
		self.nav = input('Enter the home team, away team, and teh date of the game you are looking for : ')
		if self.nav == 'back':
			self.game_page()
		elif self.nav == 'home':
			self.home_page()
		elif self.nav == 'year' or self.nav == 'team':
			if self.nav == 'year':
				self.nav = input('Enter the desired year to display all games by that year (Ex: 2015): ')
				print('showing games from ', self.nav)
				# run query to get all games from that year
				if self.nav not in years:
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
				if self.nav not in team_names:
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

	def print_game_info(self):
		# run query to get the game data
		inputs = self.nav.split(', ')
		# make sure the inputs are valid
		if inputs[0] in team_names and inputs[1] in team_names:
			home_team = inputs[0]
			away_team = inputs[1]
			game_date = inputs[2]
			# run the query
			query = "select a.city ,a.shortName, b.city, b.shortName, c.* from Games c left join TeamNames a on c.homeTeam = a.abbreviation left join TeamNames b on c.awayTeam = b.abbreviation where homeTeam = '" + team_names[inputs[0]] + "' and awayTeam = '"+ team_names[inputs[1]] +"' and gameDate='" + game_date + "';"
			self.cursor.execute(query)
			# get the number of rows
			results = self.cursor.fetchone()
			if not results:
				print('Game Does Not Exist')
				self.game_info()
			else:
				print(results[2], results[3], 'at', results[0], results[1], 'on', results[9])
				print('Final Score: \t(', results[8], ')', results[1], 'vs. (', results[6], ')', results[3])
				print('Venue:\t \t', results[10])
				print('Attendance:\t', results[11])
				print('Start Time:\t', results[12])
				print('Delay:\t \t', results[13], 'mins')
				print('Game Length:\t', results[14], 'mins')
				print('Weather:\t', results[15], 'degrees')
				print('Wind:\t \t', results[16], 'mph,', results[17])
				print('\n1. (Home)', results[3])
				print('2. (Away)', results[1])
				self.nav = input('Enter the number of the team you want to view the Batter and Pitcher Stats for:')
				if self.nav == 1:
					# show home Stats
					print(results[3], 'Batting:')
					print(results[3], 'Pitching:')
				else:
					# show away stats
					print(results[1], 'Batting:')
					print(results[1], 'Pitching:')

	def team_info(self):
		print('Game Data: Combined Team Data')
		print('Type \"show teams\" to display all active teams')
		self.team = input('Enter the team\'s name of the team you are looking for (Ex. Toronto Blue Jays): ')
		if self.team == 'back':
			self.game_page()
		elif self.team == 'home':
			self.home_page()
		else:
			if self.team == 'show teams':
				self.print_teams(True)
				self.team = input('Enter the team\'s name of the team you are looking for (Ex. Toronto Blue Jays): ')
			# get the info for that team

	def pitcher_info(self):
		print('Player Data: Pitchers')
		print('Input format: <last name>, <first name>')
		print('Type \"show players\" to display all active players')
		self.nav = input('Enter the name of the pitcher you are looking for: ')
		if self.nav == 'back':
			self.player_page()
		elif self.nav == 'home':
			self.home_page()
		else:
			if self.nav == 'show players':
				self.print_players()
				self.nav = input('Enter the name of the pitcher you are looking for: ')
			# split the string
			inputs = self.nav.split(', ')
			last_name = inputs[0]
			first_name = inputs[1]

			# get the player info

	def batter_info(self):
		print('Player Data: Batters')
		print('Input format: <last name>, <first name>')
		print('Type \"show players\" to display all active players')
		self.nav = input('Enter the name of the batter you are looking for: ')
		if self.nav == 'back':
			self.player_page()
		elif self.nav == 'home':
			self.home_page()
		else:
			if self.nav == 'show players':
				self.print_players()
				self.nav = input('Enter the name of the batter you are looking for: ')
			# split the string
			inputs = self.nav.split(', ')
			last_name = inputs[0]
			first_name = inputs[1]

			# get the player info

	def cleanup(self):
		cursor.close()
		cnx.close()
		print('Thank you for using our MLB client')
		print('Exiting...')

MLB_client = MLB()
MLB_client.home_page()
