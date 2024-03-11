# agilesoftwareprojects

## Setup

Clone repo.

Change into main directory.

Create python virtual environment.

> python -m venv .venv

Activate venv.

> . ./.venv/bin/activate

Install depedencies.

> pip install -r requirements.txt

Change into src directory.

Setup database (every time you need to reset the db).

> flask db init && flask db migrate && flask db upgrade

Run server.

> flask run

Delete database: delete app.db and migrations folder.



