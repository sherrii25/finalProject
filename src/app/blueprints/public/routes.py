from operator import itemgetter
from flask import flash, redirect, render_template, url_for
from itsdangerous import Serializer, SignatureExpired, URLSafeTimedSerializer
from app.blueprints.main.routes import getRating
from flask_login import login_user
from app import db
from app.models import Module, User
from app.blueprints.public import bp
from app.blueprints.public.forms import ForgotForm, ResetForm, SignUpForm, SignInForm
from flask import Flask
from flask_mail import Mail, Message


SECRET = 'NK87KJ8KJ9GTHCJEUYRJ83457J89KDSFJDSIOFJ5674G65DF4G65DF4G5DF'

# function to insert data into chosen pages
def insertData():
	db.session.add(Module(code='CM1005', name='Introduction to Programming I', professor = 'Dr. Edward Anstead & Dr. Simon Katan', year = 1, level="4", moduleDescription="This module teaches basics of computer programming such as variables, conditionals, loops, functions and objects.", assessment="Coursework only (Type II)"))
	db.session.add(Module(code='CM1010', name='Introduction to Programming II', professor = 'Dr. Edward Anstead & Dr. Simon Katan', year = 1, level="4", moduleDescription="This module builds upon computer programming skills by teaching code maintainability, defensive coding, program testing, encapsulation and third-party libraries.", assessment="Coursework only (Type III)"))
	db.session.add(Module(code='CM1015', name='Computational Mathematics', professor = 'Dr. Sarah Santos', year = 1, level="4", moduleDescription="This module teaches computational mathematical tools such as number systems, special functions, graphing and linear algebra.", assessment="One two hour unseen written examination and coursework (Type I)"))
	db.session.add(Module(code='CM1020', name='Discrete Mathematics', professor = 'Dr. Lahcen Ouarbya & Dr. Abdelkrim Alfalah', year = 1, level="4", moduleDescription="This module teaches discrete mathematical tools such as sets, Boolean algebra, logic, functions, relations, graphs and counting.", assessment="One two hour unseen written examination and coursework (Type I)"))
	db.session.add(Module(code='CM1030', name='How Computers Work', professor = 'Dr. Marco Gillies', year = 1, level="4", moduleDescription="This module introduces the fundamental concepts of Notational Machine, computer system architectures, networking and databases.", assessment="One two hour unseen written examination and coursework (Type I)"))
	db.session.add(Module(code='CM1025', name='Fundamentals of Computer Science', professor = 'Dr. Golnaz Badkobeh', year = 1, level="4", moduleDescription="This module teaches fundamental concepts in computer science such as binary representations, complexity, finite state machines, languages and grammar.", assessment="One two hour unseen written examination and coursework (Type I)"))
	db.session.add(Module(code='CM1040', name='Web Development', professor = 'Dr. Nick Hine', year = 1, level="4", moduleDescription="This module teaches web development skills by introducing HTML, CSS and JavaScript.", assessment="Coursework only (Type III)"))
	db.session.add(Module(code='CM1035', name='Algorithm and Data Structures I', professor = 'Dr. Matty Hoban', year = 1, level="4", moduleDescription="This module teaches algorithm and data structure concepts such as arrays, vectors, lists, flowcharts, iteration and recursion.", assessment="One two hour unseen written examination and coursework (Type I)"))

	db.session.add(Module(code='CM2005', name='Object Oriented Programming', professor = 'Dr. Matthew Yee-King', year = 2, level="5", moduleDescription="This module teaches practical object-oriented programming concepts such as object interfaces, inheritance, abstraction and polymorphism.", assessment="Coursework only (Type II)"))
	db.session.add(Module(code='CM2010', name='Software Design and Development', professor = 'Dr. Matthew Yee-King', year = 2, level="5", moduleDescription="This module teaches software development skills such as version control, exception handling, defensive coding, module coupling, cohesion and unit testing.", assessment="One two hour unseen written examination and coursework (Type I)"))
	db.session.add(Module(code='CM2040', name='Database Networks and the Web', professor = 'Dr. Elaheh Homayounvala', year = 2, level="5", moduleDescription="This module teaches relational data modelling, database implementations in SQL, query processing and socket architectures.", assessment="One two hour unseen written examination and coursework (Type I)"))
	db.session.add(Module(code='CM2020', name='Agile Software Projects', professor = 'Dr. Sean McGrath', year = 2, level="5", moduleDescription="This module teaches software development methods such as project management, market research, requirements gathering, prototyping, agile development, testing, validation and documentation.", assessment="Coursework only (Type III)"))
	db.session.add(Module(code='CM2025', name='Computer Security', professor = 'Dr. Matthew Yee-King & Dr. Robert Zimmer', year = 2, level="5", moduleDescription="This module teaches both the theory and practice of computer security by introducing mathematical underpinnings of cryptography as well as security design.", assessment="One two hour unseen written examination and coursework (Type I)"))
	db.session.add(Module(code='CM2030', name='Graphics Programming', professor = 'Dr. Theo Papatheodorou', year = 2, level="5", moduleDescription="This module teaches graphical programming concepts such as graphics synthesis, processing, representation, handling and manipulation.", assessment="Coursework only (Type II)"))
	db.session.add(Module(code='CM2035', name='Algorithm and Data Structures II', professor = 'Dr. Alejandra Beghelli Zapata', year = 2, level="5", moduleDescription="This module builds upon algorithm and data structure concepts by teaching trees, heaps, maps, stacks, queues, graphs and big-O notation.", assessment="One two hour unseen written examination and coursework (Type I)"))
	db.session.add(Module(code='CM2015', name='Programming with Data', professor = 'Dr. Sean McGrath', year = 2, level="5", moduleDescription="This module teaches data science skills such as data acquisition, manipulation, visualisation, classification and clustering.", assessment="One two hour unseen written examination and coursework (Type I)"))

	db.session.add(Module(code='CM3005', name='Data Science', professor = 'Dr. Tony Russel-Rose', year = 3, level="6", moduleDescription="This module teaches data science methods such as correlation, regression, distributions, significance and data visualisations.", assessment="One two-hour unseen written examination and coursework (Type I)"))
	db.session.add(Module(code='CM3010', name='Database and Advanced Data Techniques', professor = 'Dr. David Lewis', year = 3, level="6", moduleDescription="This module teaches advanced data manipulation concepts including data gathering, cleaning, advanced SQL skills, NoSQL, data pipelines and data security.", assessment="One two-hour unseen written examination and coursework (Type I)"))
	db.session.add(Module(code='CM3015', name='Machine Learning and Neural Networks', professor = 'Dr. Jamie Ward & Dr. Tim Blackwell', year = 3, level="6", moduleDescription="This module teaches concepts of machine learning and neural networks including regression, classification, supervised and unsupervised clustering, evaluation, dimensional reduction, multi-layer perceptrons, back propagation, network optimisers, deep and recurrent networks.", assessment="Coursework only (Type II)"))
	db.session.add(Module(code='CM3020', name='Artificial Inteligence', professor = 'Dr. Larisa Soldatova & Dr. Matthew Yee-King', year = 3, level="6", moduleDescription="This module teaches fundamentals of Artificial Intelligence such as agents, environments, ontologies, optimal decisions in games and robotics.", assessment="One two-hour unseen written examination and coursework (Type I)"))
	db.session.add(Module(code='CM3025', name='Virtual Reality', professor = 'Dr. Marco Gillies & Dr. Sylvia Pan', year = 3, level="6", moduleDescription="This module teaches practical virtual reality development concepts such as VR-related 3D graphics, immersive sound, interaction design, navigation, object interaction and physics.", assessment="Coursework only (Type III)"))
	db.session.add(Module(code='CM3030', name='Games Developement', professor = 'Dr. Tom Cole', year = 3, level="6", moduleDescription="This module teaches practical game development concepts such as game engines, prototyping, playtesting, virtual AI agents, state machines, pathfinding and behaviour trees.", assessment="Coursework only (Type III)"))
	db.session.add(Module(code='CM3035', name='Advanced Web Developement', professor = 'Dr. Daniel Buchan', year = 3, level="6", moduleDescription="This module teaches advanced web development methods using databases, front-end frameworks and server-side programming.", assessment="Coursework only (Type II)"))
	db.session.add(Module(code='CM3040', name='Physical Computing and Internet of Things', professor = 'Dr. Darpan Triboan', year = 3, level="6", moduleDescription="This module teaches programming hardware that interacts with its environment by utilising circuits, microcontrollers, sensors, motos, actuators and physical interaction design.", assessment="Coursework only (Type III)"))
	db.session.add(Module(code='CM3045', name='3D Graphics and Animation', professor = 'Dr. Marco Gillies & Dr. Sylvia Pan', year = 3, level="6", moduleDescription="This module teaches advanced graphics and animation programming techniques such as 3D transformations, keyframe and character animation, rendering, lighting, texturing, vertex and fragment shaders.", assessment="One two hour unseen written examination and coursework (Type I)"))
	db.session.add(Module(code='CM3050', name='Mobile Development', professor = 'Joe McAlister', year = 3, level="6", moduleDescription="This module teaches mobile application development skills such as user interface design, cloud service integration, sensor programming, advanced APIs and deployment.", assessment="Coursework only (Type III)"))
	db.session.add(Module(code='CM3055', name='Interaction Design', professor = 'Dr. Sarah Wiseman & Dr. Sean McGrath', year = 3, level="6", moduleDescription="This module teaches user experience design and production concepts such as specification, design, prototyping and evaluation of user interfaces including case studies.", assessment="One two-hour unseen written examination and coursework (Type I)"))
	db.session.add(Module(code='CM3060', name='Natural Language Processing', professor = 'Dr. Tony Russel-Rose', year = 3, level="6", moduleDescription="This module teaches natural language processing concepts such as information retrieval, curation, formal grammars, rule based and statistical natural language processing, named entity recognition, readers, stemmers, taggers and parsers.", assessment="One two-hour unseen written examination and coursework (Type I)"))
	db.session.add(Module(code='CM3065', name='Intelligent Signal Processing', professor = 'Dr. Francisco Marti Perez', year = 3, level="6", moduleDescription="This module teaches digital signal processing techniques such as signal capturing, processing, time and frequency domain representations and processing.", assessment="Coursework only (Type II)"))
	db.session.commit()


