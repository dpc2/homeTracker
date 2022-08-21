import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
	connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO plants (name, lastWatered, dryOut) VALUES (?, ?, ?)",
		('Plant #1', '2022-07-31', '18')
	)

cur.execute("INSERT INTO plants (name, lastWatered, dryOut) VALUES (?, ?, ?)", 
		('Plant #2', '2022-08-05', '14')
	)

connection.commit()
connection.close()
