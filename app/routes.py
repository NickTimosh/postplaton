from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return render_template("index.html", title="Home")

@main.route("/events")
def events():
    mock_events = [
        {
            "id": 1,
            "title": "Morning Yoga",
            "date": "2025-12-05",
            "host": "Alice",
            "description": "A calming morning yoga session for all levels."
        },
        {
            "id": 2,
            "title": "Cooking Class",
            "date": "2025-12-10",
            "host": "Bob",
            "description": "Learn to cook a 3-course Italian dinner."
        },
        {
            "id": 3,
            "title": "Tech Talk: AI Trends",
            "date": "2025-12-14",
            "host": "Charlie",
            "description": "A friendly discussion about new AI tools."
        }
    ]

    return render_template("events.html", events=mock_events, title="Events")
