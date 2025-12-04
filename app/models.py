from . import db
from datetime import datetime

# --- Tag table ---
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    icon = db.Column(db.String(16), nullable=True)

    def __repr__(self):
        return f"<Tag {self.name}>"

# --- Event tags ---
class EventTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), nullable=False)

    def __repr__(self):
        return f"<EventTag event={self.event_id} tag={self.tag_id}>"


class EventResource(db.Model):
    __tablename__ = 'event_resource'  # explicit table name
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(500), nullable=False)

    event = db.relationship('Event', backref=db.backref('resources', lazy=True, cascade="all, delete-orphan"))

    def __repr__(self):
        return f"<EventResource {self.title} for Event {self.event_id}>"
    
# --- Resource tags ---
class ResourceTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resource_id = db.Column(db.Integer, db.ForeignKey('event_resource.id'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), nullable=False)

    def __repr__(self):
        return f"<ResourceTag resource={self.resource_id} tag={self.tag_id}>"

# --- Existing models ---

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    event_datetime = db.Column(db.DateTime, nullable=False)
    host = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Event {self.title}>"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    is_host = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}, host={self.is_host}>"

