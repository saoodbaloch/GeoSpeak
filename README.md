# GeoSpeak


GeoSpeak is a speech-to-text web application built with Flask and SQLAlchemy.


## Features
- Real-time speech-to-text
- Stores results in a database (SQLAlchemy)
- Simple responsive frontend


## Prerequisites
- Python 3.8+ installed
- (Optional) Node/npm if you have a frontend build


## Local Setup (Windows / Mac/Linux)
1. Clone the repository:
```bash
git clone https://github.com/YOUR-USERNAME/GeoSpeak.git
cd GeoSpeak

Create a virtual environment:
python -m venv venv

Activate virtual environment:
# Windows
venv\Scripts\activate
# Mac / Linux
source venv/bin/activate

Install dependencies:
pip install -r requirements.txt

(Optional) Initialize DB / migrations (if you use Flask-Migrate):
flask db init
flask db migrate -m "Initial"
flask db upgrade

Run the app:
python app.py
# or
export FLASK_APP=app.py
flask run

Open http://127.0.0.1:5000 in your browser.
