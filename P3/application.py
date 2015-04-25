'''Movie Director App
	Created by Linus Dong April 22nd 2015
'''
from flask import Flask, render_template, request, redirect,jsonify, url_for, flash
app = Flask(__name__)

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
				'bio': 'dummy_bio3', 'trailer': 'dummy_trailer3', 'director_id': '3'},
			{	'name': 'Jersey Boys', 'id': '2', 'image': 'dummy',
				'bio': 'dummy_bio2', 'trailer': 'dummy_trailer2', 'director_id': '2'},
			{	'name': 'J. Edgar ', 'id': '1', 'image': 'dummy',
				'bio': 'dummy_bio1', 'trailer': 'dummy_trailer1', 'director_id': '1'}
		]
movie = {	'name': 'J. Edgar ', 'id': '1', 'image': 'dummy',
			'bio': 'dummy_bio1', 'trailer': 'dummy_trailer1', 'director_id': '1'}


# list movie directors
@app.route('/')
@app.route('/directors/')
@app.route('/directors')
def listAllDirectors():
	if directors is None:
		flash("No director on the list. Let's add one")
	return render_template('index.html', directors = directors)

# Create new movie director
@app.route('/director/new', methods=['GET','POST'])
def newDirector():
	return render_template('newDirector.html')

# Update movie director information
@app.route('/director/<int:director_id>/edit', methods=['GET','POST'])
def editDirector(director_id):
	return render_template('editDirector.html', director = director)

# Read movie and director information
@app.route('/director/<int:director_id>/')
@app.route('/director/<int:director_id>')
def listDirector(director_id):
	return render_template('listDirector.html', director = director, movies = movies)

# Delete Movie director information
@app.route('/director/<int:director_id>/delete', methods=['GET','POST'])
def deleteDirector(director_id):
	return render_template('deleteDirector.html', director = director)

# list movies
@app.route('/movies/')
@app.route('/movies')
def listAllMovies():
	return render_template('listAllMovies.html', movies = movies)

# Create new movie
@app.route('/director/<int:director_id>/movie/new', methods=['GET','POST'])
def newMovie(director_id):
	return render_template('newMovie.html', director = director)

# Update movie information
@app.route('/director/<int:director_id>/movie/<int:movie_id>/edit',
			methods=['GET','POST'])
def editMovie(director_id, movie_id):
	return render_template('editMovie.html', movie = movie, director = director)

# Read movie information
@app.route('/director/<int:director_id>/movie/<int:movie_id>/')
@app.route('/director/<int:director_id>/movie/<int:movie_id>')
def listMovie(director_id, movie_id):
	return render_template('listMovie.html', movie = movie)

# Delete Movie information
@app.route('/director/<string:director_id>/movie/<string:movie_id>/delete',
			methods=['GET','POST'])
def deleteMovie(director_id, movie_id):
	return render_template('deleteMovie.html', movie = movie)

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 8000)