from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import (
    BooleanField,
    PasswordField,
    SelectField,
    TextAreaField,
    StringField,
    SubmitField,
    SelectField,
    IntegerField
)
from wtforms.fields.html5 import EmailField
from wtforms.validators import (
    Email,
    EqualTo,
    InputRequired,
    Length,
)

from app import db
from app.models import Role, User, Status
import datetime
from markupsafe import escape

class ChangeUserEmailForm(FlaskForm):
    email = EmailField(
        'New email', validators=[InputRequired(),
                                 Length(1, 64),
                                 Email()])
    submit = SubmitField('Update email')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class ChangeAccountTypeForm(FlaskForm):
    role = QuerySelectField(
        'New account type',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(Role).order_by('permissions'))
    submit = SubmitField('Update role')


class InviteUserForm(FlaskForm):
    first_name = StringField(
        'First name', validators=[InputRequired(),
                                  Length(1, 64)])
    last_name = StringField(
        'Last name', validators=[InputRequired(),
                                 Length(1, 64)])
    email = EmailField(
        'Email', validators=[InputRequired(),
                             Length(1, 64),
                             Email()])
    submit = SubmitField('Invite')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class NewUserForm(InviteUserForm):
    role = QuerySelectField(
        'Account type',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(Role).filter(Role.id!=3).order_by('permissions'))
    password = PasswordField(
        'Password',
        validators=[
            InputRequired(),
            EqualTo('password2', 'Passwords must match.')
        ])
    password2 = PasswordField('Confirm password', validators=[InputRequired()])

    submit = SubmitField('Create')

class NewVolunteerForm(InviteUserForm):
    pa_residency = SelectField('Have you lived in PA for 10 consecutive years or more?'
      , choices=[('Yes','Yes'), ('No', 'No')],
        validators=[InputRequired()])
    organization_corporation = StringField(
        'Organization/Corporation', validators=[InputRequired(),
                                              Length(1, 64)])
    street = StringField(
        'Street', validators=[InputRequired(),
                              Length(1, 64)])
    city = StringField(
        'City', validators=[InputRequired(),
                            Length(1, 64)])

    state = SelectField(choices=[('PA', 'PA'), ('NJ', 'NJ')],
        validators=[InputRequired()])

    phone_number = IntegerField(
        'Phone Number', validators=[InputRequired()])
    password = PasswordField(
        'Password',
        validators=[
            InputRequired(),
            EqualTo('password2', 'Passwords must match.')
        ])
    password2 = PasswordField('Confirm password', validators=[InputRequired()])

    submit = SubmitField('Create')


def coerce_for_enum(enum):
    def coerce(name):
        if isinstance(name, enum):
            return name
        try:
            return enum[name]
        except KeyError:
            raise ValueError(name)
    return coerce


class Clearance1StatusForm(FlaskForm):
    new_status_1 = SelectField(
        'Status',
        choices=[(v, escape(v)) for v in Status],
        coerce=coerce_for_enum(Status)
    )
    comment_1 = TextAreaField()
    submit_clearance_1 = SubmitField()


class Clearance2StatusForm(FlaskForm):
    new_status_2 = SelectField(
        'Status',
        choices=[(v, escape(v)) for v in Status],
        coerce=coerce_for_enum(Status)
    )
    comment_2 = TextAreaField()
    submit_clearance_2 = SubmitField()


class Clearance3StatusForm(FlaskForm):
    new_status_3 = SelectField(
        'Status',
        choices=[(v, escape(v)) for v in Status],
        coerce=coerce_for_enum(Status)
    )
    comment_3 = TextAreaField()
    submit_clearance_3 = SubmitField()


class Clearance4StatusForm(FlaskForm):
    new_status_4 = SelectField(
        'Status',
        choices=[(v, escape(v)) for v in Status],
        coerce=coerce_for_enum(Status)
    )
    comment_4 = TextAreaField()
    submit_clearance_4 = SubmitField()

class DownloadCSVForm(FlaskForm):
    download_csv = SubmitField("Download CSV")

