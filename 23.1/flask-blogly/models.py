"""Models for Blogly."""

# createdb blogly_db

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Default_Image_URL = 'https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/271deea8-e28c-41a3-aaf5-2913f5f48be6/de7834s-6515bd40-8b2c-4dc6-a843-5ac1a95a8b55.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzI3MWRlZWE4LWUyOGMtNDFhMy1hYWY1LTI5MTNmNWY0OGJlNlwvZGU3ODM0cy02NTE1YmQ0MC04YjJjLTRkYzYtYTg0My01YWMxYTk1YThiNTUuanBnIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.BopkDn1ptIwbmcKHdAOlYHyAOOACXW0Zfgbs0-6BY-E'


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

    image_url = db.Column(db.String(), nullable=False)

    def __repr__(self):
        """Show info about user"""

        u = self
        return f'<User {u.id} {u.first_name} {u.last_name} {u.image_url}>'
    
    def full_name(self):
        """Returns user's full name"""
        return f'<User {self.first_name} + ' ' + {self.last_name}>'
    
    # @property
    # def full_name(self):
    #     u = self
    #     return f"{self.first_name} {self.last_name}"
    
    # https: // www.python-course.eu/python3_properties.php
    


# 2021-08-26 21: 17: 13, 596 INFO sqlalchemy.engine.Engine
# CREATE TABLE users(
# 	id SERIAL NOT NULL,
# 	first_name VARCHAR(50) NOT NULL,
# 	last_name VARCHAR(50) NOT NULL,
# 	image_url VARCHAR(50),
# 	PRIMARY KEY(id)
# )

# You are now connected to database "blogly_db" as user "......".
# blogly_db =  # SELECT * FROM users;
# id | first_name | last_name | image_url
# ----+------------+-----------+-----------
# (0 rows)
