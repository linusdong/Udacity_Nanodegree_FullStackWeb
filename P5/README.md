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

## How to use the project.
```bash
bash setup_server.sh
sudo reboot
```
## Extra credits
### Firewall setup
The firewall has been configured to monitor for repeat unsuccessful login attempts and appropriately ban attackers.
```bash
tail /var/log/ufw.log
May 19 01:33:17 ip-10-20-47-247 kernel: [ 8760.564705] [UFW BLOCK] IN=eth0 OUT= MAC=06:4b:df:ce:28:a5:06:76:02:0a:47:92:08:00 SRC=93.174.93.114 DST=10.20.47.247 LEN=40 TOS=0x00 PREC=0x00 TTL=237 ID=22957 PROTO=TCP SPT=55748 DPT=22 WINDOW=1024 RES=0x00 SYN URGP=0 
May 19 01:46:42 ip-10-20-47-247 kernel: [ 9564.815287] [UFW BLOCK] IN=eth0 OUT= MAC=06:4b:df:ce:28:a5:06:76:02:0a:47:92:08:00 SRC=43.255.188.134 DST=10.20.47.247 LEN=40 TOS=0x08 PREC=0x20 TTL=239 ID=54321 PROTO=TCP SPT=56308 DPT=22 WINDOW=65535 RES=0x00 SYN URGP=0 
May 19 02:02:07 ip-10-20-47-247 kernel: [10490.376880] [UFW BLOCK] IN=eth0 OUT= MAC=06:4b:df:ce:28:a5:06:76:02:0a:47:92:08:00 SRC=222.186.34.200 DST=10.20.47.247 LEN=40 TOS=0x00 PREC=0x00 TTL=98 ID=256 PROTO=TCP SPT=6000 DPT=22 WINDOW=16384 RES=0x00 SYN URGP=0 
May 19 02:23:19 ip-10-20-47-247 kernel: [   64.813718] [UFW BLOCK] IN=eth0 OUT= MAC=06:4b:df:ce:28:a5:06:76:02:0a:47:92:08:00 SRC=185.2.101.170 DST=10.20.47.247 LEN=40 TOS=0x00 PREC=0x00 TTL=238 ID=54321 PROTO=TCP SPT=43452 DPT=22 WINDOW=65535 RES=0x00 SYN URGP=0

less /etc/ufw/before.rules
# all other non-local packets are dropped, except ufw allowed packets
-A ufw-not-local -m limit --limit 3/min --limit-burst 10 -j ufw-logging-deny
-A ufw-not-local -j DROP
```
### Monitoring application
The VM includes monitoring applications that provide automated feedback on application availability status and/or system security alerts.
```bash
# https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-monit
# https://mmonit.com/wiki/Monit/MonitorApacheStatus
apt-get install -y monit sendmail
# configure monit
cat << EOT >> /etc/monit/monitrc
# update email alert
  set alert $email
# setup mail server
  set mailserver localhost                   # fallback relay
                 
# uncomment or update servieces
# setup http deamon
  set httpd port 2812
    use address $externalIP  # only accept connection from localhost
    allow 0.0.0.0/0.0.0.0        # allow localhost to connect to the server and
    allow admin:monit      # require user 'admin' with password 'monit'
# set basic system monitor
  check system localhost
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
    if failed host localhost port 80
          protocol apache-status  dnslimit > 25% or 
                                  loglimit > 80% or 
                                  waitlimit < 20%
          then alert
    group server
EOT
# check control file syntax and start monit
monit -t
monit reload
monit start all
```
### Configuration File Comments
Comments are thorough and concise. Code is self documenting.
## guide references
1. [configure database](http://www.postgresql.org/docs/9.4/static/auth-pg-hba-conf.html)
1. [configure UFW](https://help.ubuntu.com/community/UFW)
1. [configure apache2](https://www.digitalocean.com/community/tutorials/how-to-set-up-apache-virtual-hosts-on-ubuntu-14-04-lts)
1. [configure Monit](https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-monit)
1. [Monit example](https://mmonit.com/wiki/Monit/MonitorApacheStatus)
