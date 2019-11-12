from flask_wtf import FlaskForm
from wtforms.fields import (
    StringField,
    SubmitField,
)


class UploadClearanceForm(FlaskForm):
    link1 = StringField('')
    submit1 = SubmitField('Submit')

    link2 = StringField('')
    submit2 = SubmitField('Submit')

    link3 = StringField('')
    submit3 = SubmitField('Submit')

    link4 = StringField('')
    submit4 = SubmitField('Submit')
