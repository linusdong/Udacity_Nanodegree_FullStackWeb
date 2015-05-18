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

## guide references
1. [configure database](http://www.postgresql.org/docs/9.4/static/auth-pg-hba-conf.html)
1. [configure UFW](https://help.ubuntu.com/community/UFW)
1. [configure apache2](https://www.digitalocean.com/community/tutorials/how-to-set-up-apache-virtual-hosts-on-ubuntu-14-04-lts)
1. [configure Monit](https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-monit)
1. [Monit example](https://mmonit.com/wiki/Monit/MonitorApacheStatus)
