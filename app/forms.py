from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, PasswordField, DateTimeLocalField
from wtforms.validators import DataRequired, URL
from app.models import Event

class HostLoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")
    
class EventForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    event_datetime = DateTimeLocalField("Event Time",format="%Y-%m-%dT%H:%M",validators=[DataRequired()])
    host = StringField("Host", validators=[DataRequired()])
    description = TextAreaField("Description")
    submit = SubmitField("Save")

class ResourceForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    url = StringField("URL", validators=[DataRequired(), URL()])
    event_id = SelectField("Related Event", coerce=int, default=0)
    submit = SubmitField("Save")

    def set_event_choices(self):
        events = Event.query.order_by(Event.event_datetime.desc()).all()
        self.event_id.choices = [(0, "— No event —")] + [
            (e.id, f"{e.title} — {e.event_datetime.strftime('%Y-%m-%d')}")
            for e in events
        ]
