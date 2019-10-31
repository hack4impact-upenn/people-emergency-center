from flask import (
    Blueprint,
    render_template,
)
from flask_login import current_user, login_required

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


@volunteer.route('/view_status')
@login_required
@volunteer_required
def view_status():
    volunteer = Volunteer.query.filter_by(id=current_user.id).first()
    return render_template('volunteer/view_status.html', volunteer=volunteer)
