from enum import unique
import json

from flask_login import UserMixin
from sqlalchemy import event, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash


from app import db, login

@login.user_loader
def load_user(id):
	return User.query.get(id)

# class to represent user table
class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(500), unique=True, index=True)
	password = db.Column(db.String(500))
	name = db.Column(db.String(500))
	reviews = db.relationship('Rating', backref='user')
	usermodules = db.relationship('UserModule', backref='user', lazy='dynamic')

	def set_password(self, password):
		self.password = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password, password)

# class to represent module table
class Module(db.Model):
	code = db.Column(db.String(20), primary_key=True)
	name = db.Column(db.String(100))
	professor = db.Column(db.String(100))
	year = db.Column(db.Integer)
	level = db.Column(db.String(5))
	moduleDescription = db.Column(db.Text)
	assessment = db.Column(db.Text)
	ratings = db.relationship('Rating', backref='module')
	userNotes = db.relationship('UserNotes', backref='module')
	
	
	usermodules = db.relationship('UserModule', backref='module', lazy='dynamic')


# class to represent user module table
class UserModule(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	userId = db.Column(db.Integer, ForeignKey(User.__tablename__ + '.id'), nullable=False)
	moduleCode = db.Column(db.Integer, ForeignKey(Module.__tablename__ + '.code'), nullable=False)
	predicted = db.Column(db.Float)
	actual = db.Column(db.Float)
	year = db.Column(db.Integer)
	slot = db.Column(db.Integer)

# class to represent rating table
class Rating(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	userId = db.Column(db.Integer, ForeignKey(User.__tablename__ + '.id'), nullable=False)
	moduleCode = db.Column(db.Integer, ForeignKey(Module.__tablename__ + '.code'), nullable=False)
	time = db.Column(db.Integer)
	midterm = db.Column(db.Integer)
	final = db.Column(db.Integer)
	lectures = db.Column(db.Integer)
	usefulness = db.Column(db.Integer)
	pros = db.Column(db.Text)
	cons = db.Column(db.Text)
	helpful = db.Column(db.Integer, default= 0)
	nothelpful = db.Column(db.Integer, default= 0)
	created_on = db.Column(db.DateTime, server_default=db.func.now())

# class to represent user notes table
class UserNotes(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	userId = db.Column(db.Integer, ForeignKey(User.__tablename__ + '.id'), nullable=False)
	moduleCode = db.Column(db.Integer, ForeignKey(Module.__tablename__ + '.code'), nullable=False)
	title = db.Column(db.String(500))
	content = db.Column(db.Text)

	



