from .. import db
import enum
from sqlalchemy.exc import IntegrityError
import random
from random import seed, choice, randint
from faker import Faker
from sqlalchemy import String


class Status(enum.Enum):
    NOT_SUBMITTED = 'Not Submitted'  # not finished
    SUBMITTED = 'Submitted'  # finished
    PENDING_STATE_REVIEW = 'Pending (state review)'  # this is something admin needs to update
    PENDING_PEC_REVIEW = 'Pending (pec review)'
    CLEARED = 'Cleared'
    RESUBMISSION = 'Resubmission requested'
    DECLINED = 'Declined'
    EXPIRED = 'Expired'


class Volunteer(db.Model):
    __tablename__ = 'volunteers'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(String(64))
    last_name = db.Column(String(64))
    email = db.Column(String(64))
    phone_number = db.Column(db.String(16))
    address_number = db.Column(db.Integer())
    address_street = db.Column(db.String(64))
    address_city = db.Column(db.String(64))
    address_state = db.Column(db.String(2))
    organization = db.Column(db.String(128))
    year_pa = db.Column(db.Integer())

    # link, comment, status
    status1 = db.Column(db.Enum(Status), default=0)
    comment1 = db.Column(db.String(512))
    link1 = db.Column(db.String(128))

    status2 = db.Column(db.Enum(Status), default=0)
    comment2 = db.Column(db.String(512))
    link2 = db.Column(db.String(128))

    status3 = db.Column(db.Enum(Status), default=0)
    comment3 = db.Column(db.String(512))
    link3 = db.Column(db.String(128))

    def __repr__(self):
       return ('<Voucher \n'
             f'First Name: {self.first_name}\n'
             f'Last Name: {self.last_name}\n'
             f'Email Address: {self.email}\n'
             f'Phone Number: {self.phone_number}\n'
             f'Address: {self.address_number} {self.address_street}, {self.address_city}, {self.address_state}\n'
             f'Organization: {self.organization}\n'
             f'Year Moved to PA: {self.year_pa}\n'
             f'Status of Clearance 1: {self.status1}\n'
             f'Comment on Clearance 1: {self.comment1}\n'
             f'Link to Clearance 1: {self.link1}\n'
             f'Status of Clearance 2: {self.status2}\n'
             f'Comment on Clearance 2: {self.comment2}\n'
             f'Link to Clearance 2: {self.link2}\n'
             f'Status of Clearance 3: {self.status3}\n'
             f'Comment on Clearance 3: {self.comment3}\n'
             f'Link to Clearance 3: {self.link3}>')

    def __str__(self):
      return self.__repr__()

    @staticmethod
    def generate_fake(count=10, **kwargs):
        from sqlalchemy.exc import IntegrityError

        fake = Faker()

        for i in range(count):
            v = Volunteer(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                phone_number=fake.phone_number(),
                address_number=fake.building_number(),
                address_street=fake.street_address().partition(' ')[2],
                address_city=fake.city(),
                address_state=fake.state_abbr(include_territories=True),
                organization=fake.company(),
                year_pa=fake.year(),
                status1=random.choice(list(Status)),
                comment1=fake.text(max_nb_chars=100, ext_word_list=None),
                link1=fake.uri(),
                status2=random.choice(list(Status)),
                comment2=fake.text(max_nb_chars=100, ext_word_list=None),
                link2=fake.uri(),
                status3=random.choice(list(Status)),
                comment3=fake.text(max_nb_chars=100, ext_word_list=None),
                link3=fake.uri(),
                **kwargs)
            db.session.add(v)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
