from flask import current_app
from flask_login import AnonymousUserMixin, UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from werkzeug.security import check_password_hash, generate_password_hash

from .. import db, login_manager


class Permission:
    VOLUNTEER = 0x01
    STAFFER = 0x80
    ADMINISTER = 0xff


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    index = db.Column(db.String(64))
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'Volunteer': (Permission.VOLUNTEER,
                'volunteer',
                True),
            'Staff': (Permission.STAFFER,
                'staff',
                True),
            'Administrator': (
                Permission.ADMINISTER,
                'admin',
                False  # grants all permissions
            )
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.index = roles[r][1]
            role.default = roles[r][2]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role \'%s\'>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    confirmed = db.Column(db.Boolean, default=False)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    phone_number = db.Column(db.String(16))
    pa_residency = db.Column(db.String(4))
    street = db.Column(db.String(64))
    city = db.Column(db.String(64))
    state = db.Column(db.String(2))
    organization_corporation = db.Column(db.String(64))
    volunteer_id = db.Column(db.Integer, db.ForeignKey('volunteers.id'))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['ADMIN_EMAIL']:
                self.role = Role.query.filter_by(
                    permissions=Permission.ADMINISTER).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_admin(self):
        return self.can(Permission.ADMINISTER)

    @property
    def password(self):
        raise AttributeError('`password` is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=604800):
        """Generate a confirmation token to email a new user."""

        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def generate_email_change_token(self, new_email, expiration=3600):
        """Generate an email change token to email an existing user."""
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def generate_password_reset_token(self, expiration=3600):
        """
        Generate a password reset change token to email to an existing user.
        """
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def confirm_account(self, token):
        """Verify that the provided token is for this user's id."""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except (BadSignature, SignatureExpired):
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    def change_email(self, token):
        """Verify the new email for this user."""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except (BadSignature, SignatureExpired):
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        db.session.commit()
        return True

    def reset_password(self, token, new_password):
        """Verify the new password for this user."""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except (BadSignature, SignatureExpired):
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        db.session.commit()
        return True

    ### Generate Fake Data ###
    # Generates fake data for Volunteers and Users
    # Volunteers and Users share common attributes for the following:
    # first_name, last_name, email, phone_number, street, city, state, organization
    # First the user is cadded to session, then the volunteer
    # First 5 Volunteers have all their statuses cleared
    # Note: generate_fake() in volunteer.py is no longer used.
    ##########################
    @staticmethod
    def generate_fake(count=100, **kwargs):
        """Generate a number of fake users for testing."""
        from sqlalchemy.exc import IntegrityError
        from random import seed, choice
        import random
        import enum
        import datetime
        from faker import Faker
        from app.models import Volunteer, Status

        fake = Faker()
        roles = Role.query.all()
        now = datetime.datetime.now()
        seed()

        for i in range(count):
            fake_first_name = fake.first_name()
            fake_last_name = fake.last_name()
            fake_email = fake.email()
            fake_phone_number = fake.phone_number()
            fake_street = fake.street_address()
            fake_city = fake.city()
            fake_state = fake.state_abbr(include_territories=True)
            fake_organization = fake.company()
            fake_clearance_exp = fake.month_name() + " " + fake.day_of_month() + " " + fake.year()
            fake_residency = random.choice(["Yes", "No"])
            user_role = choice(roles)

            u = User(
                first_name=fake_first_name,
                last_name=fake_last_name,
                email=fake_email,
                phone_number=fake_phone_number,
                street=fake_street,
                city=fake_city,
                state=fake_state,
                organization_corporation=fake_organization,
                pa_residency = fake_residency,
                password='password',
                confirmed=True,
                role = user_role,
                **kwargs)

            # User is only assigned as a volunteer if its user_role is 'Volunteer'
            if (user_role.name == 'Volunteer'):
                if (i < 5):
                    v = Volunteer(
                        first_name=fake_first_name,
                        last_name=fake_last_name,
                        email=fake_email,
                        phone_number=fake_phone_number,
                        address_street=fake_street,
                        address_city=fake_city,
                        address_state=fake_state,
                        organization=fake_organization,
                        year_pa=fake_residency,
                        clearance_expiration = fake_clearance_exp,
                        status1=Status.CLEARED,
                        comment1=fake.text(max_nb_chars=100, ext_word_list=None),
                        link1=fake.uri(),
                        status2=Status.CLEARED,
                        comment2=fake.text(max_nb_chars=100, ext_word_list=None),
                        link2=fake.uri(),
                        status3=Status.CLEARED,
                        comment3=fake.text(max_nb_chars=100, ext_word_list=None),
                        link3=fake.uri(),
                        status4=Status.CLEARED,
                        comment4=fake.text(max_nb_chars=100, ext_word_list=None),
                        link4=fake.uri(),
                        **kwargs)
                else:
                    v = Volunteer(
                        first_name=fake_first_name,
                        last_name=fake_last_name,
                        email=fake_email,
                        phone_number=fake_phone_number,
                        address_street=fake_street,
                        address_city=fake_city,
                        address_state=fake_state,
                        organization=fake_organization,
                        year_pa=fake_residency,
                        clearance_expiration = fake_clearance_exp,
                        status1=random.choice(list(Status)),
                        comment1=fake.text(max_nb_chars=100, ext_word_list=None),
                        link1=fake.uri(),
                        status2=random.choice(list(Status)),
                        comment2=fake.text(max_nb_chars=100, ext_word_list=None),
                        link2=fake.uri(),
                        status3=random.choice(list(Status)),
                        comment3=fake.text(max_nb_chars=100, ext_word_list=None),
                        link3=fake.uri(),
                        status4=random.choice(list(Status)),
                        comment4=fake.text(max_nb_chars=100, ext_word_list=None),
                        link4=fake.uri(),
                        **kwargs)

            db.session.add(u)
            # User is only assigned as a volunteer if its user_role is 'Volunteer'
            if (user_role.name == 'Volunteer'):
                db.session.add(v)

            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def __repr__(self):
        return '<User \'%s\'>' % self.full_name()


class AnonymousUser(AnonymousUserMixin):
    def can(self, _):
        return False

    def is_admin(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
