#! /bin/bash

cd /opt/django-community-board
python3.11 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