# route for home page
@bp.route('/')
def home():
	mods = Module.query.all()
	if(len(mods) == 0):
		insertData()
	return render_template('public/home.html')


# route for sign-up page
@bp.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
	form = SignUpForm()

	# if form.password.data != form.password_confirm.data:
	# 	flash('Password and Confirm Password do not match')
	# 	return render_template('public/sign-up.html', form=form)

	if form.validate_on_submit():
		user = User(
			email=form.email.data,
			name=form.name.data
		)
		user.set_password(form.password.data)

		db.session.add(user)
		db.session.commit()

		flash('User sign up successful.')

		return redirect(url_for('public.sign_in'))


	return render_template('public/sign-up.html', form=form)


# route for sign-in page
@bp.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
	form = SignInForm()

	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		
		if not user:
			flash('Email or password is incorrect.')
			return redirect(url_for('public.sign_in'))

		if user.check_password(form.password.data):
			login_user(user)
			flash('Signed in successfully.')
			return redirect(url_for('main.main'))
		else:
			flash('Email or password is incorrect.')
			return redirect(url_for('public.sign_in'))

	return render_template('public/sign-in.html', form=form)

# route for forgot password page
@bp.route('/forgot-password', methods=['GET', 'POST'])
def forgotPassword():
	form = ForgotForm()

	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		
		if not user:
			flash('No User found with this email.')
			return redirect(url_for('public.forgotPassword'))
		else:
			
			app = Flask(__name__)
			app.config['MAIL_SERVER']='mail.privateemail.com'
			app.config['MAIL_PORT'] = 587
			app.config['MAIL_USERNAME'] = 'user@romidhillon.com'
			app.config['MAIL_PASSWORD'] = 'password12345'
			app.config['MAIL_USE_TLS'] = True
			app.config['MAIL_USE_SSL'] = False

			mail = Mail(app)


			msg = Message('Reset Your Password', sender = 'user@romidhillon.com', recipients = [form.email.data])
			token = get_reset_token(user.id)
			msg.body = f'''Go to link Below to reset your passwrod:\n{url_for('public.reset_passwrod', token=token, _external=True)}">'''
			mail.send(msg)
			flash('Link Sent to your Registered Email Address.')
			return redirect(url_for('public.sign_in'))

	return render_template('public/forgot.html', form=form)

