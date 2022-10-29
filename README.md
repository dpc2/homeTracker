<h1>Plant Tracker Flask app</h1>

This is a Flask web app that I made to help track the differing watering schedules for my
many house plants.
<br>
One Python script initializes the Flask server and details the app routes
needed to add, edit, and delete SQLite records. The second Python script is triggered by a
cronjob to run every day at noon; it checks how long it's been since each plant was watered,
updates a Days Remaining column in the SQLite table, and sends me an email (from myself)
using Yagmail which tells me which plants are thirsty, and how long it's been since they
were watered.

<h2>Technologies/Libraries Used</h2>
<ul>
	<li>Python</li>
	<li>Flask</li>
	<li>HTML</li>
	<li>CSS</li>
	<li>SQLite3</li>
	<li>Yagmail</li>
</ul>
<br>
<p align="center">
  <img width="600" height="300" src="/static/20221024.jpg">
</p>
<br>
<p align="center">
  <img width="597" height="616" src="/static/plantEmail.png">
</p>
