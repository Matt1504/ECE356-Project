// Client Application Code

//#include <mysql.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>

// function definitions 
void gamePage();
void playerPage();
void homePage();
void gameInfo();
void teamInfo(); 
void pitcherInfo();
void batterInfo();
void printPlayers();
void printTeams(); 
int getPlayerInfo(int bp); 
int runSqlQuery(); 
int main(const int argc, const char* argv[]);

char nav[10]; 
char name[50];
char game[50];
char team[50];

// hard code the sql params 
const char* USERID = "db356test1"; 
const char* PASSWORD = "...";
const char* SERVER = "marmoset04.shoshin.uwaterloo.ca";
const char* DBNAME = "project_36";

MYSQL mysql;
MYSQL* pMysql = &mysql;

MYSQL_RES* pQueryResult;                                  // Pointer to query result handler
MYSQL_ROW  row;                                           // Space for result row
int numFields; 

int main(const int argc, const char* argv[]) {

	const int bufLen = 256;
	char passwd[bufLen]; 

	if (!mysql_init(pMysql)) {
		fprintf(stderr, "%s: mysql_init() error: insufficient memory\n", argv[0]);
		return -1*ENOMEM;
	}

  // Use default port (3306)
	if (!mysql_real_connect(pMysql, SERVER, USERID, passwd, DBNAME, 0, NULL, 0)) {
		fprintf(stderr, "%s: mysql_real_connect() error: %s\n",argv[0],mysql_error(pMysql));
		return -1
	}

	homePage(); 
}

void homePage() {
	printf("Welcome to the MLB Stats Database for the 2015 to 2018 Regular Seasons!\n");
	printf("Input \"back\" to go to previous page, or \"home\" to go back to this page at any point.\n");
	printf("Do you want to view:\n"); 
	printf("\t1. Game Data\n");
	printf("\t2. Player Data\n"); 
	printf("Enter where you want to go: "); 
	scanf("%s", nav); 
	if (strcmp(nav, "1") == 0) {
		gamePage();
	} else if (strcmp(nav, "2") == 0) {
		playerPage(); 
	} else if (strcmp(nav, "home") == 0) {
		homePage(); 
	} else if (strcmp(nav, "back") == 0) {
		homePage(); 
	}
}

void gamePage() {
	// Game Data
	printf("Game Data\n");
	printf("Do you want to view: \n");
	printf("\t 1. A Single Game\n");
	printf("\t 2. Combined Team Data\n");
	printf("Enter where you want to go: "); 
	scanf("%s", nav);
	if (strcmp(nav, "1") == 0) {
		gameInfo();
	} else if (strcmp(nav, "2") == 0) {
		teamInfo(); 
	} else if (strcmp(nav, "back") == 0) {
		homePage(); 
	} else if (strcmp(nav, "home") == 0) {
		homePage(); 
	}
}

void playerPage() {
	// Player Data
	printf("Player Data\n");
	printf("Do you want to view: \n");
	printf("\t 1. Pitcher's Data\n");
	printf("\t 2. Batter's Data\n");
	printf("Enter where you want to go: "); 
	scanf("%s", nav);
	if (strcmp(nav, "1") == 0) {
		pitcherInfo(); 
	} else if (strcmp(nav, "2") == 0) {
		batterInfo(); 
	} else if (strcmp(nav, "back") == 0) {
		homePage(); 
	} else if (strcmp(nav, "home") == 0) {
		homePage(); 
	}

}

void gameInfo() {
	printf("Game Data: Single Game\n"); 
	printf("Enter the home team, away team, and date of the game you are looking for:\n");
	printf("Format <home_team> <away_team> <yyy-mm-dd>\n");
	printf("Type \"year\" to filter games by year.\n"); 
	printf("Type \"team\" to filter games by team\n"); 
	scanf("%s", game); 
	if (strcmp(game, "back") == 0) {
		gamePage(); 
	} else if (strcmp(game, "home") == 0) {
		homePage(); 
	} else {
		if (strcmp(game, "year") == 0 || strcmp(game, "team") == 0) { 
			if (strcmp(game, "year") == 0) {
				scanf("Enter the desired year to display all games by that year (2015-2018) %s\n", game);
				printf("showing games from %s", game); 
		// run query to get all games from that year 

			} else if (strcmp(game, "team") == 0) {
		// run query to get all team names 
		// ....
		// display teams 
				printf("Below are all MLB teams\n"); 
			}
			printf("Enter the home team, away team, and date of the game you are looking for:\n");
			printf("Format <home_team> <away_team> <yyy-mm-dd>\n");
			scanf("%s", game); 
		}
	// run query to get the game 
	// have to split the char first 
	}
}

