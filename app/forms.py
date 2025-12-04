from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, PasswordField, DateTimeLocalField, SelectMultipleField
from wtforms.validators import DataRequired, URL, Optional
from app.models import Event,EventTag, ResourceTag

class HostLoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")
    
class EventForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    event_datetime = DateTimeLocalField("Event Time",format="%Y-%m-%dT%H:%M",validators=[DataRequired()])
    host = StringField("Host", validators=[DataRequired()])
    description = TextAreaField("Description")

    # Multi-select for event tags
    tag = SelectField(
        "Topics (Tags)",
        coerce=int, 
        validators=[Optional()]
    )

    submit = SubmitField("Save")

class ResourceForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    url = StringField("URL", validators=[DataRequired(), URL()])
    event_id = SelectField("Link to Event (optional)", coerce=int, default=0)

    # Single tag
    tag = SelectField("Category", coerce=int, validators=[DataRequired()])
    

    submit = SubmitField("Save")

    def set_event_choices(self):
        events = Event.query.order_by(Event.event_datetime.desc()).all()
        self.event_id.choices = [(0, "— No event —")] + [
            (e.id, f"{e.title} — {e.event_datetime.strftime('%Y-%m-%d')}")
            for e in events
        ]

        tags = ResourceTag.query.order_by(ResourceTag.name).all()
        self.tag.choices = [(tag.id, tag.name) for tag in tags]
