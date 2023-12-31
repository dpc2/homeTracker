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

# Upload configurations
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

def get_plant(plantName):
	conn = get_db_connection()
	plant = conn.execute('SELECT * FROM plants WHERE name = ?', (plantName,)).fetchone()
	conn.close()
	#if plant is None:
	#	abort(404)
	return plant

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
	plants = conn.execute('SELECT * FROM plants ORDER BY name').fetchall()
	thirstyToday = conn.execute('SELECT * FROM plants WHERE remaining < 1 ORDER BY name').fetchall()
	conn.close()


	for item in thirstyToday:
		lastWatered = dt.datetime.strptime(item[2], '%Y-%m-%d')
		print(lastWatered)
		delta = int(item[3])
		deltaDays = today - lastWatered
		itsBeen = deltaDays.days

		print(item[1] + " was last watered on " + item[2])
		print("That means it has been " + str(itsBeen) + " days." + "\n") 

	return render_template('plantTracker.html', thirstyToday=thirstyToday, plants=plants, itsBeen=itsBeen)


@app.route('/addNew/', methods=('GET', 'POST'))
def addNew():
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
			conn.execute('INSERT INTO plants (name, lastWatered, dryOut) VALUES (?, ?, ?)',
				(name, lastWatered, dryOut))
			conn.commit()
			conn.close()
			return redirect(url_for('plantTracker'))

	return render_template('addNew.html')



@app.route('/<string:plantName>/edit/', methods=('GET', 'POST'))
def edit(plantName):
	plant = get_plant(plantName)
	print(plant)

	if request.method == 'POST':
		myName = request.form['name']
		myLastWatered = request.form['lastWatered']
		myDryOut = request.form['dryOut']

		print(myName)
		print(myLastWatered)
		print(myDryOut)

		if not myName:
			flash('Plant name is required!')
		elif not myLastWatered:
			flash('Last watered date is required!')
		elif not myDryOut:
			flash('Dry out period is required!')
		else:
			conn = get_db_connection()

			try:
				conn.execute('UPDATE plants SET name = ?, lastWatered = ?, dryOut = ? WHERE name = ?',
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
			return redirect(url_for('plantTracker'))
	return render_template('edit.html', plant=plant)


@app.route('/<string:plantName>/wateredToday/', methods=('POST',))
def wateredToday(plantName):
	plant = get_plant(plantName)
	conn = get_db_connection()
	temp = dt.datetime.now()
	today = temp.strftime('%Y-%m-%d')
	conn.execute('UPDATE plants SET lastWatered = ? WHERE name = ?', (today, plantName))
	conn.execute('UPDATE plants SET remaining = ? WHERE name = ?', (plant['dryOut'], plantName))
	conn.commit()
	conn.close()
	#flash('"{}" was watered today!'.format(plant['name']))
	return redirect(url_for('plantTracker'))


@app.route('/<string:plantName>/delete/', methods=('POST',))
def delete(plantName):
	plant = get_plant(plantName)
	conn = get_db_connection()
	conn.execute('DELETE FROM plants WHERE name = ?', (plantName,))
	conn.commit()
	conn.close()
	#flash('"{}" was successfully deleted!'.format(plant['name']))
	return redirect(url_for('plantTracker'))


@app.route('/<string:plantName>/viewPics/', methods=('GET',))
def viewPics(plantName):
	plant = get_plant(plantName)

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

@app.route('/refreshDb')
def refreshDb():
   result = subprocess.check_output("python3 updateDb_noEmail.py", shell=True)
   return redirect(url_for('plantTracker'))



#------------------------------------#
#	 	  Bee Tracker Routes
#------------------------------------#

@app.route('/beeTracker')
def beeTracker():

	return render_template('beeTracker.html')