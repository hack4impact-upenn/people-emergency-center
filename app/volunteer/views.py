from flask import (
    Blueprint,
    render_template,
    request,
)
from flask_login import current_user, login_required
import boto3
import boto.s3
from boto.s3.key import Key
import boto.s3.connection
import json
import time
import os

from app import db
from app.decorators import volunteer_required
from app.models import Volunteer, Status
from app.volunteer.forms import UploadClearanceForm

volunteer = Blueprint('volunteer', __name__)


@volunteer.route('/')
@login_required
@volunteer_required
def index():
    """Volunteer dashboard page."""
    return render_template('volunteer/index.html')


@volunteer.route('/upload_clearances', methods=['GET', 'POST'])
@login_required
@volunteer_required
def upload_clearances():
    form = UploadClearanceForm()

    current_volunteer = Volunteer.query.filter_by(email=current_user.email).first()

    if form.validate_on_submit() and form.submit1.data:
        if form.link1.data.strip() != '':
            current_volunteer.link1 = form.link1.data
            current_volunteer.status1 = Status.SUBMITTED
        else:
            current_volunteer.status1 = Status.NOT_SUBMITTED

    elif form.validate_on_submit() and form.submit2.data:
        if form.link2.data.strip() != '':
            current_volunteer.link2 = form.link2.data
            current_volunteer.status2 = Status.SUBMITTED
        else:
            current_volunteer.status2 = Status.NOT_SUBMITTED

    elif form.validate_on_submit() and form.submit3.data:
        if form.link3.data.strip() != '':
            current_volunteer.link3 = form.link3.data
            current_volunteer.status3 = Status.SUBMITTED
        else:
            current_volunteer.status3 = Status.NOT_SUBMITTED

    elif form.validate_on_submit() and form.submit4.data:
        if form.link4.data.strip() != '':
            current_volunteer.link4 = form.link4.data
            current_volunteer.status4 = Status.SUBMITTED
        else:
            current_volunteer.status4 = Status.NOT_SUBMITTED

    db.session.commit()

    return render_template(
        'volunteer/upload_clearances.html', volunteer=current_volunteer,  form=form)


@volunteer_required
@volunteer.route('sign-s3/')
@login_required
def sign_s3():
    # Load necessary information into the application
    S3_BUCKET = "h4i-test2"
    TARGET_FOLDER = 'json/'
    S3_REGION = 'us-east-2'

    # Load required data from the request
    pre_file_name = request.args.get('file-name')
    file_name = ''.join(pre_file_name.split('.')[:-1]) + \
                str(time.time()).replace('.',  '-') + '.' + \
                ''.join(pre_file_name.split('.')[-1:])
    file_type = request.args.get('file-type')

    # Initialise the S3 client
    s3 = boto3.client('s3', S3_REGION)

    # Generate and return the presigned URL
    presigned_post = s3.generate_presigned_post(
        Bucket=S3_BUCKET,
        Key=TARGET_FOLDER + file_name,
        Fields={
            "acl": "public-read",
            "Content-Type": file_type
        },
        Conditions=[{
            "acl": "public-read"
        }, {
            "Content-Type": file_type
        }],
        ExpiresIn=60000)

    # Return the data to the client
    return json.dumps({
        'data':
            presigned_post,
        'url_upload':
            'https://%s.%s.amazonaws.com' % (S3_BUCKET, S3_REGION),
        'url':
            'https://%s.amazonaws.com/%s/json/%s' % (S3_REGION, S3_BUCKET,
                                                     file_name)
    })



# May not need this
@volunteer.route('/view_status')
@login_required
@volunteer_required
def view_status():
    volunteer = Volunteer.query.filter_by(id=current_user.id).first()
    return render_template('volunteer/view_status.html', volunteer=volunteer)
