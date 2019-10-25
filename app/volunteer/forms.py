from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import (
    StringField,
    SubmitField,
)
from wtforms.fields.html5 import EmailField
from wtforms.validators import (
    Email,
    EqualTo,
    InputRequired,
    Length,
)

from app import db
from app.models import Role, User


class UploadClearanceForm(FlaskForm):
    link = StringField(
        'Link to clearance', validators=[InputRequired(),
                            Length(1, 256)]
    )
    submit = SubmitField('Submit')

