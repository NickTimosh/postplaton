from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.models import Event
from app import db
from app.forms import EventForm

events_bp = Blueprint("events", __name__, url_prefix="/events")

# List all Events
@events_bp.route("/")
def events_list():
    all_events = Event.query.all()
    return render_template("events.html", events=all_events, title="Events")

# Event detail page
@events_bp.route("/<int:event_id>")
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template("event_detail.html", event=event, title=event.title)

# Create new event
@events_bp.route("/new", methods=["GET", "POST"])
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        new_event = Event(
            title=form.title.data,
            date=form.date.data,
            host=form.host.data,
            description=form.description.data
        )
        db.session.add(new_event)
        db.session.commit()
        flash("Event created successfully!")
        return redirect(url_for("events.events_list"))
    return render_template("event_form.html", form=form, title="Create Event")

# Edit existing event
@events_bp.route("/<int:event_id>/edit", methods=["GET", "POST"])
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    form = EventForm(obj=event)  # pre-fill form with current data
    if form.validate_on_submit():
        event.title = form.title.data
        event.date = form.date.data
        event.host = form.host.data
        event.description = form.description.data
        db.session.commit()
        flash("Event updated successfully!")
        return redirect(url_for("events.event_detail", event_id=event.id))
    return render_template("event_form.html", form=form, title="Edit Event")

# Delete event
@events_bp.route("/<int:event_id>/delete", methods=["POST"])
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash("Event deleted successfully!")
    return redirect(url_for("events.events_list"))