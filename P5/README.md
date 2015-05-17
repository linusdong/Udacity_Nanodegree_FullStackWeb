#P5: Linux Server Configuration
The IP for my VM is

```bash
http://52.25.92.241/
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
* setup user and SSH
```bash
# inside vm as root
adduser grader
# password and username is the same
usermod -a -G admin grader
# update and upgrade the installed packages
sudo apt-get update
sudo apt-get upgrade -y
# change ssh port from 22 to 2200
nano /etc/ssh/sshd_config
Port 2200
PermitRootLogin no
AllowUsers catalog grader
# reboot machine
reboot
# login using 2200 port via ssh
ssh -i .ssh/udacity_key.rsa grader@52.25.92.241 -p2200
# use netstat to check the change
netstat
# update ufw policy
# https://help.ubuntu.com/community/UFW
ufw allow ntp
ufw allow http
ufw allow 2200
# configure to UTC time
timedatectl set-timezone Europe/London
```
* Setup database and migration
```bash
# install apache2, mod_wsgi and PostgreSQL and dependencies
sudo su
apt-get install -y libapache2-mod-wsgi apache2 postgresql
apt-get -qqy install postgresql python-psycopg2
apt-get -qqy install python-flask python-sqlalchemy
apt-get -qqy install python-pip
pip install bleach
pip install oauth2client
pip install requests
pip install httplib2
# configure database 
# http://www.postgresql.org/docs/9.4/static/auth-pg-hba-conf.html
# read the Note block after the definition for "host" field, keep the file as is.
sudo su postgres -c 'createdb catalog'
sudo su postgres -c 'psql catalog'
# inside sql env
create user catalog PASSWORD 'udacity';
# setup database
python database_setup.py
python fill_database.py
```
* Setup web application copy source files to /var/www
```bash
# configure mod_wsgi and python web applicaiton
# http://flask.pocoo.org/docs/0.10/deploying/mod_wsgi/
sudo mkdir -p /var/www/catalog
# create wsgi file
sudo cat << EOT > /var/www/catalog/item_catalog.wsgi
import sys
sys.path.insert(0, '/var/www/catalog')
from item_catalog import app as application
EOT
# conf file for wsgi
sudo cat << EOT > /etc/apache2/sites-available/item_catalog.conf
<VirtualHost *:80>
    ServerName 52.25.92.241

    WSGIDaemonProcess item_catalog user=catalog group=admin threads=5
    WSGIScriptAlias / /var/www/catalog/item_catalog.wsgi
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
    Alias /uploads /var/www/catalog/uploads
    <Directory /var/www/catalog>
        WSGIProcessGroup item_catalog
        WSGIApplicationGroup %{GLOBAL}
        Order deny,allow
        Allow from all
    </Directory>
</VirtualHost>
EOT
# enable item_catalog application
sudo a2ensite item_catalog.conf
# reload server to apply the change
sudo service apache2 reload
```
* linux server hardening
```bash
# http://www.rackaid.com/blog/how-to-block-ssh-brute-force-attacks/
/sbin/iptables -I INPUT -p tcp --dport 22 -i eth0 -m state --state NEW -m recent --set
/sbin/iptables -I INPUT -p tcp --dport 22 -i eth0 -m state --state NEW -m recent  --update --seconds 60 --hitcount 4 -j DROP
# manage auto update
sudo cat << EOT > /etc/cron.weekly/autoaupdt
#!/bin/bash
apt-get update
apt-get upgrade -y
apt-get autoclean
EOT
```
* install monitoring applications
```bash
# https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-monit
# https://mmonit.com/wiki/Monit/MonitorApacheStatus
apt-get install monit
# set server status page
sudo nano /etc/apache2/sites-available/item_catalog.conf
# insert the following line inside virtual host
<Location /server-status>
         SetHandler server-status
         Order deny,allow
         Deny from all
         Allow from 127.0.0.1
</Location>
# configure monit
sudo nano /etc/monit/monitrc
# update email alert
set alert webadmin@foo.bar
# uncomment or update servieces
# setup http deamon
  set httpd port 2812
    use address 12.34.56.789  # only accept connection from localhost
    allow 0.0.0.0/0.0.0.0        # allow localhost to connect to the server and
    allow admin:monit      # require user 'admin' with password 'monit'
# set basic system monitor
  check system myhost.mydomain.tld
    if loadavg (1min) > 4 then alert
    if loadavg (5min) > 2 then alert
    if memory usage > 75% then alert
    if swap usage > 25% then alert
    if cpu usage (user) > 70% then alert
    if cpu usage (system) > 30% then alert
    if cpu usage (wait) > 20% then alert
# setup for apache monitor
  check process apache2 with pidfile /var/run/apache2/apache2.pid
    start program = "service apache2 start" with timeout 60 seconds
    stop program  = "service apache2 stop"
    if cpu > 60% for 2 cycles then alert
    if cpu > 80% for 5 cycles then restart
    if totalmem > 200.0 MB for 5 cycles then restart
    if children > 250 then restart
    if loadavg(5min) greater than 10 for 8 cycles then stop
    if failed host www.example.co.uk port 80
          protocol apache-status  dnslimit > 25% or 
                                  loglimit > 80% or 
                                  waitlimit < 20%
          then alert
    group server
# check control file syntax and start monit
monit -t
monit reload
monit start all
```
