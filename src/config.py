from pathlib import Path

basedir = Path(__file__).parent.absolute()

class Config:
	SQLALCHEMY_DATABASE_URI = f'sqlite:///{basedir.joinpath("app.db")}'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SECRET_KEY = 'romidhillon'



