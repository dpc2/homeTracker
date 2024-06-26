import sqlite3
import os
import re
from os.path import dirname, join
import datetime as dt
from datetime import datetime
from werkzeug.utils import secure_filename
import subprocess
from flask import (
	Flask, render_template,
	request, url_for, flash, redirect,
	send_from_directory
)


app = Flask(__name__)
app.secret_key = os.urandom(12)

# Picture upload configurations
currentDir = dirname(__file__)
imagePath = join(currentDir, "static/images/")
ALLOWED_EXTENSIONS = {'jpg','jpeg'}
app.add_url_rule(
	"/<string:plantName>/upload/", endpoint="upload", build_only=True
)


def get_db_connection():
	conn = sqlite3.connect('database.db')
	conn.row_factory = sqlite3.Row
	return conn

def get_plant(plantName, source):
	conn = get_db_connection()

	if source == "plantTracker" or source == "treeTracker":
		plant = conn.execute('SELECT * FROM plants WHERE name = ?', (plantName,)).fetchone()
	elif source == "gardenTracker":
		plant = conn.execute('SELECT * FROM garden WHERE name = ?', (plantName,)).fetchone()
	conn.close()
	#if plant is None:
	#	abort(404)
	return plant

def get_garden(plantName):
	conn = get_db_connection()
	gardenPlant = conn.execute('SELECT * FROM garden WHERE name = ?', (plantName,)).fetchone()
	conn.close()
	#if plant is None:
	#	abort(404)
	return gardenPlant

def allowed_file(filename):
        return '.' in filename and \
                filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#------------------------------------#
#				Index
#------------------------------------#

@app.route('/')
def index():

	return render_template('index.html')

#------------------------------------#
#	 	Plant Tracker Routes
#------------------------------------#

@app.route('/plantTracker')
def plantTracker():
	today = dt.datetime.now()
	conn = get_db_connection()
	plants = conn.execute('SELECT * FROM plants WHERE type = "housePlant" ORDER BY name').fetchall()
	thirstyToday = conn.execute('SELECT * FROM plants WHERE remaining < 1 AND type = "housePlant" ORDER BY name').fetchall()
	conn.close()

	# Initializing variable, program breaks if there are no thirsty plants and this is not set to 0
	itsBeen = 0

	for item in thirstyToday:
		lastWatered = dt.datetime.strptime(item[2], '%Y-%m-%d')
		print(lastWatered)
		delta = int(item[3])
		deltaDays = today - lastWatered
		itsBeen = deltaDays.days

		#print(item[1] + " was last watered on " + item[2])
		#print("That means it has been " + str(itsBeen) + " days." + "\n") 

	return render_template('plantTracker.html', thirstyToday=thirstyToday, plants=plants, itsBeen=itsBeen)


@app.route('/addNew/', methods=('GET', 'POST'))
def addNew():
	if request.method == 'POST':
		name = request.form['name']
		lastWatered = request.form['lastWatered']
		dryOut = request.form['dryOut']
		type = request.form['type']

		print(name + " " + type)

		if not name:
			flash('Name is required!')
		elif not lastWatered:
			flash('Date last watered is required!')
		elif not dryOut:
			flash('Dry out duration is required!')
		else:
			conn = get_db_connection()
			conn.execute('INSERT INTO plants (name, lastWatered, dryOut, type) VALUES (?, ?, ?, ?)',
				(name, lastWatered, dryOut, type))
			conn.commit()
			conn.close()
			return redirect(url_for('plantTracker'))

	return render_template('addNew.html')

#'/<string:devID>:<string:type>/delete/'


