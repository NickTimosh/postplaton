from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from datetime import date, timedelta
from app.models import Event
from app import db
from app.forms import EventForm
from flask_login import login_required, current_user

events_bp = Blueprint("events", __name__, url_prefix="/events")


# ----------------------------
# Grouping logic (updated)
# ----------------------------
def group_events(events):
    """Group events into Today, This Week, Next 30 Days using datetime."""
    
    today = date.today()
    end_of_week = today + timedelta(days=7)
    next_30 = today + timedelta(days=30)

    groups = {
        "Today": [],
        "This Week": [],
        "Next 30 Days": []
    }

    for e in events:
        event_date = e.event_datetime.date()

        if event_date == today:
            groups["Today"].append(e)
        elif today < event_date <= end_of_week:
            groups["This Week"].append(e)
        elif end_of_week < event_date <= next_30:
            groups["Next 30 Days"].append(e)

    return groups


# ----------------------------
# Events list
# ----------------------------
@events_bp.route("/")
def events_list():
    all_events = Event.query.order_by(Event.event_datetime.asc()).all()

    # Add end_datetime = start + 1 hour
    for e in all_events:
        e.end_datetime = e.event_datetime + timedelta(hours=2)

    grouped = group_events(all_events)

    return render_template(
        "events.html",
        title="Events",
        groups=grouped
    )


# ----------------------------
# Event detail page
# ----------------------------
@events_bp.route("/<int:event_id>")
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template("event_detail.html", event=event, title=event.title)


# ----------------------------
# Create new event
# ----------------------------
@events_bp.route("/new", methods=["GET", "POST"])
@login_required
def create_event():

    if not current_user.is_host:
        abort(403)

    form = EventForm()

    if form.validate_on_submit():

        new_event = Event(
            title=form.title.data,
            event_datetime=form.event_datetime.data,
            host=form.host.data,
            description=form.description.data,
        )

        db.session.add(new_event)
        db.session.commit()

        flash("Event created successfully!")
        return redirect(url_for("events.events_list"))

    return render_template("event_form.html", form=form, title="Create Event")


# ----------------------------
# Edit existing event
# ----------------------------
@events_bp.route("/<int:event_id>/edit", methods=["GET", "POST"])
@login_required
def edit_event(event_id):

    if not current_user.is_host:
        abort(403)

    event = Event.query.get_or_404(event_id)
    form = EventForm(obj=event)

    if form.validate_on_submit():

        event.title = form.title.data
        event.event_datetime = form.event_datetime.data
        event.host = form.host.data
        event.description = form.description.data

        db.session.commit()
        flash("Event updated successfully!")

        return redirect(url_for("events.event_detail", event_id=event.id))

    return render_template("event_form.html", form=form, title="Edit Event")


# ----------------------------
# Delete event
# ----------------------------
@events_bp.route("/<int:event_id>/delete", methods=["POST"])
@login_required
def delete_event(event_id):

    if not current_user.is_host:
        abort(403)

    event = Event.query.get_or_404(event_id)

    db.session.delete(event)
    db.session.commit()

    flash("Event deleted successfully!")
    return redirect(url_for("events.events_list"))
