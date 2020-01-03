#!/usr/bin/env bash
# code that automatically installs "engine x" and inserts a string in the site
# install nginx if not installed
sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y install nginx
sudo ufw allow 'Nginx HTTP'
# Create a folder
sudo mkdir -p /data/
sudo mkdir -p /data/web_static/
sudo mkdir -p /data/web_static/releases/
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/
sudo echo "<h1>Holberton School! :)</h1>" | sudo tee -a /data/web_static/releases/test/index.html
sudo ln -sfn /data/web_static/releases/test/ /data/web_static/current
# Checkers dont pass the next two lines so I had to do it in one
#sudo chown -R ubuntu /data/
#sudo chown -R :ubuntu /data/
sudo chown -R ubuntu:ubuntu /data/
sudo sed -i "17i \\\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t\tautoindex off;\n\t}\n" /etc/nginx/sites-available/default
sudo service nginx restart
