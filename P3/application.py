'''Movie Director App
	Created by Linus Dong April 22nd 2015
'''
from flask import Flask, render_template, request, redirect,jsonify, url_for, flash
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Director, Base, Movie

engine = create_engine('sqlite:///directors.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

directors = [	{	'name': 'The CRUDdy Crab', 'id': '1',
					'bio': 'dummy_bio1', 'movies': ['ABC', 'DEF'],
					'image': 'http://ia.media-imdb.com/images/M/MV5BMTg3MDc0MjY0OV5BMl5BanBnXkFtZTcwNzU1MDAxOA@@._V1._SY209_CR7,0,140,209_.jpg'},
				{	'name': 'Blue Burgers', 'id': '2',
					'bio': 'dummy_bio2', 'movies': ['UVW', 'XYZ'],
					'image': 'http://ia.media-imdb.com/images/M/MV5BMTg3MDc0MjY0OV5BMl5BanBnXkFtZTcwNzU1MDAxOA@@._V1._SY209_CR7,0,140,209_.jpg'},
				{	'name': 'Taco Hut', 'id': '3',
					'bio': 'dummy_bio3', 'movies': ['FGH', 'IJK'],
					'image': 'http://ia.media-imdb.com/images/M/MV5BMTg3MDc0MjY0OV5BMl5BanBnXkFtZTcwNzU1MDAxOA@@._V1._SY209_CR7,0,140,209_.jpg'}
			]

director = {'name': 'Taco Hut', 'id': '3', 'bio': 'dummy_bio3',
			'movies': ['FGH', 'IJK']
			}

movies=	[	{	'name': 'American Sniper', 'id': '3', 'image': 'dummy',
				'description': 'dummy_bio3', 'trailer': 'dummy_trailer3', 'director_id': '3'},
			{	'name': 'Jersey Boys', 'id': '2', 'image': 'dummy',
				'description': 'dummy_bio2', 'trailer': 'dummy_trailer2', 'director_id': '2'},
			{	'name': 'J. Edgar ', 'id': '1', 'image': 'dummy',
				'description': 'dummy_bio1', 'trailer': 'dummy_trailer1', 'director_id': '1'}
		]
movie = {	'name': 'J. Edgar ', 'id': '1', 'image': 'dummy',
			'description': 'dummy_bio1', 'trailer': 'dummy_trailer1', 'director_id': '1'}


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
	if directors is None:
		flash("No director on the list. Let's add one")
	return render_template('index.html', directors = directors)

# Create new movie director
@app.route('/director/new', methods=['GET','POST'])
def newDirector():
	if request.method == 'POST':
		newDirector = Director(	name = request.form['name'], 
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
	editedDirector = session.query(Director).filter_by(id = director_id).one()
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
		return redirect(url_for('listDirector', director = editedDirector))
	else:
		return render_template('editDirector.html', director = editedDirector)

# Read movie and director information
@app.route('/director/<int:director_id>/')
@app.route('/director/<int:director_id>')
def listDirector(director_id):
	director = session.query(Director).filter_by(id = director_id).one()
	movies = session.query(Movie).filter_by(director_id = director_id).all()
	if movies is None:
		flash("No movie on the list. Let's add one")
	return render_template('listDirector.html', director = director,
												movies = movies)

# Delete Movie director information
@app.route('/director/<int:director_id>/delete', methods=['GET','POST'])
def deleteDirector(director_id):
	directorToDelete = session.query(Director).filter_by(id = director_id).one()
	moviesToDelete = session.query(Movie).filter_by(director_id = director_id).all()
	if request.method == 'POST':
		session.delete(directorToDelete)
		session.delete(moviesToDelete)
		session.commit()
		flash("Director Delete Successfully!")
		return redirect(url_for('listAllDirectors'))
	else:
		return render_template('deleteDirector.html', director = directorToDelete)

# list movies
@app.route('/movies/')
@app.route('/movies')
def listAllMovies():
	if movies is None:
		flash("No movie on the list. Let's add one")
	return render_template('listAllMovies.html', movies = movies)

# Create new movie
@app.route('/director/<int:director_id>/movie/new', methods=['GET','POST'])
def newMovie(director_id):
	director = session.query(Director).filter_by(id = director_id).one()
	if request.method == 'POST':
		newMovie = Movie(	name = request.form['name'],
							image = request.form['image'],
							trailer = request.form['trailer'],
							description = request.form['description'],
							director_id = director_id)
		session.add(newMovie)
		session.commit()
		flash("Movie Created Successfully!")
		return redirect(url_for('listDirector', director = director))
	else:
		return render_template('newMovie.html', director_id = director_id)

# Update movie information
@app.route('/director/<int:director_id>/movie/<int:movie_id>/edit',
			methods=['GET','POST'])
def editMovie(director_id, movie_id):
	director = session.query(Director).filter_by(id = director_id).one()
	editedMovie = session.query(Movie).filter_by(id = movie_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedMovie.name = request.form['name']
		if request.form['image']:
			editedMovie.image = request.form['image']
		if request.form['description']:
			editedMovie.description = request.form['description']
		if request.form['trailer']:
			editedMovie.trailer = request.form['trailer']
		session.add(editedMovie)
		session.commit()
		flash("Movie Edited Successfully!")
		return redirect(url_for('listDirector', director = director))
	else:
		return render_template('editMovie.html', movie = editedMovie)

# Read movie information
@app.route('/director/<int:director_id>/movie/<int:movie_id>/')
@app.route('/director/<int:director_id>/movie/<int:movie_id>')
def listMovie(director_id, movie_id):
	movie = session.query(Movie).filter_by(id = movie_id).one()
	return render_template('listMovie.html', movie = movie)

# Delete Movie information
@app.route('/director/<string:director_id>/movie/<string:movie_id>/delete',
			methods=['GET','POST'])
def deleteMovie(director_id, movie_id):
	director = session.query(Director).filter_by(id = director_id).one()
	movieToDelete = session.query(Movie).filter_by(id = movie_id).one()
	if request.method == 'POST':
		session.delete(directorToDelete)
		session.commit()
		flash("Movie Deleted Successfully!")
		return redirect(url_for('listDirector', director = director))
	else:
		return render_template('deleteMovie.html', movie = movieToDelete)

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 8000)