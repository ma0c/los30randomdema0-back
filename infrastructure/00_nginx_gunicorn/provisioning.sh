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