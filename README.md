# Audio Articles
Audio Articles was my 4-week personal project I completed during my time as a software engineering fellow at Hackbright. 
Audio Articles allows users to save, organize and listen to articles of any sort. Intended for a time-strapped, 
audiobooks-loving demographic or the visually impaired, this app provides functionality to save article text and organize with tags. 
Users can then view their articles by different tags, last listened or date saved, etc. The most useful feature is that 
for any article, users can select from a host of possible voices and accents, and have their article text read 
aloud to them in that voice.

![alt text](static/headphones.jpg "Description goes here")

# Technologies
Backend: Python, Flask, PostgreSQL, SQLAlchemy
Frontend: JavaScript, jQuery, AJAX, Jinja2, Bootstrap, HTML5, CSS3, some React
APIs: Amazon Polly

# Features
-User account creation
-Functionality to add/delete articles, and access later
-Article tagging/organization/filtering
-Playing audio of article text utilizing Amazon Polly API

# Installation
To run Audio Articles:
-Install PostgreSQL (Mac OSX)
-Clone or fork this repo:
https://github.com/KallieFriedman/audio_articles
-Create and activate a virtual environment inside your Audio Articles directory:
virtualenv env
source env/bin/activate
-Install the dependencies:
pip install -r requirements.txt
-Sign up for Amazon Web Services and follow steps to install AWS in your Terminal
-Set up the database:
python model.py
-Run the app:
python server.py
You can now navigate to 'localhost:5000/' to access Audio Articles
