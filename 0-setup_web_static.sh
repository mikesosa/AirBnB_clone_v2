#!/usr/bin/env bash
# Sets up the environment and directory for web server deployment
sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y install nginx
sudo mkdir -p /data/
sudo mkdir -p /data/web_static/
sudo mkdir -p /data/web_static/releases/
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/
sudo touch /data/web_static/releases/test/index.html
sudo echo "<html><head>poooop</head>Poop.</html>" | sudo tee -a /data/web_static/releases/test/index.html
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/
sudo sed -i --follow-symlink "29i location /hbnb_static{\nalias /data/web_static/current/;autoindex off;\n}" /etc/nginx/sites-available/default
sudo service nginx restart
