from flask import url_for
from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import (
    BooleanField,
    PasswordField,
    StringField,
    SubmitField,
    SelectField,
    IntegerField
)
from wtforms.fields.html5 import EmailField
from wtforms_alchemy import PhoneNumberField
from wtforms.validators import Email, EqualTo, InputRequired, Length

from app.models import User


class LoginForm(FlaskForm):
    email = EmailField(
        'Email', validators=[InputRequired(),
                             Length(1, 64),
                             Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')


class RegistrationForm(FlaskForm):
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
            EqualTo('password2', 'Passwords must match')
        ])
    password2 = PasswordField('Confirm password', validators=[InputRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered. (Did you mean to '
                                  '<a href="{}">log in</a> instead?)'.format(
                                    url_for('account.login')))

        surgery_month = SelectField(choices=[('',''), ('January', 'January'), ('February', 'February'),
    ('March', 'March'), ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'),
    ('August', 'August'), ('September', 'September'), ('October', 'October'),
    ('November', 'November'), ('December', 'December')])


class RequestResetPasswordForm(FlaskForm):
    email = EmailField(
        'Email', validators=[InputRequired(),
                             Length(1, 64),
                             Email()])
    submit = SubmitField('Reset password')

    # We don't validate the email address so we don't confirm to attackers
    # that an account with the given email exists.


class ResetPasswordForm(FlaskForm):
    email = EmailField(
        'Email', validators=[InputRequired(),
                             Length(1, 64),
                             Email()])
    new_password = PasswordField(
        'New password',
        validators=[
            InputRequired(),
            EqualTo('new_password2', 'Passwords must match.')
        ])
    new_password2 = PasswordField(
        'Confirm new password', validators=[InputRequired()])
    submit = SubmitField('Reset password')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown email address.')


class CreatePasswordForm(FlaskForm):
    password = PasswordField(
        'Password',
        validators=[
            InputRequired(),
            EqualTo('password2', 'Passwords must match.')
        ])
    password2 = PasswordField(
        'Confirm new password', validators=[InputRequired()])
    submit = SubmitField('Set password')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[InputRequired()])
    new_password = PasswordField(
        'New password',
        validators=[
            InputRequired(),
            EqualTo('new_password2', 'Passwords must match.')
        ])
    new_password2 = PasswordField(
        'Confirm new password', validators=[InputRequired()])
    submit = SubmitField('Update password')

class EditAccountInfoForm(FlaskForm):
    phone_number = IntegerField(
        'Phone Number')
    street = StringField(
        'Street', validators=[Length(1, 64)])
    city = StringField(
        'City', validators=[Length(1, 64)])
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
        ('WA', 'WA'), ('WV', 'WV'), ('WI', 'WI'), ('WY', 'WY')])

    pa_residency = SelectField('Have you lived in PA for 10 consecutive years or more?'
      , choices=[('Yes','Yes'), ('No', 'No')])
    organization_corporation = StringField(
        'Organization/Corporation', validators=[Length(1, 64)])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Update account information')
class ChangeEmailForm(FlaskForm):
    email = EmailField(
        'New email', validators=[InputRequired(),
                                 Length(1, 64),
                                 Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Update email')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
