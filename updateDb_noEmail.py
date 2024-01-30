#!/usr/bin/python3

import sqlite3
import datetime as dt
from datetime import datetime, timedelta
import yagmail


conn = sqlite3.connect('database.db')
plants = conn.execute('SELECT * FROM plants').fetchall()
garden = conn.execute('SELECT * FROM garden').fetchall()

today = dt.datetime.now()
temp = today.strftime('%Y-%m-%d')

thirsty = ''
email_list = "emailAddresses.txt"
thirsty_boi = "/home/danny/scripts/plantTracker/venv/plantFlask/static/thirstyBoy.png"

if plants:
	for item in plants:
		lastWatered = dt.datetime.strptime(item[2], '%Y-%m-%d')
		delta = int(item[3])
		daysSince = today - lastWatered
		daysMod = daysSince.days
		name = item[1]
		timeLeft = delta - daysMod

		if daysMod >= delta:
				thirsty += str(item[1]) + """ bby says, "Please water me! It's been """ + str(daysMod) + " whole days!\"\n\n"

		conn.execute('UPDATE plants SET remaining = ? WHERE name = ?', (timeLeft, name))

if garden:
	for item in garden:
		lastWatered = dt.datetime.strptime(item[2], '%Y-%m-%d')
		delta = int(item[3])
		daysSince = today - lastWatered
		daysMod = daysSince.days
		name = item[1]
		timeLeft = delta - daysMod

		if daysMod >= delta:
				thirsty += str(item[1]) + """ bby says, "Please water me! It's been """ + str(daysMod) + " whole days!\"\n\n"

		conn.execute('UPDATE garden SET remaining = ? WHERE name = ?', (timeLeft, name))		

conn.commit()
conn.close()

