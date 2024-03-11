from ast import walk
from datetime import date, timedelta
import json
from operator import itemgetter, mod
import os
import random
from flask import redirect, render_template, request, session, url_for, flash
from app.models import Module, Rating, User, UserModule, UserNotes
from flask_login import login_required, logout_user, current_user
from ..main import bp
from app import db, login
from flask import send_file



# route for main page
@bp.route('/main')
@login_required
def main():
	mods = Module.query.all()
	userId = current_user.id
	allReviews = Rating.query.all()
	myreviews = Rating.query.filter_by(userId=userId)

	modules = []

	for mod in mods:
		ratings = getRating(mod.ratings)
		overallAvg = (ratings['time']['count'] + ratings['midterm']['count'] + ratings['final']['count'] + ratings['lecture']['count']  + ratings['usefulness']['count'])/5
		if(ratings['time']['count'] != 0):
			modules.append({'module' : mod, 'rating' : ratings, 'overallAvg' : overallAvg})

	newlist = sorted(modules, key=itemgetter('overallAvg'), reverse=True) 


	return render_template('main/dashboard.html', allmodules = mods ,modules = newlist, myreviews = myreviews, allReviews = allReviews)

# route for logout page
@bp.route('/logout')
@login_required
def logout():
	logout_user()
	if session.get('was_once_logged_in'):
		# prevent flashing automatically logged out message
		del session['was_once_logged_in']
	return redirect(url_for('main.main'))

# route for modules page
@bp.route('/modules')
@login_required
def modules():
	mods = Module.query.all()
	modules = []
	for mod in mods:
		ratings = getRating(mod.ratings)
		overallAvg = (ratings['time']['avg'] + ratings['midterm']['avg'] + ratings['final']['avg'] + ratings['lecture']['avg']  + ratings['usefulness']['avg'])/5
		modules.append({'module' : mod, 'rating' : ratings, 'overallAvg' : overallAvg})

	newlist = sorted(modules, key=itemgetter('overallAvg'), reverse=True) 
	return render_template('main/modules.html', modules = modules)


# route for module page
@bp.route('/module/<id>', methods=['GET'])
@login_required
def module(id):
	mod = Module.query.get(id)
	ratings = getRating(mod.ratings)
	userIdd = current_user.id
	allRatings = Rating.query.filter(Rating.userId!=userIdd, Rating.moduleCode == id).all()
	myRatings = Rating.query.filter_by(userId=userIdd, moduleCode = id).all()
	return render_template('main/module.html', module = mod, allRatings = myRatings + allRatings, ratings = ratings, myRatings = myRatings)

# function for get rating
def getRating(rating):
	timeTotal = 0
	midtermTotal = 0
	finalTotal = 0
	lecturesTotal = 0
	usefulnessTotal = 0
	count = 0
	for rat in rating:
		timeTotal = timeTotal + rat.time
		midtermTotal = midtermTotal + rat.midterm
		finalTotal = finalTotal + rat.final
		lecturesTotal = lecturesTotal + rat.lectures
		usefulnessTotal = usefulnessTotal + rat.usefulness
		count = count + 1

	if(count == 0):
		return {"time" : {'count': 0, 'avg' : 0}, "midterm" : {'count': 0, 'avg' : 0}, "final" : {'count': 0, 'avg' : 0}, "lecture" : {'count': 0, 'avg' : 0}, "usefulness" : {'count': 0, 'avg' : 0}}
	else:
		return {"time" : {'count': count, 'avg' : timeTotal/count}, "midterm" : {'count': count, 'avg' : midtermTotal/count}, "final" : {'count': count, 'avg' : finalTotal/count}, "lecture" : {'count': count, 'avg' : lecturesTotal/count}, "usefulness" : {'count': count, 'avg' : usefulnessTotal/count}}
	


# route for module POST method
@bp.route('/module/<id>', methods=['POST'])
@login_required
def addReview(id):
	data = request.form
	userId = current_user.id
	ratings = Rating(userId = userId, moduleCode = id, time = data['time'], midterm = data['midterm'], final = data['final'], lectures = data['lectures'], usefulness = data['usefullness'], pros = data['pros'], cons = data['cons'])
	db.session.add(ratings)
	db.session.commit()
	flash('Review Added Successfully.')
	return redirect('/module/' + id)

