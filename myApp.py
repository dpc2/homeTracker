import sqlite3
import datetime as dt
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import (
	Flask, render_template,
	request, url_for, flash, redirect
)


app = Flask(__name__)
app.secret_key = '9caa106935603b215fd25ebffd88baf7ce4fb5e237ce3a04'
app.add_url_rule(
	"/<string:plantName>/upload/", endpoint="upload", build_only=True
)
ALLOWED_EXTENSIONS = {'jpg'}


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
#		Routes
#------------------------------------#

@app.route('/')
def index():
	conn = get_db_connection()
	plants = conn.execute('SELECT * FROM plants ORDER BY name').fetchall()
	conn.close()
	return render_template('index.html', plants=plants)

 
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
			return redirect(url_for('index'))

	return render_template('addNew.html')



@app.route('/<string:plantName>/edit/', methods=('GET', 'POST'))
def edit(plantName):
	plant = get_plant(plantName)

	if request.method == 'POST':
		print(request.form)
		myName = request.form['name']
		myLastWatered = request.form['lastWatered']
		myDryOut = request.form['dryOut']

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
			return redirect(url_for('index'))
	return render_template('edit.html', plant=plant)


@app.route('/<string:plantName>/wateredToday/', methods=('POST',))
def wateredToday(plantName):
	plant = get_plant(plantName)
	conn = get_db_connection()
	temp = dt.datetime.now()
	today = temp.strftime('%Y-%m-%d')
	conn.execute('UPDATE plants SET lastWatered = ? WHERE name = ?', (today, plantName))
	conn.commit()
	conn.close()
	#flash('"{}" was watered today!'.format(plant['name']))
	return redirect(url_for('index'))


@app.route('/<string:plantName>/delete/', methods=('POST',))
def delete(plantName):
	plant = get_plant(plantName)
	conn = get_db_connection()
	conn.execute('DELETE FROM plants WHERE name = ?', (plantName,))
	conn.commit()
	conn.close()
	#flash('"{}" was successfully deleted!'.format(plant['name']))
	return redirect(url_for('index'))


@app.route('/<string:plantName>/upload/', methods=['GET', 'POST'])
def upload(plantName):
	if request.method == 'POST':
		#UPLOAD_FOLDER = getFolder(plantName):
		UPLOAD_FOLDER = '/home/danny/scripts/venv/plantFlask/static/'
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']

		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)

		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return redirect(url_for('upload', name=filename))
	return redirect(url_for('upload'))
