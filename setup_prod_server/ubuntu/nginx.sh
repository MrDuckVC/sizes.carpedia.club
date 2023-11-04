# Installing Nginx.

# Install Nginx.
echo "Installing Nginx."
sudo apt update
sudo apt install -y nginx

# Set up site configuration.
echo "Setting up site configuration."
sudo cp ./deploy/ubuntu/nginx.conf /etc/nginx/conf.d/carpedia.conf

# Restart Nginx.
echo "Restarting Nginx."
sudo systemctl restart nginx

# Enable Nginx to start on boot.
echo "Enabling Nginx to start on boot."
sudo systemctl enable nginx

# Install snapd for certbot.
echo "Installing snapd for certbot."
sudo apt install -y snapd

# Remove certbot-auto and any Certbot OS packages if you have them installed.
echo "Removing certbot-auto and any Certbot OS packages if you have them installed."
sudo apt-get remove certbot

# Install certbot.
echo "Installing certbot."
sudo snap install --classic certbot

# Prepare the Certbot command.
echo "Preparing the Certbot command."
sudo ln -s /snap/bin/certbot /usr/bin/certbot

# Choose how you'd like to run Certbot.
echo "Choose how you'd like to run Certbot (nginx)."
sudo certbot --nginx

# Test automatic renewal.
echo "Testing automatic renewal."
sudo certbot renew --dry-run
