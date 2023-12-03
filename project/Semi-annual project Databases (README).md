# Semi-annual project Databases / Proyecto semestral Bases de Datos

## Integrantes:

- David García T. - [github Dagt07](https://github.com/Dagt07)
- José Villalobos C. - [github JVC2003](https://github.com/JVC2003)
- Martín Bahamonde M. - [github Asterix265](https://github.com/Asterix265)
- Víctor Alfaro P. - [github gitonina](https://github.com/gitonina)

## Fuente de Datos:

[NBA Stats (1947-present)](https://www.kaggle.com/sumitrodatta/nba-aba-baa-stats)

[https://www.kaggle.com/sumitrodatta/nba-aba-baa-stats](https://www.kaggle.com/sumitrodatta/nba-aba-baa-stats)

Extraídos de una de las paginas de fuentes de datos brindadas por el cuerpo docente

## Problema a resolver:

Estudiar mediante un *análisis de datos* la evolución del deporte en esta liga, que tanto ha cambiado desde sus inicios a la actualidad el deporte (ejemplo aumento a través del tiempo de la ofensiva/cantidad de puntos por juego, relación de esto último con el aumento de lanzamientos de 3 puntos efectivos).

## Modelo entidad relación

modelo entidad relación del proyecto, hito 1 (pre feedback):

![ModeloER hito 1.drawio.png](project%20images/ModeloER_hito_1.drawio.png)

modelo entidad relación del proyecto hito 2 (post feedback):

![ModeloER hito2.drawio (2).png](project%20images/ModeloER_hito2.drawio_(2).png)

## Modelo relacional

modelo relacional del proyecto, hito 1 (pre feedback):

![Untitled](project%20images/Untitled.png)

modelo relacional del proyecto, hito 2 (post feedback):

![Untitled](project%20images/Untitled%201.png)

## Código SQL Creación de tablas

Cabe destacar que nuestro proyecto consiste en un análisis de datos (y no una página web) por tanto no nos proporcionaron una VM. Consultamos con el profe y nos recomendó crear la base de datos usando postgres. Para ello usamos beekeper studio para crear la data base: ‘batos’.

Luego el código SQL usado para crear las tablas de acuerdo a nuestro modelo relacional es el siguiente:

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

## Glosario de términos

- dws (defensive win share): Estadística que contempla el impacto/habilidad que tiene un jugador para prevenir que el equipo
rival anote.
- ows (offensive win share): Estadistica que contempla el impacto/habilidad que tiene un jugador anotar al equipo rival
- obpm(offensive box plus/minus): Mide la aportacion al rendimiento total del equipo en ataque a traves de las estadisticas del
jugador, por cada cien posesiones
- dbm(deffensive box plus/minus): Mide la aportacion al rendimiento total del equipo en defense a traves de las estadisticas
del jugador, por cada cien posesiones.
- 2p%: Porcentaje que refleja el acierto de un jugador al anotar 2 puntos
- 2p: Cantidad de dobles que anoto un jugador en una temporada
- 2pa: Cantidad de doble que intentó un jugador, no necesariamente es igual a 2p.
- FT: La cantidad de tiros libres que anotó un jugador
- FT%: Porcentaje que refleja la cantidad de tiros libres anotados por un jugador.
- FGA: Cantidad de tiros intentados tanto de triples como de dobles.
- FG: Cantidad de tiros anotados, tanto triples como dobles.
- assists: asistencias de un jugador en una temporada.
- pf: fouls de un jugador en una temporada.
- blocks: Cada de bloqueos/tapones de un jugador.
- drb:  Cantidad de rebotes defensivos
- stl: Cantidad de robos
- experience: Cantidad de años jugados por un jugador desde su llegada a la NBA.
- player-position: alude a la posicion en la que juega un jugador por el equipo, puede ser escolta, alero, base, etc.
- avg_dist_fga: Promedio de la distancia de los tiros intentados.