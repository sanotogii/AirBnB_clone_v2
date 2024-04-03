#!/usr/bin/env bash
# This script sets up web servers for the deployment of web_static.

# Install nginx if not already installed
if ! command -v nginx &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y nginx
fi

# Create necessary directories
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared

# Create fake HTML file
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership to ubuntu user and group recursively
sudo chown -R ubuntu:ubuntu /data/

# Update nginx configuration
config_file="/etc/nginx/sites-available/default"
sudo sed -i '/location \/hbnb_static {/a \        alias /data/web_static/current/;' "$config_file"

# Restart nginx
sudo service nginx restart

exit 0
