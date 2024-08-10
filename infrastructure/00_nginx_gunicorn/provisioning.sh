#!/usr/bin/env bash
sudo apt update -y
sudo apt upgrade -y
sudo apt install -y \
  python3 \
  python3.12-venv \
  git \
  postgresql-client-common \
  libpq-dev \
  postgresql-client-16 \
  direnv \
  nginx \
  gunicorn
mkdir -p projects
cd projects
git clone https://github.com/ma0c/los30randomdema0-back.git
cd los30randomdema0-back/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure gunicorn
sudo su
touch /etc/systemd/system/gunicorn.socket

cat > /etc/gunicorn/back.los30randomdema0.com.conf <<EOL
SEE back.los30randomdema0.com.conf
EOL

cat > /etc/systemd/system/gunicorn.socket <<EOL
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
EOL

cat > /etc/systemd/system/gunicorn.service <<EOL
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=ubuntu
Group=www-data
EnvironmentFile=/etc/gunicorn/back.los30randomdema0.com.conf
WorkingDirectory=/home/ubuntu/projects/los30randomdema0-back
ExecStart=/home/ubuntu/projects/los30randomdema0-back/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          los30randomdema0.wsgi:application

[Install]
WantedBy=multi-user.target
EOL
exit
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket

sudo systemctl status gunicorn.socket

file /run/gunicorn.sock
sudo journalctl -u gunicorn.socket

# Reload gunicorn
sudo systemctl daemon-reload
sudo systemctl restart gunicorn

cat > /etc/nginx/sites-available/back.los30randomdema0.com <<EOL
server {
    listen 80;
    server_name back.los30randomdema0.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/ubuntu/projects/los30randomdema0-back;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
EOL

sudo ln -s /etc/nginx/sites-available/back.los30randomdema0.com /etc/nginx/sites-enabled/

sudo nginx -t
sudo systemctl restart nginx

sudo usermod -a -G ubuntu www-data
sudo chown -R :www-data /home/ubuntu/projects/los30randomdema0-back/static



# using https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu#step-7-creating-systemd-socket-and-service-files-for-gunicorn