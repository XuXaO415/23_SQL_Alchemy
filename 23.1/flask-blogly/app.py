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
    """Redirects to list of users"""
    return redirect('/users')

@app.route('/users', methods=["GET"])
def list_users():
    """List users"""
    users = User.query.all()
    return render_template('user_list.html', users=users)

@app.route('/users/new', methods=["GET"])
def show_user_form():
    """Shows add form to users"""
    return render_template('new_user_form.html')

@app.route('/users/new', methods=['POST'])
def add_new_user():
    """Process add form and add user"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url'] or None
    
    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    
    db.session.add(user)
    db.session.commit()
    return redirect('/users')
    

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show details about a single given user"""
    # user = User.query.get(user_id)
    # return f"<h1>{user.first_name}</h1>"
    user = User.query.get_or_404(user_id)
    return render_template('user_details.html', user=user)
    
    
@app.route('/users/<int:user_id>/edit')
def display_user_edit(user_id):
    """show edit page to user"""
    user = User.query.get_or_404(user_id)
    return render_template('edit_page.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def post_user_edit(user_id):
    """Process the edit form, returning the user to the /users page."""
    u = User.query.get_or_404(user_id)
    u.first_name = request.form['first_name']
    u.last_name = request.form['last_name']
    u.image_url = request.form['image_url']
    
    db.session.add(u)
    db.session.commit()
    
    return redirect('/users')
    

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete the user."""
    u = User.query.get_or_404(user_id)
    
    db.session.delete(u)
    db.session.commit()
    
    return redirect('/users')
    




