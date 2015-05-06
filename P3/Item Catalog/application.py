'''Movie Director App
    Created by Linus Dong April 22nd 2015
'''
from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask import flash, send_from_directory

from flask import session as login_session
import random
import string

# IMPORTS FOR LOGIN
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
from oauth2client.client import AccessTokenCredentials
import httplib2
import json
from flask import make_response
import requests
from functools import wraps

# IMPORTS FOR ATOMFEED
from urlparse import urljoin
from werkzeug.contrib.atom import AtomFeed
import db_helper


app = Flask(__name__)
# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Linus Movie App"


# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    print request.url
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


# http://flask.pocoo.org/snippets/3/
def csrf_protect(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == "POST":
            token = login_session.pop('_csrf_token', None)
            if not token or token != request.form.get('_csrf_token'):
                response = make_response(json.dumps("Token's doesn't match "
                                                    "given session token."),
                                         401)
                response.headers['Content-Type'] = 'application/json'
                return response
        return f(*args, **kwargs)
    return decorated_function


def generate_csrf_token():
    if '_csrf_token' not in login_session:
        token = ''.join(random.choice(string.ascii_uppercase
                        + string.digits) for x in xrange(32))
        login_session['_csrf_token'] = token
    return login_session['_csrf_token']

app.jinja_env.globals['csrf_token'] = generate_csrf_token


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in login_session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function


# Url helper functions
def make_external(url):
    """Generate full path URL for external use.
    Args:
        url: internal URL.
    Return:
        A string with full path URL.
    """
    return urljoin(request.url_root, url)


def check_creator(user_id):
    '''helper function to check original creator
    Return:
        False, redirect to index page if not match
    '''
    creator = db_helper.get_user_info(user_id)
    if creator.id != login_session['user_id']:
        flash("ERROR, the information is not belong to "
              "{name}.".format(name=login_session['username']))
        return False
    return True


# Create anti-forgery state token
@app.route('/login')
def show_login():
    state = ''.join(random.choice(string.ascii_uppercase
                    + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data.decode('utf-8')

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the'
                                            'authorization code.'), 401)
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
        response = make_response(json.dumps("Token's user ID doesn't match "
                                            "given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Token's client ID does not "
                                            "match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already '
                                            'connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['provider'] = 'google'
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    # replace full crediential object
    credentials = AccessTokenCredentials(login_session['credentials'],
                                         'user-agent-value')

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['image'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = db_helper.get_user_id(login_session['email'])
    if not user_id:
        user_id = db_helper.create_user(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['image']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("You are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    credentials = AccessTokenCredentials(login_session['credentials'],
                                         'user-agent-value')
    if credentials is None:
        response = make_response(json.dumps('Current user not '
                                            'connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    reason = h.request(url, 'GET')[1]
    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['credentials']
        del login_session['gplus_id']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(json.dumps('Failed to revoke token for given '
                                            'user. reason: '
                                            '{reason}'.format(reason=reason),
                                 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/director/<int:director_id>/movie/<int:movie_id>/JSON')
def movie_json(director_id, movie_id):
    movie = db_helper.get_movie(movie_id)
    return jsonify(movie=movie.serialize)


@app.route('/director/<int:director_id>/movies/JSON')
def director_movies_json(director_id):
    movies = db_helper.get_movies_by_director(director_id)
    return jsonify(movies=[m.serialize for m in movies])


@app.route('/directors/JSON')
def directors_json():
    directors = db_helper.get_directors()
    return jsonify(directors=[d.serialize for d in directors])


@app.route('/recent.atom')
def recent_feed():
    movies = db_helper.get_recent_movies()
    feed = AtomFeed('Recent Movies',
                    feed_url=request.url, url=request.url_root)
    for movie in movies:
        movie_url = 'director/{director_id}/movie/''{movie_id}'\
                    .format(director_id=movie.director_id, movie_id=movie.id)
        rendered_text = movie.description
        feed.add(movie.name, unicode(rendered_text),
                 content_type='html',
                 trailer=movie.trailer,
                 url=make_external(movie_url),
                 updated=movie.last_update)
    return feed.get_response()


# list movie directors
@app.route('/')
@app.route('/directors/')
@app.route('/directors')
def list_all_directors():
    directors = db_helper.get_directors()
    if 'user_id' not in login_session:
        user = None
    else:
        user = db_helper.get_user_info(login_session['user_id'])
        directors = db_helper.get_directors_by_creator_id(user.id)
    if not directors:
        flash("No director on the list. Let's add one")
    return render_template('index.html', directors=directors, user=user)


# Create new movie director
@app.route('/director/new', methods=['GET', 'POST'])
@login_required
def new_director():
    if request.method == 'POST':
        db_helper.create_director(login_session, request)
        flash("New Director Created!")
        return redirect(url_for('list_all_directors'))
    else:
        return render_template('newDirector.html')


# Update movie director information
@app.route('/director/<int:director_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_director(director_id):
    edited_director = db_helper.get_director(director_id)
    if request.method == 'POST':
        i_amcreator = check_creator(edited_director.user_id)
        if i_amcreator is not True:
            return redirect(url_for('list_all_directors'))
        edited_director = db_helper.edit_director(request, director_id)
        flash("Director Edited Successfully!")
        return redirect(url_for('list_director', director_id=director_id))
    else:
        return render_template('editDirector.html', director=edited_director)


# Read movie and director information
@app.route('/director/<int:director_id>/')
@app.route('/director/<int:director_id>')
def list_director(director_id):
    director = db_helper.get_director(director_id)
    movies = db_helper.get_movies_by_director(director_id)
    if not movies:
        flash("No movie on the list. Let's add one")
    if 'user_id' not in login_session:
        user = None
    else:
        user = "user is logined."
        i_amcreator = check_creator(director.user_id)
        if i_amcreator is not True:
            return redirect(url_for('list_all_directors'))
    return render_template('listDirector.html', director=director,
                           movies=movies, user=user)


# Delete Movie director information
@app.route('/director/<int:director_id>/delete', methods=['GET', 'POST'])
@login_required
@csrf_protect
def delete_director(director_id):
    director_to_delete = db_helper.get_director(director_id)
    i_amcreator = check_creator(director_to_delete.user_id)
    if i_amcreator is not True:
        return redirect(url_for('list_all_directors'))
    if request.method == 'POST':
        db_helper.delete_movies_by_director(director_id)
        director_to_delete = db_helper.delete_director(director_id)
        flash("Director Delete Successfully!")
        return redirect(url_for('list_all_directors'))
    else:
        return render_template('deleteDirector.html', director=director_to_delete)


# Create new movie
@app.route('/director/<int:director_id>/movie/new', methods=['GET', 'POST'])
@login_required
def new_movie(director_id):
    if request.method == 'POST':
        db_helper.new_movie(director_id, request, login_session)
        flash("Movie Created Successfully!")
        return redirect(url_for('list_director', director_id=director_id))
    else:
        return render_template('newMovie.html', director_id=director_id)


# Update movie information
@app.route('/director/<int:director_id>/movie/<int:movie_id>/edit',
           methods=['GET', 'POST'])
@login_required
def edit_movie(director_id, movie_id):
    edited_movie = db_helper.get_movie(movie_id)
    if request.method == 'POST':
        i_amcreator = check_creator(edited_movie.user_id)
        if i_amcreator is not True:
            return redirect(url_for('list_all_directors'))
        edited_movie = db_helper.edit_movie(movie_id, request)
        flash("Movie Edited Successfully!")
        return redirect(url_for('list_movie', director_id=director_id,
                                movie_id=movie_id))
    else:
        return render_template('editMovie.html', movie=edited_movie)


# Read movie information
@app.route('/director/<int:director_id>/movie/<int:movie_id>/')
@app.route('/director/<int:director_id>/movie/<int:movie_id>')
def list_movie(director_id, movie_id):
    director = db_helper.get_director(director_id)
    movie = db_helper.get_movie(movie_id)
    if 'user_id' not in login_session:
        user = None
    else:
        user = "user is logined."
        i_amcreator = check_creator(movie.user_id)
        if i_amcreator is not True:
            return redirect(url_for('list_all_directors'))
    return render_template('listMovie.html', movie=movie, director=director,
                           user=user)


# Delete Movie information
@app.route('/director/<string:director_id>/movie/<string:movie_id>/delete',
           methods=['GET', 'POST'])
@login_required
@csrf_protect
def delete_movie(director_id, movie_id):
    movie_to_delete = db_helper.get_movie(movie_id)
    i_amcreator = check_creator(movie_to_delete.user_id)
    if i_amcreator is not True:
        return redirect(url_for('list_all_directors'))
    if request.method == 'POST':
        movie_to_delete = db_helper.delete_movie(movie_id)
        flash("Movie Deleted Successfully!")
        return redirect(url_for('list_director', director_id=director_id))
    else:
        return render_template('deleteMovie.html', movie=movie_to_delete)


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
        del login_session['username']
        del login_session['email']
        del login_session['image']
        del login_session['user_id']
        del login_session['provider']
        flash("You have been logged out.")
        return redirect(url_for('list_all_directors'))
    else:
        flash("You were not logged in")
        return redirect(url_for('list_all_directors'))

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
