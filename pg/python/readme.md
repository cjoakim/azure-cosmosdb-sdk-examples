## PostgreSQL with Python - Examples


### psql.ps1 helper script

```
PS ...\python> .\psql.ps1

Usage:
.\psql.ps1 <env> <db> - where env is local, flex, or cosmos
.\psql.ps1 local postgres
.\psql.ps1 local dev
.\psql.ps1 flex postgres
.\psql.ps1 cosmos citus
```

### baseball_deldef.ps1 script

```
PS ...\python> .\baseball_deldef.ps1

Usage:
.\psql.ps1 <env> <db> - where env is local, flex, or cosmos
.\psql.ps1 local postgres
.\psql.ps1 local dev
.\psql.ps1 flex postgres
.\psql.ps1 cosmos citus
```

### main.py

```
python main.py check_environment_variables

python main.py load_baseball_players <envname> <dbname>

python main.py load_baseball_players local postgres
python main.py load_baseball_players flex postgres
python main.py load_baseball_players cosmos citus

python main.py load_baseball_batters local postgres
python main.py load_baseball_batters flex postgres
python main.py load_baseball_batters cosmos citus
```

### psql with Cosmos DB PostgreSQL example

Open a psql shell and get the 'citus=>' prompt.

```
> .\psql.ps1 cosmos citus
...

citus=>
```

Count the players rows.

```
citus=> select count (*) from public.players;
 count
-------
 18221
(1 row)
```

Count the batters rows.

```
citus=> select count (*) from public.batters;
 count
-------
  5263
(1 row)
```

Turn on expanded display for column-per-line output instead of wide output.

```
citus=> \x on
Expanded display is on.
```

Display the schema of the players and batters tables.

```
citus=> \d players
                                        Table "public.players"
      Column      |         Type          | Collation | Nullable |               Default
------------------+-----------------------+-----------+----------+-------------------------------------
 id               | bigint                |           | not null | nextval('players_id_seq'::regclass)
 player_id        | character varying(32) |           |          |
 birth_year       | integer               |           |          |
 birth_country    | character varying(32) |           |          |
 first_name       | character varying(32) |           |          |
 last_name        | character varying(32) |           |          |
 bats             | character(1)          |           |          |
 throws           | character(1)          |           |          |
 category         | character varying(16) |           |          |
 primary_position | character varying(2)  |           |          |
 primary_team     | character varying(8)  |           |          |
 debut_year       | integer               |           |          |
 final_year       | integer               |           |          |
 total_games      | integer               |           |          |
 teams_data       | jsonb                 |           |          |
 pitching_data    | jsonb                 |           |          |
 batting_data     | jsonb                 |           |          |
Indexes:
    "players_pkey" PRIMARY KEY, btree (id)


citus=> \d batters
                                        Table "public.batters"
      Column      |         Type          | Collation | Nullable |               Default
------------------+-----------------------+-----------+----------+-------------------------------------
 id               | bigint                |           | not null | nextval('batters_id_seq'::regclass)
 player_id        | character varying(32) |           |          |
 birth_year       | integer               |           |          |
 birth_country    | character varying(32) |           |          |
 first_name       | character varying(32) |           |          |
 last_name        | character varying(32) |           |          |
 bats             | character(1)          |           |          |
 throws           | character(1)          |           |          |
 primary_position | character varying(2)  |           |          |
 primary_team     | character varying(8)  |           |          |
 debut_year       | integer               |           |          |
 final_year       | integer               |           |          |
 total_games      | integer               |           |          |
 atbats           | integer               |           |          |
 runs             | integer               |           |          |
 hits             | integer               |           |          |
 doubles          | integer               |           |          |
 triples          | integer               |           |          |
 homeruns         | integer               |           |          |
 rbi              | integer               |           |          |
 stolen_bases     | integer               |           |          |
 caught_stealing  | integer               |           |          |
 bb               | integer               |           |          |
 so               | integer               |           |          |
 ibb              | integer               |           |          |
 hbp              | integer               |           |          |
 sacfly           | integer               |           |          |
 runs_per_ab      | numeric(16,12)        |           |          |
 batting_avg      | numeric(16,12)        |           |          |
 double_avg       | numeric(16,12)        |           |          |
 triple_avg       | numeric(16,12)        |           |          |
 hr_avg           | numeric(16,12)        |           |          |
 rbi_avg          | numeric(16,12)        |           |          |
 bb_avg           | numeric(16,12)        |           |          |
 so_avg           | numeric(16,12)        |           |          |
 ibb_avg          | numeric(16,12)        |           |          |
 hbp_avg          | numeric(16,12)        |           |          |
 sb_pct           | numeric(16,12)        |           |          |
Indexes:
    "batters_pkey" PRIMARY KEY, btree (id)
```

Search for Rickey Henderson.

```
citus=> select * from batters where batters.player_id = 'henderi01';
-[ RECORD 1 ]----+---------------
id               | 7043
player_id        | henderi01
birth_year       | 1958
birth_country    | USA
first_name       | Rickey
last_name        | Henderson
bats             | R
throws           | L
primary_position | LF
primary_team     | OAK
debut_year       | 1979
final_year       | 2003
total_games      | 3081
atbats           | 10961
runs             | 2295
hits             | 3055
doubles          | 510
triples          | 66
homeruns         | 297
rbi              | 1115
stolen_bases     | 1406
caught_stealing  | 335
bb               | 2190
so               | 1694
ibb              | 61
hbp              | 98
sacfly           | 67
runs_per_ab      | 0.209378706322
batting_avg      | 0.278715445671
double_avg       | 0.046528601405
triple_avg       | 0.006021348417
hr_avg           | 0.027096067877
rbi_avg          | 0.101724295229
bb_avg           | 0.199799288386
so_avg           | 0.154547942706
ibb_avg          | 0.005565185658
hbp_avg          | 0.008940790074
sb_pct           | 0.807581849512


citus=> select * from players where players.player_id = 'henderi01';
-[ RECORD 1 ]----+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
id               | 7043
player_id        | henderi01
birth_year       | 1958
birth_country    | USA
first_name       | Rickey
last_name        | Henderson
bats             | R
throws           | L
category         | fielder
primary_position | LF
primary_team     | OAK
debut_year       | 1979
final_year       | 2003
total_games      | 3081
teams_data       | {"teams": {"ANA": 32, "BOS": 72, "LAN": 30, "NYA": 596, "NYN": 152, "OAK": 1704, "SDN": 359, "SEA": 92, "TOR": 44}, "total_games": 3081, "primary_team": "OAK"}
pitching_data    | {}
batting_data     | {"G": 3081, "H": 3055, "R": 2295, "2B": 510, "3B": 66, "AB": 10961, "BB": 2190, "CS": 335, "HR": 297, "SB": 1406, "SF": 67, "SO": 1694, "HBP": 98, "IBB": 61, "RBI": 1115, "calculated": {"2b_avg": 0.046528601404981294, "3b_avg": 0.006021348417115227, "bb_avg": 0.19979928838609615, "hr_avg": 0.027096067877018522, "sb_pct": 0.8075818495117748, "so_avg": 0.15454794270595748, "hbp_avg": 0.008940790073898367, "ibb_avg": 0.005565185658242861, "rbi_avg": 0.10172429522853754, "batting_avg": 0.2787154456710154, "runs_per_ab": 0.20937870632241584}}

```