# route for reset password
@bp.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_passwrod(token):
	user = verify_reset_token(token)
	if user is None:
		flash('This is an invalid or expired token', 'alert-warning')  
		return redirect(url_for('public.forgotPassword'))  

	form = ResetForm()
	if form.validate_on_submit():
		app = Flask(__name__)
		user.set_password(form.password.data)
		db.session.commit()
		flash('Your password has been updated', 'alert-success')
		return redirect(url_for('public.sign_in'))
	return render_template('public/reset.html', form=form)
		


# route for ratings page
@bp.route('/ratings', methods=['GET'])
def ratings():
	mods = Module.query.all()
	modules = []
	for mod in mods:
		ratings = getRating(mod.ratings)
		overallAvg = (ratings['time']['avg'] + ratings['midterm']['avg'] + ratings['final']['avg'] + ratings['lecture']['avg']  + ratings['usefulness']['avg'])/5
		modules.append({'module' : mod, 'rating' : ratings, 'overallAvg' : overallAvg})

	newlist = sorted(modules, key=itemgetter('overallAvg'), reverse=True) 
	return render_template('public/modules.html', modules = modules)

# function to reset token
def get_reset_token(userid, expire_sec=1800):
          s = URLSafeTimedSerializer('Thisisasecret!')
          return s.dumps({'user_id':userid})

# function to verify token
def verify_reset_token(token):
          s = URLSafeTimedSerializer('Thisisasecret!')
          try:
               user_id = s.loads(token)['user_id']  
          except:
               return None
          return User.query.get(user_id)







