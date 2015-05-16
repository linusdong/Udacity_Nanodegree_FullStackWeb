'''DB helper function
    Created by Linus Dong May 2nd 2015
'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Director, Base, Movie, User
import datetime
import re
import os
from werkzeug import secure_filename
import random
import string


engine = create_engine('postgresql://catalog:udacity@localhost/catalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
UPLOAD_URL = '/uploads/'


# rename given filename to prevent duplicate name
def create_unique_name(filename):
    random_string = ''.join(random.choice(string.ascii_uppercase
                                          + string.digits) for x in range(8))
    filename = random_string + '_' + filename
    return filename


# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# Extract the youtube ID from the url
def get_youtube_id(youtube_url):
    youtube_id = re.search(r'(?<=v=)[^&#]+', youtube_url)
    youtube_id = youtube_id or re.search(r'(?<=be/)[^&#]+',
                                         youtube_url)
    youtube_id = youtube_id or re.search(r'(?<=embed/)[^&#]+',
                                         youtube_url)
    trailer_youtube_id = youtube_id.group(0) if youtube_id else None
    return trailer_youtube_id


def create_user(login_session):
    now = datetime.datetime.now()
    new_user = User(name=login_session['username'],
                    image=login_session['image'],
                    email=login_session['email'],
                    create_date=now, last_update=now)
    session.add(new_user)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def get_user_info(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def get_user_id(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return


def get_directors():
    directors = session.query(Director).all()
    return directors


def get_directors_by_creator_id(user_id):
    directors = session.query(Director).filter_by(user_id=user_id).all()
    return directors


def get_director(director_id):
    director = session.query(Director).filter_by(id=director_id).one()
    return director


def create_director(login_session, request):
    now = datetime.datetime.now()
    if request.files['image']:
        # Get the name of the uploaded file
        file = request.files['image']
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
            # prevent duplicated name
            new_name = create_unique_name(filename)
            # Move the file form the temporal folder to
            # the upload folder we setup
            file.save(os.path.join(UPLOAD_FOLDER, new_name))
            url = '{url}{filename}'.format(url=UPLOAD_URL, filename=new_name)
    new_director = Director(create_date=now, last_update=now,
                            user_id=login_session['user_id'],
                            name=request.form['name'],
                            image=url,
                            bio=request.form['bio'])
    session.add(new_director)
    session.commit()
    return True


def edit_director(request, director_id):
    edited_director = get_director(director_id)
    if request.form['name']:
        edited_director.name = request.form['name']
    if request.files['image']:
        # Get the name of the uploaded file
        file = request.files['image']
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
            # prevent duplicated name
            new_name = create_unique_name(filename)
            # Move the file form the temporal folder to
            # the upload folder we setup
            file.save(os.path.join(UPLOAD_FOLDER, new_name))
            url = '{url}{filename}'.format(url=UPLOAD_URL, filename=new_name)
            edited_director.image = url
    if request.form['bio']:
        edited_director.bio = request.form['bio']
    now = datetime.datetime.now()
    edited_director.last_update = now
    session.add(edited_director)
    session.commit()
    return edited_director


def delete_director(director_id):
    deleted_director = session.query(Director).filter_by(id=director_id).one()
    session.delete(deleted_director)
    session.commit()


def get_movie(movie_id):
    movie = session.query(Movie).filter_by(id=movie_id).one()
    return movie


def get_movies_by_director(director_id):
    movies = session.query(Movie).filter_by(director_id=director_id).all()
    return movies


def get_recent_movies():
    movies = session.query(Movie).order_by(Movie.create_date.desc())\
                    .limit(15).all()
    return movies


def new_movie(director_id, request, login_session):
    trailer_id = get_youtube_id(request.form['trailer'])
    now = datetime.datetime.now()
    if request.files['image']:
        # Get the name of the uploaded file
        file = request.files['image']
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
            # prevent duplicated name
            new_name = create_unique_name(filename)
            # Move the file form the temporal folder to
            # the upload folder we setup
            file.save(os.path.join(UPLOAD_FOLDER, new_name))
            url = '{url}{filename}'.format(url=UPLOAD_URL, filename=new_name)
    new_movie = Movie(create_date=now, last_update=now,
                      user_id=login_session['user_id'],
                      name=request.form['name'],
                      image=url,
                      trailer=trailer_id,
                      description=request.form['description'],
                      director_id=director_id)
    session.add(new_movie)
    session.commit()
    return True


def edit_movie(movie_id, request):
    edited_movie = get_movie(movie_id)
    if request.form['name']:
        edited_movie.name = request.form['name']
    if request.files['image']:
        # Get the name of the uploaded file
        file = request.files['image']
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
            # prevent duplicated name
            new_name = create_unique_name(filename)
            # Move the file form the temporal folder to
            # the upload folder we setup
            file.save(os.path.join(UPLOAD_FOLDER, new_name))
            url = '{url}{filename}'.format(url=UPLOAD_URL, filename=new_name)
        edited_movie.image = url
    if request.form['description']:
        edited_movie.description = request.form['description']
    if request.form['trailer']:
        trailer_id = get_youtube_id(request.form['trailer'])
        edited_movie.trailer = trailer_id
    now = datetime.datetime.now()
    edited_movie.last_update = now
    session.add(edited_movie)
    session.commit()
    return edited_movie


def delete_movie(movie_id):
    deleted_movie = session.query(Movie).filter_by(id=movie_id).one()
    session.delete(deleted_movie)
    session.commit()
    return deleted_movie


def delete_movies_by_director(director_id):
    deleted_movies = get_movies_by_director(director_id)
    for movie in deleted_movies:
        session.delete(movie)
    session.commit
    return True
