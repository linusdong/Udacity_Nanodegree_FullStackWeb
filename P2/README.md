# Tournament Results: Getting Started

## Change log
* April 14th 2015, support multiple tournaments. write test cases for extra credit.
* April 12th 2015, pass all basic test1 to test8.
* April 11th 2015, pass test 1 to test 5.
* April 10th 2015, initial commit.

## Project description
For complete project details, make sure you check out Lesson 5 of the Intro to Relational Databases course, including the [Project Description](https://www.udacity.com/course/viewer#!/c-ud197-nd/l-3521918727/m-3519689284).

## How to use the project
1. Make sure you have the VM setup. Check the link [here](https://www.udacity.com/wiki/ud197/install-vagrant).
2. SSH into VM
3. Inside VM, install git. (If you have git, skip this step)
```bash
sudo apt-get install git
```
* clone the project into VM
```bash
git clone https://github.com/linusdong/Udacity_Nanodegree_FullStackWeb.git
```
* setup database
```bash
psql -f tournament.sql
```
* run test script
```bash
python tournament_test.py
```
* check result
* extra credit database and test script is with "extra_" prefix.

## Extra credit
1. Support more than one tournament in the database.
2. When two players have the same number of wins, rank them according to OMW (Opponent Match Wins), the total number of wins by players they have played against.
3. Support games where a draw (tied game) is possible. This will require changing the arguments to reportMatch.
4. Dont assume an even number of players. If there is an odd number of players, assign one player a skipped round. A bye counts as a free win. A player should not receive more than one bye in a tournament.
