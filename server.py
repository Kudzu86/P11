import datetime
import os
from flask import Flask, render_template, request, redirect, flash, url_for, session
import json

def loadClubs():
   # Charge les clubs depuis le fichier json
   with open(os.getenv('CLUBS_JSON_FILE', 'clubs.json')) as c:
        return json.load(c)['clubs']

def loadCompetitions():
   # Charge les compétitions depuis le fichier json 
   with open(os.getenv('COMPETITIONS_JSON_FILE', 'competitions.json')) as comps:
        return json.load(comps)['competitions']

def create_app(test_config=None):
   app = Flask(__name__)
   app.secret_key = 'something_special'
   
   # Charge la config des fichiers ou de test
   if test_config is None:
       app.config.from_mapping(
           CLUBS=loadClubs(),
           COMPETITIONS=loadCompetitions()
       )
   else:
       app.config.update(test_config)

   @app.route('/')
   def index():
       return render_template('index.html')

   @app.route('/showSummary', methods=['GET', 'POST']) 
   def showSummary():
       if request.method == 'POST':
           # Trouve le club par email
           club = next((club for club in app.config['CLUBS'] if club['email'] == request.form['email']), None)
           if club:
               session['email'] = club['email']
               return render_template('welcome.html', club=club, competitions=app.config['COMPETITIONS'])
           flash("Sorry, that email wasn't found.")
           return redirect(url_for('index'))
       
       if 'email' in session:
           club = next((club for club in app.config['CLUBS'] if club['email'] == session['email']), None)
           return render_template('welcome.html', club=club, competitions=app.config['COMPETITIONS'])
       return redirect(url_for('index'))

   @app.route('/book/<competition>/<club>')
   def book(competition, club):
       foundClub = next((c for c in app.config['CLUBS'] if c['name'] == club), None)
       foundCompetition = next((c for c in app.config['COMPETITIONS'] if c['name'] == competition), None)

       if foundClub and foundCompetition:
           # Vérifie si la compétition est passée
           if datetime.datetime.strptime(foundCompetition['date'], '%Y-%m-%d %H:%M:%S') < datetime.datetime.now():
               flash("Cannot book places for a past competition.")
               return render_template('welcome.html', club=foundClub, competitions=app.config['COMPETITIONS'])
           return render_template('booking.html', club=foundClub, competition=foundCompetition)

       flash("Something went wrong - please try again.")
       return render_template('welcome.html', club=club, competitions=app.config['COMPETITIONS'])

   @app.route('/purchasePlaces', methods=['POST'])
   def purchasePlaces():
       competition = next((c for c in app.config['COMPETITIONS'] if c['name'] == request.form['competition']), None)
       club = next((c for c in app.config['CLUBS'] if c['name'] == request.form['club']), None)

       # Validation du nombre de places
       try:
           placesRequired = int(request.form['places'])
           if placesRequired <= 0:
               flash("You cannot book a negative or zero number of places.")
               return render_template('welcome.html', club=club, competitions=app.config['COMPETITIONS'])
       except ValueError:
           flash("Invalid input. Please enter a valid number of places.")
           return render_template('welcome.html', club=club, competitions=app.config['COMPETITIONS'])

       # Vérification des limites de réservation
       if placesRequired > 12:
           flash("You cannot book more than 12 places for a competition.")
           return render_template('welcome.html', club=club, competitions=app.config['COMPETITIONS'])

       if int(club['points']) < placesRequired:
           flash("You do not have enough points to book these places.")
           return render_template('welcome.html', club=club, competitions=app.config['COMPETITIONS'])

       if int(competition['numberOfPlaces']) < placesRequired:
           flash("Not enough places available in the competition.")
           return render_template('welcome.html', club=club, competitions=app.config['COMPETITIONS'])
       
       # Mise à jour des données compétition et club
       competition['numberOfPlaces'] = str(int(competition['numberOfPlaces']) - placesRequired)
       club['points'] = str(int(club['points']) - placesRequired)

       # Sauvegarde si pas en mode test
       if not app.config.get('TESTING'):
           with open(os.getenv('CLUBS_JSON_FILE', 'clubs.json'), 'w') as f:
               json.dump({'clubs': app.config['CLUBS']}, f, indent=4)
           with open(os.getenv('COMPETITIONS_JSON_FILE', 'competitions.json'), 'w') as f:
               json.dump({'competitions': app.config['COMPETITIONS']}, f, indent=4)

       flash('Great-booking complete! Points have been deducted.')
       return render_template('welcome.html', club=club, competitions=app.config['COMPETITIONS'])

   @app.route('/showClubs')
   def showClubs():
       return render_template('clubs.html', clubs=app.config['CLUBS'])

   @app.route('/logout')
   def logout():
       session.pop('email', None)
       return redirect(url_for('index'))

   return app

app = create_app()