void teamInfo() {
	printf("Game Data: Combined Team Data\n"); 
	printf("Enter the team's name of the team you are looking for\n"); 
	printf("Type \"show teams\" to display all active teams\n"); 
	scanf("%s", team); 
	if (strcmp(team, "back") == 0) {
		gamePage(); 
	} else if (strcmp(team, "home") == 0) {
		homePage(); 
	} else  {
		if (strcmp(team, "show teams") == 0) {
			printTeams(); 
			printf("Enter the team's name of the team you are looking for\n"); 
			scanf("%s", team); 
		}
		// get the info for that team 
	}
}

void pitcherInfo() {
	printf("Player Data: Pitchers\n");
	printf("Enter the name of the pitcher you are looking for: \n");
	printf("(Format: <first name>, <last name>)\n");
	printf("Type \"show players\" to display all active players\n"); 
	scanf("%s", name); 
	if (strcmp(nav, "back") == 0) {
		playerPage(); 
	} else if (strcmp(nav, "home") == 0) {
		homePage(); 
	} else {
		if (strcmp(name, "show players") == 0) {
			printPlayers(); 
			printf("Enter the name of the pitcher you are looking for: \n");
			scanf("%s", name); 
		}
		// run query 
		// first should check that the player exists 
		getPlayerInfo(1); 
	}
}


void batterInfo() {
	printf("Player Data: Batters\n");
	printf("Enter the name of the batter you are looking for: \n");
	printf("(Format: <first name>, <last name>)\n");
	printf("Type \"show players\" to display all active players\n"); 
	scanf("%s", name); 
	if (strcmp(nav, "back") == 0) {
		playerPage(); 
	} else if (strcmp(nav, "home") == 0) {
		homePage(); 
	} else {
		if (strcmp(name, "show players") == 0) {
			printPlayers(); 
			printf("Enter the name of the pitcher you are looking for: \n");
			scanf("%s", name); 
		}
		// run query 
		// first should check that the player exists 
		getPlayerInfo(0); 
	}
}

void printPlayers() {
	// run query to display all players 
	char query[] = "select concat(firstName, ' ',lastName) from PlayerNames;";
	 // Run the query
	printf("Showing active players\n"); 
	runSqlQuery(query);
	// print the data
}

void printTeams() {
	// run query to display all teams 
	char query[] = "select concat(city, ' ', shortName) from TeamNames;"; 
	// run the query
	printf("Showing active teams\n"); 
	runSqlQuery(query); 
	// print the data
}

int getPlayerInfo(int bp) {
	// first split the string to get first name last name 
	char *token;
	char *firstName;
	char *lastName;
	char buffer[100]; 

	token = strtok(name, ", "); 
	// this will get the first name
	strcpy(firstName, token); 

	token = strtok(NULL, ", "); 
	// this will get the last name
	strcpy(lastName, token); 

	char str1[100] = "select 1 from PlayerNames where firstName = '";
	char str2[100] = "' and lastName = '";
	char str3[100] = "';";

	strcat(buffer, str1); 
	strcat(buffer, firstName); 
	strcat(buffer, str2); 
	strcat(buffer, lastName); 
	strcat(buffer, str3); 

	runSqlQuery(buffer);

	// if the player exists get their stats
	// bp == 1 -- pitch info
	// bp == 0 -- bat info 

	return 0; 
}

int runSqlQuery(char* query) {
// Run the query
	int rc =  mysql_query(pMysql, query);
	if (rc) {
		fprintf(stderr, "%s: mysql_query() error: %s\n",argv[0],mysql_error(pMysql));
		fprintf(stderr, "rc: %d\n", rc);
		return -1;
	}

	// Fetch the results
	pQueryResult =  mysql_store_result(pMysql);
	numFields = mysql_field_count(pMysql);                     // And get the field count
	if (!pQueryResult) {                                       // We got nothing back; that may be OK
		if (numFields == 0) {                                    // We should have nothing back!
			fprintf(stderr, "%s: Information: Query \"%s\" returned zero rows\n", argv[0], query);
		}
		else {
			fprintf(stderr, "%s: Error: Query \"%s\" failed to return expected data\n", argv[0], query);
			fprintf(stderr, "%s: error information: %s\n",argv[0],mysql_error(pMysql));
			return -1;
		}
	}
	return 0; 
}