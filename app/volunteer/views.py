from flask import (
    Blueprint,
    render_template,
    request,
)
from flask_login import current_user, login_required

from app import db
from app.decorators import volunteer_required
from app.models import Volunteer, Status
from app.volunteer.forms import (
    UploadClearanceForm1,
    UploadClearanceForm2,
    UploadClearanceForm3,
    UploadClearanceForm4
)

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
    form1 = UploadClearanceForm1()
    form2 = UploadClearanceForm2()
    form3 = UploadClearanceForm3()
    form4 = UploadClearanceForm4()

    current_volunteer = Volunteer.query.filter_by(email=current_user.email).first()

    if form1.validate_on_submit() and form1.submit.data:
        if form1.form1_file_urls.data != '':
            current_volunteer.link1 = form1.form1_file_urls.data
            current_volunteer.status1 = Status.SUBMITTED
        else:
            current_volunteer.status1 = Status.NOT_SUBMITTED

    elif form2.validate_on_submit() and form2.submit.data:
        if form2.form2_file_urls != '':
            current_volunteer.link2 = form2.form2_file_urls.data
            current_volunteer.status2 = Status.SUBMITTED
        else:
            current_volunteer.status2 = Status.NOT_SUBMITTED

    elif form3.validate_on_submit() and form3.submit.data:
        if form3.form3_file_urls != '':
            current_volunteer.link3 = form3.form3_file_urls.data
            current_volunteer.status3 = Status.SUBMITTED
        else:
            current_volunteer.status3 = Status.NOT_SUBMITTED

    elif form4.validate_on_submit() and form4.submit.data:
        if form4.form4_file_urls != '':
            current_volunteer.link4 = form4.form4_file_urls.data
            current_volunteer.status4 = Status.SUBMITTED
        else:
            current_volunteer.status4 = Status.NOT_SUBMITTED

    db.session.commit()

    return render_template(
        'volunteer/upload_clearances.html', volunteer=current_volunteer,
        form1=form1,
        form2=form2,
        form3=form3,
        form4=form4
    )


# May not need this
@volunteer.route('/view_status')
@login_required
@volunteer_required
def view_status():
    volunteer = Volunteer.query.filter_by(id=current_user.id).first()
    return render_template('volunteer/view_status.html', volunteer=volunteer)
