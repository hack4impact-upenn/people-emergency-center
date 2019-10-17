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
from app.decorators import staff_required
from app.models import EditableHTML, Role, User, Volunteer

staff = Blueprint('staff', __name__)

@staff.route('/')
@login_required
@staff_required
def index():
    """Volunteer dashboard page."""
    return render_template('staff/index.html')

@staff.route('/view_volunteers')
@login_required
@staff_required
def view_volunteers():
    """View all volunteers."""
    volunteers = Volunteer.query.all()
    return render_template('staff/view_volunteers.html', volunteers=volunteers)
