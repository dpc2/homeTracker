# Plant Tracker Flask app

This is a Flask web app that I made to help track the various watering schedules for my
many house plants. One Python script sets up the Flask server and details the app routes
needed to add, edit, and delete SQLite records. The second Python script is triggered to
run by a cronjob every day at noon. It checks how long it's been since each plant was
watered, updates a column in the database, and sends me an email (from myself) detailing
which plants are thirsty.

<h2>Technologies/Libraries Used</h2>
- Python
- Flask
- SQLite3
- Yagmail
