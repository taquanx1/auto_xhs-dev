#!/bin/bash

# ----------------------------
# Configuration Variables
# ----------------------------
APP_DIR="/var/www/conversion_server"             # Deployment directory
REPO_URL="https://github.com/yourusername/conversion_server.git"  # Replace with your repo URL
DOMAIN="conversion.yourdomain.com"               # Domain for your conversion server
EMAIL="your-email@example.com"                   # Email for Certbot notifications

# ----------------------------
# Update System and Install Dependencies
# ----------------------------
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-venv python3-pip git nginx certbot python3-certbot-nginx

# ----------------------------
# Clone or Update the Repository
# ----------------------------
if [ ! -d "$APP_DIR" ]; then
    sudo mkdir -p "$APP_DIR"
    sudo chown $USER:$USER "$APP_DIR"
    git clone $REPO_URL "$APP_DIR"
else
    cd "$APP_DIR" && git pull
fi

# ----------------------------
# Set Up Python Virtual Environment and Install Requirements
# ----------------------------
cd "$APP_DIR"
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# ----------------------------
# Create a systemd Service File for Gunicorn
# ----------------------------
sudo tee /etc/systemd/system/conversion_server.service > /dev/null <<EOF
[Unit]
Description=Gunicorn instance to serve the Conversion Server
After=network.target

[Service]
User=$USER
Group=www-data
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
ExecStart=$APP_DIR/venv/bin/gunicorn --workers 4 --bind unix:$APP_DIR/conversion_server.sock -m 007 conversion_server:app

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and start the service
sudo systemctl daemon-reload
sudo systemctl start conversion_server
sudo systemctl enable conversion_server

# ----------------------------
# Configure Nginx as a Reverse Proxy
# ----------------------------
sudo tee /etc/nginx/sites-available/conversion_server > /dev/null <<EOF
server {
    listen 80;
    server_name $DOMAIN;

    location / {
        include proxy_params;
        proxy_pass http://unix:$APP_DIR/conversion_server.sock;
    }
}
EOF

# Enable the site and test the configuration
sudo ln -s /etc/nginx/sites-available/conversion_server /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl restart nginx

# ----------------------------
# Set Up SSL with Certbot
# ----------------------------
sudo certbot --nginx -d $DOMAIN --non-interactive --agree-tos -m $EMAIL

echo "Deployment complete. Your conversion server is now live at https://$DOMAIN, and SSL auto-renewal is configured."
