"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)
    
#Models
    
class User(db.Model):
        """User."""
        __tablename__ = 'users'
        
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)

        first_name = db.column(db.Text(50), nullable=False)
    
        last_name = db.column(db.Text(50), nullable=False)
    
        image_url = db.column(db.Text(50), nullable=True)
    
    
        def __repr__(self):
            """Show info about user"""
        
            u = self
            return f"<User {u.id} {u.first_name} {u.last_name} {u.image_url}>"
    
