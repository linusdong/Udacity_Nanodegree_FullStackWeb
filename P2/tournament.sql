-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- CLEAR ALL DATA!! psql -f tournament.sql
DROP DATABASE IF EXISTS tournament;

-- Build database from scratch
CREATE DATABASE tournament;

--connect to database
\c tournament

-- player table holds basic information for player. we assume the 
-- same player can attend multiple tournaments 
create table players (
	id SERIAL,
	name TEXT,
	primary key (id)
);

-- extra credit for multiple tournaments
create table tournaments (
	id SERIAL,
	name TEXT,
	primary key (id)
);

-- matches holds match_id, player_id and tournament_id. There are
-- 3 value in i_am_winner for extra credit.
-- -1 means the player loses
-- 0 means the game is draw
-- 1 means the player wins
create table matches (
	id SERIAL,
	player_id INTEGER references players (id),
	tournament_id INTEGER references tournaments (id),
	i_am_winner SMALLINT,
	primary key (id)
);