# route for rating delete post method
@bp.route('/rating/<id>/delete', methods=['POST'])
@login_required
def deleteReview(id):
	rat = Rating.query.get(id)
	moduleCode = rat.moduleCode
	db.session.delete(rat)
	db.session.commit()
	flash('Review Deleted Successfully.')
	return redirect('/main')

# route for degree planner
@bp.route('/degree-planner')
@login_required
def degree():
	year1Modules = Module.query.filter_by(year = 1).all()
	year2Modules = Module.query.filter_by(year = 2).all()
	year3Modules = Module.query.filter_by(year = 3).all()

	usermodules = current_user.usermodules

	prdCount = 0
	actCount = 0
	prdSum = 0
	actSum = 0

	for um in usermodules:
		if um.predicted >= 0:
			prdCount += 1
			prdSum += um.predicted
		if um.actual >= 0:
			actCount += 1
			actSum += um.actual

	data = {
		'actualAvg' : actSum / actCount if actCount else '',
		'manualPredicted':prdSum/prdCount if prdCount else '',
		'modulesRemaining': 24 - usermodules.count()
	}

	allModules = [
		{'year': 1, 'mods' : year1Modules},
		{'year': 2, 'mods' : year2Modules},
		{'year': 3, 'mods' : year3Modules}
	]

	selections = {1: {}, 2: {}, 3: {}}
	for um in usermodules:
		selections[um.year][um.slot] = um

	return render_template('main/degree.html', modules = allModules, data = data, selections = selections)

# route for degree planner post method
@bp.route('/degree-planner', methods=['POST'])
@login_required
def degreePost():

	formdata = request.form

	current_user.usermodules.delete()
	db.session.commit()

	for mod in [1, 2, 3]:
		for i in range(0,8):
			moduleCode = formdata['mod' + str(mod) + str(i)]
			if moduleCode == "Select":
				continue

			predicted = formdata['pred' + str(mod) + str(i)]
			if predicted == "":
				predicted = -1

			actual = formdata['act' + str(mod) + str(i)]
			if actual == "":
				actual = -1

			db.session.add(UserModule(user=current_user, moduleCode=moduleCode, year=mod, slot=i, predicted=predicted, actual=actual))
	
	db.session.commit()

	return redirect(url_for('main.degree'))


# routes for resources page
@bp.route('/resources')
def resources():
	mods = Module.query.all()
	return render_template('main/resources.html', modules = mods)



@bp.route('/module/resources/<id>')
@login_required
def viewResources(id):
	mod = Module.query.get(id)
	files = []
	try:
		for file in os.listdir("contents\\"+ mod.code):
			f = open("contents\\"+ mod.code+ "\\" + file, "r")
			data = f.read()
			dataArr = data.split("~~~")
			print(dataArr)

			files.append({'name': file.split('.')[0], 'link' : dataArr[0], 'detail' : dataArr[1]})

	except:
		print("An exception occurred")

	return render_template('main/view-resources.html', module = mod, files = files)


@bp.route('/module/<id>/resources/<resourceName>')
def downloadFile (id, resourceName):
    path = "../contents/"+id+"/" + resourceName
    return send_file(path, as_attachment=True)


@bp.route('/module/resources/<id>', methods=['POST'])
@login_required
def psotNote(id):
	formdata = request.form
	userId = current_user.id
	note = UserNotes(userId = userId, moduleCode = id, title = formdata['title'], content = formdata['content'])
	db.session.add(note)
	db.session.commit()
	flash('Added Successfully.')

	return redirect('/module/resources/' + id)


@bp.route('/module/resources/<modCode>/delete/<id>', methods=['GET'])
def deleteNode(modCode, id):
	note = UserNotes.query.get(id)
	db.session.delete(note)
	db.session.commit()
	flash('Deleted Successfully.')

	return redirect('/module/resources/' + modCode)