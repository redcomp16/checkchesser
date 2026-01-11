---
title: CheckChesser Backend
emoji: ♟️
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# Setup

## 1. Clone repository:

git clone https://github.com/redcomp16/checkchesser

cd checkchesser

## 2. Setup and run backend (terminal 1):

python -m venv venv

./venv/Scripts/activate

pip install -r requirements.txt

cd backend

python manage.py runserver

## 3. Setup and run frontend (terminal 2):

cd frontend

python -m http.server 5500

## 4. Access app:

Open in browser: http://localhost:5500/Website.html
