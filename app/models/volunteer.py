from sqlalchemy.orm import relationship

from .. import db
import enum
import random
from faker import Faker
from sqlalchemy import String
from app.models import User


class Status(enum.Enum):
    NOT_SUBMITTED = 'Not Submitted'  # not finished
    SUBMITTED = 'Submitted'  # finished
    PENDING_STATE_REVIEW = 'Pending (state review)'  # this is something admin needs to update
    PENDING_PEC_REVIEW = 'Pending (pec review)'
    CLEARED = 'Cleared'
    RESUBMISSION = 'Resubmission requested'
    DECLINED = 'Declined'
    EXPIRED = 'Expired'
    NOT_NEEDED = 'Not Needed'

    def __str__(self):
        return self.name

    def __html__(self):
        return self.value


class Volunteer(db.Model):
    __tablename__ = 'volunteers'
    id = db.Column(db.Integer, primary_key=True)
    user = relationship("User", uselist=False, backref="volunteer")
    first_name = db.Column(String(64))
    last_name = db.Column(String(64))
    email = db.Column(String(64))
    phone_number = db.Column(db.String(16))
    address_street = db.Column(db.String(64))
    address_city = db.Column(db.String(64))
    address_state = db.Column(db.String(2))
    address_zip_code = db.Column(db.Integer)
    organization = db.Column(db.String(128))
    year_pa = db.Column(db.String(4))
    clearance_expiration = db.Column(db.String(64))

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

    status4 = db.Column(db.Enum(Status), default=0)
    comment4 = db.Column(db.String(512))
    link4 = db.Column(db.String(128))

    def __init__(self, **kwargs):
        super(Volunteer, self).__init__(**kwargs)
        # Will email be enough for uniqueness?
        self.user = User.query.filter_by(email=self.email).first()

    def __repr__(self):
       return ('<Volunteer \n'
             f'First Name: {self.first_name}\n'
             f'Last Name: {self.last_name}\n'
             f'Email Address: {self.email}\n'
             f'Phone Number: {self.phone_number}\n'
             f'Address: {self.address_street}, {self.address_city}, {self.address_state} {self.address_zip_code}\n'
             f'Organization: {self.organization}\n'
             f'Year Moved to PA: {self.year_pa}\n'
             f'Clearance Expiration: {self.clearance_expiration}\n'
             f'Status of Clearance 1: {self.status1}\n'
             f'Comment on Clearance 1: {self.comment1}\n'
             f'Link to Clearance 1: {self.link1}\n'
             f'Status of Clearance 2: {self.status2}\n'
             f'Comment on Clearance 2: {self.comment2}\n'
             f'Link to Clearance 2: {self.link2}\n'
             f'Status of Clearance 3: {self.status3}\n'
             f'Comment on Clearance 3: {self.comment3}\n'
             f'Link to Clearance 3: {self.link3}\n'
             f'Status of Clearance 4: {self.status4}\n'
             f'Comment on Clearance 4: {self.comment4}\n'
             f'Link to Clearance 4: {self.link4}\n')

    def __str__(self):
      return self.__repr__()