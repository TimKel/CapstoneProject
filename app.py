import os 
import requests
from flask import Flask, request, render_template, redirect, flash, jsonify, session, g 
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from models import bcrypt, db, connect_db, User, Skatepark
from forms import UserAddForm, UserEditForm, LoginForm, AddSkatepark

from secret import APIkey 

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///skateparks'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)
# db.drop_all()
db.create_all()
########################################################################################
# Routes
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



@app.route('/')
def homepage():
    
    return render_template('home.html')


@app.route('/search', methods=["POST"])
def list_parks():
    """Show a message."""

    skateparks = Skatepark.query.all()
    return render_template('search.html', skateparks=skateparks)


@app.route('/search/<int:skatepark_id>', methods=["GET"])
def show_park(skatepark_id):
    """Show a message."""

    skateparks = Skatepark.query.get_or_404(skatepark_id)
    return render_template('search.html', skateparks=skateparks)



# @app.route('/search', methods=["POST"])
# def search_parks():

#     search = request.form['search']
#     res = requests.get(f"https://maps.googleapis.com/maps/api/place/findplacefromtext/output?parameters")
#     print(search)
#     return render_template('search.html', search=search)



@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.
    If form not valid, present form.
    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = UserAddForm()

    flash("Why sign up? Future features include adding your own skate spots as our community grows. As members contribute, the skate community will have access to the best spots all around the world!", 'warning')
    if g.user in session:
        flash("You're already signed in.")
        return redirect('/')

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


@app.route('/users/delete', methods=["DELETE"])
def delete_user():
    """Delete user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    
    do_logout()

    db.session.delete(g.user)
    db.session.commit()
    flash("Profile Deleted", "danger")
    return redirect("/signup")

@app.route('/addpark', methods=["GET", "POST"])
def add_park():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.
    If form not valid, present form.
    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = AddSkatepark()
    
    if not g.user:
        flash("Must be signed in to add a skatepark.", "danger")
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


@app.route('/')
def homepage_selection():
    """Show homepage:

    - anon users: no messages
    - logged in: 100 most recent messages of followed_users
    """

    if g.user in session:
        
        return render_template('home.html')

    else:
        return render_template('home-anon.html')