@app.route('/<string:plantName>:<string:source>/wateredToday/', methods=('POST',))
def wateredToday(plantName, source):
	thisPlant = get_plant(plantName, source)
	conn = get_db_connection()
	temp = dt.datetime.now()

	print(thisPlant['dryOut'])
	print(plantName)
	print(source)

	today = temp.strftime('%Y-%m-%d')

	if source == "plantTracker" or source == "treeTracker":
		conn.execute('UPDATE plants SET lastWatered = ? WHERE name = ?', (today, plantName))
		conn.execute('UPDATE plants SET remaining = ? WHERE name = ?', (thisPlant['dryOut'], plantName))
	elif source == "gardenTracker":
                conn.execute('UPDATE garden SET lastWatered = ? WHERE name = ?', (today, plantName))
                conn.execute('UPDATE garden SET remaining = ? WHERE name = ?', (thisPlant['dryOut'], plantName))
	conn.commit()
	conn.close()
	#flash('"{}" was watered today!'.format(plant['name']))

	if source == "plantTracker":
		return redirect(url_for('plantTracker'))
	elif source == "gardenTracker":
		return redirect(url_for('gardenTracker'))
	elif source == "treeTracker":
		return redirect(url_for('treeTracker'))

@app.route('/<string:plantName>:<string:source>/viewPics/', methods=('GET',))
def viewPics(plantName, source):
	plant = get_plant(plantName, source)

	plantName = plantName.replace(' ','')
	print(plantName)
	fullPath = imagePath + plantName

	imgList = sorted(os.listdir(fullPath))
	print(imgList)
	imgList = ['images/' + plantName + '/' + i for i in imgList]
	print("imgList: \n")
	print(imgList)
	print("last item: \n")
	print(imgList[-1])

	string = ''.join(imgList)
	myDates = re.findall('[2][0][2-9][0-9][0-9][0-9][0-9][0-9]', string)
	print(myDates)

	def dateShuffle(datesIn):
		for i, date in enumerate(datesIn):
			myYear = str(date[0:4])
			myMonth = str(date[4:6])
			myDay = str(date[6:])
			datesIn[i] = myMonth + '/' + myDay + '/' + myYear
			print(date)
		return datesIn

	dateList = dateShuffle(myDates)	

	return render_template('viewPics.html', plant=plant, imageList = imgList,
							enumerate = enumerate, dateList = dateList)


@app.route('/pod/', methods=('GET',))
def pod():
	conn = get_db_connection()
	todayPOD = conn.execute('SELECT * FROM pod WHERE id = "1"').fetchone()
	conn.close()

	plantName = todayPOD['name']
	print(plantName)

	filePath = todayPOD['filePath']
	print(filePath)

	return render_template('pod.html', todayPOD=todayPOD, mostRecent=filePath)


#------------------------------------#
#			Common Routes
#------------------------------------#


@app.route('/<string:plantName>:<string:source>/edit/', methods=('GET', 'POST'))
def edit(plantName, source):

	print(source)
	plant = get_plant(plantName, source)

	#print(plant)

	if request.method == 'POST':
		myName = request.form['name']
		myLastWatered = request.form['lastWatered']
		myDryOut = request.form['dryOut']

		#print(myName)
		#print(myLastWatered)
		#print(myDryOut)

		if not myName:
			flash('Plant name is required!')
		elif not myLastWatered:
			flash('Last watered date is required!')
		elif not myDryOut:
			flash('Dry out period is required!')
		else:
			conn = get_db_connection()

			if source == "plantTracker" or source == "treeTracker":
				try:
					conn.execute('UPDATE plants SET name = ?, lastWatered = ?, dryOut = ? WHERE name = ?',
						(myName, myLastWatered, myDryOut, plantName))
				except sqlite3.IntegrityError:
					conn.close()
					return redirect('/integrityError')
			elif source == "gardenTracker":
				try:
					conn.execute('UPDATE garden SET name = ?, lastWatered = ?, dryOut = ? WHERE name = ?',
						(myName, myLastWatered, myDryOut, plantName))
				except sqlite3.IntegrityError:
					conn.close()
					return redirect('/integrityError')

			conn.commit()
			conn.close()

		# Uploading daily picture
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']

		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)

		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			myDirectory = imagePath + myName.replace(' ','')

			if os.path.exists(myDirectory) == False:
				os.mkdir(myDirectory)
				print('Created folder!')

			file.save(myDirectory + '/' + filename)

			#if source == "plantTracker":
				#return redirect(url_for('plantTracker'))
			#	return render_template('edit.html', plant=plant, source=source)
			#elif source == "gardenTracker":
				#return redirect(url_for('gardenTracker'))
			return render_template('edit.html', plant=plant, source=source)

	return render_template('edit.html', plant=plant, source=source)


