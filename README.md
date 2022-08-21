# Plant Tracker Flask app

This is a Flask web app that I made to help track the various watering schedules for my
numerous house plants. One Python script sets up the Flask server and details the various
app routes needed to add, edit, and delete SQLite records. The other Python script checks
how long it's been since each plant was watered, updates a column in the database, and
sends me an email (from myself) detailing which plants require attention, if any.
