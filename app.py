import os 
import requests
from flask import Flask, request, render_template, redirect, flash, jsonify, session, g 
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from models import bcrypt, db, connect_db, User, Skatepark
from forms import UserAddForm, UserEditForm, LoginForm, AddSkatepark

# from secret import APIkey 

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///skateparks'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "spotitsecrets")
toolbar = DebugToolbarExtension(app)

connect_db(app)
# db.drop_all()
db.create_all()

filename = 'apikey.txt'

def get_file_contents(filename):
    """Get contents of file"""
    try:
        with open(filename, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print("'%s' file not found" % filename)

APIkey = os.environ.get('APIkey', get_file_contents(filename))

########################################################################################
# Routes
########################################################################################

########################################################################################
# Create global user, login and logout routes
########################################################################################
@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

########################################################################################
# Sign-up, Edit Profile, Log In and Log Out 
########################################################################################

@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.
    If form not valid, present form.
    If the there already is a user with that username: flash message
    and re-present form.
    """
    if g.user:
        flash("You're already signed in.", "danger")
        return redirect('/')

    form = UserAddForm()

    flash("Why sign up? An account will allow you to add your own skate spots or parks to support and share amongst your local skate community.", 'warning')
    # if g.user in session:
    #     flash("You're already signed in.")
    #     return redirect('/')

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data,
                location=form.location.data
                
            )
            db.session.commit()
            flash(f"{user.username} successfully signed up", 'success')

        except IntegrityError:
            flash("Username already taken", 'danger') 
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    

    else:
        return render_template('users/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""
    if not g.user:
        flash("We're sorry, no one is currently signed in", "warning")
        return redirect('/login')
    session.pop(CURR_USER_KEY)
    flash("You've succesfully signed out", "success")
    return redirect('/login')


@app.route('/users/profile', methods=["GET", "POST"])
def edit_profile():
    """Update profile for current user."""

    if not g.user:
        flash("Access unauthorized. Please sign in.", "danger")
        return redirect("/")

    user = g.user 
    form = UserEditForm(obj=user)

    if form.validate_on_submit():
        if User.authenticate(user.username, form.password.data):
            user.username = form.username.data
            user.email = form.email.data 
            user.image_url = form.image_url.data
            user.location = form.location.data 
            user.password = form.password.data 

            db.session.commit()
            flash("Profile updated", "success")
            return redirect("/")
        
        flash("Wrong username or password. Please try again.", "danger")

    return render_template("/users/edit.html", form=form, user_id=user.id)


########################################################################################
# User Flow: Homepage, search parks, add parks and get directions 
########################################################################################

@app.route('/', methods=["GET"])
def homepage():
    
    return render_template('home.html')


@app.route('/', methods=["POST"])
def homepage_search():
    
    location = request.form["search"]
    search = Skatepark.query.filter(Skatepark.address.like('%{location}%'))
    return render_template('home.html', location=location, search=search)


@app.route('/search')
def all_parks():
    """Allows user to search all parks in DB"""
    skateparks = Skatepark.query.limit(20)
    key = APIkey
    api = requests.get(f"https://maps.googleapis.com/maps/api/staticmap?size=400x400&maptype=roadmap\&markers=size:mid%7Ccolor:red{{park.address}}&key={APIkey}")
    return render_template('search.html', skateparks=skateparks, api=api, key=key)

@app.route('/search', methods=["GET","POST"])
def list_parks():
    """Search all parks or specified location."""
    
    location = request.form["search"]
    if location == "":
        skateparks = Skatepark.query.limit(20)
        key = APIkey
        api = requests.get(f"https://maps.googleapis.com/maps/api/staticmap?size=400x400&maptype=roadmap\&markers=size:mid%7Ccolor:red{{park.address}}&key={APIkey}")
        return render_template('search.html', skateparks=skateparks, api=api, key=key)
    elif location != "":
        print(location)
        skateparks = Skatepark.query.filter(Skatepark.address.ilike(f'%{location}%')).limit(20)
        key = APIkey
        api = requests.get(f"https://maps.googleapis.com/maps/api/staticmap?size=400x400&maptype=roadmap\&markers=size:mid%7Ccolor:red{{park.address}}&key={APIkey}")
        if skateparks == [] or None:
            flash(f"Uh oh. No parks or spots added in this area. If you see something, add something!", "danger")
        return render_template('search.html', skateparks=skateparks, api=api, key=key)
    else:
        flash(f"Uh oh. No parks or spots added in this area. If you see something, add something!", "danger")
        print("$$$$$$$$$$$$$$$$$$$$$$$$$")
        print("UH OH")
        return render_template('search.html')


@app.route('/directions/<int:skatepark_id>', methods=["GET","POST"])
def show_park(skatepark_id):
    """Get directions to a park from current location"""

    skateparks = Skatepark.query.get_or_404(skatepark_id)
    spot = request.form["saddr"]
    print(spot)
    key = APIkey

    return render_template('directions.html', skateparks=skateparks, key=key, spot=spot)


@app.route('/addpark', methods=["GET", "POST"])
def add_park():
    """Allows logged in users to add skate spots or parks to database."""

    form = AddSkatepark()
    
    if not g.user:
        flash("Must be signed in to add a skatepark or skate spot.", "danger")
        return redirect("/")

    if form.validate_on_submit():
        try:
            skatepark = Skatepark(
                name=form.name.data,
                address=form.address.data,
                image_url=form.image_url.data,
                description=form.description.data
            )
            db.session.add(skatepark)
            db.session.commit()
            flash(f"{skatepark.name} successfully added", 'success')
        except IntegrityError:
            
            flash("Incorrect or false info. Please try again.", 'danger')
            
            return render_template('addpark.html', form=form)

        return redirect("/")

    else:
        return render_template('addpark.html', form=form)
