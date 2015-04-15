-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- CLEAR ALL DATA!! psql -f tournament.sql
DROP DATABASE IF EXISTS tournament;

-- Build database from scratch. Support multiple tournaments.
CREATE DATABASE tournament;

--connect to database
\c tournament

-- tournaments table hold tournament_id and tournament_name. Support more than
-- one tournament in the database.
create table tournaments (
	t_id INTEGER,
	t_name TEXT,
	primary key (t_id)
);

-- players table holds basic information for player. We assume that the number
-- of players in a tournament is an even number. This means that no player
-- will be left out of a round.
create table players (
	p_id SERIAL,
	p_name TEXT,
	tournament_id INTEGER references tournaments (t_id),
	primary key (p_id)
);

-- matches table holds match_id, winner_id and loser_id. This table does not support
-- tied game.
create table matches (
	match_id SERIAL,
	w_player_id INTEGER references players (p_id),
	l_player_id INTEGER references players (p_id),
	tournament_id INTEGER references tournaments (t_id),
	primary key (match_id, w_player_id)
);

-- view for the total number of the player in each tournament.
create view num_players AS
	select count(*) as num
	from players
	group by tournament_id
	order by num;

-- view for the number of matches each player has won include zero win
create view num_wins AS
	select players.p_id as player_id, count(matches.w_player_id) as wins,
	players.tournament_id as tournament
	from players left join matches
	on players.p_id = matches.w_player_id
	and players.tournament_id = matches.tournament_id
	group by players.p_id
	order by players.p_id;

-- view for the number of matches each player has played include zero match
create view num_matches AS
	select players.p_id as player_id, count(matches.match_id) as matches,
	players.tournament_id as tournament
	from players left join matches
	on (players.p_id = matches.w_player_id
	or players.p_id = matches.l_player_id)
	and players.tournament_id = matches.tournament_id
	group by players.p_id
	order by players.p_id;

--view for player with total number of wins and mathes, sorted by wins
create view player_standings AS
	select players.p_id as player_id, players.p_name as player_name,
	num_wins.wins, num_matches.matches, players.tournament_id
	from num_matches, num_wins, players
	where num_matches.player_id = num_wins.player_id
	and players.p_id = num_matches.player_id
	order by num_wins.wins desc;

--view for swiss_pairings in the same tournament, even number of players only.
create view swiss_pairings AS
	select a.player_id as player1, a.player_name as player1_name,
	b.player_id as player2, b.player_name as player2_name, a.tournament_id as tournament_id
	from player_standings as a, player_standings as b
	where a.matches = b.matches
	and a.wins = b.wins
	and a.tournament_id = b.tournament_id
	and a.player_id < b.player_id;