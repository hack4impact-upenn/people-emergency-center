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
    IntegerField,
)
from wtforms.fields.html5 import EmailField
from wtforms.validators import (
    Email,
    EqualTo,
    InputRequired,
    Length,
)
from app.volunteer.forms import MultipleFileUploadField

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
        query_factory=lambda: db.session.query(Role).filter(Role.id!=1).order_by('permissions'))
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

    state = SelectField(choices=[('PA', 'PA'), ('AL', 'AL'),
        ('AK', 'AK'), ('AZ', 'AZ'), ('AR', 'AR'), ('CA', 'CA'),
        ('CO', 'CO'), ('CT', 'CT'), ('DE', 'DE'), ('FL', 'FL'),
        ('GA', 'GA'), ('HI', 'HI'), ('ID', 'ID'), ('IL', 'IL'),
        ('IN', 'IN'), ('IA', 'IA'), ('KS', 'KS'), ('KY', 'KY'),
        ('LA', 'LA'), ('ME', 'ME'), ('MD', 'MD'), ('MA', 'MA'),
        ('MI', 'MI'), ('MN', 'MN'), ('MS', 'MS'), ('MO', 'MO'),
        ('MT', 'MT'), ('NE', 'NE'), ('NV', 'NV'), ('NH', 'NH'),
        ('NJ', 'NJ'), ('NM', 'NM'), ('NY', 'NY'), ('NC', 'NC'),
        ('ND', 'ND'), ('OH', 'OH'), ('OK', 'OK'), ('OR', 'OR'),
        ('RI', 'RI'), ('SC', 'SC'), ('SD', 'SD'), ('TN', 'TN'),
        ('TA', 'TA'), ('UT', 'UT'), ('VT', 'VT'), ('VA', 'VA'),
        ('WA', 'WA'), ('WV', 'WV'), ('WI', 'WI'), ('WY', 'WY')],
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


class ClearanceExpirationForm(FlaskForm):
    clearance_expiration = StringField(
        'Clearace Expiration Date', validators=[Length(1, 64)])
    submit_expiration_date = SubmitField()


class Clearance1StatusForm(FlaskForm):
    new_status_1 = SelectField(
        'Status',
        choices=[(v, escape(v)) for v in Status],
        coerce=coerce_for_enum(Status)
    )
    form1_file_urls = MultipleFileUploadField()
    comment_1 = TextAreaField()
    submit_clearance_1 = SubmitField()


class Clearance2StatusForm(FlaskForm):
    new_status_2 = SelectField(
        'Status',
        choices=[(v, escape(v)) for v in Status],
        coerce=coerce_for_enum(Status)
    )
    form2_file_urls = MultipleFileUploadField()
    comment_2 = TextAreaField()
    submit_clearance_2 = SubmitField()


class Clearance3StatusForm(FlaskForm):
    new_status_3 = SelectField(
        'Status',
        choices=[(v, escape(v)) for v in Status],
        coerce=coerce_for_enum(Status)
    )
    form3_file_urls = MultipleFileUploadField()
    comment_3 = TextAreaField()
    submit_clearance_3 = SubmitField()


class Clearance4StatusForm(FlaskForm):
    new_status_4 = SelectField(
        'Status',
        choices=[(v, escape(v)) for v in Status],
        coerce=coerce_for_enum(Status)
    )
    form4_file_urls = MultipleFileUploadField()
    comment_4 = TextAreaField()
    submit_clearance_4 = SubmitField()


class DownloadCSVForm(FlaskForm):
    download_csv = SubmitField("Download CSV")
