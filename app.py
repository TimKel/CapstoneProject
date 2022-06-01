from flask import Flask, request, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///skateparks'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)

########################################################################################
# Routes