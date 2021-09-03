"""Models for Blogly."""

# createdb blogly_db

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# From solutions
Default_Image_URL = 'https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/271deea8-e28c-41a3-aaf5-2913f5f48be6/de7834s-6515bd40-8b2c-4dc6-a843-5ac1a95a8b55.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzI3MWRlZWE4LWUyOGMtNDFhMy1hYWY1LTI5MTNmNWY0OGJlNlwvZGU3ODM0cy02NTE1YmQ0MC04YjJjLTRkYzYtYTg0My01YWMxYTk1YThiNTUuanBnIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.BopkDn1ptIwbmcKHdAOlYHyAOOACXW0Zfgbs0-6BY-E'


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
    # datetime.utcnow())
    
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
    
