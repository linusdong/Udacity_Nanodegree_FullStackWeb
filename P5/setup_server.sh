#!/bin/bash
# assume current user is root
# create catalog user
externalIP='52.25.92.241'

userName="catalog"
result=$(grep $userName /etc/passwd)
if [[ -z $result ]]; then
    echo 'Adding user $userName'
    adduser catalog
    usermod -a -G admin catalog
else
    echo "User $var has been added to the system. Next step."
fi

# check user if existd
userName="grader"
result=$(grep $userName /etc/passwd)
if [[ -z $result ]]; then
    echo 'Adding user $userName'
    adduser grader
    usermod -a -G admin grader
else
    echo "User $var has been added to the system. Next step."
fi
# update and upgrade the installed packages
apt-get update
apt-get upgrade -y
# update sshd_config
portNumber="Port 2200"
path='/etc/ssh/sshd_config'
result=$(grep -w "^$portNumber" $path)
if [[ -z $result ]]; then
    echo 'Updating sshd_config'
    sed -i 's/Port 22/Port 2200/' $path
    sed -i 's/PermitRootLogin yes/PermitRootLogin no/' $path
    sed -i 's/ChallengeResponseAuthentication yes/ChallengeResponseAuthentication no/' $path
    sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/' $path
    sed -i 's/UsePAM yes/UsePAM no/' $path
else
    echo "$result has been placed. Next step."
fi

# update ufw policy
# https://help.ubuntu.com/community/UFW
ufw allow ntp
ufw allow http
ufw allow 2200
# configure to UTC time
timedatectl set-timezone Europe/London

# Setup database and migration
# install git
apt-get install git
# install apache2, mod_wsgi and PostgreSQL and dependencies
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
su postgres -c 'createdb catalog'
su postgres
psql <<EOF
\c catalog
create user catalog PASSWORD 'udacity';
EOF
# back to root account
exit
# setup database
su catalog
cd ~
git clone https://github.com/linusdong/Udacity_Nanodegree_FullStackWeb.git
path='/home/catalog/Udacity_Nanodegree_FullStackWeb/P5/'
# alter application.py to item_catalog.py
mv $path"application.py" $path"item_catalog.py"
python $path"database_setup.py"
python $path"fill_database.py"

# Setup web application
# copy source files to /var/www
# https://www.digitalocean.com/community/tutorials/how-to-set-up-apache-virtual-hosts-on-ubuntu-14-04-lts
sudo mkdir -p /var/www/catalog
sudo cp -R $path /var/www/catalog
# create wsgi file
sudo cat << EOT > /var/www/catalog/item_catalog.wsgi
import sys
sys.path.insert(0, '/var/www/catalog')
from item_catalog import app as application
EOT
# current user is catalog
sudo chown -R $USER:$USER /var/www/catalog/
# make sure there is no permission error
sudo chmod -R 755 /var/www
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
    <Location /server-status>
         SetHandler server-status
         Order deny,allow
         Deny from all
         Allow from 127.0.0.1
    </Location>
</VirtualHost>
EOT
# enable item_catalog application
sudo a2ensite item_catalog.conf
# reload server to apply the change
sudo service apache2 reload


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

# https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-monit
# https://mmonit.com/wiki/Monit/MonitorApacheStatus
sudo apt-get install -y monit
# configure monit
sudo cat << EOT >> /etc/monit/monitrc
# update email alert
set alert webadmin@foo.bar
# uncomment or update servieces
# setup http deamon
  set httpd port 2812
    use address $externalIP  # only accept connection from localhost
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
    start program = "/etc/init.d/apache2 start" with timeout 60 seconds
    stop program  = "/etc/init.d/apache2 stop"
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
EOT
# check control file syntax and start monit
sudo su
monit -t
monit reload
monit start all






