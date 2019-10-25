from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required
from flask_rq import get_queue

from app import db
from app.decorators import volunteer_required
from app.models import EditableHTML, Role, User, Volunteer
from app.volunteer.forms import UploadClearanceForm

volunteer = Blueprint('volunteer', __name__)

@volunteer.route('/')
@login_required
@volunteer_required
def index():
    """Volunteer dashboard page."""
    return render_template('volunteer/index.html')

@volunteer.route('/upload_clearances')
@login_required
@volunteer_required
def upload_clearances():
    form1 = UploadClearanceForm()
    volunteer = Volunteer.query.filter_by(id=current_user.id).first()
    if form1.validate_on_submit():
        volunteer.link1 = str(form1.link)
        dbsession.flush()
    form2 = UploadClearanceForm()
    volunteer = Volunteer.query.filter_by(id=current_user.id).first()
    if form1.validate_on_submit():
        volunteer.link2 = str(form2.link)
        dbsession.flush()
    form3 = UploadClearanceForm()
    volunteer = Volunteer.query.filter_by(id=current_user.id).first()
    if form1.validate_on_submit():
        volunteer.link3 = str(form3s.link)
        dbsession.flush()
    return render_template('volunteer/upload_clearances.html', volunteer=volunteer,  form1=form1, form2=form2, form3=form3)

@volunteer.route('/view_status')
@login_required
@volunteer_required
def view_status():
    volunteer = Volunteer.query.filter_by(id=current_user.id).first()
    return render_template('volunteer/view_status.html', volunteer=volunteer)
