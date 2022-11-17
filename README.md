<h1>Plant Tracker Flask app</h1>

<p>
This is a Flask web app that I made to help track the differing watering schedules for my many house plants.
</p>
<p>
One Python script initializes the Flask server and details the app routes needed to add, edit, and delete SQLite records. The second Python
script is triggered by a cronjob to run every day at noon. It checks how many days since each plant was watered, updates a Days Remaining 
column in the SQLite table, and sends me an email from myself using Yagmail if there are any thirsty plants.
</p>
<p>
The Flask server currently runs on a Raspberry Pi 4 connected to my home WiFi network, though I'd like to eventually run it off a more legitimate 
home server.
</p>

<h2>Technologies/Libraries Used</h2>
<ul>
	<li>Python</li>
	<ul>
		<li>Flask</li>
		<li>SQLite3</li>
		<li>Yagmail</li>
	</ul>
        <li>HTML</li>
        <li>CSS</li>
        <li>Raspberry Pi 4</li>
</ul>



<br>
<p align="center">
  <img width="600" height="300" src="/static/20221024.jpg">
</p>
<br>
<p align="center">
  <img width="597" height="616" src="/static/plantEmail.png">
</p>
