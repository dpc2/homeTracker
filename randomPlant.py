#!/usr/bin/python3

import os
import sqlite3
from os.path import dirname, join

currentDir = dirname(__file__)
imagePath = join(currentDir, "static/images/")

# Connect to SQLite3 db
conn = sqlite3.connect('database.db')
conn.row_factory = sqlite3.Row

todayPOD = conn.execute('SELECT * FROM plants ORDER BY RANDOM() LIMIT 1').fetchone()
plantName = todayPOD['name']
filePath = plantName.replace(' ','')

fullPath = imagePath + filePath
imgList = sorted(os.listdir(fullPath))

imgList = ['images/' + filePath + '/' + i for i in imgList]

mostRecent = imgList[-1]

print(plantName)
print(mostRecent)

try:
	conn.execute('UPDATE pod SET name = ?, filePath = ? WHERE id = "1"', (plantName, mostRecent))
	conn.commit()
	conn.close()
except sqlite3.IntegrityError:
	conn.close()
