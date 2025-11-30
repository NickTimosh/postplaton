from flask import Blueprint, render_template
from app.models import Event
from . import db

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return render_template("index.html", title="Home")

@main.route("/events")
def events():
    all_events = Event.query.all()

    return render_template("events.html", events=all_events, title="Events")

@main.route("/events/<int:event_id>")
def event_detail(event_id):
    
    event = Event.query.get(event_id)

    if not event:
        return "Event not found", 404
    
    return render_template("event_detail.html", event=event, title=event.title)