@app.route('/<string:source>/refreshDb')
def refreshDb(source):
	result = subprocess.check_output("python3 updateDb_noEmail.py", shell=True)

	if source == 'plantTracker':
		return redirect(url_for('plantTracker'))
	if source == 'gardenTracker':
		return redirect(url_for('gardenTracker'))
	if source == "treeTracker":
		return redirect(url_for('treeTracker'))


@app.route('/<string:plantName>:<string:source>/delete/', methods=('POST',))
def delete(plantName, source):
	plant = get_plant(plantName, source)
	conn = get_db_connection()

	print(plantName + " is getting deleted from " + source + "\n")

	if source == 'plantTracker' or source == "treeTracker":
		conn.execute('DELETE FROM plants WHERE name = ?', (plantName,))
	if source == 'gardenTracker':
		conn.execute('DELETE FROM garden WHERE name = ?', (plantName,))

	conn.commit()
	conn.close()

	if source == 'plantTracker':
		return redirect(url_for('plantTracker'))
	if source == 'gardenTracker':
		return redirect(url_for('gardenTracker'))


#------------------------------------#
#	 	  Garden Tracker Routes
#------------------------------------#

@app.route('/gardenTracker')
def gardenTracker():
	today = dt.datetime.now()
	conn = get_db_connection()
	plants = conn.execute('SELECT * FROM garden ORDER BY name').fetchall()
	thirstyToday = conn.execute('SELECT * FROM garden WHERE remaining < 1 ORDER BY name').fetchall()
	conn.close()

	# Initializing variable, program breaks if there are no thirsty plants and this is not set to 0
	itsBeen = 0

	for item in thirstyToday:
		lastWatered = dt.datetime.strptime(item[2], '%Y-%m-%d')
		#print(lastWatered)
		delta = int(item[3])
		deltaDays = today - lastWatered
		itsBeen = deltaDays.days

		#print(item[1] + " was last watered on " + item[2])
		#print("That means it has been " + str(itsBeen) + " days." + "\n") 

	return render_template('gardenTracker.html', thirstyToday=thirstyToday, plants=plants, itsBeen=itsBeen)


@app.route('/addNewGarden/', methods=('GET', 'POST'))
def addNewGarden():
	if request.method == 'POST':
		name = request.form['name']
		lastWatered = request.form['lastWatered']
		dryOut = request.form['dryOut']

		if not name:
			flash('Name is required!')
		elif not lastWatered:
			flash('Date last watered is required!')
		elif not dryOut:
			flash('Dry out duration is required!')
		else:
			conn = get_db_connection()
			conn.execute('INSERT INTO garden (name, lastWatered, dryOut) VALUES (?, ?, ?)',
				(name, lastWatered, dryOut))
			conn.commit()
			conn.close()
			return redirect(url_for('gardenTracker'))

	return render_template('addNewGarden.html')



#------------------------------------#
#		Tree Tracker
#------------------------------------#

@app.route('/treeTracker')
def treeTracker():
        today = dt.datetime.now()
        conn = get_db_connection()
        plants = conn.execute('SELECT * FROM plants WHERE type = "bonsai" OR type = "tree" ORDER BY name').fetchall()
        thirstyToday = conn.execute('SELECT * FROM plants WHERE remaining < 1 AND type = "bonsai" OR type = "tree" ORDER BY name').fetchall()
        conn.close()

        # Initializing variable, program breaks if there are no thirsty plants and this is not set to 0
        itsBeen = 0

        for item in thirstyToday:
                lastWatered = dt.datetime.strptime(item[2], '%Y-%m-%d')
                #print(lastWatered)
                delta = int(item[3])
                deltaDays = today - lastWatered
                itsBeen = deltaDays.days

                #print(item[1] + " was last watered on " + item[2])
                #print("That means it has been " + str(itsBeen) + " days." + "\n") 

        return render_template('treeTracker.html', thirstyToday=thirstyToday, plants=plants, itsBeen=itsBeen)



#------------------------------------#
#	 	  Bee Tracker Routes
#------------------------------------#

@app.route('/beeTracker')
def beeTracker():

	return render_template('beeTracker.html')
