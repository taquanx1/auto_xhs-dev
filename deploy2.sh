#!/bin/bash

# ----------------------------
# Configuration Variables
# ----------------------------
PROJECT_NAME="XhsCat"             # Deployment directory
SERVER_IP="167.172.91.13"
DOMAIN="xhscat.com"

# Update and install necessary packages
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv supervisor libaugeas0
apt install gunicorn
sudo apt install nginx
sudo apt install certbot python3-certbot-nginx

# Set up a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements.txt
cat requirements.txt | xargs -n 1 pip install

# Set up Certbot
sudo dnf install python3 augeas-libs
sudo pip install certbot
sudo pip install --upgrade yarl

# Set up Supervisor configuration for $PROJECT_NAME
sudo bash -c 'cat << EOF > /etc/supervisor/conf.d/XhsCat.conf
[program:XhsCat]
directory=/root/auto_xhs-dev
command=/root/auto_xhs-dev/venv/bin/gunicorn -w 4 --timeout 1200 -b 0.0.0.0:8000 run_prod:app
autostart=true
autorestart=true
stderr_logfile=/var/log/XhsCat.err.log
stdout_logfile=/var/log/XhsCat.out.log
environment=PATH="/root/auto_xhs-dev/venv/bin",PYTHONPATH="/root/auto_xhs-dev"
EOF'

# Reload Supervisor to apply the new configuration
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start XhsCat

echo "$PROJECT_NAME setup complete and running under Supervisor."


#!/bin/bash

# Backup the original nginx configuration file
sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.bak

# Write the redirect configuration for HTTP to HTTPS
sudo tee /etc/nginx/sites-available/default > /dev/null <<'EOL'
server {
    listen 80;
    server_name 104.248.159.130 xhscat.com;

    # Redirect all HTTP requests to HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name 104.248.159.130 xhscat.com;

    ssl_certificate     /etc/letsencrypt/live/xhscat.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/xhscat.com/privkey.pem;
    client_max_body_size 100M;

    location / {
        # If your app is plain HTTP locally, use http://127.0.0.1:8000
        proxy_pass http://127.0.0.1:8000;

        # now these $… stay intact for Nginx
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_connect_timeout 60s;
        proxy_read_timeout    60s;
        proxy_send_timeout    60s;

        add_header 'Access-Control-Allow-Origin'  '*';
        add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS' always;
        add_header 'Access-Control-Allow-Headers' 'Origin, Content-Type, Accept, Authorization';
        add_header 'Access-Control-Expose-Headers' 'Content-Length' always;

        if ($request_method = 'OPTIONS') {
            add_header 'Access-Control-Allow-Origin'  '*';
            add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
            add_header 'Access-Control-Allow-Headers' 'Origin, Content-Type, Accept, Authorization';
            add_header 'Access-Control-Max-Age' 3600;
            return 204;
        }
    }
}
EOL

# Test the nginx configuration for syntax errors
sudo nginx -t

sudo certbot certonly --standalone -d "$DOMAIN" -d www."$DOMAIN"

# If no errors, reload nginx
if [ $? -eq 0 ]; then
    sudo systemctl reload nginx
    echo "Nginx reloaded successfully. HTTP is now redirected to HTTPS."
else
    echo "Nginx configuration test failed. Check the syntax."
fi