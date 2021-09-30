"""Blogly application."""
# https: // docs.sqlalchemy.org/en/14/core/sqlelement.html  # sqlalchemy.sql.expression.ColumnOperators.in_
import os
import datetime
from operator import and_
from flask import Flask, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag

import pdb


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URL'] = os.environ.get(
    'DATABASE_URL','postgresql:///blogly_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get('API_KEY')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def redirect_to_users():
    """Redirects to list of users"""
    return redirect('/users')

@app.errorhandler(404)
def not_found(e):
    return render_template('404_page.html'), 404

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
    tags = Tag.query.all()
    # pdb.set_trace()
    # post = Post.query.get_or_404(post_id)
    return render_template('new_post_form.html', user=user, tags=tags)

    
@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    """Handle add form; add post and redirect to the user detail page"""
    user = User.query.get_or_404(user_id)
    title = request.form['title']
    content = request.form['content']
    # tag_ids = request.form.getlist('tags')
    # tags = Tag.query(Tag).filter(and_(Tag.ids == tag_ids)).first()
    tag_ids = [int(num) for num in request.form.getlist('tags')]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    
    new_post = Post(user=user, title=title, content=content, tags=tags )
    db.session.add(new_post)
    db.session.commit()
    return redirect(f'/users/{user_id}')

    # return render_template('edit_post.html', user=user)
    
    
@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Shows post detail page"""
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)
    # pdb.set_trace()
    return render_template('post_details.html', post=post, user=user)
    
    
@app.route('/posts/<int:post_id>/edit')
def show_form(post_id):
    """Show form to edit a post, and to cancel (back to user page)"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('edit_post.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def handle_post(post_id):
    """Handle editing of a post. Redirect back to the post view"""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    
    # tag_ids = request.form.getlist('tags')
    # tags = Tag.query(Tag).filter(and_(Tag.ids == tag_ids)).first()
    #From solutions
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    # post.created_at = datetime.now()
    
    db.session.add(post)
    db.session.commit()
    # pdb.set_trace()
    return redirect(f'/users/{post.user_id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Delete post"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{post.user_id}')


#######################################################
#Adding tags

@app.route('/tags')
def list_tags():
    """List all tags with links to the tag detail page"""
    tags = Tag.query.all()
    return render_template('list_tags.html', tags=tags)
    # return render_template('tag_detail.html', tags=tags)
    
    
@app.route('/tags/<int:tag_id>')
def tag_detail(tag_id):
    """Shows page detailing a specific tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag_detail.html', tag=tag)


@app.route('/tags/new')
def add_new_tag():
    """Shows form to add a new tag"""
    # posts = Post.query.all()
    return render_template('add_tag.html')


@app.route('/tags/new', methods=['POST'])
def post_new_tag():
    """Process add form, adds tag, and redirect to tag list"""
    # request.form.getlist('key')
    #.getlist sends 'key' multiple times and returns a list of values. get only returns the first value
    # name = request.form.getlist('name')
    # name = request.form('name')
    post_ids = request.form.getlist('posts')
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(tag)
    db.session.commit()
    # pdb.set_trace()
    # return render_template('list_tags.html', tag=tag)

    return redirect('/tags')


@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    """"Show edit form for a tag"""
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('edit_tag.html', tag=tag, posts=posts)


@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def post_edit_tag(tag_id):
    """"Process edit form, edit tag, and redirects to the tags list"""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    #From solution
    post_ids = request.form.getlist('posts')
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    
    return redirect('/tags')


@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    """Delete a tag"""
    tag = Tag.query.get_or_404(tag_id)
    
    db.session.delete(tag)
    db.session.commit()
    
    return redirect(f'/tags')
    

    

    




#Notes:
# request.args: the key/value pairs in the URL query string
# request.form: the key/value pairs in the body, from a HTML post form, or JavaScript request that isn't JSON encoded
# request.files: the files in the body, which Flask keeps separate from form. HTML forms must use enctype =multipart/form-data or files will not be uploaded.
# request.values: combined args and form, preferring args if keys overlap
# All of these are MultiDict instances. You can access values using:

# request.form['name']: use indexing if you know the key exists
# request.form.get('name'): use get if the key might not exist
# request.form.getlist('name'): use getlist if the key is sent multiple times and you want a list of values. getlist only returns the first value.
#https://www.sistemasagiles.com.ar/examples/global/vars/request/getlist
