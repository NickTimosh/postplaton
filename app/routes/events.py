from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from datetime import date, datetime, timedelta
from app.models import Event, EventTag
from app import db
from app.forms import EventForm
from flask_login import login_required, current_user

events_bp = Blueprint("events", __name__, url_prefix="/events")

# ----------------------------
# Grouping logic
# ----------------------------
def group_events(events):
    """Group events into Today, This Week, Next 30 Days using Kyiv time."""

    today = datetime.now().date()
    end_of_week = today + timedelta(days=7)
    next_30 = today + timedelta(days=30)

    groups = {
        "Today": [],
        "This Week": [],
        "Next 30 Days": []
    }

    for e in events:
        # Use Kyiv local datetime for grouping
        event_date = e.event_datetime.date()
        e.local_dt = e.event_datetime

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

    grouped = group_events(all_events)  # this now also sets e.local_dt

    # Optional: set end datetime for template
    for group in grouped.values():
        for e in group:
            e.end_datetime = e.local_dt + timedelta(hours=2)

    return render_template(
        "events.html",
        title="Events",
        groups=grouped
    )

# ----------------------------
# Past events with pagination
# ----------------------------
@events_bp.route("/past")
def past_events():

    page = request.args.get("page", 1, type=int)
    per_page = 10

    tag_id = request.args.get("tag_id", type=int)

    today = datetime.now()

    query = (
        Event.query
        .filter(Event.event_datetime < today)
        .order_by(Event.event_datetime.desc())
    )

    # --- NEW FILTER ---
    if tag_id:
        query = query.filter(Event.tag_id == tag_id)

    pagination = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False,
    )

    events = pagination.items

    # Compute end time
    for e in events:
        e.local_dt = e.event_datetime
        e.end_dt = e.local_dt + timedelta(hours=2)

    # Tag list for filter dropdown
    all_tags = EventTag.query.order_by(EventTag.name).all()

    return render_template(
        "past_events.html",
        title="Past Events",
        events=events,
        pagination=pagination,
        all_tags=all_tags,
        tag_id=tag_id
    )

# ----------------------------
# Event detail page
# ----------------------------
@events_bp.route("/<int:event_id>")
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)

    event.local_dt = event.event_datetime
    event.end_dt = event.local_dt + timedelta(hours=2)

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
    form.tag.choices = [
        (t.id, f"{t.icon or ''} {t.name}") for t in EventTag.query.order_by(EventTag.name).all()
    ]

    if form.validate_on_submit():

        new_event = Event(
            title=form.title.data,
            event_datetime=form.event_datetime.data,
            host=form.host.data,
            description=form.description.data,
        )

        # Set tags
        new_event.tag = EventTag.query.get(form.tag.data) if form.tag.data != 0 else None

        db.session.add(new_event)
        db.session.commit()

        flash("Event created successfully!")
        return redirect(url_for("events.events_list"))

    return render_template(
        "event_form.html", 
        form=form, 
        title="Create Event")


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

    # Populate tag choices
    form.tag.choices =  [
        (t.id, f"{t.icon or ''} {t.name}") for t in EventTag.query.order_by(EventTag.name).all()
    ]

    # Pre-select current tag
    if request.method == "GET" and event.tag:
        form.tag.data = event.tag.id

    if form.validate_on_submit():

        event.title = form.title.data
        event.event_datetime = form.event_datetime.data
        event.host = form.host.data
        event.description = form.description.data

        # Update tag
        event.tag = EventTag.query.get(form.tag.data) if form.tag.data != 0 else None

        db.session.commit()
        flash("Event updated successfully!")

        return redirect(url_for("events.events_list"))

    return render_template(
        "event_form.html", 
        form=form, 
        title="Edit Event",
        event=event
    )


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