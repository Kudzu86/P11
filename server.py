import json
import datetime
from flask import Flask,render_template,request,redirect,flash,url_for


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    club = [club for club in clubs if club['email'] == request.form['email']][0]
    return render_template('welcome.html',club=club,competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    # Recherche du club et de la compétition
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]

    # Vérification si la compétition existe
    if foundClub and foundCompetition:
        # Récupérer la date de la compétition et la convertir en objet datetime
        competition_date = datetime.datetime.strptime(foundCompetition['date'], '%Y-%m-%d %H:%M:%S') # Assurez-vous que le format de la date est correct
        current_date = datetime.datetime.now()

        # Si la compétition est dans le passé, on affiche un message d'erreur
        if competition_date < current_date:
            flash("Cannot book places for a past competition.")
            return render_template('welcome.html', club=foundClub, competitions=competitions)
        else:
            # Si la compétition est valide, on affiche la page de réservation
            flash("Competition is valid. Proceed with booking.")
            return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong - please try again.")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])

    # Vérifier si le nombre de places demandées dépasse 12
    if placesRequired > 12:
        flash("You cannot book more than 12 places for a competition.")
        return render_template('welcome.html', club=club, competitions=competitions)

    # Vérifier si la compétition a suffisamment de places disponibles
    if int(competition['numberOfPlaces']) < placesRequired:
        flash("Not enough places available in the competition.")
        return render_template('welcome.html', club=club, competitions=competitions)
    
    # Mettre à jour le nombre de places du concours
    competition['numberOfPlaces'] = str(int(competition['numberOfPlaces']) - placesRequired)
    
    # Mettre à jour les points du club
    club_points = int(club['points'])
    club['points'] = str(club_points - placesRequired)

    # Sauvegarder les modifications dans le fichier clubs.json
    with open('clubs.json', 'w') as f:
        json.dump({'clubs': clubs}, f, indent=4)

    flash('Great-booking complete! Points have been deducted.')
    return render_template('welcome.html', club=club, competitions=competitions)



@app.route('/showClubs')
def showClubs():
    return render_template('clubs.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
