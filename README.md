GeoSpeak (Windows Setup)

GeoSpeak is a speech-to-text web application built with Flask and SQLAlchemy.

Features

Real-time speech-to-text

Stores results in a database (SQLAlchemy)

Simple responsive frontend

Prerequisites

Python 3.8+ installed

(Optional) Node/npm if you have a frontend build

Local Setup (Windows)

Clone the repository:

git clone https://github.com/saoodbaloch/GeoSpeak.git
cd GeoSpeak


Create a virtual environment:

python -m venv venv


Activate the virtual environment (Windows):

venv\Scripts\activate


Install dependencies:

pip install deepl
pip install flask flask-migrate flask-sqlalchemy
pip install -r requirements.txt


Initialize database / migrations (if using Flask-Migrate):

python -m flask db init
python -m flask db migrate -m "Initial"
python -m flask db upgrade


Run the app:

python app.py
# or
python -m flask run


Open in browser:

http://127.0.0.1:5000


💡 Notes for Windows users:

Never type import commands directly in PowerShell; always run them inside Python or a script.

All Flask CLI commands should be prefixed with python -m flask to avoid PATH issues.
