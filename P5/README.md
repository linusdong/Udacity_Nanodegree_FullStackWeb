#P5: Linux Server Configuration
The IP for my VM is

```bash
54.191.139.237
```
## Step by step process
1. Launch your Virtual Machine with your Udacity account
1. Follow the instructions provided to SSH into your server
1. Create a new user named grader
1. Give the grader the permission to sudo
1. Update all currently installed packages
1. Change the SSH port from 22 to 2200
1. Configure the Universal Firewall to only allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123)
1. Configure the local timezone to UTC
1. Install and configure Apache to serve a Python mod_wsgi application
1. Install and configure PostgreSQL:
1. Do not allow remote connections
1. Create a new user named catalog that has limited permissions to your catalog application database
1. Install git, clone and setup your Catalog App project (from your GitHub repository from earlier in the Nanodegree program) so that it functions correctly when visiting your server’s IP address in a browser. Remember to set this up appropriately so that your .git directory is not publicly accessible via a browser!

## Step by step guide

```bash
# inside vm
sudo su
useradd grader
visudo
# look for root user, then add the following line after root
grader  ALL=(ALL:ALL) ALL
# Ctrl + x to exit
# press y to save the change
# update and upgrade the installed packages
sudo apt-get update
sudo apt-get upgrade -y
# change ssh port from 22 to 2200
nano /etc/ssh/sshd_config
Port 2200
# reboot machine
reboot
# login using 2200 port via ssh
ssh -i .ssh/udacity_key.rsa root@54.191.139.237 -p2200
# use netstat to check the change
netstat
# update ufw policy
# https://help.ubuntu.com/community/UFW
ufw allow ntp
ufw allow http
ufw allow ssh
ufw allow 2200/udp
ufw allow 2200/tcp
# configure to UTC time
timedatectl set-timezone Europe/London
# install apache2, mod_wsgi and PostgreSQL
apt-get install -y libapache2-mod-wsgi apache2 postgresql
# configure database 
# http://www.postgresql.org/docs/9.4/static/auth-pg-hba-conf.html
# read the Note block after the definition for "host" field 
keep the file as is.
su postgres -c 'createuser -dRS vagrant'
su vagrant -c 'createdb'
su vagrant -c 'createdb forum'
su vagrant -c 'psql forum -f /vagrant/forum/forum.sql'
# configure mod_wsgi and python web applicaiton
# http://flask.pocoo.org/docs/0.10/deploying/mod_wsgi/
```
