"""Blogly application."""

from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, request, render_template, redirect, session
from models import db, connect_db, User

# createdb blogly_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "0111001101100101011"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def redirect_to_users():
    """Redirects to users"""
    return redirect('/users')

@app.route('/users')
def list_users():
    """List users"""
    
    users = User.query.all()
    return render_template('user_list.html', users=users)

# @app.route('/', methods=["POST"])
# def create_user():
#     return "Your added you info"

# @app.route('/<int:user_id>')
# def show_user(user_id):
#     """Show details about a single user"""
#     user = User.query.get(user_id)
#     # return f"<h1>{user.first_name}</h1>"
#     user = User.query.get_or_404(user_id)
#     return render_template('user_details.html', user=user)
    
    
    
# @app.route('/'):
#     def
# @app.route('/'):
#     def
# @app.route('/'):
#     def
# @app.route('/'):
#     def
# @app.route('/'):
#     def
# @app.route('/'):
#     def


