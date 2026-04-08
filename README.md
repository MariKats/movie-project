# Movies API

## Setup

- create a virtual environment:
  `python -m venv .venv`
- activate the virtual environment:
  `source .venv/bin/activate`
- upgrade pip:
  `python -m pip install --upgrade pip`
- install dependencies:
  `pip install -r requirements.txt`

## Database

- seed the SQLite database with:
  `python3 -m app.scripts.populate_db`
- the default database is `sqlite:///./movies.db`.

## Run

- navigate to the backend folder and start the API with uvicorn:
  `uvicorn --reload app.main:app`
