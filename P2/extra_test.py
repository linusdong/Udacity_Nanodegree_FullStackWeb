#!/usr/bin/env python
#
# Test cases for tournament.py
#
# Key features (ON GOING)
# 1. Support more than one tournament in the database. (DONE)
# 2. When two players have the same number of wins, rank them according to
#    OMW (Opponent Match Wins), the total number of wins by players they
#    have played against.
# 3. Support games where a draw (tied game) is possible. This will require
#    changing the arguments to reportMatch.
# 4. Dont assume an even number of players. If there is an odd number of
#    players, assign one player a skipped round. A bye counts as a
#    free win. A player should not receive more than one bye in a tournament.

from extra_tournament import *

def testDelete():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    print "1. All records can be deleted."

def testRegister():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    registerTournament(112,"Golf")
    registerPlayer("Chandra Nalaar", 112)
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "2. After registering a player, countPlayers() returns 1."

def testStandingsBeforeMatches():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    registerTournament(112,"Golf")
    registerTournament(223,"Baseball")
    registerPlayer("Melpomene Murray", 112)
    registerPlayer("Randy Schwartz", 223)
    standings = playerStandings(112)
    if len(standings) < 1:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 1:
        raise ValueError("Only registered players in the SAME tournament should appear in standings.")
    [(id1, name1, wins1, matches1,tournament1)] = standings
    if tournament1 != 112:
    	raise ValueError("Only players on #112 tournament, no other players on different tournament")
    print "3. Newly registered players appear in the standings with no matches."

def testReportMatches():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    registerTournament(112,"Golf")
    registerPlayer("Bruno Walton", 112)
    registerPlayer("Boots O'Neal", 112)
    registerPlayer("Cathy Burton", 112)
    registerPlayer("Diane Grant", 112)
    standings = playerStandings(112)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2, 112)
    reportMatch(id3, id4, 112)
    standings = playerStandings(112)
    for (i, n, w, m, t) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
        if t != 112:
            raise ValueError("Matches should in #112 tournament.")
    print "4. After a match, players have updated standings."

def testPairings():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    registerTournament(112,"Golf")
    registerTournament(223,"Baseball")
    registerPlayer("Bruno Walton", 223)
    registerPlayer("Boots O'Neal", 223)
    registerPlayer("Cathy Burton", 223)
    registerPlayer("Diane Grant", 223)
    registerPlayer("Twilight Sparkle", 112)
    registerPlayer("Fluttershy", 112)
    registerPlayer("Applejack", 112)
    registerPlayer("Pinkie Pie", 112)
    standings = playerStandings(112)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2, 112)
    reportMatch(id3, id4, 112)
    standings = playerStandings(223)
    [id1_223, id2_223, id3_223,id4_223] = [row[0] for row in standings]
    reportMatch(id1_223, id2_223, 223)
    reportMatch(id4_223, id3_223, 223)
    pairings = swissPairings(112)
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2,tid1), (pid3, pname3, pid4, pname4,tid1)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "5. After one match, players with one win are paired."


if __name__ == '__main__':
    testDelete()
    testRegister()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    print "Success!  All tests pass!"
