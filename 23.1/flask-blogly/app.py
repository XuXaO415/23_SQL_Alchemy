"""Blogly application."""


from flask import Flask, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post
# import pdb


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

@app.route('/users')
def list_users():
    """List users"""
    users = User.query.all()
    return render_template('user_list.html', users=users)

@app.route('/users/new')
def show_user_form():
    """Shows form to users"""
    return render_template('new_user_form.html')

# From solutions 
@app.route('/users/new', methods=['POST'])
def add_new_user():
    """Process form; add user"""
  
    first_name = request.form['first_name'],
    last_name = request.form['last_name'],
    image_url = request.form['image_url'] or None 

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    
    db.session.add(new_user)
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
    # user = User.query.filter().all()
    return render_template('edit_page.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def post_user_edit(user_id):
    """Process the edit form, returning the user to the /users page."""
    user = User.query.get_or_404(user_id)
    # pdb.set_trace()
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']
    
    # user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    
    db.session.add(user)
    db.session.commit()
    
    return redirect('/users')
    

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete the user."""
    user = User.query.get_or_404(user_id)
    
    db.session.delete(user)
    db.session.commit()    

    
    return redirect('/users')


################################################################
#Part Two: Adding Posts

@app.route('/users/<int:user_id>/posts/new')
def show_post_form(user_id):
    """Show form to add user's post"""
    user = User.query.get_or_404(user_id)
    # pdb.set_trace()
    return render_template('add_post_form.html', user=user)

    
@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    """Handle add form; add post and redirect to the user detail page"""
    user = User.query.get_or_404(user_id)
    
    title = request.form['title']
    content = request.form['content']
    
    new_post = Post(title=title, content=content, user=user)
    
    db.session.add(new_post)
    db.session.commit()
    return redirect(f'/users/{user_id}')
    
    
@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Shows post detail page"""
    post = Post.query.get_or_404(post_id)
  
    return render_template('', post=post)
    
    

    
# @app.route('/posts/<int:post_id>/edit')
# def show_form(post_id):
#     """Show form to edit a post, and to cancel (back to user page)"""
#     post = Post.query.get_or_404(post_id)
#     return render_template(post=post)


# @app.route('/posts/<int:post_id>/edit', methods=['POST'])
# def handle_post(post_id):
#     """Handle editing of a post. Redirect back to the post view"""
#     post = Post.query.get_or_404(post_id)
#     post.title = request.form['title']
#     post.content = request.form['content']
#     db.session.add(post)
#     db.session.commit()
    
#     return redirect('/users/{post')

# @app.route('/posts/<int:post_id>/delete', methods=['POST'])
# def delete_post():
#     """Delete post"""





