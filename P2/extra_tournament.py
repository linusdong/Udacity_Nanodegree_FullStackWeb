#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteTournaments():
    """Remove all the tournament records from the database."""
    query= '''
    delete from tournaments;
    '''
    db = connect()
    c = db.cursor()
    c.execute(query)
    db.commit()
    db.close()

def deleteMatches():
    """Remove all the match records from the database."""
    query= '''
    delete from matches;
    '''
    db = connect()
    c = db.cursor()
    c.execute(query)
    db.commit()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    query= '''
    delete from players;
    '''
    db = connect()
    c = db.cursor()
    c.execute(query)
    db.commit()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    query= '''
    select * from num_players;
    '''
    db = connect()
    c = db.cursor()
    c.execute(query)
    row = c.fetchone()
    number = row[0]
    db.commit()
    db.close()
    assert number >= 0 # make sure zero or positive number get returned
    return number

def registerTournament(t_id,name):
    """Adds a tournament to the tournament database.
  
    The database assigns a unique serial id number for the tournament.
  
    Args:
      name: the Tournament's full name (need not be unique).
    """
    query = '''
    insert into tournaments (t_id, t_name) values(%s,%s);
    '''
    db = connect()
    c = db.cursor()
    c.execute(query, (t_id,name))
    db.commit()
    db.close()

def registerPlayer(name, tournament_id):
    """Adds a player to the tournament database with tournament_id.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    query = '''
    insert into players (p_name, tournament_id) values(%s,%s);
    '''
    db = connect()
    c = db.cursor()
    c.execute(query, (name,tournament_id))
    db.commit()
    db.close()

def playerStandings(tournament_id):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    query = '''
    select * from player_standings where tournament_id = %s;
    '''
    db = connect()
    c = db.cursor()
    c.execute(query,(tournament_id,))
    standings = c.fetchall()
    db.commit()
    db.close()
    return standings

def reportMatch(winner, loser, tournament_id):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    query = '''
    insert into matches (w_player_id, l_player_id,tournament_id) values(%s,%s,%s);
    '''
    db = connect()
    c = db.cursor()
    c.execute(query, (winner,loser, tournament_id))
    db.commit()
    db.close()
 
def swissPairings(tournament_id):
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    query = '''
    select * from swiss_pairings where tournament_id = %s;
    '''
    db = connect()
    c = db.cursor()
    c.execute(query, (tournament_id,))
    swissPairings = c.fetchall()
    db.commit()
    db.close()
    return swissPairings