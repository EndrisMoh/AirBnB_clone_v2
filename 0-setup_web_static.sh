#!/usr/bin/env bash
# A Bash script that sets up your web servers for the deployment of `web_static`

# Installing nginx
sudo apt-get -y update
sudo apt-get -y install nginx
sudo service nginx start

# Configuring file system or folders
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/
echo "Holberton School" | sudo tee /data/web_static/releases/test/index.html > /dev/null
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Setting permissions
sudo chown -R ubuntu:ubuntu /data/

# Configuring nginx
sudo sed -i '44i \\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}' /etc/nginx/sites-available/default

# Restart web server
sudo service nginx restart
