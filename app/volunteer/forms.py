from flask_wtf import FlaskForm
from wtforms.fields import (
    StringField,
    SubmitField,
)


class UploadClearanceForm(FlaskForm):
    link1 = StringField('Link')
    submit1 = SubmitField('Submit')

    link2 = StringField('Link')
    submit2 = SubmitField('Submit')

    link3 = StringField('Link')
    submit3 = SubmitField('Submit')

    link4 = StringField('Link')
    submit4 = SubmitField('Submit')
