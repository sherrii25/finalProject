from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# login
# mail

from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'public.sign_in'
login.login_message = 'You are not authorized to access this page, please log in.'


def create_app():
	app = Flask(__name__)
	app.config.from_object(Config)

	db.init_app(app)
	migrate.init_app(app, db)
	login.init_app(app)

	# register blueprints

	from app.blueprints import main, public

	app.register_blueprint(main.bp)
	app.register_blueprint(public.bp)


	return app





