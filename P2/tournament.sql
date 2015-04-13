-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- CLEAR ALL DATA!! psql -f tournament.sql
DROP DATABASE IF EXISTS tournament;

-- Build database from scratch. One tournament at a time. When you want to run
-- a new tournament, all the game records from the previous tournament will
-- need to be deleted.
CREATE DATABASE tournament;

--connect to database
\c tournament

-- player table holds basic information for player. We assume that the number
-- of players in a tournament is an even number. This means that no player
-- will be left out of a round.
create table players (
	p_id SERIAL,
	p_name TEXT,
	primary key (p_id)
);

-- matches holds match_id, winner id and loser id. This table does not support
-- tied game.
create table matches (
	match_id SERIAL,
	w_player_id INTEGER references players (p_id),
	l_player_id INTEGER references players (p_id),
	primary key (match_id, w_player_id)
);

-- view for the total number of the player
create view num_players AS
	select count(*) as num
	from players
	order by num;

-- view for the number of matches each player has won include zero win
create view num_wins AS
	select players.p_id as player_id, count(matches.w_player_id) as wins
	from players left join matches
	on players.p_id = matches.w_player_id
	group by players.p_id
	order by players.p_id;

-- view for the number of matches each player has played include zero match
create view num_matches AS
	select players.p_id as player_id, count(matches.match_id) as matches
	from players left join matches
	on players.p_id = matches.w_player_id
	or players.p_id = matches.l_player_id
	group by players.p_id
	order by players.p_id;

--view for player with total number of wins and mathes, sorted by wins
create view player_standings AS
	select players.p_id as player_id, players.p_name as player_name, num_wins.wins, num_matches.matches
	from num_matches, num_wins, players
	where num_matches.player_id = num_wins.player_id
	and players.p_id = num_matches.player_id
	order by num_wins.wins desc;

--view for swiss_pairings, even number player only
create view swiss_pairings AS
	select a.player_id as player1, a.player_name as player1_name, b.player_id as player2, b.player_name as player2_name
	from player_standings as a, player_standings as b
	where a.matches = b.matches
	and a.wins = b.wins
	and a.player_id < b.player_id;