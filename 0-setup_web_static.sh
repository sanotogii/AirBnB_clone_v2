#!/usr/bin/env bash
# Install nginx and create folders

if ! command -v nginx &> /dev/null; then
    sudo apt-get update
    sudo apt-get install nginx -y
fi

sudo mkdir -p /data/web_static/releases
sudo mkdir -p /data/web_static/shared
sudo mkdir -p /data/web_static/releases/test

echo '<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>' | sudo tee /data/web_static/releases/test/index.html
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data

config_file="/etc/nginx/sites-available/default"
sudo sed -i '/location \/hbnb_static {/a \        alias /data/web_static/current/;' "$config_file"

sudo service nginx restart
exit 0

