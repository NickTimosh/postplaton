from . import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.tag_icons import EVENT_TAG_ICONS, RESOURCE_TAG_ICONS
# -------------------------------------------------------
# Association Tables (M2M)
# -------------------------------------------------------

event_eventtag = db.Table(
    "event_eventtag",
    db.Column("event_id", db.Integer, db.ForeignKey("event.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("event_tag.id"), primary_key=True)
)

resource_resourcetag = db.Table(
    "resource_resourcetag",
    db.Column("resource_id", db.Integer, db.ForeignKey("resource.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("resource_tag.id"), primary_key=True)
)

# -------------------------------------------------------
# Event Tags (topics: art, music, history)
# -------------------------------------------------------

class EventTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    icon = db.Column(db.String(10), nullable=True)  # <-- add this column


    def __repr__(self):
        return f"<EventTag {self.name}>"

# -------------------------------------------------------
# Resource Tags (categories: video, article, audio)
# -------------------------------------------------------

class ResourceTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    icon = db.Column(db.String(10), nullable=True)  # <-- add this column

    def __repr__(self):
        return f"<ResourceTag {self.name}>"

# -------------------------------------------------------
# Event
# -------------------------------------------------------

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    event_datetime = db.Column(db.DateTime, nullable=False)
    host = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)

    # Tags
    tags = db.relationship(
        "EventTag",
        secondary=event_eventtag,
        backref=db.backref("events", lazy="dynamic")
    )

    def __repr__(self):
        return f"<Event {self.title}>"

# -------------------------------------------------------
# User
# -------------------------------------------------------

class User(db.Model, UserMixin):
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

# -------------------------------------------------------
# Resource
# -------------------------------------------------------

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=True)
    title = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(500), nullable=False)

    # Relationship to event
    event = db.relationship(
        "Event",
        backref=db.backref("resources", lazy=True, cascade="all, delete-orphan")
    )

   # tag
    tag_id = db.Column(
        db.Integer,
        db.ForeignKey('resource_tag.id', name="fk_resource_tag_id"),  # constraint name here
        nullable=True
    )    
    tag = db.relationship("ResourceTag", backref=db.backref("resources", lazy=True))

    def __repr__(self):
        return f"<Resource {self.title}>"
