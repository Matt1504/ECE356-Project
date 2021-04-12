import mysql.connector
from mysql.connector import Error
from prettytable import PrettyTable
import datetime
import math
from getpass import getpass

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
	def __init__(self, at_bats = 0, hits = 0, walks = 0, rbi = 0, strikeouts = 0, singles = 0, doubles = 0, triples = 0, home_runs = 0, sacs = 0):
		self.at_bats = at_bats
		self.hits = hits
		self.walks = walks
		self.rbi = rbi
		self.strikeouts = strikeouts
		self.singles = singles
		self.doubles = doubles
		self.triples = triples
		self.home_runs = home_runs
		self.sacs = sacs

class Pitcher:
	def __init__(self, innings = 0.0, hits = 0, runs = 0, walks = 0, strikeouts = 0, home_runs = 0):
		self.innings = innings
		self.hits = hits
		self.runs = runs
		self.walks = walks
		self.strikeouts = strikeouts
		self.home_runs = home_runs

class Ejected:
	def __init__(self, player, inning, des):
		self.player = player
		self.inning = inning,
		self.des = des

class MLB:
	def __init__(self):
		self.nav = ''
		self.playerID = 0
		self.home = ''
		self.away = ''
		self.gameID = 0

		user_name = input('Enter SQL User: ')
		pwd = getpass()
		host_name = 'marmoset04.shoshin.uwaterloo.ca'
		db = 'project_36'

		self.cnx = mysql.connector.connect(user=user_name, password=pwd, host=host_name, database=db)
		self.cursor = self.cnx.cursor()

		self.years = ['2015', '2016', '2017', '2018']
		self.team_names = {}
		self.team_abbrev = {}
		self.team_cities = {}

	def inning_add_out(self, num, times):
		r = num
		for x in range(times):
			r += 1.0
			r = round(r,1)
			if int((r * 10) % 10) == 3:
				r += 0.7
				r = round(r,1)
		return r

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
		length = self.cursor.rowcount
		splt = math.ceil(length/6)
		for i in range(splt):
			num_a = i + splt
			num_b = i + (2 * splt)
			num_c = i + (3 * splt)
			num_d = i + (4 * splt)
			num_e = i + (5 * splt)
			num_f = i + (6 * splt)

			first = results[i][0]
			second = results[num_a][0] if num_a < length else ''
			third = results[num_b][0] if num_b < length else ''
			fourth = results[num_c][0] if num_c < length else ''
			fifth = results[num_d][0] if num_d < length else ''
			sixth = results[num_e][0] if num_e < length else ''
			seventh = results[num_f][0] if num_f < length else ''

			print('{:<20}{:<20}{:<20}{:<20}{:<20}{:<20}{:<}'.format(first,second,third, fourth, fifth, sixth, seventh))

	def print_players(self, pitchers=True):
		if pitchers:
			query = "select concat(lastName, ', ', firstName) from PlayerNames where id in (select distinct pitcherID from AtBats);"
		else:
			query = "select concat(lastName, ', ', firstName) from PlayerNames where id in (select distinct batterID from AtBats);"
		# run the query
		# print the results
		self.cursor.execute(query)
		results = self.cursor.fetchall()
		length = self.cursor.rowcount
		splt = math.ceil(length/5)
		for i in range(splt + 1):
			num_a = i + splt
			num_b = i + (2 * splt)
			num_c = i + (3 * splt)
			num_d = i + (4 * splt)

			first = results[i][0]
			second = results[num_a][0] if num_a < length else ''
			third = results[num_b][0] if num_b < length else ''
			fourth = results[num_c][0] if num_c < length else ''
			fifth = results[num_d][0] if num_d < length else ''

			print('{:<20}{:<20}{:<20}{:<20}{:<}'.format(first,second,third, fourth, fifth))

	def home_page(self):
		print('\nWelcome to the MLB Stats Database for the 2015-2018 Regular Seasons')
		print('Input \"back\" to go to previous page, or \"home\" to go back to this page at any point, or \"exit\" to close the application')
		print('Do you want to: ')
		print('\t1. View Stats')
		print('\t2. Modify Stats')
		self.nav = input('Enter where you want to go: ')
		if self.nav == '1':
			self.view_page()
		elif self.nav == '2':
			self.modify_page()
		elif self.nav == 'home':
			self.home_page()
		elif self.nav == 'back':
			self.home_page()
		elif self.nav == 'exit':
			self.cleanup()
		else:
			print('Invalid Input')
			self.home_page()

	def view_page(self):
		print('\nDo you want to view:')
		print('\t1. Game Data')
		print('\t2. Team Data')
		print('\t3. Player Data')
		self.nav = input('Enter where you want to go: ')
		if self.nav == '1':
			self.game_info()
		elif self.nav == '2':
			self.team_info()
		elif self.nav == '3':
			self.player_page()
		elif self.nav == 'home':
			self.home_page()
		elif self.nav == 'back':
			self.home_page()
		elif self.nav == 'exit':
			self.cleanup()
		else:
			print('Invalid Input')
			self.view_page()

	def modify_page(self):
		print('\nDo you want to modify it by:')
		print('\t1. Updating Data')
		print('\t2. Inserting Data')
		print('\t3. Deleting Data')
		self.nav = input('Enter where you want to go: ')
		if self.nav == '1':
			self.update_page()
		elif self.nav == '2':
			self.insert_page()
		elif self.nav == '3':
			self.delete_page()
		elif self.nav == 'home':
			self.home_page()
		elif self.nav == 'back':
			self.home_page()
		elif self.nav == 'exit':
			self.cleanup()
		else:
			print('Invalid Input')
			self.modify_page()

	def insert_page(self):
		print('\nDo you want to insert new data to:')
		print('\t1. Teams Data')
		print('\t2. Players Data')
		print('\t3. Ejections Data')
		print('\t4. Games Data')
		self.nav = input('Enter where you want to go: ')
		if self.nav == '1':
			self.insert_team_page()
		elif self.nav == '2':
			self.insert_player_page()
		elif self.nav == '3':
			self.insert_ejection_page()
		elif self.nav == '4':
			self.insert_game_page()
		elif self.nav == 'home':
			self.home_page()
		elif self.nav == 'back':
			self.modify_page()
		elif self.nav == 'exit':
			self.cleanup()
		else:
			print('Invalid Input')
			self.insert_page()

	def insert_team_page(self):
		print('\nInsert New Team')
		print('Type \"show teams\" to display all active teams')
		print('Input format: \"<Abbreviation>, <City>, <Short Name>\". Example: TOR, Toronto, Blue Jays')
		self.nav = input('Enter the team\'s info: ')
		if self.nav == 'back':
			self.insert_page()
		elif self.nav == 'home':
			self.home_page()
		elif self.nav == 'exit':
			self.cleanup()
		elif self.nav == 'show teams':
			self.print_teams(False)
			self.insert_team_page()
		else:
			# we have some input
			user_input = self.nav.split(", ")
			if len(user_input) != 3:
				print('Invalid Input')
				self.insert_team_page()
			else:
				# check if abbreviation or short name already exists
				if user_input[0] in self.team_abbrev or user_input[2] in self.team_names:
					print('Abbreviation and Team Name must be unique.')
					self.insert_team_page()
				else:
					team_name = ""
					index = 0
					for x in user_input:
						if index != 0:
							team_name += ", "
						team_name = team_name + "\"" + x + "\""
						index += 1
					query = "insert into TeamNames values (" + team_name + ");"
					try:
						self.cursor.execute(query)
						self.cnx.commit()
						print("Success!")
					except Error as e:
						# print(f"The error '{e}' occurred")
						print('Invalid Input')
			self.insert_team_page()

	def insert_player_page(self):
		print('\nInsert New Player')
		print('Type \"show players\" to display all players')
		print('Input format: \"<ID>, <First Name>, <Last Name>\". Example: 123456, Paul, Ward')
		self.nav = input('Enter the player\'s info: ')
		if self.nav == 'back':
			self.insert_page()
		elif self.nav == 'home':
			self.home_page()
		elif self.nav == 'exit':
			self.cleanup()
		elif self.nav == 'show players':
			query = "select concat(lastName, ', ', firstName) from PlayerNames;"
			# run the query
			# print the results
			self.cursor.execute(query)
			results = self.cursor.fetchall()
			length = self.cursor.rowcount
			splt = math.ceil(length/5)
			for i in range(splt + 1):
				num_a = i + splt
				num_b = i + (2 * splt)
				num_c = i + (3 * splt)
				num_d = i + (4 * splt)

				first = results[i][0]
				second = results[num_a][0] if num_a < length else ''
				third = results[num_b][0] if num_b < length else ''
				fourth = results[num_c][0] if num_c < length else ''
				fifth = results[num_d][0] if num_d < length else ''

				print('{:<20}{:<20}{:<20}{:<20}{:<}'.format(first,second,third, fourth, fifth))
			self.insert_player_page()
		else:
			# we have some input
			user_input = self.nav.split(", ")
			if (len(user_input) != 3):
				print('Invalid Input')
				self.insert_player_page()
			player_name = ""
			index = 0
			for x in user_input:
				if (index != 0):
					player_name += ", "
				player_name = player_name + "\"" + x + "\""
				index += 1
			query = "insert into PlayerNames values (" + player_name + ");"
			try:
				self.cursor.execute(query)
				self.cnx.commit()
				print("Success!")
			except Error as e:
				# print(f"The error '{e}' occurred")
				print('Invalid Input')
			self.insert_player_page()

	def insert_ejection_page(self):
		print('\nInsert Ejection')
		print('Input format: \"<At Bat ID>, <Player ID>, <Team>, <Description>, <Arguing B/S>, <Correct Ejection>\". Must be valid IDs and Team. Last two are T/F value')
		print('Example: 2015000001, 000001, TOR, Toronto first baseman Paul Ward ejected by HP Harder W, FALSE, TRUE')
		self.nav = input('Enter the ejection\'s info: ')
		if self.nav == 'back':
			self.insert_page()
		elif self.nav == 'home':
			self.home_page()
		elif self.nav == 'exit':
			self.cleanup()
		else:
			# we have some input
			user_input = self.nav.split(", ")
			if (len(user_input) != 6):
				print('Invalid Input')
				self.insert_ejection_page()
			if (user_input[4].upper() != "TRUE" and user_input[4].upper() != "FALSE"):
				print('Invalid Input')
				self.insert_ejection_page()
			if (user_input[5].upper() != "TRUE" and user_input[5].upper() != "FALSE" and user_input[5].upper() != "NULL"):
				print('Invalid Input')
				self.insert_ejection_page()
			ejection = ""
			index = 0
			for x in user_input:
				if (index != 0):
					ejection += ", "
				if (index == 0 or index == 1):
					ejection = ejection + x
				else:
					ejection = ejection + "\"" + x + "\""
				index += 1
			query = "insert into Ejections values (" + ejection + ");"
			try:
				self.cursor.execute(query)
				self.cnx.commit()
				print("Success!")
			except Error as e:
				# print(f"The error '{e}' occurred")
				print('Invalid Input')
			self.insert_ejection_page()

	def insert_game_page(self):
		print('\nInsert Game')
		print('Input format: \"<Game ID>, <Home Team>, <Home Score>, <Away Team>, <Away Score>, <Date>, <Venue>, <Attendance>, <Start Time>, <Delay>, <Elapsed Time>, <Weather Degrees>, <Wind Speed in MPH>, <Wind Direction>, <Winning Team>\". Must be valid ID and Teams')
		print('Example: 201500000, TOR, 0, ANA, 3, 2015-01-01, Roger Centre, 0, 19:00:00, 0, 180, 45, 0, None, ANA')
		self.nav = input('Enter the game\'s info: ')
		if self.nav == 'back':
			self.insert_page()
		elif self.nav == 'home':
			self.home_page()
		elif self.nav == 'exit':
			self.cleanup()
		else:
			# we have some input
			user_input = self.nav.split(", ")
			if (len(user_input) != 15):
				print('Invalid Input')
				self.insert_game_page()
			flag1 = False
			flag2 = False
			flag3 = False
			for team, abbrev in self.team_abbrev.items():
				if (user_input[1] == abbrev):
					flag1 = True
				if (user_input[3] == abbrev):
					flag2 = True
				if (user_input[14] == abbrev):
					flag3 = True
			if (not(flag1 and flag2 and flag3)):
				print('Not a valid team name!')
				self.insert_game_page()
			if (user_input[14] != user_input[1] and user_input[14] != user_input[3]):
				print('Not a valid team name!')
				self.insert_game_page()
			game = ""
			index = 0
			for x in user_input:
				if (index != 0):
					game += ", "
				if (index in [0, 2, 4, 7, 9, 10, 11, 12]):
					game = game + x
				else:
					game = game + "\"" + x + "\""
				index += 1
			query = "insert into Games values (" + game + ");"
			try:
				self.cursor.execute(query)
				self.cnx.commit()
				print("Success!")
			except Error as e:
				# print(f"The error '{e}' occurred")
				print('Invalid Input')
			self.insert_game_page()

	def update_page(self):
		print('\nDo you want to update:')
		print('\t1. Teams Data')
		print('\t2. Players Data')
		print('\t3. Ejections Data')
		print('\t4. Games Data')
		self.nav = input('Enter where you want to go: ')
		if self.nav == '1':
			self.update_team_page()
		elif self.nav == '2':
			self.update_player_page()
		elif self.nav == '3':
			self.update_ejection_page()
		elif self.nav == '4':
			self.update_game_page()
		elif self.nav == 'home':
			self.home_page()
		elif self.nav == 'back':
			self.modify_page()
		elif self.nav == 'exit':
			self.cleanup()
		else:
			print('Invalid Input')
			self.update_page()

	def update_team_page(self):
		print('\nUpdate Team')
		print('Type \"show teams\" to display all active teams')
		print('Input format: \"<Abbreviation>, <City>, <Short Name>\". Must be a valid Abbreviation. Example: TOR, Toronto, Blue Jays')
		self.nav = input('Enter the team\'s info: ')
		if self.nav == 'back':
			self.update_page()
		elif self.nav == 'home':
			self.home_page()
		elif self.nav == 'exit':
			self.cleanup()
		elif self.nav == 'show teams':
			self.print_teams(False)
			self.update_team_page()
		else:
			# we have some input
			user_input = self.nav.split(", ")
			if (len(user_input) != 3):
				print('Invalid Input')
				self.update_team_page()
			flag = False
			for team, abbrev in self.team_abbrev.items():
				if (user_input[0] == abbrev):
					flag = True
			if (not flag):
				print('Not a valid team name!')
				self.update_team_page()
			query = "update TeamNames set city=\"" + user_input[1] + "\", shortName=\"" + user_input[2] + "\" where abbreviation=\"" + user_input[0] + "\";"
			try:
				self.cursor.execute(query)
				self.cnx.commit()
				print("Success!")
			except Error as e:
				# print(f"The error '{e}' occurred")
				print('Invalid Input')
			self.update_team_page()

	def update_player_page(self):
		print('\nUpdate Player')
		print('Type \"show players\" to display all players')
		print('Input format: \"<ID>, <First Name>, <Last Name>\". Must be a valid ID. Example: 123456, Paul, Ward')
		self.nav = input('Enter the player\'s info: ')
		if self.nav == 'back':
			self.update_page()
		elif self.nav == 'home':
			self.home_page()
		elif self.nav == 'exit':
			self.cleanup()
		elif self.nav == 'show players':
			query = "select concat(lastName, ', ', firstName) from PlayerNames;"
			# run the query
			# print the results
			self.cursor.execute(query)
			results = self.cursor.fetchall()
			for x in results:
				print(x[0])
			self.insert_player_page()
		else:
			# we have some input
			user_input = self.nav.split(", ")
			if (len(user_input) != 3):
				print('Invalid Input')
				self.update_player_page()
			query = "update PlayerNames set firstName=\"" + user_input[1] + "\", lastName=\"" + user_input[2] + "\" where id=\"" + user_input[0] + "\";"
			try:
				self.cursor.execute(query)
				self.cnx.commit()
				print("Success!")
			except Error as e:
				# print(f"The error '{e}' occurred")
				print('Invalid Input')
			self.update_player_page()

	def update_ejection_page(self):
		print('\nUpdate Ejection')
		print('Input format: \"<At Bat ID>, <Player ID>, <Team>, <Description>, <Arguing B/S>, <Correct Ejection>\". Must be valid IDs and Team. Last two are T/F value')
		print('Example: 2015000001, 000001, TOR, Toronto first baseman Paul Ward ejected by HP Harder W, FALSE, TRUE')
		self.nav = input('Enter the ejection\'s info: ')
		if self.nav == 'back':
			self.update_page()
		elif self.nav == 'home':
			self.home_page()
		elif self.nav == 'exit':
			self.cleanup()
		else:
			# we have some input
			user_input = self.nav.split(", ")
			if (len(user_input) != 6):
				print('Invalid Input')
				self.update_ejection_page()
			if (user_input[4].upper() != "TRUE" and user_input[4].upper() != "FALSE"):
				print('Invalid Input')
				self.update_ejection_page()
			if (user_input[5].upper() != "TRUE" and user_input[5].upper() != "FALSE" and user_input[5].upper() != "NULL"):
				print('Invalid Input')
				self.update_ejection_page()
			query = "update Ejections set abID=" + user_input[0] + ", playerID=" + user_input[1] + ", team=\"" + user_input[2] + "\", description=\"" + user_input[3] + "\", argueBallsStrikes=\"" + user_input[4].upper() + "\", correctEjection=\"" + user_input[5].upper() + "\" where abID=\"" + user_input[0] + "\" and playerID=\"" + user_input[1] + "\";"
			try:
				self.cursor.execute(query)
				self.cnx.commit()
				print("Success!")
			except Error as e:
				# print(f"The error '{e}' occurred")
				print('Invalid Input')
			self.update_ejection_page()

	def update_game_page(self):
		print('\nUpdate Game')
		print('Input format: \"<Game ID>, <Home Team>, <Home Score>, <Away Team>, <Away Score>, <Date>, <Venue>, <Attendance>, <Start Time>, <Delay>, <Elapsed Time>, <Weather Degrees>, <Wind Speed in MPH>, <Wind Direction>, <Winning Team>\". Must be valid ID and Teams')
		print('Example: 201500000, TOR, 0, ANA, 3, 2015-01-01, Roger Centre, 0, 19:00:00, 0, 180, 45, 0, None, TOR')
		self.nav = input('Enter the game\'s info: ')
		if self.nav == 'back':
			self.update_page()
		elif self.nav == 'home':
			self.home_page()
		elif self.nav == 'exit':
			self.cleanup()
		else:
			# we have some input
			user_input = self.nav.split(", ")
			if (len(user_input) != 15):
				print('Invalid Input')
				self.update_game_page()
			flag1 = False
			flag2 = False
			flag3 = False
			for team, abbrev in self.team_abbrev.items():
				if (user_input[1] == abbrev):
					flag1 = True
				if (user_input[3] == abbrev):
					flag2 = True
				if (user_input[14] == abbrev):
					flag3 = True
			if (not(flag1 and flag2 and flag3)):
				print('Not a valid team name!')
				self.update_game_page()
			if (user_input[14] != user_input[1] and user_input[14] != user_input[3]):
				print('Not a valid team name!')
				self.update_game_page()
			query = "update Games set homeTeam=\"" + user_input[1] + "\", homeFinalScore=" + user_input[2] + ", awayTeam=\"" + user_input[3] + "\", awayFinalScore=" + user_input[4] + ", gameDate=\"" + user_input[5] + "\", venueName=\"" + user_input[6] + "\", attendance=" + user_input[7]  + ", startTime=\"" + user_input[8] + "\", delay=" + user_input[9] + ", elapsedTime=" + user_input[10] + ", weatherDegrees=" + user_input[11] + ", elapsedTime=" + user_input[12] + ", windDirection=\"" + user_input[13] + "\", winningTeam=\"" + user_input[14] + "\" where gID =" + user_input[0] + ";"
			try:
				self.cursor.execute(query)
				self.cnx.commit()
				print("Success!")
			except Error as e:
				# print(f"The error '{e}' occurred")
				print('Invalid Input')
			self.update_game_page()

	def delete_page(self):
		print('\nDo you want to delete:')
		print('\t1. Teams Data')
		print('\t2. Players Data')
		print('\t3. Ejections Data')
		print('\t4. Games Data')
		self.nav = input('Enter where you want to go: ')
		if self.nav == '1':
			self.delete_team_page()
		elif self.nav == '2':
			self.delete_player_page()
		elif self.nav == '3':
			self.delete_ejection_page()
		elif self.nav == '4':
			self.delete_game_page()
		elif self.nav == 'home':
			self.home_page()
		elif self.nav == 'back':
			self.modify_page()
		elif self.nav == 'exit':
			self.cleanup()
		else:
			print('Invalid Input')
			self.delete_page()

	def delete_team_page(self):
		print('\nDelete Team')
		print('Type \"show teams\" to display all active teams')
		print('Input format: \"<Abbreviation>\". Must be a valid abbreviation')
		print('Example: TOR')
		self.nav = input('Enter the team\'s info: ')
		if self.nav == 'back':
			self.delete_page()
		elif self.nav == 'show teams':
			self.print_teams(False)
			self.delete_team_page()
		elif self.nav == 'home':
			self.home_page()
		elif self.nav == 'exit':
			self.cleanup()
		else:
			# we have some input
			query = "delete from TeamNames where abbreviation=\"" + self.nav + "\";"
			print('Are you sure you want to delete this data?')
			print('\t1. Yes')
			print('\t2. No')
			self.nav = input("Your decision: ")
			if self.nav != '1':
				self.delete_team_page()
			try:
				self.cursor.execute(query)
				self.cnx.commit()
				print("Success!")
			except Error as e:
				# print(f"The error '{e}' occurred")
				print('Invalid Input')
			self.delete_team_page()

	def delete_player_page(self):
		print('\nDelete Player')
		print('Input format: \"<Player ID>\". Must be a valid ID')
		print('Example: 000001')
		self.nav = input('Enter the player\'s info: ')
		if self.nav == 'back':
			self.delete_page()
		elif self.nav == 'home':
			self.home_page()
		elif self.nav == 'exit':
			self.cleanup()
		else:
			# we have some input
			query = "delete from PlayerNames where id=" + self.nav + ";"
			print('Are you sure you want to delete this data?')
			print('\t1. Yes')
			print('\t2. No')
			self.nav = input("Your decision: ")
			if self.nav != '1':
				self.delete_player_page()
			try:
				self.cursor.execute(query)
				self.cnx.commit()
				print("Success!")
			except Error as e:
				# print(f"The error '{e}' occurred")
				print('Invalid Input')
			self.delete_player_page()

	def delete_ejection_page(self):
		print('\nDelete Ejection')
		print('Input format: \"<At Bat ID>, <Player ID>\". Must be a valid IDs')
		print('Example: 2015000000, 000001')
		self.nav = input('Enter the ejection\'s info: ')
		if self.nav == 'back':
			self.delete_page()
		elif self.nav == 'home':
			self.home_page()
		elif self.nav == 'exit':
			self.cleanup()
		else:
			# we have some input
			user_input = self.nav.split(", ")
			if (len(user_input) != 2):
				print('Invalid Input')
				self.delete_ejection_page()
			query = "delete from Ejections where abID=" + user_input[0] + " and playerID=" + user_input[1] + ";"
			print('Are you sure you want to delete this data?')
			print('\t1. Yes')
			print('\t2. No')
			self.nav = input("Your decision: ")
			if self.nav != '1':
				self.delete_ejection_page()
			try:
				self.cursor.execute(query)
				self.cnx.commit()
				print("Success!")
			except Error as e:
				# print(f"The error '{e}' occurred")
				print('Invalid Input')
			self.delete_ejection_page()

	def delete_game_page(self):
		print('\nDelete Game')
		print('Input format: \"<Game ID>\". Must be a valid ID')
		print('Example: 201500001')
		self.nav = input('Enter the game\'s info: ')
		if self.nav == 'back':
			self.delete_page()
		elif self.nav == 'home':
			self.home_page()
		elif self.nav == 'exit':
			self.cleanup()
		else:
			# we have some input
			query = "delete from Games where gID=" + self.nav + ";"
			print('Are you sure you want to delete this data?')
			print('\t1. Yes')
			print('\t2. No')
			self.nav = input("Your decision: ")
			if self.nav != '1':
				self.delete_game_page()
			try:
				self.cursor.execute(query)
				self.cnx.commit()
				print("Success!")
			except Error as e:
				# print(f"The error '{e}' occurred")
				print('Invalid Input')
			self.delete_game_page()

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
			self.view_page()
		elif self.nav == 'exit':
			self.cleanup()
		else:
			print('Invalid Input')
			self.player_page()

	def game_info(self):
		print('\nGame Data: Single Game')
		print('Type \"year team\" to filter games by year for a team')
		print('Input format: \"<home_team>, <away_team>, <yyyy-mm-dd>\". (Example: Cubs, Cardinals, 2015-04-05)')
		self.nav = input('Enter the home team, away team, and the date of the game you are looking for : ')
		if self.nav == 'back':
			self.view_page()
		elif self.nav == 'home':
			self.home_page()
		elif self.nav == 'exit':
			self.cleanup()
		elif self.nav == 'year team':
			# run query to get all team names
			# print teams
			self.print_teams(False)
			self.nav = input('Enter the number of the games you want to see from the desired team for a given year (Ex: 2015, Blue Jays): ')
			# run query to get all games from that team
			# split the result 
			inputs = self.nav.split(', ')
			if len(inputs) != 2:
				print('Not a valid team name!')
				self.game_info()
			elif inputs[1] not in self.team_abbrev or inputs[0] not in self.years:
				print('Not a valid team name!')
				self.game_info()
			else:
				query = "select concat(a.shortName,', ', b.shortName, ', ', c.gameDate) from Games c left join TeamNames a on c.homeTeam = a.abbreviation left join TeamNames b on c.awayTeam = b.abbreviation where year(gameDate) = " + inputs[0] + " and (homeTeam = '" + self.team_abbrev[inputs[1]] + "' or awayTeam = '" + self.team_abbrev[inputs[1]] + "');"
				self.cursor.execute(query)
				results = self.cursor.fetchall()
				length = self.cursor.rowcount
				splt = math.ceil(length/4)
				t = PrettyTable()
				t.field_names = ['', '  ', '   ']
				t.align = 'l'
				for i in range(splt + 1):
					num_a = i + splt
					num_b = i + (2 * splt)

					first = results[i][0]
					second = results[num_a][0] if num_a < length else ''
					third = results[num_b][0] if num_b < length else ''

					t.add_row([first, second, third])
				print(t)
				self.game_info()
		else:
			self.print_game_info()
			self.game_info()

	def team_info(self):
		print('\nTeam Data')
		print('Type \"show teams\" to display all active teams')
		print('Input format: \"<team_name>\". Do not include the city. (Example: Blue Jays)')
		self.nav = input('Enter the team\'s name of the team you are looking for: ')
		if self.nav == 'back':
			self.view_page()
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
			self.print_team_ejection_info()
			self.team_info()

	def print_game_info(self):
		# run query to get the game data
		inputs = self.nav.split(', ')
		# make sure the inputs are valid
		if len(inputs) != 3:
			print('invalid Input Format')
		elif inputs[0] in self.team_abbrev and inputs[1] in self.team_abbrev:
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
				print('')
				print(t.get_string(title=table_title))
				self.print_game_ejection_info()
				self.print_game_details()
		else:
			print('Invalid Input Format')

	def print_game_details(self):
		print('\n1. (Home)', self.team_names[self.home])
		print('2. (Away)', self.team_names[self.away])
		self.nav = input('Enter the number of the team you want to view the Batter and Pitcher Stats for:')
		if self.nav == '1' or self.nav == '2':
			query = "select distinct abID, inning, topInning, concat(b.firstName,' ', b.lastName) as batter, pt.bScore, concat(p.firstName, ' ', p.lastName) as pitcher, a.event, pt.outs, concat(ep.firstName, ' ', ep.lastName) as ejectedPlayer, e.description from AtBats a left join PlayerNames b on a.batterID = b.id left join PlayerNames p on a.pitcherID = p.id left join Pitches pt using (abID) left join Ejections e using (abID) left join PlayerNames ep on e.playerID = ep.id where gID = " + str(self.gameID) + ";"
			self.cursor.execute(query)
			results = self.cursor.fetchall()

			# batters and pitchers set where the key will be the player name and the value will be the the Batter or Pitcher class
			batters = {}
			pitchers = {}

			tb = PrettyTable()
			tb.field_names = ['Batting', 'AB', 'H', 'BB', 'RBI', 'SO', 'BA', 'OBP', 'SLG', 'OPS']
			tb.align = 'l'

			tp = PrettyTable()
			tp.field_names = ['Pitching', 'IP', 'H', 'ER', 'BB', 'SO', 'HR', 'ERA' ]
			tp.align = 'l'

			te = PrettyTable()
			te.field_names = ['Ejected Player', 'Inning Ejected', 'Description']
			te.align = 'l'

			if self.nav == '1':
				# show home Stats
				# get the batting stats
				# home will bat at the bottom of the inning, so topInning = 'FALSE'
				curr_score = 0
				prev_batter = ''
				ejected_players = []
				prev_id = 0
				seen = set()

				for x in results:
					if x[2] == 'TRUE':
						continue
					# batting stats include Player, At Bats, Runs, Hits, Walks, RBI

					# first check if someone was ejected
					if x[8] is not None:
						# someone was ejected
						# make sure the person ejected was on our team
						if x[9].split(' ')[0] == self.team_cities[self.away] and x[9].split(' ')[1] == self.team_names[self.away]:
							if x[8] not in seen:
								seen.add(x[8])
								ejected_p = Ejected(x[8], x[1], x[9])
								ejected_players.append(ejected_p)

					# check if prev batter is the same (possible for double ejections on same play)
					if prev_id == x[0]:
						continue

					if x[3] not in batters:
						# add the player to the set
						batters[x[3]] = Batter()

					if curr_score != x[4]:
						# at least 1 run has been made in the previous play
						# increase the previous player's rbi by the score difference
						batters[prev_batter].rbi += x[4] - curr_score
						curr_score = x[4]

					if x[6] in not_at_bat:
						if x[6] == 'Walk' or x[6] == 'Intent Walk':
							batters[x[3]].walks += 1
						else:
							batters[x[3]].sacs += 1
					else:
						batters[x[3]].at_bats += 1
						if x[6] == 'Strikeout':
							batters[x[3]].strikeouts += 1
						elif x[6] in hit_legend:
							batters[x[3]].hits += 1
							if x[6] == 'Single':
								batters[x[3]].singles += 1
							elif x[6] == 'Double':
								batters[x[3]].doubles += 1
							elif x[7] == 'Triple':
								batters[x[3]].triples += 1
							else:
								batters[x[3]].home_runs += 1

					prev_batter = x[3]
					prev_id = x[0]

				# add the rows using the batters dictionary
				# add the rows using the batters dictionary
				ab_total = 0
				h_total = 0
				bb_total = 0
				rbi_total = 0
				so_total = 0
				ba_avg = 0.0
				obp_avg = 0.0
				slg_avg = 0.0
				ops_avg = 0.0
				count = 0.0
				for key in batters:
					# tb.field_names = ['Batting', 'AB', 'H', 'BB', 'RBI', 'SO', 'BA', 'OBP', 'SLG', 'OPS']
					ba = 0.000
					obp = 0.000
					slg = 0.000
					ops = 0.000
					if batters[key].at_bats > 0:
						ba = round(float(batters[key].hits/batters[key].at_bats),3)
						obp = round((batters[key].hits + batters[key].walks)/(batters[key].at_bats + batters[key].walks + batters[key].sacs), 3)
						slg = round((batters[key].singles + 2 * batters[key].doubles + 3 * batters[key].triples + 4 * batters[key].home_runs)/batters[key].at_bats,3)
						ops = obp + slg
						ba_avg += ba
						obp_avg += obp
						slg_avg += slg
						ops_avg += ops

					ab_total += batters[key].at_bats
					h_total += batters[key].hits
					bb_total += batters[key].walks
					rbi_total += batters[key].rbi
					so_total += batters[key].strikeouts

					tb.add_row([key, batters[key].at_bats, batters[key].hits, batters[key].walks, batters[key].rbi, batters[key].strikeouts, '{:.3f}'.format(ba), '{:.3f}'.format(obp), '{:.3f}'.format(slg), '{:.3f}'.format(ops)])
					count += 1.0

				# add the footer team total row
				tb.add_row(['---------------','---','---','---','---','---','-----','-----','-----','-----'])
				ba_avg = round(ba_avg/count,3)
				obp_avg = round(obp_avg/count,3)
				slg_avg = round(slg_avg/count,3)
				ops_avg = round(ops_avg/count,3)
				tb.add_row(['Team Totals', ab_total, h_total, bb_total, rbi_total, so_total, '{:.3f}'.format(ba_avg), '{:.3f}'.format(obp_avg), '{:.3f}'.format(slg_avg), '{:.3f}'.format(ops_avg)])

				# print the table
				batting_title = self.team_cities[self.home] + ' ' +  self.team_names[self.home] + ' Batting Game Stats'
				print('')
				print(tb.get_string(title=batting_title))

				# pitching stats
				# home team will be pitching at the top of the inning, so topInning = 'TRUE'
				curr_inning = 0
				inning_pitcher = ''
				full_pitch = True
				inning_outs = 0
				prev_batter = ''
				prev_id = 0
				prev_bscore = 0
				earned_runs = 0

				for x in results:
					# pitching stats include Pitcher, Innings, Hits, Walks, Strikeouts
					if x[2] == 'FALSE':
						continue

					# first check if someone was ejected
					if x[8] is not None:
						# someone was ejected
						# make sure the person ejected was on our team
						if x[9].split(' ')[0] == self.team_cities[self.away] and x[9].split(' ')[1] == self.team_names[self.away]:
							if x[8] not in seen:
								seen.add(x[8])
								ejected_p = Ejected(x[8], x[1], x[9])
								ejected_players.append(ejected_p)

					if prev_id == x[0]:
						continue

					# innings are in terms of outs
					# 3 outs made = 1 inning pitched
					# 1 out = 1/3 or 0.1, 2 outs = 2/3 or 0.2
					if x[5] not in pitchers:
						pitchers[x[5]] = Pitcher()

					if curr_inning == 0:
						curr_inning = x[1]
						inning_pitcher = x[5]

					if curr_inning != x[1]:
						if full_pitch == False:
							o = 3 - inning_outs
							# innings pitched is weird in MLB
							# 1 out = 0.1, 2 outs = 0.2, 3 outs = 1.0 (full inning pitched)
							while o > 0:
								num = int((pitchers[inning_pitcher].innings * 10) % 10)
								if num == 2:
									# the current pitched 2 outs, so the next out will make him pitch 1 full inning
									pitchers[inning_pitcher].innings += 0.8
								else:
									pitchers[inning_pitcher].innings += 0.1
								o -= 1
						else:
							pitchers[inning_pitcher].innings += 1.0
						curr_inning = x[1]
						inning_pitcher = x[5]
						full_pitch = True
						inning_outs = 0

					if inning_pitcher != x[5]:
						# pitcher changed during the inning

						# first tally how many runs the pitcher allowed
						pitchers[inning_pitcher].runs += x[4] - earned_runs
						earned_runs = x[4]

						full_pitch = False
						o = x[7] - inning_outs
						# innings pitched is weird in MLB
						# 1 out = 0.1, 2 outs = 0.2, 3 outs = 1.0 (full inning pitched)
						while o > 0:
							num = int((pitchers[inning_pitcher].innings * 10) % 10)
							if num == 2:
								# the current pitched 2 outs, so the next out will make him pitch 1 full inning
								pitchers[inning_pitcher].innings += 0.8
							else:
								pitchers[inning_pitcher].innings += 0.1
							o -= 1
						inning_outs = x[7]
						inning_pitcher = x[5]

					if x[6] in hit_legend:
						pitchers[x[5]].hits += 1
						if x[6] == 'Home Run':
							pitchers[x[5]].home_runs += 1
					else:
						if x[6] == 'Walk' or x[6] == 'Intent Walk':
							pitchers[x[5]].walks += 1
						elif 'Strikeout' in x[6] :
							pitchers[x[5]].strikeouts += 1
					prev_batter = x[3]
					prev_id = x[0]
					prev_bscore = x[4]

				# calculate how many runs the last pitcher allowed
				pitchers[inning_pitcher].runs += prev_bscore - earned_runs
				# calculate innings played for last pitcher
				if full_pitch == False:
					o = 3 - inning_outs
					# innings pitched is weird in MLB
					# 1 out = 0.1, 2 outs = 0.2, 3 outs = 1.0 (full inning pitched)
					while o > 0:
						num = int((pitchers[inning_pitcher].innings * 10) % 10)
						if num == 2:
							# the current pitched 2 outs, so the next out will make him pitch 1 full inning
							pitchers[inning_pitcher].innings += 0.8
						else:
							pitchers[inning_pitcher].innings += 0.1
						o -= 1
				else:
					pitchers[inning_pitcher].innings += 1.0

				i_total = 0
				h_total = 0
				er_total = 0
				bb_total = 0
				so_total = 0
				hr_total = 0
				era_avg = 0
				rem = 0
				for key in pitchers:
					# ['Pitching', 'IP', 'H', 'ER', 'BB', 'SO', 'HR', 'ERA' ]
					era = 0.0
					if pitchers[key].innings > 0.0:
						era = round(9.0 * pitchers[key].runs / pitchers[key].innings,2)
						era_avg += era

					# int((pitchers[inning_pitcher].innings * 10) % 10)
					# have to add the innings the same way as before
					if pitchers[key].innings.is_integer():
						i_total += int(pitchers[key].innings)
					else:
						# have to add the runs individually
						# first add the whole number
						i_total += int(math.floor(pitchers[key].innings))
						r = int((round(pitchers[key].innings - math.floor(pitchers[key].innings),1) * 10) % 10)
						rem += r
						# rem can increase by 1, 2, or 3
						# keep track of the remainder, add it at the end

					h_total += pitchers[key].hits
					er_total += pitchers[key].runs
					bb_total += pitchers[key].walks
					so_total += pitchers[key].strikeouts
					hr_total += pitchers[key].home_runs

					tp.add_row([key, pitchers[key].innings, pitchers[key].hits, pitchers[key].runs, pitchers[key].walks, pitchers[key].strikeouts, pitchers[key].home_runs, '{:.2f}'.format(era)])
					count += 1.0

				i_total += int(rem /3)
				era_avg = round(era_avg / count,2)
				tp.add_row(['---------------','---','---','---','---','---','---', '----'])
				tp.add_row(['Team Totals', i_total, h_total, er_total, bb_total, so_total, hr_total, '{:.2f}'.format(era_avg)])


				for e in ejected_players:
					te.add_row([e.player, e.inning[0], e.des])

				pitching_title = self.team_cities[self.home] + ' ' + self.team_names[self.home] + ' Pitching Game Stats'
				print('')
				print(tp.get_string(title=pitching_title))

				if len(ejected_players) > 0:
					print('')
					print(te.get_string(title='Ejected Players'))

			else:
				# show away stats
				# batting stas
				# away team bats at the top of the inning
				curr_score = 0
				prev_batter = ''
				ejected_players = []
				seen = set()
				prev_id = 0

				for x in results:
					if x[2] == 'FALSE':
						continue
					# batting stats include Player, At Bats, Runs, Hits, Walks, RBI
					# first check if someone was ejected
					if x[8] is not None:
						# someone was ejected
						# make sure the person ejected was on our team
						if x[9].split(' ')[0] == self.team_cities[self.away] and x[9].split(' ')[1] == self.team_names[self.away]:
							if x[8] not in seen:
								seen.add(x[8])
								ejected_p = Ejected(x[8], x[1], x[9])
								ejected_players.append(ejected_p)

					if prev_id == x[0]:
						continue

					if x[3] not in batters:
						# add the player to the set
						batters[x[3]] = Batter()

					if curr_score != x[4]:
						# at least 1 run has been made in the previous play
						# increase the previous player's rbi by the score difference
						batters[prev_batter].rbi += x[4] - curr_score
						curr_score = x[4]

					if x[6] in not_at_bat:
						if x[6] == 'Walk' or x[6] == 'Intent Walk':
							batters[x[3]].walks += 1
						else:
							batters[x[3]].sacs += 1
					else:
						batters[x[3]].at_bats += 1
						if 'Strikeout' in x[6]:
							batters[x[3]].strikeouts += 1
						elif x[6] in hit_legend:
							batters[x[3]].hits += 1
							if x[6] == 'Single':
								batters[x[3]].singles += 1
							elif x[6] == 'Double':
								batters[x[3]].doubles += 1
							elif x[7] == 'Triple':
								batters[x[3]].triples += 1
							else:
								batters[x[3]].home_runs += 1

					prev_batter = x[3]
					prev_id = x[0]

				# add the rows using the batters dictionary
				ab_total = 0
				h_total = 0
				bb_total = 0
				rbi_total = 0
				so_total = 0
				ba_avg = 0.0
				obp_avg = 0.0
				slg_avg = 0.0
				ops_avg = 0.0
				count = 0.0
				for key in batters:
					# tb.field_names = ['Batting', 'AB', 'H', 'BB', 'RBI', 'SO', 'BA', 'OBP', 'SLG', 'OPS']
					ba = 0.000
					obp = 0.000
					slg = 0.000
					ops = 0.000
					if batters[key].at_bats > 0:
						ba = round(float(batters[key].hits/batters[key].at_bats),3)
						obp = round((batters[key].hits + batters[key].walks)/(batters[key].at_bats + batters[key].walks + batters[key].sacs), 3)
						slg = round((batters[key].singles + 2 * batters[key].doubles + 3 * batters[key].triples + 4 * batters[key].home_runs)/batters[key].at_bats,3)
						ops = obp + slg
						ba_avg += ba
						obp_avg += obp
						slg_avg += slg
						ops_avg += ops

					ab_total += batters[key].at_bats
					h_total += batters[key].hits
					bb_total += batters[key].walks
					rbi_total += batters[key].rbi
					so_total += batters[key].strikeouts

					tb.add_row([key, batters[key].at_bats, batters[key].hits, batters[key].walks, batters[key].rbi, batters[key].strikeouts, '{:.3f}'.format(ba), '{:.3f}'.format(obp), '{:.3f}'.format(slg), '{:.3f}'.format(ops)])
					count += 1.0

				# add the footer team total row
				tb.add_row(['---------------','---','---','---','---','---','-----','-----','-----','-----'])
				ba_avg = round(ba_avg/count,3)
				obp_avg = round(obp_avg/count,3)
				slg_avg = round(slg_avg/count,3)
				ops_avg = round(ops_avg/count,3)
				tb.add_row(['Team Totals', ab_total, h_total, bb_total, rbi_total, so_total, '{:.3f}'.format(ba_avg), '{:.3f}'.format(obp_avg), '{:.3f}'.format(slg_avg), '{:.3f}'.format(ops_avg)])

				# print the table
				batting_title = self.team_cities[self.away] + ' ' +  self.team_names[self.away] + ' Batting Game Stats'
				print('')
				print(tb.get_string(title=batting_title))

				# pitching stats
				# away team will be pitching at the bottom of the inning, so topInning = 'FALSE'
				inning_pitcher = ''
				curr_inning = 0
				full_pitch = True
				inning_outs = 0
				prev_batter = ''
				prev_id = 0
				prev_bscore = 0
				earned_runs = 0

				for x in results:
					if x[2] == 'TRUE':
						continue

					# first check if someone was ejected
					if x[8] is not None:
						# someone was ejected
						# make sure the person ejected was on our team
						if x[9].split(' ')[0] == self.team_cities[self.away] and x[9].split(' ')[1] == self.team_names[self.away]:
							if x[8] not in seen:
								seen.add(x[8])
								ejected_p = Ejected(x[8], x[1], x[9])
								ejected_players.append(ejected_p)

					if prev_id == x[0]:
						continue

					# innings are in terms of outs
					# 3 outs made = 1 inning pitched
					# 1 out = 1/3 or 0.1, 2 outs = 2/3 or 0.2
					if x[5] not in pitchers:
						pitchers[x[5]] = Pitcher()

					if curr_inning == 0:
						curr_inning = x[1]
						inning_pitcher = x[5]

					if curr_inning != x[1]:
						if full_pitch == False:
							o = 3 - inning_outs
							# innings pitched is weird in MLB
							# 1 out = 0.1, 2 outs = 0.2, 3 outs = 1.0 (full inning pitched)
							while o > 0:
								num = int((pitchers[inning_pitcher].innings * 10) % 10)
								if num == 2:
									# the current pitched 2 outs, so the next out will make him pitch 1 full inning
									pitchers[inning_pitcher].innings += 0.8
								else:
									pitchers[inning_pitcher].innings += 0.1
								o -= 1
						else:
							pitchers[inning_pitcher].innings += 1.0
						curr_inning = x[1]
						inning_pitcher = x[5]
						full_pitch = True
						inning_outs = 0

					if inning_pitcher != x[5]:
						# first tally how many runs the pitcher allowed
						pitchers[inning_pitcher].runs += x[4] - earned_runs
						earned_runs = x[4]

						# pitcher changed during the inning
						full_pitch = False
						o = x[7] - inning_outs
						# innings pitched is weird in MLB
						# 1 out = 0.1, 2 outs = 0.2, 3 outs = 1.0 (full inning pitched)
						while o > 0:
							num = int((pitchers[inning_pitcher].innings * 10) % 10)
							if num == 2:
								# the current pitched 2 outs, so the next out will make him pitch 1 full inning
								pitchers[inning_pitcher].innings += 0.8
							else:
								pitchers[inning_pitcher].innings += 0.1
							o -= 1
						inning_outs = x[7]
						inning_pitcher = x[5]

					if x[6] in hit_legend:
						pitchers[x[5]].hits += 1
						if x[6] == 'Home Run':
							pitchers[x[5]].home_runs += 1
					else:
						if x[6] == 'Walk' or x[6] == 'Intent Walk':
							pitchers[x[5]].walks += 1
						elif 'Strikeout' in x[6]:
							pitchers[x[5]].strikeouts += 1
					prev_batter = x[3]
					prev_id = x[0]
					prev_bscore = x[4]

				# calculate how many runs the last pitcher allowed
				pitchers[inning_pitcher].runs += prev_bscore - earned_runs

				# calculate the innings pitched for the last pitcher
				if full_pitch == False:
					o = 3 - inning_outs
					# innings pitched is weird in MLB
					# 1 out = 0.1, 2 outs = 0.2, 3 outs = 1.0 (full inning pitched)
					while o > 0:
						num = int((pitchers[inning_pitcher].innings * 10) % 10)
						if num == 2:
							# the current pitched 2 outs, so the next out will make him pitch 1 full inning
							pitchers[inning_pitcher].innings += 0.8
						else:
							pitchers[inning_pitcher].innings += 0.1
						o -= 1
				else:
					pitchers[inning_pitcher].innings += 1.0

				i_total = 0
				h_total = 0
				er_total = 0
				bb_total = 0
				so_total = 0
				hr_total = 0
				era_avg = 0
				count = 0.0
				rem = 0
				for key in pitchers:
					# ['Pitching', 'IP', 'H', 'ER', 'BB', 'SO', 'HR', 'ERA' ]
					era = 0.0
					if pitchers[key].innings > 0.0:
						era = round(9.0 * pitchers[key].runs / pitchers[key].innings,2)
						era_avg += era

					# int((pitchers[inning_pitcher].innings * 10) % 10)
					# have to add the innings the same way as before
					if pitchers[key].innings.is_integer():
						i_total += int(pitchers[key].innings)
					else:
						# have to add the runs individually
						# first add the whole number
						i_total += int(math.floor(pitchers[key].innings))
						r = int((round(pitchers[key].innings - math.floor(pitchers[key].innings),1) * 10) % 10)
						rem += r
						# rem can increase by 1, 2, or 3
						# keep track of the remainder, add it at the end

					h_total += pitchers[key].hits
					er_total += pitchers[key].runs
					bb_total += pitchers[key].walks
					so_total += pitchers[key].strikeouts
					hr_total += pitchers[key].home_runs

					tp.add_row([key, pitchers[key].innings, pitchers[key].hits, pitchers[key].runs, pitchers[key].walks, pitchers[key].strikeouts, pitchers[key].home_runs, '{:.2f}'.format(era)])
					count += 1.0

				i_total += int(rem /3)
				era_avg = round(era_avg / count,2)
				tp.add_row(['---------------','---','---','---','---','---','---', '----'])
				tp.add_row(['Team Totals', i_total, h_total, er_total, bb_total, so_total, hr_total, '{:.2f}'.format(era_avg)])

				for e in ejected_players:
					te.add_row([e.player, e.inning[0], e.des])

				pitching_title = self.team_cities[self.away] + ' ' + self.team_names[self.away] + ' Pitching Game Stats'
				print('')
				print(tp.get_string(title=pitching_title))

				if len(ejected_players) > 0:
					print('')
					print(te.get_string(title='Ejected Players'))

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
			query = "select gameYear, sum(runs), sum(runsAllowed), sum(games), sum(wins), sum(attendance) from ((select year(gameDate) as gameYear, sum(homeFinalScore) as runs, sum(awayFinalScore) as runsAllowed, count(gID) as games, count(case when winningTeam = '" + self.team_abbrev[self.nav] + "' then 1 else null end) as wins, sum(attendance) as attendance from Games where homeTeam='" + self.team_abbrev[self.nav] + "' group by year(gameDate)) union all (select year(gameDate) as gameYear, sum(awayFinalScore) as runs, sum(awayFinalScore) as runsAllowed, count(gID) as games, count(case when winningTeam = 'TOR' then 1 else null end) as wins, 0 as attendance from Games where awayTeam = 'TOR' group by year(gameDate))) teamGames group by gameYear;"

			self.cursor.execute(query)
			results = self.cursor.fetchall()
			full_team = self.team_cities[self.team_abbrev[self.nav]] + ' ' + self.nav + ' 2015-2018'
			t = PrettyTable()
			t.field_names = ['Season', 'Record', 'Total Runs', 'Avg Runs/Game', 'Total Runs Allowed', 'Avg Runs Allowed/Game', 'Total Attendance']
			t.align='l'
			for x in results:
				t.add_row([x[0], str(x[4]) + '-' + str(int(x[3])-int(x[4])), x[1], round(float(x[1])/float(x[4]),2), x[2], round(float(x[2])/float(x[4]),2), x[5]])
			print('')
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
					print('\n' + first_name + ' ' + last_name)
					self.print_pitcher_info()
					self.print_player_ejection_info()
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
					print('\n' + first_name + ' ' + last_name)
					self.print_batter_info()
					self.print_player_ejection_info()
					self.batter_info()

	def print_pitcher_info(self):
		# note that the visiting team always bats at the top of the inning
		# earned run average = earned runs / innings pitched  * 9
		query = "select a.gID, p.pitchNum, g.homeTeam, g.awayTeam, p.bScore, g.winningTeam, a.topInning, a.pitchDir, a.event from AtBats a left join Games g using(gID) left join Pitches p using (abID) where pitcherID = " + str(self.playerID) + ";"

		# print the data
		self.cursor.execute(query)
		results = self.cursor.fetchall()

		if self.cursor.rowcount == 0:
			print('Player is not a pitcher')
			return

		hand = []
		teams = []

		win_count = [0,0,0,0]
		loss_count = [0,0,0,0]
		games_started = [0,0,0,0]
		inning_count = [0.0,0.0,0.0,0.0]
		earned_runs = [0,0,0,0]
		strikeout_count = [0,0,0,0]
		home_run_count = [0,0,0,0]
		walk_count = [0,0,0,0]
		hit_count = [0,0,0,0]
		pitch_count = [0,0,0,0]
		hit_batter_count = [0,0,0,0]
		intent_walk_count = [0,0,0,0]
		at_bat_count = [0,0,0,0]

		inning_total = 0.0

		gId = 0
		prev_bscore = 0
		# Earned Run Average (ERA) = Earned Runs / Innings Pitched * 9, where Earned Runs is just the bScore
		for x in results:
			# separate the stats based on year (from the first 4 digits of the gID)
			yr = int(str(x[0])[:4])

			# year can be from 2015 - 2018
			yr = yr - 2015

			# add the pitch count
			pitch_count[yr] += 1

			# only calculate the rest of the stats on the first pitchNum
			if x[1] != 1:
				continue

			# check the pitchDir
			hand_dir = 'Left-Handed' if x[7] == 'L' else 'Right-Handed'
			if hand_dir not in hand:
				hand.append(hand_dir)
			# if topInning is true, then that means the visiting team is batting, so player is on the home team
			if x[6] == 'TRUE':
				team = self.team_cities[x[2]] + ' ' + self.team_names[x[2]]
				if team not in teams:
					teams.append(team)
			else:
				team = self.team_cities[x[3]] + ' ' + self.team_names[x[3]]
				if team not in teams:
					teams.append(team)

			if x[8] not in not_at_bat:
				at_bat_count[yr] += 1

			# tally the earns runed in Total
			if gId != x[0] and gId != 0:
				earned_runs[yr] += prev_bscore

			# hard to judge innings played, so let's just do it based on the event
			# we can know number of outs based on the event
			if x[8] in hit_legend:
				hit_count[yr] += 1
				if x[8] == 'Home Run':
					home_run_count[yr] += 1
			elif 'Walk' in x[8]:
				if x[8] == 'Intent Walk':
					intent_walk_count[yr] += 1
				walk_count[yr] += 1
			elif x[8] == 'Hit By Pitch':
				hit_batter_count[yr] += 1
			elif 'Strikeout' in x[8]:
				strikeout_count[yr] += 1
			elif x[8] == 'Triple Play':
				# 3 outs in this play
				inning_count[yr] = self.inning_add_out(inning_count[yr], 3)
				inning_total = self.inning_add_out(inning_total, 3)
			elif 'DP' in x[8] or x[8] == 'Double Play':
				# two outs in this play
				inning_count[yr] = self.inning_add_out(inning_count[yr], 2)
				inning_total = self.inning_add_out(inning_total, 2)
			elif 'out' in x[8] or 'Out' in x[8] or 'Sac' in x[8]:
				# 1 out in this play
				inning_count[yr] = self.inning_add_out(inning_count[yr], 1)
				inning_total = self.inning_add_out(inning_total, 1)

			# check the game counter
			if gId != x[0]:
				gId = x[0]
				# if he started the game, the first record for that game should be inning 1
				if x[1] == 1:
					games_started[yr] += 1
				# check who wins and loses and increment accordingly
				# if he pitches on top inning, then he plays for the home team
				if (x[5] == x[2] and x[6] == 'TRUE') or (x[5] == x[3] and x[6] == 'FALSE'):
					win_count[yr] += 1
				else:
					loss_count[yr] += 1

			prev_bscore = x[4]

		# print the calulcated stats

		if len(hand) == 2:
			print('Pitching: Ambidexterous')
		else:
			print('Pitching: ' + hand[0])
		print('\nPast and Current Teams:')
		print(*teams, sep = "\n")
		print('')

		tb = PrettyTable()
		tb.field_names = (['Year', 'G', 'GS', 'W-L', 'ERA', 'IP', 'H', 'ER', 'HR', 'NP', 'HB', 'BB', 'IBB', 'SO', 'AVG', 'WHIP'])
		tb.align = 'l'

		era_sum = 0.0
		whip_sum = 0.0
		avg_sum = 0.0
		games_sum = 0
		year_count = 0.0
		for i in range(0, 4):
			era = 0.0
			whip = 0.0
			avg = 0.0
			if inning_count[i] > 0:
				era = round(earned_runs[i] / inning_count[i] * 9.0,2)
				whip = round((walk_count[i] + hit_count[i]) / inning_count[i],2)
				era_sum += era
				whip_sum += whip
				year_count += 1.0
			games = win_count[i] + loss_count[i]
			games_sum += games
			if at_bat_count[i] > 0:
				avg = round(hit_count[i] / at_bat_count[i],3)
				avg_sum += avg
			record = str(win_count[i]) + '-' + str(loss_count[i])
			tb.add_row([self.years[i], games, games_started[i], record, '{:.2f}'.format(era), inning_count[i], hit_count[i], earned_runs[i], home_run_count[i], pitch_count[i], hit_batter_count[i], walk_count[i], intent_walk_count[i], strikeout_count[i], '{:.3f}'.format(avg), '{:.2f}'.format(whip)])

		tb.add_row(['------------', '----', '----', '-------', '------', '-------', '-----', '----', '----', '------', '----', '----', '-----', '-----', '------', '------'])
		era_sum = round(era_sum/year_count,2)
		whip_sum = round(whip_sum/year_count,2)
		avg_sum = round(avg_sum/year_count,3)

		record = str(sum(win_count)) + '-' + str(sum(loss_count))
		tb.add_row(['Player Totals', games_sum, sum(games_started), record, '{:.2f}'.format(era_sum), sum(inning_count), sum(hit_count), sum(earned_runs), sum(home_run_count), sum(pitch_count), sum(hit_batter_count), sum(walk_count), sum(intent_walk_count), sum(strikeout_count), '{:.3f}'.format(avg_sum), '{:.2f}'.format(whip_sum)])

		print('')
		print(tb.get_string(title='Yearly Pitching Stats'))

		# grab and print pitch stats
		query = "select pitchType, count(pitchType), avg(p.startSpeed), avg(p.endSpeed), avg(p.spinRate) from Pitches p left join AtBats a using (abID) where a.pitcherID = " + str(self.playerID) + " group by p.pitchType;"
		self.cursor.execute(query)
		results = self.cursor.fetchall()

		t = PrettyTable()
		t.field_names = ['Pitch Type', 'Total Thrown', 'Average Start Speed (MPH)', 'Average End Speed (MPH)', 'Average Spin Rate']
		t.align = 'l'

		throw_total = 0
		avg_start_speed = 0.0
		avg_end_speed = 0.0
		avg_spin_rate = 0.0
		count = 0.0

		for x in results:
			if x[0] in pitch_legend:
				t.add_row([pitch_legend[x[0]], x[1], '{:.2f}'.format(round(x[2],2)), '{:.2f}'.format(round(x[3],2)), '{:.2f}'.format(round(x[4],2))])
				throw_total += x[1]
				avg_start_speed += round(x[2],2)
				avg_end_speed += round(x[3],2)
				avg_spin_rate += round(x[4],2)
				count += 1.0

		avg_start_speed = round(avg_start_speed / count,2)
		avg_end_speed = round(avg_end_speed / count,2)
		avg_spin_rate = round(avg_spin_rate / count,2)

		t.add_row(['--------------------', '--------------', '---------------------------', '-------------------------', '-------------------+'])
		t.add_row(['Player Totals', throw_total, '{:.2f}'.format(avg_start_speed), '{:.2f}'.format(avg_end_speed), '{:.2f}'.format(avg_spin_rate)])
		print('')
		print(t.get_string(title='Pitch Breakdown'))

	def print_batter_info(self):
		query = "select a.gID, g.homeTeam, g.awayTeam, g.winningTeam, a.inning, a.topInning, a.batDir, a.event from AtBats a left join Games g using (gID)  where batterID = " + str(self.playerID) + ";"
		self.cursor.execute(query)
		results = self.cursor.fetchall()

		if self.cursor.rowcount == 0:
			print('Player is not a batter')
			return

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
		if len(bat_dir) == 2:
			print('Batting: Ambidexterous')
		else:
			print('Batting: ' + bat_dir[0])
		print('\nPast and Current Teams:')
		print(*teams, sep = "\n")
		print('')

		tb = PrettyTable()
		tb.field_names = ['Year', 'GP', 'W-L', 'AB', 'H', '1B', '2B', '3B', 'HR', 'BA', 'OBP', 'SLG', 'OPS']
		tb.align = 'l'

		yr_count = 0.0
		ba_avg = 0.0
		obp_avg = 0.0
		slg_avg = 0.0
		ops_avg = 0.0

		for i in range(0, 4):
			games = win_count[i] + loss_count[i]
			record = str(win_count[i]) + '-' + str(loss_count[i])
			ba = 0.0
			obp = 0.0
			slg = 0.0
			ops = 0.0
			if at_bats[i] > 0:
				ba = round(float(hits[i]/at_bats[i]),3)
				ba_avg += ba
				obp = round(float(times_on_base[i]/at_bats[i]),3)
				obp_avg += obp
				slg = round((singles[i] + 2 * doubles[i] + 3 * triples[i] + 4 * home_runs[i])/at_bats[i],3)
				slg_avg += slg
				ops = obp + slg
				ops_avg += ops
				yr_count += 1.0
			tb.add_row([self.years[i], games, record, at_bats[i], hits[i], singles[i], doubles[i], triples[i], home_runs[i], '{:.3f}'.format(ba), '{:.3f}'.format(obp), '{:.3f}'.format(slg), '{:.3f}'.format(ops)])

		ba_avg = round(ba_avg/yr_count,3)
		obp_avg = round(obp_avg/yr_count,3)
		slg_avg = round(slg_avg/yr_count,3)
		ops_avg = round(ops_avg/yr_count,3)
		game_sum = sum(win_count) + sum(loss_count)
		record = str(sum(win_count)) + '-' + str(sum(loss_count))

		tb.add_row(['-------------', '----', '-------', '-------', '------', '-------', '-----', '----', '----', '------', '----', '----', '-----'])
		tb.add_row(['Player Totals', game_sum, record, sum(at_bats), sum(hits), sum(singles), sum(doubles), sum(triples), sum(home_runs), '{:.3f}'.format(ba_avg), '{:.3f}'.format(obp_avg), '{:.3f}'.format(slg_avg), '{:.3f}'.format(ops_avg)])
		print('')
		print(tb.get_string(title='Yearly Batting Stats'))

	def print_game_ejection_info(self):
		query = "select a.inning, e.description, e.argueBallsStrikes, e.correctEjection from Ejections e left join AtBats a using (abID) where a.gID = " + str(self.gameID) + ";"
		self.cursor.execute(query)
		results = self.cursor.fetchall()

		t = PrettyTable()
		t.field_names = ['Inning', 'Description', 'Argue BS', 'Correct']
		t.align = 'l'
		t.title = 'Game Ejections'

		for x in results:
			bs = 'Yes' if x[2] == 'FALSE' else 'No'
			corr = ''
			if x[3] is None:
				corr = 'N/A'
			else:
				corr = 'Yes' if x[3] == 'TRUE' else 'No'
			t.add_row([x[0], x[1], bs, corr])
		print(t)


	def print_player_ejection_info(self):
		# have the playerID, so just run query on ejection on playerID
		query = "select g.gameDate, g.homeTeam, g.awayTeam, e.team, a.inning, e.argueBallsStrikes, e.correctEjection from Ejections e left join AtBats a using (abID) left join Games g using (gID) where playerID =" + str(self.playerID) + ";"
		self.cursor.execute(query)
		results = self.cursor.fetchall()

		te = PrettyTable()
		te.field_names = ['Game', 'Team', 'Inning', 'Argue BS', 'Correct']
		te.align = 'l'
		te.title = 'Player Ejections'

		for x in results:
			home_team = self.team_cities[x[1]] + ' ' + self.team_names[x[1]]
			away_team = self.team_cities[x[2]] + ' ' + self.team_names[x[2]]
			player_team = self.team_cities[x[3]] + ' ' + self.team_names[x[3]]
			game = away_team + ' at ' + home_team + ', ' + x[0].strftime("%Y-%m-%d")
			bs = 'Yes' if x[5] == 'TRUE' else 'No'
			corr = ''
			if x[6] is None:
				corr = 'N/A'
			else:
				corr = 'Yes' if x[6] == 'TRUE' else 'No'
			te.add_row([game, player_team, x[4], bs, corr])

		print('')
		print(te)

	def print_team_ejection_info(self):
		# use self.nav to get the selected team abbreviation
		query = "select g.homeTeam, g.awayTeam, g.gameDate, a.inning, p.firstName, p.lastName, e.argueBallsStrikes, e.correctEjection from Ejections e left join AtBats a using(abID) left join Games g using (gID) left join PlayerNames p on p.id = e.playerID  where e.team = '" + self.team_abbrev[self.nav] + "';"
		self.cursor.execute(query)
		results = self.cursor.fetchall()

		te = PrettyTable()
		te.title = 'Team Ejections 2015-2018'
		te.field_names = ['Game', 'Inning', 'Player', 'Argue BS', 'Correct']
		te.align = 'l'

		for x in results:
			home_team = self.team_cities[x[0]] + ' ' + self.team_names[x[0]]
			away_team = self.team_cities[x[1]] + ' ' + self.team_names[x[1]]
			game = away_team + ' at ' + home_team + ', ' + x[2].strftime("%Y-%m-%d")
			player = x[4] + ' ' + x[5]
			bs = 'Yes' if x[6] == 'TRUE' else 'No'
			corr = ''
			if x[7] is None:
				corr = 'N/A'
			else:
				corr = 'Yes' if x[7] == 'TRUE' else 'No'
			te.add_row([game, x[3], player, bs, corr])
		print('')
		print(te)

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
		exit()

MLB_client = MLB()
MLB_client.first_load()
