# Tournament Results: Getting Started

## Change log
* April 12th 2015, pass all basic test1 to test8.
* April 11th 2015, pass test 1 to test 5.
* April 10th 2015, initial commit.

##How to use the project
1. Make sure you have the VM setup. Check the link here(https://www.udacity.com/wiki/ud197/install-vagrant).
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