"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)
    
#Models
    
    class User(db.Model):
        __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.column(db.Text, nullable=False)
    
    last_name = db.column(db.Text, nullable=False)
    
    image_url = db.column(db.text, nullable=False)
    
    