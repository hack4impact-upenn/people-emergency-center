from flask_wtf import FlaskForm
from wtforms.fields import (
    StringField,
    SubmitField,
)


class MultipleFileUploadField(StringField):



class UploadClearanceForm(FlaskForm):
    link1_display = StringField('')
    file_urls = MultipleFileUploadField()
    submit1 = SubmitField('Submit')

    # link2 = StringField('')
    # submit2 = SubmitField('Submit')
    #
    # link3 = StringField('')
    # submit3 = SubmitField('Submit')
    #
    # link4 = StringField('')
    # submit4 = SubmitField('Submit')
