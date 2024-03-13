<h1>Plant Tracker Flask app</h1>

<p>
This is a Flask web app that I made to help track the differing watering schedules for my many house plants.
</p>

<p>
One Python script initializes the Flask server and details the app routes needed to add, edit, and delete SQLite records. The second Python
script is triggered by a cronjob to run every day at noon. It checks how many days since each plant was watered, updates a Days Remaining 
column in the SQLite table, and sends me an email from myself using Yagmail if there are any thirsty plants. Pictures are uploaded each time
a plant is watered, and past pictures can be viewed for each plant.

<u>Future features:</u>
- Incorporate Javascript to update the frontend
- Add a Rename Plant button that will take care of backend folder management
- Request photo when selecting Watered Today
- Plant profile pics displayed on front page
- Add a "Repot me!" feature
- Total number of plants at bottom of the page
- Handling iPhone photos: naming conventions
- Add most recent picture to the edit page
- Add Photo Gallery page
	- Slideshow feature
- Add In Memorium page
- Add Plant of the Day pics to daily emails
- Fix refresh function to include garden tracker
- Fix garden tracker picture upload redirect
- Fix redirect after gardenTracker picture uploads
- <s>Link to photo gallery from individual plant pages</s>
- <s>Photo viewing pages for each individual plant, generated from template</s>
- <s>Reassess dates after changing Dry Out time - Refesh button</s>
- <s>Plant of the day</s>
- <s>Bee tracker placeholder</s>
- <s>Home page</s>
- <s>Garden tracker</s>
</p>

<p>
The Flask server currently runs on a Raspberry Pi 4 connected to my home WiFi network, though I'd like to eventually run it from a more legitimate 
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


### Setup Steps
git clone git@github.com:dpc2/homeTracker.git <br>
python3 -m venv ./homeTracker <br>
source bin/active <br>
pip install flask <br>
pip install yagmail <br>

