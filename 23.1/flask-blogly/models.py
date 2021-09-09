"""Models for Blogly."""

# createdb blogly_db

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# From solutions
Default_Image_URL = 'https://i.ytimg.com/vi/g8YbJ-1vCa0/hqdefault.jpg'


def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)

# User table
class User(db.Model):
    """User."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(30), nullable=False)

    last_name = db.Column(db.String(30), nullable=False)

    image_url = db.Column(db.String(), nullable=False, default=Default_Image_URL)
    
    posts = db.relationship("Post", backref="user", cascade="all, delete")

    # def __repr__(self):
    #     """Show info about user"""

    #     u = self
    #     return f'<User {u.id} {u.first_name} {u.last_name}>'
    
    # @property
    # def full_name(self):
    #     """Returns user's full name"""
    #     user = self
    #     return f"<User {user.first_name} {user.last_name}>"
    
    
    # https: // www.python-course.eu/python3_properties.php
    

################################################################
# Post table
# https: // flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/
class Post(db.Model):
    #Post
    __tablename__ = "posts"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    title = db.Column(db.Text(), nullable=False)
    
    content = db.Column(db.Text(), nullable=False)
    
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.now())
    
    
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"),
                        nullable=False)
    
    # user = db.relationship('Users')

    
    def __repr__(self):
        """Show info about post"""
        
        # p = self
        return f"<Post {self.id} {self.title} {self.content} {self.created_at}>"
    

    # def format_date(self):
    #     return f"<Create by {self.first_name} {self.last_name} at {self.created_at}>"
    
    #From solutions
    @property
    def format_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%B %d, %Y at %-I:%M %p")

    #    https://www.codegrepper.com/code-examples/python/datetime+utcnow+python 
    
    
    
#############################################################################
#Part 3: M2M relationships


class Tag(db.Model):
    """Tag table"""
    __tablename__ = "tags"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text(), nullable=False, unique=True)
    #Through relationships
    # posts = db.relationship("Post", backref="tags", cascade="all, delete")
    posts = db.relationship("Post", secondary="posts_tags", backref="tags")
    
    def __repr__(self):
        """Show info about tags"""
        return f"<Tag {self.id} {self.name}"
    
    class PostTag(db.Model):
        """Mapping post tags"""
        __tablename__= "posts_tags"
        post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True)
        tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)
        
        def __repr__(self):
            """Show info about post tags"""
            return f"<PostTag{self.post_id} {self.tag_id}"
        