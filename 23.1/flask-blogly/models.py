"""Models for Blogly."""

# createdb blogly_db

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)

# User table
class User(db.Model):
    """User."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.Text(), nullable=False)

    last_name = db.Column(db.Text(), nullable=False)

    image_url = db.Column(db.Text(), nullable=True)

    def __repr__(self):
        """Show info about user"""

        u = self
        return f"<User {u.id} {u.first_name} {u.last_name} {u.image_url}>"
    
    # def full_name(self):
    #     """Returns user's full name"""
    #     return f"{self.first_name} {self.last_name}"
    
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
