from . import db
from datetime import datetime

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    event_datetime = db.Column(db.DateTime, nullable=False) 
    host = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f"<Event {self.title}>"

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    is_host = db.Column(db.Boolean, default=False)  # Only hosts can log in

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}, host={self.is_host}>"
    
class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=True)
    title = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(500), nullable=False)

    event = db.relationship('Event', backref=db.backref('resources', lazy=True, cascade="all, delete-orphan"))

    def __repr__(self):
        return f"<Resource {self.title} for Event {self.event_id}>"
