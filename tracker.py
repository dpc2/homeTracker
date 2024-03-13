#!/usr/bin/python3

import sqlite3
import datetime as dt
from datetime import datetime, timedelta
import yagmail


conn = sqlite3.connect('database.db')
plants = conn.execute('SELECT * FROM plants').fetchall()
garden = conn.execute('SELECT * from garden').fetchall()

today = dt.datetime.now()
temp = today.strftime('%Y-%m-%d')

thirsty = 'Thirsty plant bbs:\n\n'
email_list = "emailAddresses.txt"
thirsty_boi = "./static/thirstyBoy.png"


# Step through plants table and recalculate remaining days
for item in plants:
	lastWatered = dt.datetime.strptime(item[2], '%Y-%m-%d')
	delta = int(item[3])
	daysSince = today - lastWatered
	daysMod = daysSince.days
	name = item[1]
	timeLeft = delta - daysMod

	if daysMod >= delta:
		thirsty += str(item[1]) + """ bby says, "Please water me! It's been """ + str(daysMod) + " whole days!\"\n\n"

	conn.execute('UPDATE plants SET remaining = ?, timeEllapsed = ? WHERE name = ?', (timeLeft, daysMod, name))

thirsty += "\n\nThirsty garden bbs:\n\n"

# Step through garden table and recalculate remaining days
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

with open(email_list) as f:
	emailAddresses = f.readlines()

for i in emailAddresses:
	print(i)

if thirsty != '':
	for i in emailAddresses:
			user = 'dpculler91@gmail.com'
			password = 'fotdjuqwjkumhoqh'
			to = i
			subject = 'Plant Baby Alert!'
			text = thirsty + '\n\n\n'
			image = yagmail.inline(thirsty_boi)
			contents = [text,image]

			try:
				yag = yagmail.SMTP(user,password)
				yag.send(to,subject,contents)
			except:
				print('Oh noooo...')
