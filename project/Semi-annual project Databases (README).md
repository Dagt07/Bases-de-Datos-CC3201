# Semi-annual project Databases / Proyecto semestral Bases de Datos

## Members (Integrantes):

- David García T. - [github Dagt07](https://github.com/Dagt07)
- José Villalobos C. - [github JVC2003](https://github.com/JVC2003)
- Martín Bahamonde M. - [github Asterix265](https://github.com/Asterix265)
- Víctor Alfaro P. - [github gitonina](https://github.com/gitonina)

## Data Source (Fuente de Datos):

[NBA Stats (1947-present)](https://www.kaggle.com/sumitrodatta/nba-aba-baa-stats)

![Data Source](project%20images/datasource.png)

## Problem to solve (Problema a resolver):

To study through a data analysis the evolution of the sport in this league, which has changed so much from its beginnings to the present day (for example, the increase over time in offense/points per game, the relationship of this with the increase in effective 3-point shot attempts).

## Modelo entidad relación

Entity-Relationship model of the project, phase 1 (pre-feedback) / Modelo entidad relación del proyecto, hito 1 (pre feedback):

![ModeloERhito1](project%20images/ModeloER_hito1.png)

Entity-Relationship model of the project, phase 2 (post-feedback) / Modelo entidad relación del proyecto hito 2 (post feedback):

![ModeloERhito2](project%20images/ModeloER_hito2.png)

Entity-Relationship model of the project, phase 2 (post-feedback) / Modelo entidad relación del proyecto hito 2 (post feedback):

![ModeloERhito2](project%20images/ModeloER_hito3.png)

## Entity-Relationship Model (Modelo relacional)

Relational model of the project, phase 1 (pre-feedback) / Modelo relacional del proyecto, hito 1 (pre feedback):

![Untitled](project%20images/ModeloRHito2.png)

Relational model of the project, phase 2 (post-feedback) / Modelo relacional del proyecto, hito 2 (post feedback):

![Untitled](project%20images/ModeloRHito2feedback.png)

Relational model of the project, phase 3 (post-feedback) / Modelo relacional del proyecto, hito 3 (post feedback):

![Untitled](project%20images/ModeloRhito3.jpeg)

## SQL Table Creation Code (Código SQL Creación de tablas)

It's worth mentioning that our project consists of a data analysis (and not a web page), therefore, we were not provided with a VM (Virtual Machine). We consulted with the teacher and they recommended us to create the database using PostgreSQL. For this purpose, we used Beekeeper Studio to create the database: 'batos'.

Then, the SQL code used to create the tables according to our relational model is as follows:

```sql
CREATE SCHEMA IF NOT EXISTS batos;

CREATE TABLE batos.player ( player_id serial PRIMARY KEY , name VARCHAR (255), age INT ) ;

CREATE TABLE batos.team ( team_id serial PRIMARY KEY, teamName VARCHAR (255), abbreviation VARCHAR(255)) ;

CREATE TABLE batos.season ( season_id serial PRIMARY KEY, year INT, league VARCHAR(255)) ;

CREATE TABLE batos.team_season ( 
season_id INT,
team_id INT,
x2P INT,
x2PA INT,
x2Pp FLOAT,
FTp FLOAT,
FG INT,
FGA  INT,
FGp FLOAT,
FT INT,
x3P INT,
x3PA INT,
x3Pp FLOAT,
stl INT,
assists INT,
pf INT, 
blocks INT,
drb INT,
FOREIGN KEY (season_id) REFERENCES batos.season(season_id),
FOREIGN KEY (team_id) REFERENCES batos.team(team_id),
PRIMARY KEY (season_id, team_id) ) ;

CREATE TABLE batos.player_team_season(
id serial,
player_id INT,
team_id INT,
season_id INT,
Experience INT,
player_position VARCHAR(255),
x3P INT,
FGA INT,
FG INT, 
x2P INT,
dbpm FLOAT,
obpm FLOAT,
ows FLOAT,
dws FLOAT,
x2PA INT,
x3PA INT,
FTp FLOAT,
FT INT,
x3Pp FLOAT,
FGp FLOAT,
x2Pp FLOAT,
assits INT,
PF INT,
blocks INT,
drb INT,
stl INT,
avg_dist_fga FLOAT,
FOREIGN KEY (player_id) REFERENCES batos.player(player_id),
FOREIGN KEY (season_id) REFERENCES batos.season(season_id),
FOREIGN KEY (team_id) REFERENCES batos.team(team_id),
PRIMARY KEY (id) ) ;

CREATE TABLE batos.awards (
    award VARCHAR (255),
		pts_id INT,
    ptos_won FLOAT,
    FOREIGN KEY (pts_id) REFERENCES batos.player_team_season(id),
    PRIMARY KEY (award, pts_id)
);
```

## Glossary of terms (Glosario de términos)
- **dws (defensive win share)**: Statistic that considers the impact/ability of a player to prevent the opposing team from scoring.
- **ows (offensive win share)**: Statistic that considers the impact/ability of a player to score against the opposing team.
- **obpm (offensive box plus/minus)**: Measures the contribution to the team's total performance in attack through player statistics, per hundred possessions.
- **dbm (defensive box plus/minus)**: Measures the contribution to the team's total performance in defense through player statistics, per hundred possessions.
- **2p%**: Percentage reflecting a player's success in scoring 2-pointers.
- **2p**: Number of 2-pointers scored by a player in a season.
- **2pa**: Number of attempted 2-pointers by a player, not necessarily equal to 2p.
- **FT**: Number of free throws made by a player.
- **FT%**: Percentage reflecting the number of free throws made by a player.
- **FGA**: Number of shots attempted, both 3-pointers and 2-pointers.
- **FG**: Number of shots made, both 3-pointers and 2-pointers.
- **assists**: Player's assists in a season.
- **pf**: Player's fouls in a season.
- **blocks**: Number of blocks by a player.
- **drb**: Number of defensive rebounds.
- **stl**: Number of steals.
- **experience**: Number of years played by a player since joining the NBA.
- **player-position**: Refers to the position a player plays for the team, could be shooting guard, small forward, point guard, etc.
- **avg_dist_fga**: Average distance of attempted shots.