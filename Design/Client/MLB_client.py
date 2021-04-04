import mysql.connector

class MLB:
	def __init__(self):
		self.nav = ''
		self.cnx = mysql.connector.connect(user='scott', password='password', host='marmoset04.shoshin.uwaterloo.ca', database='project_36');
		self.cursor = cnx.cursor()

	def print_teams(self):
		query = "select concat(city, ' ', shortName) from TeamNames;"
		# run the query 
		# print the results 
		print('Below is all MLB Teams')

	def print_players(self):
		query = "select concat(lastName, ', ', firstName) from PlayerNames;"
		# run the query
		# print the results 
		print('Below is all active MLB Players')
	
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
		print('Type \"year\" to filter games by year')
		print('Type \"team\" to filter games by team')
		print('Input format: <home_team> <away_team> <yyyy-mm-dd>')
		self.nav = input('Enter the home team, away team, and teh date of the game you are looking for : ')
		if self.nav == 'back':
			self.game_page()
		elif self.nav == 'home':
			self.home_page()
		else:
			if self.nav == 'year' or self.nav == 'team':
				if self.nav == 'year':
					self.nav = input('Enter the desired year to display all games by that year (2015-2018): ')
					print('showing games from ', self.nav)
					# run query to get all games from that year 
				else:
					# run query to get all team names 
					# print teams
					self.print_teams()
					self.nav = input('Enter the number of the games you want to see from the desired team: ')
					# run query to get all games from that team 
					# print games 
					print('Input format: <home_team> <away_team> <yyyy-mm-dd>')
					self.nav = input('Enter the home team, away team, and teh date of the game you are looking for :')

				# run query to get the game data
				inputs = self.nav.split()
				home_team = inputs[0]
				away_team = inputs[1]
				game_date = inputs[2]

				# run the query 

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
				self.print_teams()
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

