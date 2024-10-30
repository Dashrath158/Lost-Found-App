# models/User.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Store hashed passwords
    email = db.Column(db.String(120), unique=True, nullable=False)

    def save(self):
        """Save the user to the database."""
        try:
            db.session.add(self)
            db.session.commit()
        except:
            raise

    def __repr__(self):
        return f'<User {self.username}>'