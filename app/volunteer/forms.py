from flask_wtf import FlaskForm
from wtforms.fields import (
    StringField,
    SubmitField,
)


class MultipleFileUploadField(StringField):
    pass


class UploadClearanceForm1(FlaskForm):
    link_display = StringField('')
    form1_file_urls = MultipleFileUploadField()
    submit = SubmitField('Submit1')


class UploadClearanceForm2(FlaskForm):
    link_display = StringField('')
    form2_file_urls = MultipleFileUploadField()
    submit = SubmitField('Submit2')


class UploadClearanceForm3(FlaskForm):
    link_display = StringField('')
    file_urls = MultipleFileUploadField()
    submit = SubmitField('Submit3')


class UploadClearanceForm4(FlaskForm):
    link_display = StringField('')
    file_urls = MultipleFileUploadField()
    submit = SubmitField('Submit4')

