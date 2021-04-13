# ECE 356 Project

Matthew Lee, Jeffrey Yuen, Martin Hsu

## Project Topic - MLB

MLB, Data found from the following Kaggle URLs

### Pitch Data

```bash
https://www.kaggle.com/pschale/mlb-pitch-data-20152018
```

Pitch-level data for every pitch thrown during the 2015-2018 MLB regular seasons. Each row represents a single pitch.

### Project Information
#### SQL Data
In this project we use create SQL queries and communicate to the database using MySQL and our tables and data is stored in the project_36 database of marmoset
### Client 
The client is written in Python, and to run the application, first make sure that you set your directory to the client folder 

```bash
cd Design/Client
```
Here you will see MLB_client.py. Before you can run the application, you should make sure you have the necessary libraries installed, specifically the mysql.connector 

```bash
pip install mysql-connector-python
```
```bash
pip install mysql-connector-python --user
```
You may have to add --user if you do not have write permissions on the ece ubuntu machines. 
The other libraries used are already part of Python already so you don't need to install those libraries. All you have to do after is run the python file and you will be prompted to login to the SQL connection and you are free to follow the instructions on the application 

```bash
python3 MLB_client.py
```
### Useful Information
Below is a legend for some of the codes and definitions in the SQL database. You can use this to understand the meaning behind some of the data, specifically in the AtBats and Pitches tables. 

#### Pitch Type Definitions
CH - Changeup

CU - Curveball

EP - Eephus*

FC - Cutter

FF - Four-seam Fastball

FO - Pitchout (also PO)*

FS - Splitter

FT - Two-seam Fastball

IN - Intentional ball

KC - Knuckle curve

KN - Knuckeball

PO - Pitchout (also FO)*

SC - Screwball*

SI - Sinker

SL - Slider

UN - Unknown*

#### Code Definitions 
B - Ball

*B - Ball in dirt

S - Swinging Strike

C - Called Strike

F - Foul

T - Foul Tip

L - Foul Bunt

I - Intentional Ball

W - Swinging Strike (Blocked)

M - Missed Bunt

P - Pitchout

Q - Swinging pitchout

R - Foul pitchout

Values that only occur on last pitch of at-bat:

X - In play, out(s)

D - In play, no out

E - In play, runs

H - Hit by pitch