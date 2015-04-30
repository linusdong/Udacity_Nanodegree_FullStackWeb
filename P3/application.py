'''Movie Director App
	Created by Linus Dong April 22nd 2015
'''
import re
from flask import Flask, render_template, request, redirect,jsonify, url_for, flash
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Director, Base, Movie, User

from flask import session as login_session
import random, string

#IMPORTS FOR LOGIN
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(
	open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME= "Linus Movie App"

engine = create_engine('sqlite:///directors.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#User Helper Functions
def createUser(login_session):
	newUser = User(	name = login_session['username'], email = login_session['email'],
					image = login_session['image'])
	session.add(newUser)
	session.commit()
	user = session.query(User).filter_by(email = login_session['email']).one()
	return user.id

def getUserInfo(user_id):
	user = session.query(User).filter_by(id = user_id).one()
	return user

def getUserID(email):
	try:
		user = session.query(User).filter_by(email = email).one()
		return user.id
	except:
		return None

#Create anti-forgery state token
@app.route('/login')
def showLogin():
	state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
	login_session['state'] = state
	return render_template('login.html', STATE = state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
	#Validate state token 
	if request.args.get('state') != login_session['state']:
		response = make_response(json.dumps('Invalid state parameter.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	#Obtain authorization code
	code = request.data.decode('utf-8')
	
	try:
		# Upgrade the authorization code into a credentials object
		oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
		oauth_flow.redirect_uri = 'postmessage'
		credentials = oauth_flow.step2_exchange(code)
	except FlowExchangeError:
		response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	
	# Check that the access token is valid.
	access_token = credentials.access_token
	url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
				 % access_token)
	h = httplib2.Http()
	result = json.loads(h.request(url, 'GET')[1])
	# If there was an error in the access token info, abort.
	if result.get('error') is not None:
		response = make_response(json.dumps(result.get('error')), 500)
		response.headers['Content-Type'] = 'application/json'

		
	# Verify that the access token is used for the intended user.
	gplus_id = credentials.id_token['sub']
	if result['user_id'] != gplus_id:
		response = make_response(
				json.dumps("Token's user ID doesn't match given user ID."), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Verify that the access token is valid for this app.
	if result['issued_to'] != CLIENT_ID:
		response = make_response(
				json.dumps("Token's client ID does not match app's."), 401)
		print "Token's client ID does not match app's."
		response.headers['Content-Type'] = 'application/json'
		return response

	stored_credentials = login_session.get('credentials')
	stored_gplus_id = login_session.get('gplus_id')
	if stored_credentials is not None and gplus_id == stored_gplus_id:
		response = make_response(json.dumps('Current user is already connected.'),
														 200)
		response.headers['Content-Type'] = 'application/json'
		return response
		
	# Store the access token in the session for later use.
	login_session['credentials'] = credentials
	login_session['gplus_id'] = gplus_id
 
	
	#Get user info
	userinfo_url =  "https://www.googleapis.com/oauth2/v1/userinfo"
	params = {'access_token': credentials.access_token, 'alt':'json'}
	answer = requests.get(userinfo_url, params=params)
	
	data = answer.json()

	login_session['username'] = data['name']
	login_session['image'] = data['image']
	login_session['email'] = data['email']

	#see if user exists, if it doesn't make a new one
	user_id = getUserID(login_session['email'])
	if not user_id:
		user_id = createUser(login_session)
	login_session['user_id'] = user_id

	output = ''
	output +='<h1>Welcome, '
	output += login_session['username']
	output += '!</h1>'
	output += '<img src="'
	output += login_session['image']
	output +=' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
	flash("You are now logged in as %s"%login_session['username'])
	print "done!"
	return output

#DISCONNECT - Revoke a current user's token and reset their login_session

@app.route('/gdisconnect')
def gdisconnect():
	#Only disconnect a connected user.
	credentials = login_session.get('credentials')
	if credentials is None:
		response = make_response(json.dumps('Current user not connected.'),401)
		response.headers['Content-Type'] = 'application/json'
		return response 
	access_token = credentials.access_token
	url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
	h = httplib2.Http()
	result = h.request(url, 'GET')[0]
	reason = h.request(url, 'GET')[1]
	if result['status'] == '200':
		#Reset the user's sesson.
		del login_session['credentials']
		del login_session['gplus_id']
		del login_session['username']
		del login_session['email']
		del login_session['image']

		response = make_response(json.dumps('Successfully disconnected.'), 200)
		response.headers['Content-Type'] = 'application/json'
		return response
	else:
		# For whatever reason, the given token was invalid.
		response = make_response(
				json.dumps('Failed to revoke token for given user. reason: {reason}'\
					.format(reason = reason), 400))
		response.headers['Content-Type'] = 'application/json'
		return response

# helper function to check original creator,
# if the creator is not match the current user,
# redirect to the index page that match current user
def checkCreator(user_id):
	creator = getUserInfo(user_id)
	if creator.id != login_session['user_id']:
		flash("ERROR, the information is not belong to {name}.".format(
			name = creator.name))
		return redirect(url_for('listAllDirectors'))

# Extract the youtube ID from the url
def getYoutubeId(youtube_url):
	youtube_id_match = re.search(r'(?<=v=)[^&#]+', youtube_url)
	youtube_id_match = youtube_id_match or re.search(r'(?<=be/)[^&#]+', youtube_url)
	youtube_id_match = youtube_id_match or re.search(r'(?<=embed/)[^&#]+', youtube_url)
	trailer_youtube_id = youtube_id_match.group(0) if youtube_id_match else None
	return trailer_youtube_id

@app.route('/director/<int:director_id>/movie/<int:movie_id>/JSON')
def movieJSON(director_id, movie_id):
	movie = session.query(Movie).filter_by(id = movie_id).one()
	return jsonify(movie= movie.serialize)

@app.route('/director/<int:director_id>/movies/JSON')
def directorMoviesJSON(director_id):
	movies = session.query(Movie).filter_by(director_id = director_id).all()
	return jsonify(movies=[m.serialize for m in movies])

@app.route('/directors/JSON')
def directorsJSON():
	directors = session.query(Director).all()
	return jsonify(directors= [d.serialize for d in directors])

# list movie directors
@app.route('/')
@app.route('/directors/')
@app.route('/directors')
def listAllDirectors():
	directors = session.query(Director).all()
	if not directors:
		flash("No director on the list. Let's add one")
	if 'user_id' not in login_session:
		user  = None
	else:
		user = getUserInfo(login_session['user_id'])
		directors = session.query(Director).filter_by(user_id = user.id).all()
	return render_template('index.html', directors = directors, user = user)

# Create new movie director
@app.route('/director/new', methods=['GET','POST'])
def newDirector():
	if 'user_id' not in login_session:
		return redirect('/login')
	if request.method == 'POST':
		newDirector = Director(	user_id = login_session['user_id'],
								name = request.form['name'], 
								image = request.form['image'],
								bio = request.form['bio'])
		session.add(newDirector)
		session.commit()
		flash("New Director Created!")
		return redirect(url_for('listAllDirectors'))
	else:
		return render_template('newDirector.html')


# Update movie director information
@app.route('/director/<int:director_id>/edit', methods=['GET','POST'])
def editDirector(director_id):
	if 'user_id' not in login_session:
		return redirect('/login')
	editedDirector = session.query(Director).filter_by(id = director_id).one()
	checkCreator(editedDirector.user_id)
	if request.method == 'POST':
		if request.form['name']:
			editedDirector.name = request.form['name']
		if request.form['image']:
			editedDirector.image = request.form['image']
		if request.form['bio']:
			editedDirector.bio = request.form['bio']
		session.add(editedDirector)
		session.commit()
		flash("Director Edited Successfully!")
		return redirect(url_for('listDirector', director_id = director_id))
	else:
		return render_template('editDirector.html', director = editedDirector)

# Read movie and director information
@app.route('/director/<int:director_id>/')
@app.route('/director/<int:director_id>')
def listDirector(director_id):
	director = session.query(Director).filter_by(id = director_id).one()
	movies = session.query(Movie).filter_by(director_id = director_id).all()
	if not movies:
		flash("No movie on the list. Let's add one")
	if 'user_id' not in login_session:
		user  = None
	else:
		user = "user is logined."
		checkCreator(director.user_id)
	return render_template('listDirector.html', director = director,
												movies = movies,
												user = user)

# Delete Movie director information
@app.route('/director/<int:director_id>/delete', methods=['GET','POST'])
def deleteDirector(director_id):
	if 'user_id' not in login_session:
		return redirect('/login')
	directorToDelete = session.query(Director).filter_by(id = director_id).one()
	checkCreator(directorToDelete.user_id)
	moviesToDelete = session.query(Movie).filter_by(director_id = director_id).all()
	if request.method == 'POST':
		for movie in moviesToDelete:
			session.delete(movie)
		session.delete(directorToDelete)
		session.commit()
		flash("Director Delete Successfully!")
		return redirect(url_for('listAllDirectors'))
	else:
		return render_template('deleteDirector.html', director = directorToDelete)

# list movies
@app.route('/movies/')
@app.route('/movies')
def listAllMovies():
	if not movies:
		flash("No movie on the list. Let's add one")
	return render_template('listAllMovies.html', movies = movies)

# Create new movie
@app.route('/director/<int:director_id>/movie/new', methods=['GET','POST'])
def newMovie(director_id):
	if 'user_id' not in login_session:
		return redirect('/login')
	director = session.query(Director).filter_by(id = director_id).one()
	if request.method == 'POST':
		# strip out youtube id
		trailer_id = getYoutubeId(request.form['trailer'])
		newMovie = Movie(	user_id = login_session['user_id'],
							name = request.form['name'],
							image = request.form['image'],
							trailer = trailer_id,
							description = request.form['description'],
							director_id = director_id)
		session.add(newMovie)
		session.commit()
		flash("Movie Created Successfully!")
		return redirect(url_for('listDirector', director_id = director_id))
	else:
		return render_template('newMovie.html', director_id = director_id)

# Update movie information
@app.route('/director/<int:director_id>/movie/<int:movie_id>/edit',
			methods=['GET','POST'])
def editMovie(director_id, movie_id):
	if 'user_id' not in login_session:
		return redirect('/login')
	editedMovie = session.query(Movie).filter_by(id = movie_id).one()
	checkCreator(editedMovie.user_id)
	if request.method == 'POST':
		if request.form['name']:
			editedMovie.name = request.form['name']
		if request.form['image']:
			editedMovie.image = request.form['image']
		if request.form['description']:
			editedMovie.description = request.form['description']
		if request.form['trailer']:
			trailer_id = getYoutubeId(request.form['trailer'])
			editedMovie.trailer = trailer_id
		session.add(editedMovie)
		session.commit()
		flash("Movie Edited Successfully!")
		return redirect(url_for('listMovie', 	director_id = director_id,
												movie_id = movie_id))
	else:
		return render_template('editMovie.html', movie = editedMovie)

# Read movie information
@app.route('/director/<int:director_id>/movie/<int:movie_id>/')
@app.route('/director/<int:director_id>/movie/<int:movie_id>')
def listMovie(director_id, movie_id):
	director = session.query(Director).filter_by(id = director_id).one()
	movie = session.query(Movie).filter_by(id = movie_id).one()
	if 'user_id' not in login_session:
		user  = None
	else:
		user = "user is logined."
		checkCreator(movie.user_id)
	return render_template('listMovie.html', 	movie = movie,
												director = director,
												user = user)

# Delete Movie information
@app.route('/director/<string:director_id>/movie/<string:movie_id>/delete',
			methods=['GET','POST'])
def deleteMovie(director_id, movie_id):
	if 'user_id' not in login_session:
		return redirect('/login')
	director = session.query(Director).filter_by(id = director_id).one()
	movieToDelete = session.query(Movie).filter_by(id = movie_id).one()
	checkCreator(movieToDelete.user_id)
	if request.method == 'POST':
		session.delete(movieToDelete)
		session.commit()
		flash("Movie Deleted Successfully!")
		return redirect(url_for('listDirector', director_id = director_id))
	else:
		return render_template('deleteMovie.html', movie = movieToDelete)

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 8000)