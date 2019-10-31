from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import (
    PasswordField,
    SelectField,
    TextAreaField,
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
from app.models import Role, User, Status



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
    role = QuerySelectField(
        'Account type',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(Role).order_by('permissions'))
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
    password = PasswordField(
        'Password',
        validators=[
            InputRequired(),
            EqualTo('password2', 'Passwords must match.')
        ])
    password2 = PasswordField('Confirm password', validators=[InputRequired()])

    submit = SubmitField('Create')

class Clearance1StatusForm(FlaskForm):
    new_status_1 = SelectField(choices=[('NOT_SUBMITTED', 'Not Submitted'), ('SUBMITTED', 'Submitted'),
    ('PENDING_STATE_REVIEW', 'Pending (state review)'), ('PENDING_PEC_REVIEW', 'Pending (pec review)'), ('CLEARED', 'Cleared'), ('RESUBMISSION', 'Resubmission requested'), ('DECLINED', 'Declined')
    , ('EXPIRED', 'Expired')], validators=[])
    comment_1 = TextAreaField()
    submit_clearance_1 = SubmitField()

class Clearance2StatusForm(FlaskForm):
    new_status_2 = SelectField(choices=[('NOT_SUBMITTED', 'Not Submitted'), ('SUBMITTED', 'Submitted'),
    ('PENDING_STATE_REVIEW', 'Pending (state review)'), ('PENDING_PEC_REVIEW', 'Pending (pec review)'), ('CLEARED', 'Cleared'), ('RESUBMISSION', 'Resubmission requested'), ('DECLINED', 'Declined')
    , ('EXPIRED', 'Expired')], validators=[])
    comment_2 = TextAreaField()
    submit_clearance_2 = SubmitField()

class Clearance3StatusForm(FlaskForm):
    new_status_3 = SelectField(choices=[('NOT_SUBMITTED', 'Not Submitted'), ('SUBMITTED', 'Submitted'),
    ('PENDING_STATE_REVIEW', 'Pending (state review)'), ('PENDING_PEC_REVIEW', 'Pending (pec review)'), ('CLEARED', 'Cleared'), ('RESUBMISSION', 'Resubmission requested'), ('DECLINED', 'Declined')
    , ('EXPIRED', 'Expired')], validators=[])
    comment_3 = TextAreaField()
    submit_clearance_3 = SubmitField()

class Clearance4StatusForm(FlaskForm):
    new_status_4 = SelectField(choices=[('NOT_SUBMITTED', 'Not Submitted'), ('SUBMITTED', 'Submitted'),
    ('PENDING_STATE_REVIEW', 'Pending (state review)'), ('PENDING_PEC_REVIEW', 'Pending (pec review)'), ('CLEARED', 'Cleared'), ('RESUBMISSION', 'Resubmission requested'), ('DECLINED', 'Declined')
    , ('EXPIRED', 'Expired')], validators=[])
    comment_4 = TextAreaField()
    submit_clearance_4 = SubmitField()
